"""Reapertura independiente de la fuente estática y su contexto, sin guardarlos."""
import json
from pathlib import Path
import bpy
from mathutils import Vector

root=Path(__file__).resolve().parents[1]
report={'physical_device':False}
bpy.ops.wm.open_mainfile(filepath=str(root/'scenes/06_escenario.blend'))
scene=bpy.context.scene
meshes=[o for o in scene.objects if o.type=='MESH']
assert len(meshes)==10 and scene.unit_settings.scale_length==1
triangles=0
for obj in meshes:
    obj.data.calc_loop_triangles(); triangles+=len(obj.data.loop_triangles)
    assert len(obj.data.materials)==1
assert triangles<12000
report.update(meshes=len(meshes),triangles=triangles)
bpy.ops.wm.open_mainfile(filepath=str(root/'scenes/06_escenario_contexto.blend'))
scene=bpy.context.scene
assert scene.render.fps==30 and scene.frame_end==1201
mouth=bpy.data.objects['Mouth']; neck=bpy.data.objects['Neck']
max_error=0
for frame in range(637,1202):
    scene.frame_set(frame); bpy.context.view_layer.update()
    max_error=max(max_error,(mouth.matrix_world.translation-neck.matrix_world.translation).length)
assert max_error<1e-5
report.update(duration=40,contact_frames=565,max_contact_m=max_error)
print('ENVIRONMENT_REOPEN_OK '+json.dumps(report))
