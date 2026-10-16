"""Hitos 8/9 originales: anatomía, detalle y vistas reproducibles sin sobrescribir.

blender -b -t 4 --python-exit-code 1 --python scripts/chupacabras.py -- 8
El paso 9 abre el hito 8. No crea rig ni actuación final.
"""
import json
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intercambio import ROOT, camera, empty, material, setup

SUFFIX = os.environ.get('CHUPA_SUFFIX', '')
NAMES = {8: '08_chupacabras_forma', 9: '09_chupacabras_acabado'}
COLORS = {'Skin': (.135, .17, .16), 'Ridge': (.23, .26, .235),
          'Mouth': (.036, .026, .028), 'Horn': (.105, .12, .12),
          'Ivory': (.59, .56, .40), 'Eye': (1, .64, .045)}


def ellipsoid(name, location, scale, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


def tube(name, points, radii, mat, sides=8):
    """Closed tapered polygon tube; variable rings follow the anatomical path."""
    points = [Vector(p) for p in points]
    vertices, faces = [], []
    for i, (p, radius) in enumerate(zip(points, radii)):
        tangent = (points[min(i+1, len(points)-1)]-points[max(0, i-1)]).normalized()
        ref = Vector((1, 0, 0)) if abs(tangent.x) < .9 else Vector((0, 1, 0))
        u = (ref-tangent*ref.dot(tangent)).normalized()
        v = tangent.cross(u)
        rx, ry = radius if isinstance(radius, tuple) else (radius, radius)
        for j in range(sides):
            a = j*math.tau/sides
            vertices.append(p+rx*math.cos(a)*u+ry*math.sin(a)*v)
    for i in range(len(points)-1):
        for j in range(sides):
            a = i*sides+j
            b = i*sides+(j+1)%sides
            faces.append((a, b, b+sides, a+sides))
    faces.extend([tuple(reversed(range(sides))),
                  tuple((len(points)-1)*sides+j for j in range(sides))])
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(mat)
    return obj


def join(objects, name):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def anatomy():
    scene = setup()
    mats = {n: material('Chupa_'+n, (.38, .40, .39) if n not in ('Eye', 'Mouth') else c)
            for n, c in COLORS.items()}
    skin = mats['Skin']
    # Continuous, narrow-waisted trunk with higher scapulae and digitigrade rear legs.
    body = [ellipsoid('Thorax', (0, -.02, 1.37), (.68, .79, .66), skin),
            ellipsoid('Waist', (0, -.71, 1.18), (.39, .63, .39), skin),
            ellipsoid('Pelvis', (0, -1.15, 1.13), (.49, .46, .43), skin),
            ellipsoid('Neck', (0, .51, 1.31), (.43, .48, .48), skin)]
    for s in (-1, 1):
        body.append(ellipsoid('Scapula', (s*.49, .03, 1.54), (.33, .48, .5), skin))
        body.append(tube('Foreleg', [(s*.53,.32,1.54),(s*.81,.07,1.12),
                         (s*.87,.27,.81),(s*.89,.70,.28),(s*.89,.83,.13)],
                         [.28,.22,.17,.105,.12], skin, 10))
        body.append(ellipsoid('Palm', (s*.89,.86,.14), (.21,.24,.12), skin))
        body.append(tube('Hindleg', [(s*.37,-1.15,1.23),(s*.63,-.92,.88),
                         (s*.69,-1.40,.41),(s*.68,-1.32,.14)],
                         [.32,.255,.12,.09], skin, 10))
        body.append(ellipsoid('Hindfoot',(s*.68,-1.17,.12),(.19,.29,.115),skin))
        for j in (-1,0,1):
            x = s*.89+j*.13
            body.append(tube('Finger', [(x,.89,.14),(x+j*.035,1.09,.105),
                             (x+j*.05,1.22-.04*abs(j),.09)], [.079,.062,.035],skin))
            x = s*.68+j*.12
            body.append(tube('Toe',[(x,-1.15,.12),(x,-.89,.085)], [.07,.04],skin))
    body.append(tube('Tail',[(0,-1.37,1.19),(.03,-1.85,1.10),(.12,-2.28,.79),
                            (.30,-2.72,.62),(.56,-3.03,.83),(.74,-3.14,1.14)],
                            [.235,.185,.135,.09,.045,.012],skin,10))
    obj = join(body,'Chupa_Body')
    # Fuse anatomical masses; no interpenetrating spherical joints in the final surface.
    mod = obj.modifiers.new('AnatomicalUnion','REMESH')
    mod.mode = 'VOXEL'; mod.voxel_size = .043
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod = obj.modifiers.new('RelaxUnion','SMOOTH'); mod.factor=.9; mod.iterations=4
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod = obj.modifiers.new('MobileSurface','DECIMATE'); mod.ratio=.25
    bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.data.materials.clear(); obj.data.materials.append(skin)
    # Head and lower jaw remain separate to allow articulation in step 11.
    head = [ellipsoid('Cranium',(0,.78,1.38),(.36,.38,.36),skin),
            tube('Muzzle',[(0,.90,1.31),(0,1.17,1.20),(0,1.48,1.13)],
                 [(.29,.21),(.22,.155),(.175,.115)],skin,10)]
    for s in (-1,1):
        head.append(tube('Cheek',[(s*.27,.77,1.27),(s*.30,1.02,1.15),
                                 (s*.20,1.29,1.10)],[.18,.12,.065],skin))
    join(head,'Chupa_Head')
    tube('Chupa_Jaw',[(0,.83,1.12),(0,1.05,.89),(0,1.44,.88)],
         [(.255,.105),(.20,.08),(.155,.055)],skin,10)
    for s in (-1,1):
        tube('Chupa_Ear'+str(s),[(s*.27,.59,1.57),(s*.43,.54,1.92),
                                (s*.48,.44,2.16)],[(.16,.09),(.10,.045),.002],skin,4)
        eye=ellipsoid('Chupa_Eye'+str(s),(s*.265,1.027,1.43),(.099,.061,.088),mats['Eye'])
        eye.rotation_euler.z=s*-.35
    # Five broad crest masses establish the silhouette before detail.
    for i,(y,z,h) in enumerate([(.44,1.76,.70),(.05,1.96,.77),(-.34,1.89,.67),
                                (-.73,1.60,.52),(-1.08,1.49,.31)]):
        tube('Chupa_Crest'+str(i),[(0,y,z),(0,y-.10,z+h*.62),(0,y-.29,z+h)],
             [(.105,.22),(.065,.12),.002],skin,4)
    root=empty('ChupacabrasAssetRoot')
    for o in list(scene.objects):
        if o.type=='MESH': o.parent=root
    for name,pos in [('JawPivot',(0,.83,1.12)),('BiteSocket',(0,1.30,1.01))]:
        empty(name,pos).parent=root
    return scene,root


def detail(root):
    mats={n:bpy.data.materials.get('Chupa_'+n) or material('Chupa_'+n,c)
          for n,c in COLORS.items()}
    for n,c in COLORS.items(): mats[n].diffuse_color=(*c,1)
    for o in list(root.children):
        if o.name.startswith(('Chupa_Crest','Chupa_Ear')):
            o.data.materials.clear(); o.data.materials.append(mats['Horn'])
    added=[]
    for s in (-1,1):
        # Slanted brow lowers expression without hiding the yellow eye.
        added.append(tube('Brow',[(s*.10,1.06,1.47),(s*.27,1.075,1.51),
                                  (s*.40,.89,1.60)],[.065,.075,.07],mats['Ridge'],6))
        added.append(ellipsoid('Nostril',(s*.105,1.487,1.15),(.042,.022,.025),mats['Mouth']))
        for y,x in [(1.33,.16),(1.14,.22),(.96,.25)]:
            added.append(tube('Fang',[(s*x,y,1.125),(s*x*.97,y+.014,1.04),
                                    (s*x*.95,y+.03,.99)],[.045,.03,.001],mats['Ivory'],6))
        for y,x in [(1.36,.12),(1.20,.16),(1.03,.19)]:
            added.append(tube('LowerTooth',[(s*x,y,.91),(s*x,y+.02,1.015)],
                              [.033,.001],mats['Ivory'],5))
        for j in (-1,0,1):
            x=s*.89+j*.18; y=1.22-.04*abs(j)
            added.append(tube('Claw',[(x,y,.095),(x,y+.13,.11),(x,y+.24,.032)],
                              [.047,.036,.0015],mats['Ivory'],6))
            x=s*.68+j*.12
            added.append(tube('HindClaw',[(x,-.89,.09),(x,-.76,.09),(x,-.67,.03)],
                              [.04,.025,.0015],mats['Ivory'],6))
        # Sparse geometric tufts follow neck, scapula and spine rather than a fur shell.
        for i in range(5):
            y=.48-i*.24; z=1.49+math.sin(i*.63)*.16
            added.append(tube('NeckTuft',[(s*.43,y,z),(s*.67,y-.13,z+.02),
                                         (s*.82,y-.36,z-.14)],
                              [(.10,.14),(.055,.09),.001],mats['Ridge'],4))
        for i in range(4):
            y=-.45-i*.25; z=1.57-i*.05
            added.append(tube('SpinalTuft',[(s*.18,y,z),(s*.32,y-.10,z+.14),
                                           (s*.40,y-.31,z+.11)],
                              [(.075,.12),(.05,.07),.001],mats['Horn'],4))
        for i in range(6):
            y=.40-i*.24; z=1.86-max(0,i-2)*.13
            height=.42-max(0,i-2)*.04
            added.append(tube('FineCrest',[(s*.12,y,z),
                                          (s*.19,y-.12,z+height*.7),
                                          (s*.22,y-.30,z+height)],
                              [(.043,.075),(.025,.04),.001],mats['Ridge'],5))
        # Faceted tendons and cheek planes are modeled, portable color detail.
        added.append(tube('CheekRidge',[(s*.33,.85,1.29),(s*.27,1.19,1.11)],
                          [.075,.012],mats['Ridge'],5))
    # Small front incisors, separated by dark mouth space.
    for x in (-.08,0,.08):
        added.append(tube('Incisor',[(x,1.47,1.075),(x,1.475,1.016)],
                          [.024,.009],mats['Ivory'],5))
    for obj in added: obj.parent=root
    # Group detail by material, except jaw's lower teeth: they need their own future bone.
    groups={n:[o for o in added if o.active_material==mats[n] and not o.name.startswith('LowerTooth')]
            for n in ('Ivory','Ridge','Horn','Mouth')}
    for n,objects in groups.items():
        if objects: join(objects,'Chupa_Detail_'+n).parent=root
    lower=[o for o in bpy.context.scene.objects if o.name.startswith('LowerTooth')]
    join(lower,'Chupa_LowerTeeth').parent=root


def unwrap(root):
    meshes=[o for o in root.children if o.type=='MESH']
    bpy.ops.object.select_all(action='DESELECT')
    for obj in meshes: obj.select_set(True)
    bpy.context.view_layer.objects.active=meshes[0]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.018)
    bpy.ops.object.mode_set(mode='OBJECT')


def report(root):
    meshes=[o for o in root.children if o.type=='MESH']
    bpy.context.view_layer.update()
    out=[]
    for o in meshes:
        o.data.calc_loop_triangles()
        vs=[o.matrix_world@v.co for v in o.data.vertices]
        out.append(dict(name=o.name,triangles=len(o.data.loop_triangles),
                        min=dict(zip('xyz',[min(v[i] for v in vs) for i in range(3)])),
                        max=dict(zip('xyz',[max(v[i] for v in vs) for i in range(3)])),
                        materials=[m.name for m in o.data.materials],uv=len(o.data.uv_layers)))
    return dict(original_model=True,rig=False,physical_device=False,facing='+Y Blender / +Z Unity',
                triangles=sum(o['triangles'] for o in out),objects=out,
                palette=[dict(name='Chupa_'+n,color=dict(zip('rgba',m.diffuse_color)))
                         for n in COLORS for m in [bpy.data.materials['Chupa_'+n]]])


def views(scene,name):
    scene.render.engine='BLENDER_WORKBENCH'
    shade=scene.display.shading
    shade.light='STUDIO'; shade.studio_light='paint.sl'
    shade.color_type='MATERIAL'; shade.show_shadows=True; shade.show_cavity=True
    shade.cavity_type='BOTH'; shade.show_specular_highlight=False
    shade.background_type='WORLD'; scene.world.color=(.045,.055,.065)
    scene.render.resolution_x=960; scene.render.resolution_y=720
    scene.view_settings.view_transform='Standard'
    cam=camera('ReviewCamera',(5,7,3.3),(0,-.55,1.1))
    cam.data.type='ORTHO'; cam.data.ortho_scale=5.5;scene.camera=cam
    for label,pos in [('frente',(0,8,2)),('perfil',(8,0,2)),
                      ('espalda',(0,-8,2)),('tres_cuartos',(5,7,3.5))]:
        cam.location=pos
        cam.rotation_euler=(Vector((0,-.5,1.2))-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(ROOT/'previews'/f'{name}_{label}.png')
        bpy.ops.render.render(write_still=True)


def main():
    step=int(sys.argv[sys.argv.index('--')+1])
    name=NAMES[step]+SUFFIX
    for folder,ext in [('scenes','.blend'),('exports','.fbx'),('exports','.json')]:
        if (ROOT/folder/(name+ext)).exists(): raise FileExistsError(name+ext)
    if step==8:
        scene,root=anatomy()
    else:
        source=os.environ.get('CHUPA_FORM','08_chupacabras_forma')
        bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(source+'.blend')),use_scripts=False)
        scene=bpy.context.scene;root=bpy.data.objects['ChupacabrasAssetRoot']
        detail(root)
    unwrap(root)
    info=report(root)
    assert info['triangles']<18000
    (ROOT/'exports'/(name+'.json')).write_text(json.dumps(info,indent=2)+'\n')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [root]+list(root.children): obj.select_set(True)
    bpy.ops.export_scene.fbx(filepath=str(ROOT/'exports'/(name+'.fbx')),use_selection=True,
        object_types={'MESH','EMPTY'},axis_forward='-Z',axis_up='Y',apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=False,bake_anim=False)
    # Save after adding review camera, before rendering. A second run never overwrites.
    cam=camera('AssetCamera',(5,7,3.5),(0,-.5,1.2));scene.camera=cam
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'scenes'/(name+'.blend')))
    views(scene,name)
    print('CHUPACABRAS_MODEL_OK '+json.dumps(dict(name=name,triangles=info['triangles'])))


if __name__=='__main__': main()
