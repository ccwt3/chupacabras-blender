"""Amplía solo la respiración R08; conserva geometría, mapas y entrega original."""
import json
from pathlib import Path
import shutil

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
NAME = 'chupacabras_nocturno_r08_respira_r02'
blend = ROOT / 'scenes' / (NAME + '.blend')
fbx = ROOT / 'exports' / (NAME + '.fbx')
textures = ROOT / 'exports' / NAME
preview = ROOT / 'previews' / NAME
assert not any(p.exists() for p in (blend, fbx, textures, preview)), 'Conservar revisión existente'
bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'scenes/chupacabras_nocturno_r08.blend'), use_scripts=False)
obj = bpy.data.objects['Chupacabras_Nocturno']
rig = obj.modifiers['Respiracion'].object
scene = bpy.context.scene
properties = ('location', 'scale', 'rotation_euler')
factors = {'Torax': 2.5, 'Cabeza': 2.0}
poses = {}
for frame in range(1, 98):
    scene.frame_set(frame)
    poses[frame] = {(name, prop): tuple(getattr(rig.pose.bones[name], prop))
                    for name in factors for prop in properties}
rig.animation_data.action = rig.animation_data.action.copy()
rig.animation_data.action.name = 'Respiracion_4s_R02'
for frame, pose in poses.items():
    scene.frame_set(frame)
    for (name, prop), values in pose.items():
        baseline = poses[1][name, prop]
        setattr(rig.pose.bones[name], prop, [a + factors[name] * (v - a) for a, v in zip(baseline, values)])
        rig.pose.bones[name].keyframe_insert(prop, frame=frame)

# Check the actual deformation, not just bone curves; feet and loop must stay fixed.
def vertices(frame):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    points = np.array([evaluated.matrix_world @ v.co for v in mesh.vertices])
    evaluated.to_mesh_clear()
    return points

rest = vertices(1)
motion = max(float(np.linalg.norm(vertices(f) - rest, axis=1).max()) for f in range(1, 98))
feet = rest[:, 2] < .15
assert .12 < motion < .20, motion
assert max(np.linalg.norm((vertices(f) - rest)[feet], axis=1).max() for f in range(1, 98)) < 1e-6
assert np.linalg.norm(vertices(97) - rest, axis=1).max() < 1e-5
shutil.copytree(ROOT / 'exports/chupacabras_nocturno_r08', textures)
manifest = json.loads((textures / 'manifest.json').read_text())
manifest.update(name=NAME, source='chupacabras_nocturno_r08', breathing_revision=2,
                breathing_factors=factors, max_motion_m=motion)
(textures / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
for img in bpy.data.images:
    if img.name in ('BaseColor', 'Normal', 'Roughness', 'MetallicSmoothness'):
        img.filepath = '//../exports/' + NAME + '/' + img.name + '.png'
scene.frame_set(1)
bpy.ops.object.select_all(action='DESELECT')
for item in (rig.parent, rig, obj):
    item.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(fbx), use_selection=True, object_types={'MESH', 'EMPTY', 'ARMATURE'},
                        axis_forward='-Z', axis_up='Y', apply_unit_scale=True, apply_scale_options='FBX_SCALE_UNITS',
                        bake_space_transform=False, use_mesh_modifiers=False, add_leaf_bones=False, bake_anim=True,
                        bake_anim_use_all_actions=False, bake_anim_use_nla_strips=False, bake_anim_simplify_factor=0,
                        path_mode='STRIP')
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
preview.mkdir()
print('RESPIRACION_R02_OK', json.dumps(manifest))
