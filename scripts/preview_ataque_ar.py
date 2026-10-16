"""Review the actual authored meshes from multiple angles and key times."""
import os,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from intercambio import camera
ROOT=Path(__file__).resolve().parents[1]
NAME='ataque_ar_'+os.environ.get('CHUPA_ATTACK_REV','r01')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')),use_scripts=False)
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=960;s.render.resolution_y=640;s.render.resolution_percentage=100
s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True
s.display.shading.show_cavity=True;s.display.shading.background_type='WORLD';s.world.color=(.09,.10,.12)
out=ROOT/'previews'/NAME;out.mkdir(exist_ok=True)
s.camera=camera('AttackReview',(10,13,8),(0,-1,1),44)
for f in (1,49,61,73,85,109,157,193,229,265,301,325):
 s.frame_set(f);s.render.filepath=str(out/f'{f:03d}.png');bpy.ops.render.render(write_still=True)
s.camera=camera('AttackSide',(9,0,3),(0,.3,1),48)
s.frame_set(97);s.render.filepath=str(out/'contact_side.png');bpy.ops.render.render(write_still=True)
# A lightweight movie makes the complete timing reviewable outside Blender.
import subprocess
s.camera=bpy.data.objects['AttackReview'];s.render.resolution_x=720;s.render.resolution_y=480
frames=out/'video_frames';frames.mkdir(exist_ok=True)
for f in range(1,s.frame_end+1,2):
 s.frame_set(f);s.render.filepath=str(frames/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
subprocess.run(['ffmpeg','-nostdin','-n','-framerate','12','-pattern_type','glob','-i',str(frames/'*.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','21',str(out/'secuencia.mp4')],check=True)
