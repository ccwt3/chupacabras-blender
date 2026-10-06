"""Reabre fuente/FBX y comprueba presupuesto, mapas, pesos, apoyo y ciclo."""
import json
import math
import os
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils.kdtree import KDTree

ROOT=Path(__file__).resolve().parents[1]
NAME='chupacabras_nocturno_'+os.environ.get('CHUPA_ART_REV','r08')
OUT=ROOT/'previews'/NAME
TEX=ROOT/'exports'/NAME
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')),use_scripts=False)
scene=bpy.context.scene; obj=bpy.data.objects['Chupacabras_Nocturno']; mesh=obj.data
mesh.calc_loop_triangles(); count=len(mesh.loop_triangles)
assert count==json.loads((TEX/'manifest.json').read_text())['triangles']<130000
assert len(mesh.materials)==1 and len(mesh.uv_layers)==1
assert all(math.isfinite(c) for v in mesh.vertices for c in v.co)
assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in mesh.vertices)
assert max(len(v.groups) for v in mesh.vertices)<=4
bm=bmesh.new();bm.from_mesh(mesh)
assert all(e.is_manifold for e in bm.edges), 'Non-manifold edges'
assert all(f.calc_area()>1e-14 for f in bm.faces), 'Degenerate faces'
bm.free()
uv=np.array([v.uv[:] for v in mesh.uv_layers.active.data]);assert np.isfinite(uv).all() and uv.min()>=0 and uv.max()<=1
pixels={}
for name in ('BaseColor','Normal','Roughness','MetallicSmoothness'):
    img=bpy.data.images.load(str(TEX/(name+'.png')),check_existing=False)
    img.colorspace_settings.name='sRGB' if name=='BaseColor' else 'Non-Color'
    assert tuple(img.size)==(2048,2048)
    values=np.empty(2048*2048*4,dtype=np.float32);img.pixels.foreach_get(values)
    assert np.isfinite(values).all();pixels[name]=values.reshape(-1,4)
assert np.max(np.abs(pixels['MetallicSmoothness'][:,3]-(1-pixels['Roughness'][:,0])))<.009
assert pixels['MetallicSmoothness'][:,:3].max()==0

def vertices(o,frame):
    bpy.context.scene.frame_set(frame);bpy.context.view_layer.update()
    evaluated=o.evaluated_get(bpy.context.evaluated_depsgraph_get());data=evaluated.to_mesh()
    result=np.array([evaluated.matrix_world@v.co for v in data.vertices]);evaluated.to_mesh_clear()
    return result

samples={f:vertices(obj,f) for f in (1,25,49,73,97)}
rest=samples[1];feet=rest[:,2]<.15
motion=max(np.linalg.norm(v-rest,axis=1).max() for v in samples.values())
seam=np.linalg.norm(samples[97]-rest,axis=1).max()
foot=max(np.linalg.norm((v-rest)[feet],axis=1).max() for v in samples.values())
assert feet.sum()>30 and foot<1e-6,(feet.sum(),foot)
minimum, maximum = (.12, .20) if NAME.endswith('respira_r02') else (.01, .15)
assert seam<1e-5 and minimum<motion<maximum,(seam,motion)
assert rest[:,2].min()>-.005,rest[:,2].min()
# All frames remain finite and above the support plane; sampled entire loop.
for f in range(1,98):
    points=vertices(obj,f)
    assert np.isfinite(points).all() and points[:,2].min()>-.005
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(ROOT/'exports'/(NAME+'.fbx')),use_anim=True,anim_offset=0)
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1
rigs=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'];assert len(rigs)==1
assert len(rigs[0].data.bones)==4 and rigs[0].animation_data
assert not any(o.type in ('CAMERA','LIGHT') for o in bpy.context.scene.objects)
bpy.context.scene.render.fps=24
errors=[]
for f,expected in samples.items():
    actual=vertices(meshes[0],f)
    assert actual.shape==expected.shape
    # FBX reorders vertices; compare spatial correspondence without unstable float sorting.
    tree=KDTree(len(actual))
    for i,point in enumerate(actual): tree.insert(point,i)
    tree.balance()
    errors.append(float(max(tree.find(point)[2] for point in expected)))
assert max(errors)<.001,errors
result=dict(passed=True,triangles=count,bones=4,materials=1,loop_seconds=4,max_motion_m=float(motion),loop_seam_m=float(seam),foot_drift_m=float(foot),minimum_z=float(rest[:,2].min()),fbx_errors_m=errors,physical_device=False)
(OUT/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('NOCTURNO_CHECKS_OK '+json.dumps(result))
