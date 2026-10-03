"""F3 independent reopen, texture coverage, UV, closed topology and FBX round trip."""
import json
import math
import os
from pathlib import Path

import bmesh
import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
NAME = 'F3_chupacabras_superficie_' + os.environ.get('CHUPA_F3_REV', 'r05')
TEX = ROOT/'exports'/NAME
OUT = ROOT/'previews'/NAME
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')), use_scripts=False)
obj = bpy.data.objects['Chupa_F3_Surface']; mesh = obj.data
manifest = json.loads((TEX/'manifest.json').read_text())
mesh.calc_loop_triangles()
assert len(mesh.loop_triangles) == manifest['triangles'] < 35000
assert len(mesh.materials) == 1 and len(mesh.uv_layers) == 1
assert not obj.modifiers and all(math.isfinite(c) for v in mesh.vertices for c in v.co)
assert not any(o.type == 'ARMATURE' or o.animation_data for o in bpy.context.scene.objects)
bm = bmesh.new(); bm.from_mesh(mesh)
assert all(e.is_manifold for e in bm.edges)
assert all(f.calc_area() > 1e-12 for f in bm.faces)
bm.free()
uv = np.array([v.uv[:] for v in mesh.uv_layers.active.data])
assert np.isfinite(uv).all() and uv.min() >= 0 and uv.max() <= 1
tri_uv = uv.reshape(-1,3,2)
edges = tri_uv[:,1:] - tri_uv[:,:1]
areas = np.abs(edges[:,0,0]*edges[:,1,1]-edges[:,0,1]*edges[:,1,0])/2
assert areas.min() > 1e-12, float(areas.min())
centers = np.clip((tri_uv.mean(axis=1)*2048).astype(int), 0, 2047)
maps = {}
pixels = {}
for name in ['BaseColor','Normal','Roughness','MetallicSmoothness']:
    image = bpy.data.images.load(str(TEX/(name+'.png')), check_existing=False)
    image.colorspace_settings.name = 'sRGB' if name == 'BaseColor' else 'Non-Color'
    assert tuple(image.size) == (2048,2048)
    data = np.empty(2048*2048*4,dtype=np.float32); image.pixels.foreach_get(data)
    data = data.reshape(2048,2048,4); pixels[name] = data
    samples = data[centers[:,1],centers[:,0]]
    assert np.isfinite(data).all()
    if name in ('BaseColor','Roughness'):
        assert (samples[:,:3].max(axis=1) > .01).all(), (name, int((samples[:,:3].max(axis=1) <= .01).sum()))
    if name == 'Normal':
        lengths = np.linalg.norm(samples[:,:3]*2-1,axis=1)
        assert lengths.min() > .9 and lengths.max() < 1.1
    maps[name] = {'bytes': (TEX/(name+'.png')).stat().st_size, 'minimum_triangle_center_rgb': float(samples[:,:3].min())}
assert np.max(np.abs(pixels['MetallicSmoothness'][:,:,3] - (1-pixels['Roughness'][:,:,0]))) < .009
assert pixels['MetallicSmoothness'][:,:,:3].max() == 0
expected = sorted(tuple(round(float(c),5) for c in obj.matrix_world @ v.co) for v in mesh.vertices)
minimum = [min(v[i] for v in expected) for i in range(3)]
maximum = [max(v[i] for v in expected) for i in range(3)]
assert minimum[2] >= -1e-4
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(ROOT/'exports'/(NAME+'.fbx')), use_anim=False)
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
assert len(meshes) == 1
actual = sorted(tuple(round(float(c),5) for c in meshes[0].matrix_world @ v.co) for v in meshes[0].data.vertices)
assert len(actual) == len(expected)
assert np.max(np.abs(np.array(actual)-np.array(expected))) < 2e-5
meshes[0].data.calc_loop_triangles()
assert len(meshes[0].data.loop_triangles) == manifest['triangles']
assert not any(o.type in ('ARMATURE','LIGHT','CAMERA') or o.animation_data for o in bpy.context.scene.objects)
result = dict(passed=True, physical_device=False, triangles=manifest['triangles'],
              bounds_min=minimum, bounds_max=maximum, closed=True, uv_min_area=float(areas.min()),
              maps=maps, fbx_roundtrip=True, visual_acceptance='Separate six-view review; mobile pending F5')
path = OUT/'reopen_checks.json'
if path.exists(): raise FileExistsError(path)
path.write_text(json.dumps(result,indent=2)+'\n')
print('F3_REOPEN_OK '+json.dumps(result))
