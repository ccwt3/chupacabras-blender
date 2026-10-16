"""Render de respiración a cámara fija; el clip real también se entrega en FBX."""
import os
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1]
NAME='chupacabras_nocturno_'+os.environ.get('CHUPA_ART_REV','r08')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')),use_scripts=False)
scene=bpy.context.scene
scene.render.resolution_x=640;scene.render.resolution_y=480
scene.cycles.samples=8;scene.cycles.use_denoising=True
out=ROOT/'previews'/NAME/'respiracion_frames'
out.mkdir(exist_ok=False)
for i,f in enumerate(range(1,97,2)):
    scene.frame_set(f);scene.render.filepath=str(out/f'{i:04d}.png')
    bpy.ops.render.render(write_still=True)
