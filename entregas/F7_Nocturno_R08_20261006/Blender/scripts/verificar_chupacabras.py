"""Reapertura independiente: geometría cerrada, UV, escala y fuente sin rig final."""
import json
import math
import os
from pathlib import Path
import bmesh
import bpy

ROOT=Path(__file__).resolve().parents[1]
name=os.environ.get('CHUPA_MODEL','08_chupacabras_forma')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(name+'.blend')),use_scripts=False)
reference=json.loads((ROOT/'exports'/(name+'.json')).read_text())
root=bpy.data.objects['ChupacabrasAssetRoot']
assert root.parent is None and tuple(root.scale)==(1,1,1)
assert bpy.context.scene.unit_settings.scale_length==1
assert not any(o.type=='ARMATURE' for o in bpy.context.scene.objects)
assert not any(i.source=='FILE' for i in bpy.data.images)
triangles=0
for entry in reference['objects']:
    obj=bpy.data.objects[entry['name']]
    assert obj.parent==root and obj.type=='MESH'
    assert not obj.modifiers and obj.animation_data is None
    obj.data.calc_loop_triangles()
    assert len(obj.data.loop_triangles)==entry['triangles']
    triangles+=len(obj.data.loop_triangles)
    assert len(obj.data.uv_layers)==1
    assert all(math.isfinite(c) and -.0001<=c<=1.0001
               for p in obj.data.uv_layers.active.data for c in p.uv)
    bm=bmesh.new();bm.from_mesh(obj.data)
    assert all(e.is_manifold for e in bm.edges),entry['name']
    assert all(f.calc_area()>1e-10 for f in bm.faces),entry['name']
    bm.free()
assert triangles==reference['triangles'] and triangles<reference.get('triangle_budget',18000)
assert (bpy.data.objects['JawPivot'].location-bpy.data.objects['BiteSocket'].location).length > .1
assert 'Chupa_Jaw' in bpy.data.objects and 'BiteSocket' in bpy.data.objects
print('CREATURE_REOPEN_OK '+json.dumps(dict(name=name,triangles=triangles,
    closed_meshes=len(reference['objects']),uv=True,external_textures=0,rig=False,physical_device=False)))
