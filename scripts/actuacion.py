"""Pasos 13–14: actuación 0–25 s; hitos independientes, sin arrastre ni loop final.

CHUPA_SUFFIX (por defecto _r07) preserva cada entrega. Blender es la fuente;
las máscaras de Unity verifican el ocultamiento con la geometría importada.
"""
import json
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intercambio import ROOT, camera, export
from oveja import positions
from rig_oveja import key_pose

SUFFIX = os.environ.get('CHUPA_SUFFIX', '_r07')


def smooth(t, start, end):
    u = max(0., min(1., (t-start)/(end-start)))
    return u*u*u*(10+u*(-15+6*u))


def mix(a, b, u):
    return Vector(a).lerp(Vector(b), u)


def path(t):
    # Keep the proven barn silhouette, then withdraw before 15 seconds.
    if t < 12:
        return mix((-2.25, 7.85, 0), (-2.15, 7.70, 0), smooth(t, 0, 12)), -math.pi/2
    if t < 13:
        return mix((-2.15, 7.70, 0), (-2.15, 9.8, 0), smooth(t, 12, 13)), -math.pi/2
    if t < 14:
        u = smooth(t, 13, 14)
        return mix((-2.15, 9.8, 0), (-3.3, 9.8, 0), u), -math.pi/2-u*math.pi/2
    if t <= 20:
        return mix((-3.3, 9.8, 0), (-3.3, 8.3, 0), smooth(t, 14, 15)), -math.pi
    if t < 21.2:
        u = (t-20)/1.2
        # A lateral, high arc clears the barn, passes near the internal camera,
        # then descends toward the sheep. No teleport at the take-off boundary.
        p = ((1-u)**3*Vector((-3.3, 8.3, 0)) +
             3*(1-u)**2*u*Vector((1.0, 10.8, 9.5)) +
             3*(1-u)*u*u*Vector((-2.5, -8., 4.5)) +
             u**3*Vector((0, -1, 0)))
        return p, -math.pi*(1-smooth(t, 20, 21.2))
    return Vector((0, -1, 0)), 0.


def animate(scene, rig, sr, root, sw, sheep, cam):
    meshes = [o for o in scene.objects if o.name.startswith('Chupa_') and o.type == 'MESH']
    for frame in range(1, 752):
        t = (frame-1)/30
        scene.frame_set(frame)
        for r in (rig, sr):
            for b in r.pose.bones:
                b.matrix_basis = Matrix.Identity(4)
                b.rotation_mode = 'XYZ'
        # Unequal frequencies and a slow head turn avoid a metronomic grazing loop.
        sr.pose.bones['Shoulders'].rotation_euler.x = -1.30+.025*math.sin(t*1.7)
        sr.pose.bones['Neck'].rotation_euler.x = -.80+.045*math.sin(t*2.3+.4)
        sr.pose.bones['Head'].rotation_euler = (.60+.035*math.sin(t*3.7), .08*math.sin(t*.63), 0)
        sw.location = (0, .7, .004064235836267471)
        sw.rotation_euler = (0, 0, -.65*(1-smooth(t, 20.7, 21.2)))
        p, angle = path(t)
        root.location = p
        root.rotation_euler = (0, 0, angle)
        # Quiet weight shifts, head survey and tail follow-through in the shadows.
        stalk = 1-smooth(t, 13, 15)
        rig.pose.bones['Neck'].rotation_euler.x = -.07*stalk
        rig.pose.bones['Head'].rotation_euler.y = .06*math.sin(t*.7)*stalk
        for i in range(5):
            rig.pose.bones[f'Tail{i}'].rotation_euler.y = .035*math.sin(t*.85-i*.4)*stalk
        crouch = .26*(smooth(t, 19.25, 19.9)-smooth(t, 20, 20.20))
        if 20 < t < 21.2:
            flight = math.sin(math.pi*(t-20)/1.2)
            crouch += .5*flight
            rig.pose.bones['Spine'].rotation_euler.x = -.12*flight
            rig.pose.bones['Jaw'].rotation_euler.x = -.45*flight
            for i in range(5):
                rig.pose.bones[f'Tail{i}'].rotation_euler.x = .10*flight
        if t >= 21.2:
            impact = math.sin(math.pi*min(1., (t-21.2)/.45))
            struggle = smooth(t, 21.5, 22.)
            crouch = .24*impact+.035*math.sin((t-21.2)*9)*struggle
            rig.pose.bones['Neck'].rotation_euler.x = -.05-.035*math.sin(t*7)*struggle
            rig.pose.bones['Jaw'].rotation_euler.x = -.16-.06*math.sin(t*6)*struggle
            rig.pose.bones['Head'].rotation_euler.y = .025*math.sin(t*8)*struggle
            # Collapse occurs behind the attacker. Keep actual sheep rendered;
            # no visibility keys, scaling tricks, dust or substitute occluders.
            fall = smooth(t, 21.2, 21.7)
            sw.rotation_euler.y = math.pi/2*fall
            sw.location.x = -.75*fall-.10*math.sin(math.pi*fall)
            sw.location.y += .10*math.sin(math.pi*fall)
            sr.pose.bones['Shoulders'].rotation_euler.x *= 1-fall
            sr.pose.bones['Neck'].rotation_euler.x *= 1-fall
            sr.pose.bones['Head'].rotation_euler.x *= 1-fall
            sr.pose.bones['FrontFoot.L'].location.y = -.22*math.sin(t*9)*fall
            sr.pose.bones['BackFoot.R'].location.x = -.18*math.sin(t*8+.7)*fall
        for side in ('L', 'R'):
            stride = .16*math.sin(t*9+(0 if side == 'L' else math.pi))*smooth(t,12,12.3)*(1-smooth(t,14.7,15))
            rig.pose.bones['Arm.'+side].rotation_euler.x = crouch+stride
            rig.pose.bones['Forearm.'+side].rotation_euler.x = -1.4*crouch-.4*stride
            rig.pose.bones['Thigh.'+side].rotation_euler.x = crouch-stride
            rig.pose.bones['Shin.'+side].rotation_euler.x = -1.3*crouch
        bpy.context.view_layer.update()
        sw.location.z -= min(v.z for v in positions(sheep))
        # Bake floor compensation while retaining the authored airborne arc.
        root.location.z += p.z-min(v.z for m in meshes for v in positions(m))
        u = smooth(t, 18.5, 20.5)
        cam.location = mix((0, -12, 4), (.3, -4, 2.8), u)
        target = mix((0, .8, 1.5), (0, 0, .95), u)
        follow = smooth(t, 18.5, 20.3)*(1-smooth(t, 20.4, 21.2))
        target += Vector((0, 2*follow, 3*follow))
        cam.rotation_euler = (target-cam.location).to_track_quat('-Z', 'Y').to_euler()
        key_pose(rig, frame)
        key_pose(sr, frame)
        for obj in (root, sw, cam):
            for prop in ('location', 'rotation_euler'):
                obj.keyframe_insert(prop, frame=frame)
    # Dense samples are already eased analytically. Linear interpolation prevents
    # overshoot between export samples and survives the FBX round trip.
    for action in bpy.data.actions:
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for k in curve.keyframe_points:
                            k.interpolation = 'LINEAR'


def reference(scene, name, end):
    records = []
    meshes = [o for o in scene.objects if o.type == 'MESH' and not o.name.startswith('Env_')]
    cam = scene.camera
    for frame in range(1, end+1):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        samples = []
        for mesh in meshes:
            pts = positions(mesh)
            indices = list(range(0, len(pts), max(1, len(pts)//24)))
            samples.append(dict(name=mesh.name, vertices=[dict(zip('xyz', pts[i])) for i in indices]))
        records.append(dict(time=(frame-1)/30, meshes=samples,
                            camera=dict(zip('xyz', cam.matrix_world.translation)),
                            forward=dict(zip('xyz', cam.matrix_world.to_quaternion() @ Vector((0, 0, -1)))),
                            creature=dict(zip('xyz', bpy.data.objects['ChupacabrasAssetRoot'].location))))
    return dict(name=name, duration=(end-1)/30, production_duration=40,
                physical_device=False, source='11_rigs_contacto_demacrado_r01',
                fps=30, samples=records)


def main():
    names = [('13_calma'+SUFFIX, 601), ('14_ataque'+SUFFIX, 751)]
    for name, _ in names:
        for folder, ext in [('scenes', '.blend'), ('exports', '.fbx'), ('exports', '.json')]:
            if (ROOT/folder/(name+ext)).exists():
                raise FileExistsError(name+ext)
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/11_rigs_contacto_demacrado_r01.blend'), use_scripts=False)
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end, scene.render.fps = 1, 751, 30
    for o in list(scene.objects):
        o.animation_data_clear()
        if o.type == 'CAMERA' or o.name in ('UpperContact', 'LowerContact', 'NeckUpper', 'NeckLower'):
            bpy.data.objects.remove(o, do_unlink=True)
    rig, sr = bpy.data.objects['ChupaRig'], bpy.data.objects['SheepRig']
    root, sw = bpy.data.objects['ChupacabrasAssetRoot'], bpy.data.objects['SheepAssetRoot']
    sheep = bpy.data.objects['Sheep_Quaternius']
    sheep.data.shape_keys.animation_data_clear()
    sheep.data.shape_keys.key_blocks['WoolCompression'].value = 0
    with bpy.data.libraries.load(str(ROOT/'scenes/06_escenario.blend'), link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n.startswith('Env_')]
    for o in dst.objects:
        scene.collection.objects.link(o)
    cam = camera('CinemaCamera', (0, -12, 4), (0, .8, 1.5), 35)
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = 960, 540
    scene.render.resolution_percentage = 100
    animate(scene, rig, sr, root, sw, sheep, cam)
    for name, end in names:
        scene.frame_end = end
        data = reference(scene, name, end)
        export(name)
        (ROOT/'exports'/(name+'.json')).write_text(json.dumps(data, separators=(',', ':'))+'\n')
        print('ACTUACION_EXPORT_OK', name, data['duration'], flush=True)


if __name__ == '__main__':
    main()
