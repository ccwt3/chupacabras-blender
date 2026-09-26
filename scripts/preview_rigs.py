"""Evidencia Workbench a 15 fps: fuente 30 fps, sin alterar el .blend."""
import os
import sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from intercambio import ROOT,camera,material
name=os.environ.get('CHUPA_RIG','11_rigs_contacto')
frames=ROOT/'previews'/(name+'_frames')
frames.mkdir(exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(name+'.blend')),use_scripts=False)
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=960;scene.render.resolution_y=540;scene.render.resolution_percentage=100
scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL'
scene.display.shading.show_cavity=True;scene.display.shading.show_shadows=True
scene.display.shading.background_type='WORLD';scene.world.color=(.06,.065,.075)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.005))
bpy.context.object.data.materials.append(material('ReviewFloor',(.10,.11,.13)))
scene.camera=camera('ReviewCamera',(6,6,3.5),(-.6,0,.8),40)
for index,frame in enumerate(range(scene.frame_start,scene.frame_end,2),1):
    scene.frame_set(frame);scene.render.filepath=str(frames/f'{index:04d}.png')
    bpy.ops.render.render(write_still=True)
print('RIG_PREVIEW_FRAMES',index)
