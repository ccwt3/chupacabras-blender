"""Reabre F2: topología, apoyo, asimetría y proximidad de detalles a su soporte.

CHUPA_F2_REV=r04 blender -b -t 4 --python-exit-code 1 --python scripts/verificar_figura_forma.py
No acredita apariencia móvil, UV finales, ni reemplaza la revisión de seis vistas.
"""
import json
import math
import os
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
NAME = 'F2_chupacabras_forma_' + os.environ.get('CHUPA_F2_REV', 'r04')
OUT = ROOT/'previews'/NAME
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')), use_scripts=False)
root = bpy.data.objects['ChupacabrasAssetRoot']
expected = json.loads((OUT/'geometry.json').read_text())
assert root.parent is None and tuple(root.scale) == (1,1,1)
assert bpy.context.scene.unit_settings.scale_length == 1
assert not any(o.type == 'ARMATURE' or o.animation_data for o in bpy.context.scene.objects)
meshes = [o for o in root.children if o.type == 'MESH']
triangles = 0
islands = {}
trees = {}
for obj in meshes:
    assert not obj.modifiers and all(math.isfinite(c) for v in obj.data.vertices for c in v.co)
    obj.data.calc_loop_triangles(); triangles += len(obj.data.loop_triangles)
    bm = bmesh.new(); bm.from_mesh(obj.data)
    assert all(e.is_manifold for e in bm.edges), obj.name
    assert all(f.calc_area() > 1e-12 for f in bm.faces), obj.name
    trees[obj.name] = BVHTree.FromBMesh(bm)
    remaining = set(bm.verts); components = []
    while remaining:
        pending = [remaining.pop()]; points = []
        while pending:
            v = pending.pop(); points.append(v.co.copy())
            for edge in v.link_edges:
                other = edge.other_vert(v)
                if other in remaining:
                    remaining.remove(other); pending.append(other)
        components.append(points)
    islands[obj.name] = components
    bm.free()
assert triangles == expected['triangles']
assert len(islands['Chupa_Body']) == 1 and len(islands['Chupa_Head']) == 1
# Every separate tooth, claw, brow/crest/tuft must reach its support surface.
attachments = {}
signed_attachments = {}
for name, support in [('Chupa_LowerTeeth','Chupa_Jaw'),('Chupa_Detail_Ivory',None),
                      ('Chupa_Detail_Horn','Chupa_Body'),('Chupa_Detail_Ridge','Chupa_Body')]:
    distances = []; signed = []
    for points in islands[name]:
        target = support or ('Chupa_Body' if max(v.z for v in points)<.4 else 'Chupa_Head')
        nearest = [trees[target].find_nearest(v) for v in points]
        distances.append(min(n[3] for n in nearest))
        signed.append(min((v-n[0]).dot(n[1]) for v,n in zip(points,nearest)))
    attachments[name] = distances
    signed_attachments[name] = signed
print('SIGNED_ATTACHMENTS '+json.dumps(signed_attachments))
assert all(minimum < .001 for values in signed_attachments.values() for minimum in values), signed_attachments
# Surface samples are discrete; log distances separately from aesthetic judgement.
assert max(attachments['Chupa_LowerTeeth']) < .025, attachments
assert max(attachments['Chupa_Detail_Ivory']) < .04, attachments
body = bpy.data.objects['Chupa_Body']
feet = {}
for side, sign in [('left',-1),('right',1)]:
    for end in ['front','hind']:
        points = [v.co for v in body.data.vertices if sign*v.co.x>.45 and v.co.z<.15 and (v.co.y>0 if end=='front' else v.co.y<-.5)]
        feet[side+'_'+end] = {'min_z':min(p.z for p in points),'center_y':sum(p.y for p in points)/len(points)}
assert all(-1e-5 <= f['min_z'] < .005 for f in feet.values()), feet
assert abs(feet['left_front']['center_y']-feet['right_front']['center_y']) > .25, feet
assert min(v.co.z for o in meshes for v in o.data.vertices) >= -1e-4
for label in ['base','forma']:
    for view in ['frente','perfil','espalda','tres_cuartos','inferior','rostro']:
        assert (OUT/(label+'_'+view+'.png')).is_file()
result = dict(passed=True,source=NAME,physical_device=False,triangles=triangles,closed_meshes=len(meshes),
    components={n:len(c) for n,c in islands.items()},attachment_distances_m=attachments,signed_attachment_minima_m=signed_attachments,feet=feet,
    final_uv_materials_and_mobile_budget=False)
output = OUT/'reopen_checks.json'
if output.exists(): raise FileExistsError(output)
output.write_text(json.dumps(result,indent=2)+'\n')
print('F2_REOPEN_OK '+json.dumps(result))
