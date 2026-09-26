"""Paso 5: bloqueo geométrico de 40 s, independiente de las demos.

Exporta un clip conjunto con cámara; las formas son provisionales, no los
recursos finales de los pasos 6–11. No sobrescribe fuentes ni exportaciones.
"""
import json
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Quaternion, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intercambio import ROOT, camera, cube, empty, export, material, setup


def attach(obj, parent):
    obj.parent = parent
    return obj


def ellipsoid(name, location, scale, mat, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    obj.parent = parent
    return obj


def key(obj, t, location=None, angle=None):
    if location is not None:
        obj.location = location
        obj.keyframe_insert('location', frame=round(t*30)+1)
    if angle is not None:
        obj.rotation_euler.z = math.radians(angle)
        obj.keyframe_insert('rotation_euler', frame=round(t*30)+1)


def main():
    scene = setup()
    wool = material('Wool', (.78, .74, .58))
    hide = material('Hide', (.23, .32, .30))
    dark = material('Dark', (.08, .07, .065))
    soil = material('Soil', (.18, .15, .14))
    wood = material('Wood', (.28, .18, .15))
    eye = material('Eyes', (1, .7, .12))
    moon = material('Moon', (.78, .79, .67))
    cube('Ground', (0, 2, -.15), (100, 100, .3), soil)
    cube('BarnMass', (-3.3, 3.1, 1.5), (3.4, 2.2, 3), wood)
    vertices=[(-5.1,1.9,3),(-1.5,1.9,3),(-3.3,1.9,4.3),
              (-5.1,4.3,3),(-1.5,4.3,3),(-3.3,4.3,4.3)]
    mesh=bpy.data.meshes.new('RoofMass')
    mesh.from_pydata(vertices,[],[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)])
    roof=bpy.data.objects.new('BarnRoof',mesh)
    bpy.context.collection.objects.link(roof)
    roof.data.materials.append(wood)
    cube('BarnDoor', (-3.3, 1.985, 1), (1.05, .03, 2), dark)
    ellipsoid('Moon', (3, 8, 4), (.65, .2, .65), moon)
    pair = empty('PairPath')
    creature = empty('CreatureRoot')
    creature.parent = pair
    # Broad shoulder block intentionally tests complete occlusion without dust.
    attach(cube('CreatureShoulders', (0, 0, 1), (2.0, 1.3, 1.9), hide), creature)
    ellipsoid('CreatureHead', (0, .75, .85), (.48, .65, .48), hide, creature)
    for x in (-.23, .23):
        ellipsoid('CreatureEye', (x, 1.27, 1), (.075, .055, .075), eye, creature)
    for x in (-.70, .70):
        for y in (-.42, .42):
            attach(cube('CreatureLeg', (x, y, .28), (.26, .3, .56), hide), creature)
    for y in (-.55, -.15, .25):
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=.2, depth=.6, location=(0, y, 2.12))
        obj = bpy.context.object
        obj.name = 'CreatureCrest'
        obj.data.materials.append(hide)
        obj.parent = creature
    tail = ellipsoid('CreatureTail', (0, -1, .6), (.17, .9, .17), hide, creature)
    sheep = empty('SheepRoot', (0, 1.7, 0))
    sheep.parent = pair
    ellipsoid('SheepBody', (0, 0, .75), (.47, .68, .43), wool, sheep)
    head = empty('SheepHeadPivot', (0, -.62, .72))
    head.parent = sheep
    ellipsoid('SheepHead', (0, -.12, 0), (.23, .33, .22), dark, head)
    for x in (-.3, .3):
        for y in (-.4, .4):
            attach(cube('SheepLeg', (x, y, .27), (.14, .15, .54), dark), sheep)
    mouth = empty('Mouth', (0, 1, .75)); mouth.parent = creature
    neck = empty('Neck', (0, -.7, .75)); neck.parent = sheep
    # Independent calm sheep; attach to the shared contact path at landing.
    for t, loc, angle in [
        (0, (0,-1,0), 0), (25,(0,-1,0),0), (26,(-.35,-1,0),-70),
        (29,(-2.8,-.8,0),-90), (31,(-3.5,.2,0),-180),
        (33,(-2.3,1.2,0),-270), (36,(4,1.2,0),-270),
        (39,(14,1.2,0),-270), (40,(14,1.2,0),-270)]:
        key(pair,t,loc,angle)
    for t, loc in [
        (0,(-2.25,5.4,0)), (12,(-2.20,5.25,0)), (14,(-2.25,5.25,0)),
        (15,(-3.3,5.4,0)), (20-1/30,(-3.3,5.4,0)),
        (20,(0,-7,0)), (20.3,(0,-4,2.5)), (20.8,(0,-1,2)),
        (21.2,(0,0,0)), (25,(0,0,0)), (40,(0,0,0))]:
        key(creature,t,loc)
    for t, angle in [(0,-90),(20-1/30,-90),(20,0),(40,0)]:
        key(creature,t,angle=angle)
    sheep.rotation_mode='QUATERNION'
    legs=[obj for obj in bpy.data.objects if obj.name.startswith('SheepLeg')]
    for frame in range(1, 1202):
        t=(frame-1)/30
        fall=min(1,max(0,(t-21.2)/.8))
        roll=90*fall + (4*math.sin(t*9) if 25<=t<39 else 0)
        sheep.rotation_quaternion=(Quaternion((1,0,0),math.radians(-20*fall))
                                   @ Quaternion((0,1,0),math.radians(roll)))
        sheep.location=Vector((0,1,.75))-sheep.rotation_quaternion@Vector((0,-.7,.75))
        sheep.keyframe_insert('location',frame=frame)
        sheep.keyframe_insert('rotation_quaternion',frame=frame)
        for i,leg in enumerate(legs):
            leg.rotation_euler.x=.3*math.sin(t*7+i*math.pi) if 25<=t<39 else 0
            leg.keyframe_insert('rotation_euler',frame=frame)
        # Motion stays small enough to retain neck contact after landing.
        head.rotation_euler.x = .35*math.sin(t*1.4) if t < 20 else 0
        head.keyframe_insert('rotation_euler',frame=frame)
        if 25 <= t < 39:
            tail.rotation_euler.z = .12*math.sin(t*5)
            tail.keyframe_insert('rotation_euler',frame=frame)
    cam = camera('CinemaCamera', (0,-12,4), (0,.8,1.5), 35)
    scene.camera = cam
    shots = [(0,(0,-12,4),(0,.8,1.5),35),
             (20-1/30,(0,-12,4),(0,.8,1.5),35),
             (20,(0,-6,1.1),(0,0,.95),32),
             (25-1/30,(0,-6,1.1),(0,0,.95),32),
             (25,(7,-7,5),(0,0,1),35),
             (28,(5,-11,6),(0,0,1),35),
             (40,(5,-11,6),(0,0,1),35)]
    for t, pos, target, lens in shots:
        cam.location = pos
        cam.rotation_euler = (Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.keyframe_insert('location',frame=round(t*30)+1)
        cam.keyframe_insert('rotation_euler',frame=round(t*30)+1)
        cam.data.lens = lens
        cam.data.keyframe_insert('lens',frame=round(t*30)+1)
    # Explicit linear interpolation; no spline overshoot through the contact path.
    for action in bpy.data.actions:
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for point in curve.keyframe_points:
                            point.interpolation='LINEAR'
    for name,t in [('PASTOREO',0),('OCULTO',15),('SALTO',20),('ATERRIZAJE',21.2),
                   ('ARRASTRE_IZQUIERDA',25),('GIRO_A_DERECHA',31),('VACIO',39),('LIMITE',40)]:
        scene.timeline_markers.new(name,frame=round(t*30)+1)
    records=[]
    for frame in range(1,1202):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        t=(frame-1)/30
        error=(mouth.matrix_world.translation-neck.matrix_world.translation).length
        if t >= 21.2:
            assert error < 1e-5, (t,error)
        if frame % 30 == 1 or frame in (637,750,751):
            records.append(dict(time=t,contact_error=error,
                                camera=dict(zip('xyz',cam.matrix_world.translation)),
                                pair=dict(zip('xyz',pair.matrix_world.translation))))
    name='05_blocking'+os.environ.get('CHUPA_SUFFIX','')
    export(name)
    (ROOT/'exports'/(name+'.json')).write_text(json.dumps(dict(duration=40,fps=30,
        landing=21.2,samples=records,placeholder_assets=True),indent=2)+'\n')


if __name__=='__main__':
    main()
