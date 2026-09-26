"""Paso 10: rig CC0 existente, lana deformable y muestra de poses de ocho segundos.

CHUPA_SUFFIX crea revisiones; ninguna entrega previa se sobrescribe.
"""
import json
import math
import os
import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intercambio import ROOT, camera
from oveja import positions, export

NAME = '10_rig_oveja' + os.environ.get('CHUPA_SUFFIX', '')


def key_pose(rig, frame):
    for bone in rig.pose.bones:
        bone.keyframe_insert('location', frame=frame)
        bone.keyframe_insert('rotation_euler', frame=frame)
        bone.keyframe_insert('scale', frame=frame)


def linear_actions():
    for action in bpy.data.actions:
        if not action.name.startswith(('RigTest', 'ContactTest')):
            continue
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for key in curve.keyframe_points:
                            key.interpolation = 'LINEAR'


def sample(meshes, frame, label=''):
    bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.update()
    return dict(time=(frame-1)/30, label=label,
                meshes=[dict(name=m.name, vertices=[dict(zip('xyz', v)) for v in positions(m)])
                        for m in meshes])


def previews(name, samples):
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x, scene.render.resolution_y = 960, 540
    scene.render.resolution_percentage = 100
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.color_type = 'MATERIAL'
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.display.shading.background_type = 'WORLD'
    scene.world.color = (.055, .055, .055)
    scene.camera = camera('RigReviewCamera', (2.5, -3.5, 1.9), (0, -.1, .55), 45)
    for frame, label in samples:
        scene.frame_set(frame)
        scene.render.filepath = str(ROOT/'previews'/f'{name}_{label}.png')
        bpy.ops.render.render(write_still=True)


def main():
    for folder, ext in [('scenes', '.blend'), ('exports', '.fbx'), ('exports', '.json')]:
        if (ROOT/folder/(NAME+ext)).exists():
            raise FileExistsError(NAME+ext)
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/07_oveja_r04.blend'), use_scripts=False)
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 1, 241
    rig = bpy.data.objects['SheepRig']
    mesh = bpy.data.objects['Sheep_Quaternius']
    wrapper = bpy.data.objects['SheepAssetRoot']
    rig.animation_data.action = bpy.data.actions.new('RigTest_Sheep_8s')
    for bone in rig.pose.bones:
        bone.matrix_basis = Matrix.Identity(4)
        bone.rotation_mode = 'XYZ'
    bpy.context.view_layer.update()
    rest = positions(mesh)
    mesh.shape_key_add(name='Basis')
    compression = mesh.shape_key_add(name='WoolCompression')
    wool = {i for p in mesh.data.polygons if p.material_index == 0 for i in p.vertices}
    inv = mesh.matrix_world.inverted()
    affected = []
    for i in wool:
        p = rest[i].copy()
        # Smooth neck band. Compress the wool on both sides, leaving skin/head/legs intact.
        strength = math.exp(-((p.y+.52)/.20)**2) * math.exp(-((p.z-.90)/.34)**2)
        if strength < .02:
            continue
        p.x *= 1-.42*strength
        p.z = .90+(p.z-.90)*(1-.16*strength)
        compression.data[i].co = inv @ p
        affected.append(i)
    # Test extremes and reversible return, independent of the definitive 40-second acting.
    poses = [(1,'neutral'), (61,'grazing'), (91,'grazing_turn'),
             (121,'struggle_left'), (151,'struggle_right'), (181,'side_compressed'),
             (211,'side_kick'), (241,'neutral_end')]
    for frame,label in poses:
        scene.frame_set(frame)
        wrapper.rotation_euler = (0,0,0)
        wrapper.location = (0,0,.004064235836267471)
        for bone in rig.pose.bones:
            bone.matrix_basis = Matrix.Identity(4)
        if label.startswith('grazing'):
            for n,a in [('Shoulders',-1.3),('Neck',-.8),('Head',.6)]:
                rig.pose.bones[n].rotation_euler.x = a
            if frame == 91:
                rig.pose.bones['Head'].rotation_euler.y = .12
        if label.startswith('struggle'):
            sign = 1 if frame == 121 else -1
            rig.pose.bones['Neck'].rotation_euler = (-.5, .25*sign, .12*sign)
            rig.pose.bones['Head'].rotation_euler = (.2, -.18*sign, 0)
            rig.pose.bones['Body'].rotation_euler.y = .08*sign
            rig.pose.bones['FrontFoot.L' if sign>0 else 'FrontFoot.R'].location.y = -.3
        if label.startswith('side'):
            wrapper.rotation_euler.y = math.pi/2
            rig.pose.bones['Neck'].rotation_euler.x = -.25
            rig.pose.bones['Head'].rotation_euler.x = .15
            if frame == 211:
                rig.pose.bones['FrontFoot.L'].location.y = -.7
                rig.pose.bones['BackFoot.L'].location.x = -.5
        compression.value = 1 if 121 <= frame <= 211 else 0
        compression.keyframe_insert('value', frame=frame)
        key_pose(rig, frame)
        wrapper.keyframe_insert('location', frame=frame)
        wrapper.keyframe_insert('rotation_euler', frame=frame)
    # Name auxiliary actions for consistent linear interpolation.
    wrapper.animation_data.action.name = 'RigTest_SheepRoot_8s'
    mesh.data.shape_keys.animation_data.action.name = 'RigTest_Wool_8s'
    linear_actions()
    # Ground support is baked for every frame, including interpolated roll transitions.
    for frame in range(1,242):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        wrapper.location.z -= min(v.z for v in positions(mesh))
        wrapper.keyframe_insert('location', frame=frame)
    linear_actions()
    records = []
    labels = dict(poses)
    head = [v.index for v in mesh.data.vertices if any(
        mesh.vertex_groups[g.group].name=='Head' and g.weight>.5 for g in v.groups)]
    for frame in range(1,242):
        record = sample([mesh], frame, labels.get(frame,''))
        record['shape'] = compression.value
        records.append(record)
    min_height = min(v['z'] for s in records for v in s['meshes'][0]['vertices'])
    grazing_height = min(records[60]['meshes'][0]['vertices'][i]['z'] for i in head)
    assert min_height > -1e-5
    assert 0 <= grazing_height < .04, grazing_height
    assert len(affected)>10
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')))
    export(ROOT/'exports'/(NAME+'.fbx'), True)
    report = dict(name=NAME, duration=8, bones=24, triangles=612,
                  shape_vertices=len(affected), max_influences=4, physical_device=False,
                  grazing_height=grazing_height, min_height=min_height, samples=records)
    (ROOT/'exports'/(NAME+'.json')).write_text(json.dumps(report,separators=(',',':'))+'\n')
    previews(NAME, poses)
    print('RIG_SHEEP_OK',json.dumps({k:v for k,v in report.items() if k!='samples'}))

if __name__ == '__main__':
    main()
