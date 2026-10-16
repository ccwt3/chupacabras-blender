"""Reabre el hito: curvas horneadas, apoyo, cámara y cruce del salto; no prueba física."""
import json
import math
import os
import sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from intercambio import ROOT
from oveja import positions

name = os.environ.get('CHUPA_ACTING', '14_ataque_r07')
ref = json.loads((ROOT/'exports'/(name+'.json')).read_text())
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(name+'.blend')), use_scripts=False)
scene = bpy.context.scene
assert (scene.frame_end-1)/scene.render.fps == ref['duration']
meshes = [o for o in scene.objects if o.type == 'MESH' and not o.name.startswith('Env_')]
creature = [o for o in meshes if o.name.startswith('Chupa_')]
cam = scene.camera
errors, floors, steps, camera_steps, collisions = [], [], [], [], []
prev_cam = prev_root = prev_rotation = None
angular_steps = []
closest = (100, 0)
for index, sample in enumerate(ref['samples']):
    frame = index+1; t = index/30
    scene.frame_set(frame); bpy.context.view_layer.update()
    for m in sample['meshes']:
        pts = positions(bpy.data.objects[m['name']])
        indices = list(range(0, len(pts), max(1, len(pts)//24)))
        errors += [(pts[i]-Vector(tuple(v[k] for k in 'xyz'))).length for i,v in zip(indices,m['vertices'])]
    pts = [p for m in creature for p in positions(m)]
    floor = min(p.z for p in pts)
    sheep_floor = min(p.z for p in positions(bpy.data.objects['Sheep_Quaternius']))
    assert sheep_floor > -1e-5, (frame, sheep_floor)
    floors.append(floor)
    # Sampled vertices against conservative wall/roof boxes, excluding the ground.
    if any((-5.08 < p.x < -1.52 and 4.84 < p.y < 6.34 and .001 < p.z < 3.04) or
           (-5.15 < p.x < -1.45 and 4.80 < p.y < 6.38 and 3.0 < p.z < 4.35-abs(p.x+3.3)*1.25/1.75)
           for p in pts):
        collisions.append(frame)
    root = bpy.data.objects['ChupacabrasAssetRoot'].matrix_world.translation
    if prev_cam is not None:
        camera_steps.append((cam.location-prev_cam).length)
        angular_steps.append(prev_rotation.rotation_difference(cam.rotation_euler.to_quaternion()).angle)
        steps.append((root-prev_root).length)
    prev_cam, prev_root = cam.location.copy(), root.copy()
    prev_rotation = cam.rotation_euler.to_quaternion()
    if 20 < t < 21.2:
        distance = math.hypot(root.x-cam.location.x, root.y-cam.location.y)
        if distance < closest[0]: closest = (distance,t)
assert max(errors) < 1e-5, max(errors)
assert min(floors) > -1e-5, min(floors)
assert max(camera_steps) < .26, max(camera_steps)
assert max(steps) < .9, max(steps)
assert max(angular_steps) < .15, max(angular_steps)
assert not collisions, collisions[:20]
scene.frame_set(601); takeoff = bpy.data.objects['ChupacabrasAssetRoot'].location.copy()
assert (takeoff-Vector((-3.3,8.3,takeoff.z))).length < 1e-5
if ref['duration']>20:
    calm = json.loads((ROOT/'exports'/(name.replace('14_ataque','13_calma')+'.json')).read_text())
    assert calm['samples'] == ref['samples'][:601], 'Discontinuidad entre los hitos 13 y 14'
    assert floors[600]<1e-5 and floors[601]>.1 and floors[636]<1e-5
    assert closest[0] < 3, closest
report = dict(passed=True, name=name, frames=len(ref['samples']), duration=ref['duration'],
              production_duration=40, max_reference_error=max(errors), min_floor=min(floors),
              max_camera_step=max(camera_steps), max_camera_rotation_step_degrees=math.degrees(max(angular_steps)),
              max_creature_step=max(steps),
              barn_wall_roof_intersections=collisions, closest_jump_to_camera_xy=closest,
              physical_device=False, occlusion='Comprobar máscaras Unity separadamente')
out = ROOT/'docs/evidencias/2026-10-02_actuacion'/(name+'_blender.json')
out.write_text(json.dumps(report, indent=2)+'\n')
print('ACTUACION_BLENDER_OK',json.dumps(report))
