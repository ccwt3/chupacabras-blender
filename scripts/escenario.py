"""Paso 6: escenario estático de bajo costo, con recorrido R04 comprobado.

No modifica el bloqueo ni las demos. CHUPA_SUFFIX permite otra revisión.
"""
import json
import math
import os
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intercambio import ROOT, cube, export, material, setup

NAME = '06_escenario' + os.environ.get('CHUPA_SUFFIX', '')


def bounds(obj):
    points = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return ([min(p[i] for p in points) for i in range(3)],
            [max(p[i] for p in points) for i in range(3)])


def mesh(name, vertices, faces, mat):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def cone(name, pos, radius, height, mat):
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=radius, radius2=0,
                                   depth=height, location=pos)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def main():
    outputs = [ROOT/'scenes'/f'{NAME}.blend', ROOT/'exports'/f'{NAME}.fbx',
               ROOT/'exports'/f'{NAME}.json']
    if any(p.exists() for p in outputs):
        raise FileExistsError('Use CHUPA_SUFFIX; no se sobrescriben entregas')
    # Read actual evaluated R04 trajectories, without writing that source.
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/05_blocking_r04.blend'))
    # Move only the calm/stalking section upstage with the barn; keep timings/camera/drag.
    creature = bpy.data.objects['CreatureRoot']
    for layer in creature.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    if curve.data_path == 'location' and curve.array_index == 1:
                        for key in curve.keyframe_points:
                            if key.co.x < 601:
                                key.co.y += 3.2
                                key.handle_left.y += 3.2
                                key.handle_right.y += 3.2
    actors = [o for o in bpy.context.scene.objects if o.type == 'MESH'
              and o.name.startswith(('Creature', 'Sheep'))]
    swept = []
    for frame in range(1, 1201):
        bpy.context.scene.frame_set(frame)
        bpy.context.view_layer.update()
        swept.append([bounds(o) for o in actors])
    # Separate context export retains all provisional actors and the original camera.
    # Its original static forms will be disabled only in the new Unity scene.
    context_name = NAME + '_contexto'
    export(context_name)
    scene = setup()
    rng = random.Random(6024)
    colors = {
        'Soil': (.19, .155, .13), 'DryPatches': (.245, .205, .16),
        'Wood': (.28, .21, .16), 'WoodLight': (.37, .285, .20),
        'ShadowWood': (.09, .065, .055), 'Roof': (.14, .20, .25),
        'Grass': (.26, .29, .20), 'Forest': (.045, .09, .13),
        'Rock': (.24, .28, .29), 'Moon': (.84, .87, .75),
    }
    mats = {name: material('Env_'+name, color) for name, color in colors.items()}
    cube('Ground', (0, 5, -.13), (110, 110, .24), mats['Soil'])
    # Roof/walls stay behind the drag path and in front of the stalking volume.
    # Opaque backing retains the proven hiding silhouette despite plank gaps.
    cube('BarnBacking', (-3.3, 2.48, 1.5), (3.4, 1.24, 3), mats['ShadowWood'])
    for i in range(18):
        x = -4.91 + i*.19
        height = 2.94-rng.uniform(0,.07)
        obj = cube('BarnPlank', (x, 1.838, height/2+.025),
                   (.18, .055, height), mats['WoodLight' if i%4 == 0 else 'Wood'])
        obj.rotation_euler.y = rng.uniform(-.003,.003)
    for side in (-5.025,-1.575):
        for i in range(7):
            cube('SidePlank', (side, 1.93+i*.18, 1.49), (.05,.17,2.98), mats['Wood'])
    # Door, lintel, brace and iron strap are shallow geometry, no texture dependency.
    cube('DoorRecess', (-3.3,1.79,1.02),(1.22,.03,2.04),mats['ShadowWood'])
    for i in range(6):
        cube('DoorBoard',(-3.8+i*.20,1.766,1),(.185,.04,1.98),mats['Wood'])
    for x in (-3.98,-2.62):
        cube('DoorPost',(x,1.73,1.09),(.11,.10,2.18),mats['WoodLight'])
    cube('Lintel',(-3.3,1.73,2.17),(1.48,.11,.14),mats['WoodLight'])
    for z in (.4,1.65):
        cube('DoorRail',(-3.3,1.72,z),(1.2,.06,.105),mats['WoodLight'])
    brace=cube('DoorBrace',(-3.3,1.70,1.02),(.095,.065,1.75),mats['WoodLight'])
    brace.rotation_euler.y=math.radians(34)
    for x in (-3.49,-3.10):
        cube('DoorLatch',(x,1.665,1.07),(.14,.025,.045),mats['ShadowWood'])
    vertices=[(-5.05,1.82,3),(-1.55,1.82,3),(-3.3,1.82,4.25),
              (-5.05,3.12,3),(-1.55,3.12,3),(-3.3,3.12,4.25)]
    mesh('BarnGables',vertices,[(0,1,2),(3,5,4)],mats['Wood'])
    for side in (-1,1):
        x=-3.3+side*.93
        panel=cube('RoofPanel',(x,2.47,3.635),(2.28,1.36,.12),mats['Roof'])
        panel.rotation_euler.y=side*math.atan2(1.25,1.75)
    for x in (-4.8,-4.3,-3.8,-2.8,-2.3,-1.8):
        z=4.28-abs(x+3.3)*1.25/1.75
        cube('RoofSeam',(x,2.47,z),(.045,1.36,.045),mats['Roof'])
    # Geometry checks use individual bounding boxes, conservative for slanted pieces.
    bpy.context.view_layer.update()
    barn = [o for o in scene.objects if o.type=='MESH' and o.name!='Ground']
    for obj in barn:
        obj.location.y += 3.2
    bpy.context.view_layer.update()
    collisions=[]
    for obj in barn:
        lo,hi=bounds(obj)
        for frame, boxes in enumerate(swept,1):
            if any(all(min(hi[i],b[i])-max(lo[i],a[i]) > .005 for i in range(3)) for a,b in boxes):
                collisions.append((obj.name,frame)); break
    if collisions:
        raise AssertionError(('Barn intersects actor bounds',collisions))
    # Union of every trajectory sample, padded horizontally, reserves all exits.
    def clear(x,y,pad=.30):
        return not any(a[0]-pad<x<b[0]+pad and a[1]-pad<y<b[1]+pad
                       for boxes in swept[::3] for a,b in boxes)
    for i in range(45):
        x,y=rng.uniform(-15,18),rng.uniform(-9,15)
        radius=rng.uniform(.18,.7)
        n=5
        points=[(x,y,-.002)] + [(x+radius*math.cos(a*math.tau/n),
                                y+radius*.5*math.sin(a*math.tau/n),-.002) for a in range(n)]
        mesh('DryPatch',points,[(0,j+1,(j+1)%n+1) for j in range(n)],mats['DryPatches'])
    for i in range(155):
        x,y=rng.uniform(-12,16),rng.uniform(-7,14)
        if not clear(x,y,.65) or (-5.4<x<-1.2 and 4.6<y<6.7):
            continue
        for j in range(3):
            a=j*math.tau/3+rng.random()
            h=rng.uniform(.12,.30)
            dx,dy=.11*math.cos(a),.11*math.sin(a)
            mesh('GrassTuft',[(x-dy*.3,y+dx*.3,0),(x+dy*.3,y-dx*.3,0),
                              (x+dx,y+dy,h)],[(0,1,2),(2,1,0)],mats['Grass'])
    for i in range(22):
        x,y=rng.uniform(-13,16),rng.uniform(-7,14)
        if not clear(x,y,.8) or (-5.5<x<-1.1 and 4.4<y<6.8):
            continue
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(x,y,.05))
        obj=bpy.context.object; obj.name='Stone'
        obj.scale=(rng.uniform(.12,.32),.18,.11)
        obj.data.materials.append(mats['Rock'])
    for i in range(38):
        x=-27+i*1.5+rng.uniform(-.3,.3); y=rng.uniform(13,20)
        h=rng.uniform(3,7)
        cone('Pine',(x,y,h*.49),h*.24,h*.78,mats['Forest'])
        cone('PineTop',(x,y,h*.77),h*.16,h*.62,mats['Forest'])
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(3,8,4))
    moon=bpy.context.object; moon.name='Moon'; moon.scale=(.65,.2,.65)
    moon.data.materials.append(mats['Moon'])
    # One mesh per shared material keeps static renderer/submesh count bounded.
    for mat in mats.values():
        objs=[o for o in scene.objects if o.type=='MESH' and o.active_material==mat]
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objs: obj.select_set(True)
        bpy.context.view_layer.objects.active=objs[0]
        bpy.ops.object.join()
        obj=bpy.context.object; obj.name=mat.name
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    meshes=[o for o in scene.objects if o.type=='MESH']
    total=0
    for obj in meshes:
        obj.data.calc_loop_triangles(); total+=len(obj.data.loop_triangles)
    assert total<12000 and len(meshes)<=10
    bpy.ops.wm.save_as_mainfile(filepath=str(outputs[0]))
    bpy.ops.export_scene.fbx(filepath=str(outputs[1]),object_types={'MESH'},axis_forward='-Z',
        axis_up='Y',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',
        bake_space_transform=False,use_mesh_modifiers=True,bake_anim=False)
    outputs[2].write_text(json.dumps(dict(blender=bpy.app.version_string,
        meshes=len(meshes),triangles=total,materials=colors,route_frames=1200,
        barn_actor_aabb_overlaps=collisions,physical_device=False,
        grass_route_sampling_hz=10,units='meters',
        objects=[dict(name=o.name,bounds=bounds(o)) for o in meshes]),indent=2)+'\n')

if __name__=='__main__':
    main()
