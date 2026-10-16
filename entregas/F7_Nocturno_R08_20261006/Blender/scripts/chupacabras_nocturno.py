"""Revisión artística independiente: piel, cresta orgánica y respiración exportable.

CHUPA_ART_REV=r01 blender -b -t 6 --python-exit-code 1 --python scripts/chupacabras_nocturno.py
"""
import json
import math
import os
import random
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils import noise as mnoise

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chupacabras import tube, join, ellipsoid
from figura_forma import apply, pose, smoothstep
import figura_superficie as surf

ROOT = Path(__file__).resolve().parents[1]
NAME = 'chupacabras_nocturno_' + os.environ.get('CHUPA_ART_REV', 'r08')
OUT = ROOT / 'previews' / NAME
TEX = ROOT / 'exports' / NAME


def material(name, colors, roughness, skin=False):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*colors[1], 1)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    coord = nodes.new('ShaderNodeTexCoord')
    def noise(scale, detail=3, vector=None):
        n = nodes.new('ShaderNodeTexNoise')
        n.inputs['Scale'].default_value = scale
        n.inputs['Detail'].default_value = detail
        n.inputs['Roughness'].default_value = .72
        links.new(vector if vector is not None else coord.outputs['Object'], n.inputs['Vector'])
        return n.outputs['Fac']
    pigment = noise(19, 5)
    links.new(surf.ramp(nodes, links, pigment, colors, 'Pigmento dérmico irregular'), bsdf.inputs['Base Color'])
    links.new(surf.ramp(nodes, links, noise(32), [(r,)*3 for r in roughness], 'Sequedad y grasa'), bsdf.inputs['Roughness'])
    if skin:
        stretch = nodes.new('ShaderNodeVectorMath'); stretch.operation = 'MULTIPLY'
        links.new(coord.outputs['Object'], stretch.inputs[0]); stretch.inputs[1].default_value = (1, 1.2, 4)
        fold = nodes.new('ShaderNodeBump'); fold.inputs['Strength'].default_value = .46; fold.inputs['Distance'].default_value = .024
        links.new(noise(12, 4, stretch.outputs[0]), fold.inputs['Height'])
        pore = nodes.new('ShaderNodeTexVoronoi'); pore.feature = 'DISTANCE_TO_EDGE'; pore.inputs['Scale'].default_value = 72
        links.new(coord.outputs['Object'], pore.inputs['Vector'])
        bump = nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .32; bump.inputs['Distance'].default_value = .006
        links.new(pore.outputs['Distance'], bump.inputs['Height']); links.new(fold.outputs['Normal'], bump.inputs['Normal'])
        links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    else:
        bump = nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .18; bump.inputs['Distance'].default_value = .002
        links.new(noise(100), bump.inputs['Height']); links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def skull(root, skin, mouth, ivory, eye):
    # Continuous cranial masses with real recessed sockets; no applied angry brow.
    parts=[ellipsoid('Boveda',(0,.69,1.52),(.285,.30,.35),skin),
           tube('Puente_nasal',[(0,.82,1.49),(0,1.06,1.27),(0,1.25,1.04)],[(.20,.19),(.16,.13),(.115,.09)],skin,20)]
    for s in (-1,1):
        parts.append(tube('Arco_cigomatico',[(s*.22,.69,1.47),(s*.265,.91,1.28),(s*.13,1.19,1.02)],[.11,.070,.045],skin,14))
    head=join(parts,'Craneo')
    mod=head.modifiers.new('Craneo_continuo','REMESH');mod.mode='VOXEL';mod.voxel_size=.008;apply(head,mod)
    mod=head.modifiers.new('Transiciones','SMOOTH');mod.factor=.65;mod.iterations=5;apply(head,mod)
    objects=[head]
    for s in (-1,1):
        center=(s*.191,.964,1.49)
        socket=ellipsoid('Cavidad_orbital',center,(.129,.116,.134),mouth)
        mod=head.modifiers.new('Orbita_hundida','BOOLEAN');mod.operation='DIFFERENCE';mod.object=socket;apply(head,mod)
        bpy.data.objects.remove(socket,do_unlink=True)
        lining=ellipsoid('Fondo_orbita',(s*.191,.855,1.49),(.103,.045,.105),mouth);objects.append(lining)
        eyeball=ellipsoid('Ojo_velado',(s*.191,.885,1.49),(.079,.064,.082),eye)
        mod=eyeball.modifiers.new('Cornea_lisa','SUBSURF');mod.levels=2;apply(eyeball,mod);objects.append(eyeball)
    mod=head.modifiers.new('Retopologia_orbitas','REMESH');mod.mode='VOXEL';mod.voxel_size=.007;apply(head,mod)
    mod=head.modifiers.new('Suavizado_orbitas','SMOOTH');mod.factor=.32;mod.iterations=3;apply(head,mod)
    mod=head.modifiers.new('Craneo_presupuesto','DECIMATE');mod.ratio=.30;apply(head,mod)
    jaw=tube('Mandibula',[(0,.74,1.16),(0,.98,.95),(0,1.24,.902)],[(.19,.07),(.145,.045),(.101,.036)],skin,18)
    mod=jaw.modifiers.new('Mandibula_lisa','SUBSURF');mod.levels=2;apply(jaw,mod);objects.append(jaw)
    # Oral cavity keeps the fine irregular teeth readable, without a broad cartoon lip.
    objects.append(ellipsoid('Boca',(0,1.10,.975),(.137,.19,.043),mouth))
    objects.append(ellipsoid('Nariz',(0,1.285,1.068),(.098,.026,.049),skin))
    for s in (-1,1):
        objects.append(ellipsoid('Fosa_nasal',(s*.049,1.307,1.070),(.016,.008,.023),mouth))
        for i in range(5):
            y=1.255-i*.060; x=s*(.082+i*.016); z=1.009+i*.025
            length=.115 if i==1 else .043+i*.004
            objects.append(tube('Diente_superior',[(x,y,z),(x*.99,y+.006,z-length*.45),(x*.93,y+.018,z-length)],[.016 if i!=1 else .022,.010,.0008],ivory,10))
            objects.append(tube('Diente_inferior',[(x*.87,y,.922+i*.026),(x*.86,y+.01,.955+i*.026)],[.012,.0007],ivory,9))
    for i,x in enumerate((-.060,-.025,.012,.047)):
        objects.append(tube('Incisivo',[(x,1.295,1.01),(x,1.306,.97-(i%2)*.009)],[.011,.003],ivory,9))
    for obj in objects:
        bpy.context.view_layer.objects.active=obj
        bpy.ops.object.select_all(action='DESELECT');obj.select_set(True)
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
        for v in obj.data.vertices:v.co=pose(v.co.copy())
        obj.parent=root
    return objects


def geometry():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/F2_chupacabras_forma_r04.blend'), use_scripts=False)
    root = bpy.data.objects['ChupacabrasAssetRoot']
    skin = material('Nocturno_Piel', ((.0035,.004,.0045),(.029,.022,.017)), (.72,.92), True)
    horn = material('Nocturno_Queratina', ((.008,.009,.010),(.046,.039,.029)), (.32,.59))
    inner = material('Nocturno_Oreja', ((.009,.005,.006),(.039,.019,.018)), (.55,.78), True)
    mouth = material('Nocturno_Mucosa', ((.007,.004,.004),(.037,.014,.016)), (.22,.42))
    ivory = material('Nocturno_Marfil', ((.11,.072,.030),(.51,.40,.22)), (.28,.47))
    eye = material('Nocturno_Ojo', ((.16,.12,.048),(.49,.38,.18)), (.23,.32))
    for obj in list(root.children):
        if obj.type != 'MESH':
            continue
        if obj.name.startswith(('Chupa_Crest','Chupa_Ear','Chupa_Detail_Ridge','Chupa_Detail_Horn','Chupa_Head','Chupa_Jaw','Chupa_Eye','Chupa_LowerTeeth','Chupa_Detail_Mouth')):
            bpy.data.objects.remove(obj, do_unlink=True)
            continue
        if obj.name == 'Chupa_Detail_Ivory':
            import bmesh
            bm=bmesh.new();bm.from_mesh(obj.data)
            bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.z>.5],context='VERTS')
            bm.to_mesh(obj.data);bm.free()
        if obj.name.startswith('Chupa_Eye'):
            center = sum((v.co for v in obj.data.vertices), Vector())/len(obj.data.vertices)
            for v in obj.data.vertices:
                v.co = center + Vector(((v.co.x-center.x)*1.18, (v.co.y-center.y)*1.12, (v.co.z-center.z)*1.43))
            mat = eye
        elif 'Ivory' in obj.name or 'Teeth' in obj.name: mat = ivory
        elif 'Mouth' in obj.name or 'Sockets' in obj.name: mat = mouth
        else: mat = skin
        obj.data.materials.clear(); obj.data.materials.append(mat)
        if obj.name in ('Chupa_Body', 'Chupa_Head', 'Chupa_Jaw'):
            if obj.name != 'Chupa_Body':
                mod = obj.modifiers.new('Resolucion_rostro', 'DECIMATE'); mod.ratio = .26; apply(obj, mod)
            mod = obj.modifiers.new('Superficie_organica', 'SUBSURF'); mod.levels = 1; apply(obj, mod)
            mod = obj.modifiers.new('Presupuesto_superficie', 'DECIMATE'); mod.ratio = .36; apply(obj, mod)
            normals = [v.normal.copy() for v in obj.data.vertices]
            for v, normal in zip(obj.data.vertices, normals):
                # Very shallow physical irregularity; finer pores remain in normal maps.
                v.co += normal * (.0028*mnoise.noise_vector(v.co*24).x)
        if obj.name == 'Chupa_Jaw' or 'LowerTeeth' in obj.name:
            for v in obj.data.vertices: v.co.z += .043*smoothstep(.8,1.3,v.co.y)
    skull(root, skin, mouth, ivory, eye)
    body = bpy.data.objects['Chupa_Body']
    tree = BVHTree.FromPolygons([v.co for v in body.data.vertices], [list(p.vertices) for p in body.data.polygons])
    rng = random.Random(41)
    added = []
    # Dense, swept needle crest: varying length and spacing avoid a row of identical horns.
    for row in (-1,0,1):
        for i in range(29):
            y = .59-i*.071+rng.uniform(-.022,.022)
            x = row*(.095+rng.uniform(-.025,.025))
            hit = tree.ray_cast(Vector((x,y,3.2)), Vector((0,0,-1)))
            if hit[0] is None: continue
            p = hit[0]; h=(.22+.42*math.exp(-((y+.02)/.64)**2))*rng.uniform(.72,1.2)
            if row: h *= .73
            end = p+Vector((row*.13+rng.uniform(-.035,.035),-.30*h/.5,h))
            spine = tube('Espina_dorsal', [p-Vector((0,0,.035)),p+Vector((row*.025,-.015,h*.23)),p.lerp(end,.68)+Vector((0,.045,.015)),end], [.019,.013,.006,.0006], horn, 7)
            added.append(spine)
    # Short, sparse whisker-like spines attached to the shoulders, not floating armor.
    for side in (-1,1):
        for i in range(18):
            y=rng.uniform(-.40,.46); z=rng.uniform(1.5,1.86)
            hit=tree.ray_cast(Vector((side*1.4,y,z)),Vector((-side,0,0)))
            if hit[0] is None: continue
            p=hit[0]; end=p+Vector((side*rng.uniform(.08,.17),-.15,rng.uniform(.05,.16)))
            added.append(tube('Cerda_escapular',[p-Vector((side*.018,0,0)),p.lerp(end,.55),end],[.011,.005,.0005],horn,6))
        # Broad, thin pointed ears with recessed warm inner skin.
        pts=[(side*.205,.63,1.54),(side*.30,.59,1.77),(side*.36,.54,1.99),(side*.39,.49,2.16)]
        for name, mat, offset, radii in [('Oreja',skin,0,[(.115,.065),(.127,.053),(.07,.029),.0009]),('Concha',inner,.046,[(.068,.012),(.083,.014),(.038,.010),.0006])]:
            ear=tube(name,[(x,y+offset,z) for x,y,z in pts],radii,mat,12)
            for v in ear.data.vertices: v.co=pose(v.co.copy())
            added.append(ear)
    for obj in added: obj.parent=root
    objects=[o for o in root.children if o.type=='MESH']
    for obj in objects:
        for poly in obj.data.polygons: poly.use_smooth=True
    obj=join(objects,'Chupacabras_Nocturno'); obj.parent=root
    mod=obj.modifiers.new('Triangulos_exportables','TRIANGULATE'); apply(obj,mod)
    import bmesh
    bm=bmesh.new(); bm.from_mesh(obj.data)
    assert all(e.is_manifold for e in bm.edges), 'La geometría debe estar cerrada antes del horneado'
    assert all(f.calc_area()>1e-14 for f in bm.faces), 'Caras degeneradas'
    bm.free()
    return root,obj


def textures(obj):
    surf.TEX=TEX
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(72),island_margin=.012,area_weight=.5)
    bpy.ops.uv.seams_from_islands(); bpy.ops.uv.unwrap(method='ANGLE_BASED',margin=.012)
    bpy.ops.uv.average_islands_scale()
    # Preserve body/face texel density: needle-shaped quill charts must not
    # inflate to the minimum inradius of an entire skin island.
    bpy.ops.uv.pack_islands(rotate=True,margin=.0025)
    bpy.ops.object.mode_set(mode='OBJECT')
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=16
    scene.render.bake.margin=12; scene.render.bake.margin_type='EXTEND'
    scene.render.bake.use_selected_to_active=False
    scene.render.bake.use_pass_direct=False; scene.render.bake.use_pass_indirect=False; scene.render.bake.use_pass_color=True
    scene.render.bake.normal_space='TANGENT'
    albedo=surf.bake(obj,'BaseColor','DIFFUSE','sRGB')
    rough=surf.bake(obj,'Roughness','ROUGHNESS','Non-Color')
    normal=surf.bake(obj,'Normal','NORMAL','Non-Color')
    pixels=np.empty(surf.SIZE*surf.SIZE*4,dtype=np.float32); rough.pixels.foreach_get(pixels)
    pixels=pixels.reshape(-1,4); smooth=1-pixels[:,0].copy(); pixels[:,:3]=0; pixels[:,3]=smooth
    mask=bpy.data.images.new('MetallicSmoothness',width=surf.SIZE,height=surf.SIZE,alpha=True)
    mask.colorspace_settings.name='Non-Color'; mask.pixels.foreach_set(pixels.ravel())
    mask.filepath_raw=str(TEX/'MetallicSmoothness.png'); mask.file_format='PNG'; mask.save()
    mat=bpy.data.materials.new('Nocturno_Surface'); mat.use_nodes=True
    nodes,links=mat.node_tree.nodes,mat.node_tree.links; bsdf=nodes.get('Principled BSDF')
    for img,socket in ((albedo,'Base Color'),(rough,'Roughness')):
        n=nodes.new('ShaderNodeTexImage'); n.image=img; links.new(n.outputs['Color'],bsdf.inputs[socket])
    n=nodes.new('ShaderNodeTexImage'); n.image=normal; bump=nodes.new('ShaderNodeNormalMap')
    links.new(n.outputs['Color'],bump.inputs['Color']); links.new(bump.outputs['Normal'],bsdf.inputs['Normal'])
    for p in obj.data.polygons:p.material_index=0
    obj.data.materials.clear(); obj.data.materials.append(mat)
    for img in (albedo,rough,normal,mask): img.filepath=bpy.path.relpath(img.filepath,start=str(ROOT/'scenes')); img.pack()


def breathe(root,obj):
    data=bpy.data.armatures.new('Respiracion'); rig=bpy.data.objects.new('Respiracion',data)
    bpy.context.collection.objects.link(rig); rig.parent=root
    bpy.context.view_layer.objects.active=rig; rig.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    for name,p,tail,parent in [('Root',(0,0,0),(0,0,.3),None),('Torax',(0,-.05,1.4),(0,-.05,1.8),'Root'),('Cabeza',(0,.5,1.4),(0,.8,1.4),'Root'),('Cola',(0,-1.4,1.3),(0,-1.9,1.1),'Root')]:
        b=data.edit_bones.new(name); b.head=p; b.tail=tail
        if parent:b.parent=data.edit_bones[parent]
    bpy.ops.object.mode_set(mode='OBJECT')
    groups={name:obj.vertex_groups.new(name=name) for name in ('Root','Torax','Cabeza','Cola')}
    for v in obj.data.vertices:
        x,y,z=v.co
        head=smoothstep(.43,.77,y)*smoothstep(.55,.85,z)
        tail=(1-smoothstep(-1.9,-1.42,y))*smoothstep(.3,.65,z)
        chest=(1-head)*(1-tail)*smoothstep(.35,1.36,z)*smoothstep(-1.38,-.55,y)
        weights={'Cabeza':head,'Cola':tail,'Torax':chest,'Root':max(0,1-head-tail-chest)}
        total=sum(weights.values())
        for name,w in weights.items():
            if w>1e-6:groups[name].add([v.index],w/total,'REPLACE')
    mod=obj.modifiers.new('Respiracion','ARMATURE'); mod.object=rig
    rig.animation_data_create(); rig.animation_data.action=bpy.data.actions.new('Respiracion_4s')
    scene=bpy.context.scene; scene.render.fps=24; scene.frame_start=1; scene.frame_end=97
    for frame in range(1,98):
        phase=math.tau*(frame-1)/96
        breath=(1-math.cos(phase))/2
        chest=rig.pose.bones['Torax']; chest.scale=(1+.055*breath,1+.038*breath,1+.012*breath)
        chest.location=(0,.016*breath,0)
        head=rig.pose.bones['Cabeza']; head.rotation_mode='XYZ'; head.rotation_euler=(.013*math.sin(phase-.35),0,.007*math.sin(phase))
        head.location=(0,0,.011*breath)
        tail=rig.pose.bones['Cola']; tail.rotation_mode='XYZ'; tail.rotation_euler=(0,.022*math.sin(phase-.6),.018*math.sin(phase-.6))
        for b in (chest,head,tail):
            for prop in ('scale','location','rotation_euler'):b.keyframe_insert(prop,frame=frame)
    scene.frame_set(1)
    return rig


def studio():
    scene=bpy.context.scene
    for obj in list(scene.objects):
        if obj.type=='LIGHT':bpy.data.objects.remove(obj,do_unlink=True)
    scene.world.use_nodes=True
    scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.09,.105,.12,1)
    scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.55
    for name,location,energy,size,color in [('Key',(3,4,6),1100,4,(1,.83,.67)),('Fill',(-4,2,3),750,3,(.66,.80,1)),('Rim',(1,-4,4),1400,3,(.67,.81,1))]:
        data=bpy.data.lights.new(name,'AREA'); data.energy=energy; data.shape='DISK'; data.size=size; data.color=color
        light=bpy.data.objects.new(name,data); scene.collection.objects.link(light); light.location=location
        light.rotation_euler=(Vector((0,-.5,1.2))-light.location).to_track_quat('-Z','Y').to_euler()
    scene.render.engine='CYCLES'; scene.cycles.samples=32; scene.cycles.use_denoising=True
    scene.render.resolution_x=1200; scene.render.resolution_y=900; scene.render.resolution_percentage=100
    scene.view_settings.view_transform='AgX'
    scene.camera.data.type='ORTHO'; scene.camera.data.ortho_scale=5.5
    scene.camera.location=(5,7,3.5); scene.camera.rotation_euler=(Vector((0,-.5,1.2))-scene.camera.location).to_track_quat('-Z','Y').to_euler()


def main():
    blend=ROOT/'scenes'/(NAME+'.blend'); fbx=ROOT/'exports'/(NAME+'.fbx')
    if any(p.exists() for p in (blend,fbx,OUT,TEX)):raise FileExistsError('Elegir CHUPA_ART_REV nueva; se conservan versiones anteriores.')
    OUT.mkdir(); TEX.mkdir()
    root,obj=geometry(); obj.data.calc_loop_triangles()
    assert len(obj.data.loop_triangles)<130000
    print('GEOMETRY',len(obj.data.loop_triangles),flush=True)
    textures(obj); rig=breathe(root,obj); studio()
    bpy.ops.object.select_all(action='DESELECT')
    for o in (root,obj,rig):o.select_set(True)
    bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'MESH','EMPTY','ARMATURE'},axis_forward='-Z',axis_up='Y',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=False,use_mesh_modifiers=False,add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,path_mode='STRIP')
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    info=dict(name=NAME,source='F2_chupacabras_forma_r04',triangles=len(obj.data.loop_triangles),meshes=1,materials=1,bones=4,atlas_size=2048,animation='Respiracion_4s',duration=4,fps=24,physical_device=False,texture_authorship='Original procedural skin, wrinkles, pores, keratin and eyes; no external image copies.',maps={'BaseColor':'sRGB','Normal':'Tangent +Y, linear','Roughness':'linear, authoring','MetallicSmoothness':'linear, R=0 A=1-roughness'})
    (TEX/'manifest.json').write_text(json.dumps(info,indent=2)+'\n')
    for name,eye,target,scale in [('tres_cuartos',(5,7,3.5),(0,-.5,1.2),5.5),('perfil',(8,0,2.3),(0,-.5,1.2),5.5),('rostro',(1.7,5,2.2),(0,.95,1.45),1.9),('espalda',(3,-7,3),(0,-.5,1.2),5.5)]:
        scene=bpy.context.scene; cam=scene.camera; cam.location=eye; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=scale
        scene.render.filepath=str(OUT/(name+'.png')); bpy.ops.render.render(write_still=True)
    print('NOCTURNO_OK '+json.dumps(info),flush=True)


if __name__=='__main__':main()
