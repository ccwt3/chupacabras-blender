"""Muestra del paso 4. Ejecutar con Blender --background --python este archivo.

Conserva la fuente con constraints; FBX hornea su evaluación a 30 Hz.
Rechaza sobrescribir entregas. CHUPA_SUFFIX permite otra revisión.
"""
import json
import math
import os
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
NAME = '04_intercambio' + os.environ.get('CHUPA_SUFFIX', '')


def material(name, rgb):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*rgb, 1)
    return mat


def empty(name, location=(0, 0, 0)):
    obj = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    return obj


def cube(name, location, size, mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    return obj


def camera(name, location, target, lens=40):
    data = bpy.data.cameras.new(name)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()
    data.lens = lens
    data.sensor_width = 36
    return obj


def setup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1
    scene.render.fps = 30
    scene.frame_start, scene.frame_end = 1, 1201
    scene.render.resolution_x, scene.render.resolution_y = 960, 540
    scene.render.resolution_percentage = 100
    return scene


def export(name):
    blend = ROOT / 'scenes' / (name + '.blend')
    fbx = ROOT / 'exports' / (name + '.fbx')
    fbx.parent.mkdir(exist_ok=True)
    if blend.exists() or fbx.exists():
        raise FileExistsError('Entrega existente; use CHUPA_SUFFIX para otra revisión')
    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.export_scene.fbx(
        filepath=str(fbx), use_selection=False, object_types={'MESH', 'ARMATURE', 'EMPTY', 'CAMERA'},
        axis_forward='-Z', axis_up='Y', global_scale=1, apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_UNITS', bake_space_transform=False,
        add_leaf_bones=False, use_mesh_modifiers=False, bake_anim=True,
        bake_anim_use_all_actions=False, bake_anim_use_nla_strips=False,
        bake_anim_force_startend_keying=True, bake_anim_step=1, bake_anim_simplify_factor=0)


def main():
    scene = setup()
    teal = material('Probe_Teal', (.15, .55, .5))
    cube('MeterCube', (-2, 0, .5), (1, 1, 1), teal)
    for name, location in [('AxisX', (1, 0, 0)), ('AxisY', (0, 1, 0)), ('AxisZ', (0, 0, 1))]:
        empty(name, location)
    bpy.ops.object.armature_add()
    rig = bpy.context.object
    rig.name = 'ProbeRig'
    bpy.ops.object.mode_set(mode='EDIT')
    root = rig.data.edit_bones[0]
    root.name = 'Base'
    root.head, root.tail = (0, 0, 0), (0, 0, .5)
    bend = rig.data.edit_bones.new('Bend')
    bend.head, bend.tail = (0, 0, .5), (0, 0, 1)
    bend.parent = root
    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = cube('WoolProbe', (0, 0, .5), (.4, .4, 1), teal)
    # Mesh geometry in rig space, allowing skin and shape deformation together.
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    mesh.parent = rig
    base = mesh.vertex_groups.new(name='Base')
    top = mesh.vertex_groups.new(name='Bend')
    for vertex in mesh.data.vertices:
        (top if vertex.co.z > .5 else base).add([vertex.index], 1, 'REPLACE')
    modifier = mesh.modifiers.new('Skin', 'ARMATURE')
    modifier.object = rig
    mesh.shape_key_add(name='Basis')
    compression = mesh.shape_key_add(name='WoolCompression')
    for vertex in compression.data:
        vertex.co.x *= .6
    mouth = empty('Mouth')
    mouth.parent, mouth.parent_type, mouth.parent_bone = rig, 'BONE', 'Bend'
    mouth.location = (0, 0, 0)
    neck = empty('Neck')
    follow = neck.constraints.new('COPY_LOCATION')
    follow.target = mouth
    for t in (0, 10, 20, 30, 40):
        frame = 1 + 30 * t
        rig.location.x = t / 20
        rig.keyframe_insert('location', frame=frame)
        rig.pose.bones['Bend'].rotation_mode = 'XYZ'
        rig.pose.bones['Bend'].rotation_euler.y = .5 * math.sin(t * math.pi / 20)
        rig.pose.bones['Bend'].keyframe_insert('rotation_euler', frame=frame)
        compression.value = .5 - .5 * math.cos(t * math.pi / 10)
        compression.keyframe_insert('value', frame=frame)
    scene.camera = camera('CinemaCamera', (4, -7, 3), (0, 0, .5))
    records = []
    for frame in range(1, 1202, 30):
        scene.frame_set(frame)
        deps = bpy.context.evaluated_depsgraph_get()
        a = mouth.evaluated_get(deps).matrix_world.translation
        b = neck.evaluated_get(deps).matrix_world.translation
        assert (a - b).length < 1e-5
        evaluated = mesh.evaluated_get(deps)
        vertices = [dict(zip('xyz', evaluated.matrix_world @ v.co)) for v in evaluated.data.vertices]
        records.append(dict(time=(frame-1)/30, mouth=dict(zip('xyz', a)), neck=dict(zip('xyz', b)), vertices=vertices,
                            shape=compression.value))
    export(NAME)
    (ROOT / 'exports' / (NAME + '.json')).write_text(json.dumps(dict(
        blender=bpy.app.version_string, fps=30, start=1, end=1201, duration=40,
        samples=records), indent=2) + '\n')


if __name__ == '__main__':
    main()
