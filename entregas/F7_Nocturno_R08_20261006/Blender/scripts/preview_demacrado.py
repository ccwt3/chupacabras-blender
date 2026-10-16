"""Turntable reproducible y comparación geométrica, sin alterar fuentes."""
import json
import math
import os
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
NAME=os.environ.get('CHUPA_MODEL','09_chupacabras_demacrado_r02')
stem=NAME+os.environ.get('CHUPA_PREVIEW_SUFFIX','')
out=ROOT/'previews'/(stem+'_giro_frames')
comparison=out.parent/(stem+'_comparacion.json')
if comparison.exists():raise FileExistsError(comparison)
out.mkdir(exist_ok=False)
metrics={}
for name in ('09_chupacabras_acabado',NAME):
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(name+'.blend')),use_scripts=False)
    body=bpy.data.objects['Chupa_Body']
    bm=bmesh.new();bm.from_mesh(body.data)
    metrics[name]={'body_volume_m3':bm.calc_volume(signed=False),'body_vertices':len(bm.verts)}
    bm.free()
ratio=metrics[NAME]['body_volume_m3']/metrics['09_chupacabras_acabado']['body_volume_m3']
assert .15<ratio<.65,ratio
metrics['volume_ratio']=ratio
metrics['physical_device']=False
comparison.write_text(json.dumps(metrics,indent=2)+'\n')
scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=960;scene.render.resolution_y=720;scene.render.resolution_percentage=100
shade=scene.display.shading
shade.light='STUDIO';shade.studio_light='paint.sl';shade.color_type='MATERIAL'
shade.show_shadows=True;shade.show_cavity=True;shade.cavity_type='BOTH'
shade.show_specular_highlight=False;shade.background_type='WORLD'
scene.world.color=(.045,.055,.065);scene.view_settings.view_transform='Standard'
cam=scene.camera;cam.data.type='ORTHO';cam.data.ortho_scale=5.5
for frame in range(120):
    angle=math.tau*frame/120+.55
    cam.location=(8*math.sin(angle),8*math.cos(angle)-.5,3.1)
    cam.rotation_euler=(Vector((0,-.5,1.2))-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/f'{frame:04d}.png')
    bpy.ops.render.render(write_still=True)
print('LEAN_PREVIEW_OK '+json.dumps(metrics))
