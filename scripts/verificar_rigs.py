"""Reabre muestras 10/11 y compara deformación, apoyo y contacto fotograma a fotograma."""
import json
import math
import os
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from intercambio import ROOT
from oveja import positions

name=os.environ.get('CHUPA_RIG','10_rig_oveja')
reference=json.loads((ROOT/'exports'/(name+'.json')).read_text())
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(name+'.blend')),use_scripts=False)
scene=bpy.context.scene
triangles=0
for mesh in [o for o in scene.objects if o.type=='MESH']:
    mesh.data.calc_loop_triangles();triangles+=len(mesh.data.loop_triangles)
assert triangles==(612 if name.startswith('10') else 11162),triangles
bm=bmesh.new();bm.from_mesh(bpy.data.objects['Sheep_Quaternius'].data)
assert not any(e.is_boundary for e in bm.edges),'Open wool boundary'
assert not any(not v.link_faces for v in bm.verts),'Loose wool vertex'
bm.free()
assert (scene.frame_end-scene.frame_start)/scene.render.fps==reference['duration']
max_error=0; min_height=100; min_area=100; max_contact=0
surface_records=[];max_surface=0;max_jump=0;previous=None
for record in reference['samples']:
    scene.frame_set(round(record['time']*30)+1)
    bpy.context.view_layer.update()
    for entry in record['meshes']:
        mesh=bpy.data.objects[entry['name']]
        points=positions(mesh)
        inds=entry.get('indices',range(len(points)))
        for i,v in zip(inds,entry['vertices']):
            max_error=max(max_error,(points[i]-Vector(tuple(v[k] for k in 'xyz'))).length)
        min_height=min(min_height,min(v.z for v in points))
        mesh.data.calc_loop_triangles()
        for tri in mesh.data.loop_triangles:
            a,b,c=[points[i] for i in tri.vertices]
            area=(b-a).cross(c-a).length/2
            assert math.isfinite(area)
            min_area=min(min_area,area)
    if 'contacto' in name:
        sheep=bpy.data.objects['Sheep_Quaternius']
        points=positions(sheep)
        upper=positions(bpy.data.objects['Chupa_Detail_Ivory'])[reference['upper_vertex']]
        lower=positions(bpy.data.objects['Chupa_LowerTeeth'])[reference['lower_vertex']]
        tree=BVHTree.FromPolygons(points,[list(p.vertices) for p in sheep.data.polygons])
        for point in (upper,lower):max_surface=max(max_surface,tree.find_nearest(point)[3])
        if previous is not None:max_jump=max(max_jump,(upper-previous).length)
        previous=upper
        surface_records.append(dict(time=record['time'],upper=dict(zip('xyz',upper)),lower=dict(zip('xyz',lower))))
        for a,b in [('UpperContact','NeckUpper'),('LowerContact','NeckLower')]:
            max_contact=max(max_contact,(bpy.data.objects[a].matrix_world.translation-bpy.data.objects[b].matrix_world.translation).length)
assert max_error<1e-5,max_error
assert min_height>-.0001,min_height
assert min_area>1e-10,min_area
assert max_contact<.001,max_contact
sheep=bpy.data.objects['Sheep_Quaternius']
assert len(sheep.data.shape_keys.key_blocks)==2
assert max(len([g for g in v.groups if g.weight>0]) for v in sheep.data.vertices)<=4
assert max_surface<.0001,max_surface
assert max_jump<.03,max_jump
if surface_records:
    path=ROOT/'exports'/(name+'_surface.json')
    data=json.dumps(dict(samples=surface_records),separators=(',',':'))+'\n'
    if path.exists():assert path.read_text()==data
    else:path.write_text(data)
print('RIG_REOPEN_OK' ,json.dumps(dict(name=name,triangles=triangles,samples=len(reference['samples']),max_vertex_error=max_error,min_height=min_height,min_triangle_area=min_area,max_contact=max_contact,max_surface=max_surface,max_jump=max_jump,physical_device=False)))
