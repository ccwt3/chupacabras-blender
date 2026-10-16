"""Reabre las fuentes sin guardarlas y registra contacto y duración.

Uso: blender -b -t 4 --python-exit-code 1 --python scripts/verificar_intercambio.py
"""
import json
from datetime import datetime, timezone
from pathlib import Path
import bpy
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
reports=[]
for filename in ('04_intercambio.blend','05_blocking_r04.blend'):
 bpy.ops.wm.open_mainfile(filepath=str(root/'scenes'/filename))
 scene=bpy.context.scene
 assert (scene.frame_start,scene.frame_end,scene.render.fps)==(1,1201,30)
 assert scene.camera.name=='CinemaCamera'
 errors=[]
 start=637 if filename.startswith('05') else 1
 for f in range(start,1202):
  scene.frame_set(f)
  deps=bpy.context.evaluated_depsgraph_get()
  a=bpy.data.objects['Mouth'].evaluated_get(deps).matrix_world.translation
  b=bpy.data.objects['Neck'].evaluated_get(deps).matrix_world.translation
  errors.append((a-b).length)
 assert max(errors)<.00001
 reports.append(dict(file=filename,frames=1201,duration_seconds=40,contact_samples=len(errors),max_contact_error=max(errors)))
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
(root/'docs/evidencias/2026-09-24_intercambio'/f'reapertura_{stamp}.json').write_text(json.dumps(reports,indent=2)+'\n')
