"""Paso 11: rig original y muestra conjunta de seis segundos; contacto sobre malla.

La muestra empieza con el agarre establecido. El ataque/agarre narrativo es 14–15.
"""
import json
import math
import os
import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from intercambio import ROOT, empty, camera
from oveja import positions, export
from rig_oveja import key_pose, linear_actions

NAME='11_rigs_contacto'+os.environ.get('CHUPA_SUFFIX','')
SOURCE=os.environ.get('CHUPA_MODEL','09_chupacabras_acabado')

def segment_distance(p,a,b):
    d=b-a
    return (p-(a+d*max(0,min(1,(p-a).dot(d)/d.length_squared)))).length


def make_rig(root, meshes):
    data=bpy.data.armatures.new('ChupaSkeleton')
    rig=bpy.data.objects.new('ChupaRig',data);bpy.context.collection.objects.link(rig)
    rig.parent=root;rig.show_in_front=True
    bpy.context.view_layer.objects.active=rig;rig.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    defs=[('Root',(0,0,0),(0,0,.4),None),
          ('Pelvis',(0,-1.1,1.25),(0,-.5,1.5),'Root'),
          ('Spine',(0,-.5,1.5),(0,.2,1.65),'Pelvis'),
          ('Neck',(0,.2,1.65),(0,.65,1.4),'Spine'),
          ('Head',(0,.65,1.4),(0,1.35,1.15),'Neck'),
          ('Jaw',(0,.83,1.12),(0,1.44,.88),'Head')]
    tail=[(0,-1.37,1.19),(.03,-1.85,1.10),(.12,-2.28,.79),(.30,-2.72,.62),(.56,-3.03,.83),(.74,-3.14,1.14)]
    for i in range(5):defs.append((f'Tail{i}',tail[i],tail[i+1],'Pelvis' if i==0 else f'Tail{i-1}'))
    for side,sign in [('L',1),('R',-1)]:
        defs.extend([(f'Arm.{side}',(sign*.53,.32,1.54),(sign*.81,.07,1.12),'Spine'),
                     (f'Forearm.{side}',(sign*.81,.07,1.12),(sign*.89,.70,.28),f'Arm.{side}'),
                     (f'Hand.{side}',(sign*.89,.70,.28),(sign*.89,1.2,.10),f'Forearm.{side}'),
                     (f'Thigh.{side}',(sign*.37,-1.15,1.23),(sign*.63,-.92,.88),'Pelvis'),
                     (f'Shin.{side}',(sign*.63,-.92,.88),(sign*.69,-1.40,.41),f'Thigh.{side}'),
                     (f'Foot.{side}',(sign*.69,-1.40,.41),(sign*.68,-.9,.10),f'Shin.{side}')])
    if 'demacrado' in SOURCE:
        # Rest joints follow the revised shoulder/pelvis, not the old body width.
        heads={'Pelvis':(0,-1.15,1.31),'Tail0':(0,-1.37,1.31)}
        for side,sign in [('L',1),('R',-1)]:
            heads['Arm.'+side]=(sign*.40,.32,1.65)
            heads['Thigh.'+side]=(sign*.28,-1.15,1.31)
        defs=[(n,heads.get(n,a),b,parent) for n,a,b,parent in defs]
    for name,a,b,parent in defs:
        bone=data.edit_bones.new(name);bone.head=a;bone.tail=b
        if parent:bone.parent=data.edit_bones[parent]
    bpy.ops.object.mode_set(mode='OBJECT')
    segments={name:(Vector(a),Vector(b)) for name,a,b,parent in defs}
    for mesh in meshes:
        # Convert local coordinates to root space before skinning; UV/materials are preserved.
        bpy.ops.object.select_all(action='DESELECT');mesh.select_set(True)
        bpy.context.view_layer.objects.active=mesh
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
        for name in segments:mesh.vertex_groups.new(name=name)
        for v in mesh.data.vertices:
            p=v.co
            if mesh.name in ('Chupa_Jaw','Chupa_LowerTeeth'):
                candidates=['Jaw']
            elif mesh.name.startswith(('Chupa_Head','Chupa_Ear','Chupa_Eye','Chupa_Detail_Mouth')):
                candidates=['Head']
            elif mesh.name.startswith('Chupa_Crest'):
                candidates=['Neck'] if p.y>.3 else ['Spine'] if p.y>-.65 else ['Pelvis']
            elif p.y> .75 and p.z>.65:
                candidates=['Head']
            elif p.y< -1.65:
                candidates=['Tail'+str(i) for i in range(5)]
            elif p.z<.70 or (abs(p.x)>.53 and p.z<1.5):
                side='L' if p.x>0 else 'R'
                candidates=[n+'.'+side for n in ('Arm','Forearm','Hand')] if p.y>-.45 else [n+'.'+side for n in ('Thigh','Shin','Foot')]
            else:
                candidates=['Pelvis','Spine','Neck']
            distances=sorted((segment_distance(p,*segments[n]),n) for n in candidates)
            nearest=distances[:2]
            # Smooth two-bone transition; rigid detailing on jaws/head stays exact.
            weights=[1/max(.035,d)**4 for d,n in nearest];total=sum(weights)
            for (distance,n),w in zip(nearest,weights):mesh.vertex_groups[n].add([v.index],w/total,'REPLACE')
        mod=mesh.modifiers.new('ChupaSkin','ARMATURE');mod.object=rig
    for b in rig.pose.bones:b.rotation_mode='XYZ'
    rig.animation_data_create();rig.animation_data.action=bpy.data.actions.new('ContactTest_Chupa_6s')
    return rig


def bone_point(rig,bone,rest):
    b=rig.pose.bones[bone]
    return rig.matrix_world @ b.matrix @ b.bone.matrix_local.inverted() @ Vector(rest)


def bisect(function, lo, hi, tolerance=1e-6):
    a=function(lo);b=function(hi)
    if a*b>0:raise ValueError(('No bracket',lo,hi,a,b))
    for _ in range(26):
        mid=(lo+hi)/2;v=function(mid)
        if abs(v)<tolerance:return mid
        if a*v<=0:hi=mid
        else:lo=mid;a=v
    return (lo+hi)/2


def main():
    for d,e in [('scenes','.blend'),('exports','.fbx'),('exports','.json')]:
        if (ROOT/d/(NAME+e)).exists():raise FileExistsError(NAME+e)
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(SOURCE+'.blend')),use_scripts=False)
    scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=181;scene.render.fps=30
    root=bpy.data.objects['ChupacabrasAssetRoot']
    meshes=[o for o in root.children if o.type=='MESH']
    # Model-only scene: discard cameras/review props from this new working scene.
    for o in list(scene.objects):
        if o!=root and o not in meshes:bpy.data.objects.remove(o,do_unlink=True)
    rig=make_rig(root,meshes)
    with bpy.data.libraries.load(str(ROOT/'scenes/10_rig_oveja.blend'),link=False) as (src,dst):
        dst.objects=['SheepAssetRoot','SheepRig','Sheep_Quaternius']
    for o in dst.objects:scene.collection.objects.link(o)
    sheep=bpy.data.objects['Sheep_Quaternius'];sr=bpy.data.objects['SheepRig'];sw=bpy.data.objects['SheepAssetRoot']
    # Preserve exact loop triangles, including the reused asset's overlapping edge.
    # Edit-mode triangulation silently drops one face on this source; rebuild by index.
    old=sheep.data;old.calc_loop_triangles()
    triangles=list(old.loop_triangles)
    group_names=[g.name for g in sheep.vertex_groups]
    weights=[[(g.group,g.weight) for g in v.groups] for v in old.vertices]
    shapes=[(k.name,[v.co.copy() for v in k.data],k.value) for k in old.shape_keys.key_blocks]
    data=bpy.data.meshes.new('Sheep_FixedTriangles')
    data.from_pydata([v.co[:] for v in old.vertices],[],[tuple(t.vertices) for t in triangles])
    for mat in old.materials:data.materials.append(mat)
    for p,t in zip(data.polygons,triangles):p.material_index=t.material_index;p.use_smooth=False
    for uv in old.uv_layers:
        new_uv=data.uv_layers.new(name=uv.name)
        for p,t in zip(data.polygons,triangles):
            for new_loop,old_loop in zip(p.loop_indices,t.loops):new_uv.data[new_loop].uv=uv.data[old_loop].uv
    sheep.data=data
    sheep.vertex_groups.clear()
    for name in group_names:sheep.vertex_groups.new(name=name)
    for i,groups in enumerate(weights):
        for group,weight in groups:sheep.vertex_groups[group].add([i],weight,'REPLACE')
    for name,coords,value in shapes:
        key=sheep.shape_key_add(name=name);key.value=value
        for v,co in zip(key.data,coords):v.co=co
    assert len(data.polygons)==612 and len(data.vertices)==307
    for o in [sw,sr]:o.animation_data_clear()
    sr.animation_data_create();sr.animation_data.action=bpy.data.actions.new('ContactTest_Sheep_6s')
    compression=sheep.data.shape_keys.key_blocks['WoolCompression']
    sheep.data.shape_keys.animation_data_clear();compression.value=1
    for bone in sr.pose.bones:bone.matrix_basis=Matrix.Identity(4);bone.rotation_mode='XYZ'
    for track in (sr.animation_data.nla_tracks if sr.animation_data else []):track.mute=True
    sequence=empty('SequenceRoot');root.parent=sequence;sw.parent=sequence
    # These world-space probes are baked from actual evaluated surface points.
    probes={n:empty(n) for n in ['UpperContact','LowerContact','NeckUpper','NeckLower']}
    for p in probes.values():p.parent=sequence
    # Pick an actual mirrored neck-band vertex; after side roll, negative X is upper.
    sw.rotation_euler=(0,0,0);sw.location=(0,0,.004064235836267471)
    bpy.context.view_layer.update();neutral=positions(sheep)
    wool={i for p in sheep.data.polygons if p.material_index==0 for i in p.vertices}
    neck_index=min(wool,key=lambda i:(neutral[i]-Vector((-.10,-.55,.84))).length)
    # Actual distal fang / lower tooth vertices, not empty sockets in air.
    upper_mesh=bpy.data.objects['Chupa_Detail_Ivory'];lower_mesh=bpy.data.objects['Chupa_LowerTeeth']
    face_width=.76 if 'demacrado' in SOURCE else 1
    upper_index=min(range(len(upper_mesh.data.vertices)),key=lambda i:(upper_mesh.data.vertices[i].co-Vector((.152*face_width,1.36,.99))).length)
    lower_index=min(range(len(lower_mesh.data.vertices)),key=lambda i:(lower_mesh.data.vertices[i].co-Vector((.12*face_width,1.38,1.015))).length)
    upper_rest=upper_mesh.data.vertices[upper_index].co.copy();lower_rest=lower_mesh.data.vertices[lower_index].co.copy()
    records=[];max_contact=0;min_floor=100
    for frame in range(1,182):
        scene.frame_set(frame);t=(frame-1)/30
        # Lateral displacement test. Production locomotion is authored in step 15.
        root.location=(-.25*t,0,0)
        for b in rig.pose.bones:b.matrix_basis=Matrix.Identity(4)
        for i in range(5):rig.pose.bones[f'Tail{i}'].rotation_euler.y=.10*math.sin(t*2-i*.5)
        rig.pose.bones['Spine'].rotation_euler.y=.025*math.sin(t*2)
        for b in sr.pose.bones:b.matrix_basis=Matrix.Identity(4)
        sr.pose.bones['Neck'].rotation_euler.x=-.2+.035*math.sin(t*4)
        sr.pose.bones['Head'].rotation_euler.x=.15
        sr.pose.bones['FrontFoot.L'].location.y=-.4-.25*math.sin(t*6)
        sr.pose.bones['BackFoot.L'].location.x=.25*math.sin(t*6+.7)
        sw.rotation_euler=(0,math.pi/2,math.pi/2)
        sw.location=(0,0,0)
        bpy.context.view_layer.update()
        sw.location.z=-min(v.z for v in positions(sheep))
        bpy.context.view_layer.update()
        neck=positions(sheep)[neck_index]
        def head_error(angle):
            rig.pose.bones['Neck'].rotation_euler.x=angle
            bpy.context.view_layer.update()
            return bone_point(rig,'Head',upper_rest).z-neck.z
        head_values=[(-1.8+i*.05,head_error(-1.8+i*.05)) for i in range(37)]
        head_brackets=[(a[0],b[0]) for a,b in zip(head_values,head_values[1:]) if a[1]*b[1]<=0]
        if not head_brackets:raise ValueError(('Head reach',frame,head_values))
        bisect(head_error,*head_brackets[-1])
        upper=bone_point(rig,'Head',upper_rest)
        sw.location.x+=upper.x-neck.x;sw.location.y+=upper.y-neck.y
        bpy.context.view_layer.update()
        sheep_points=positions(sheep)
        # Lower tooth closes onto the side/underside of the deformed wool surface.
        tree=BVHTree.FromPolygons(sheep_points,[list(p.vertices) for p in sheep.data.polygons])
        def jaw_error(angle):
            rig.pose.bones['Jaw'].rotation_euler.x=angle
            bpy.context.view_layer.update()
            p=bone_point(rig,'Jaw',lower_rest)
            hit,normal,index,distance=tree.find_nearest(p)
            return (p-hit).dot(normal)
        # Search small anatomically plausible opening range for a sign change.
        values=[]
        for i in range(41):
            angle=-.8+i*.025
            try:values.append((angle,jaw_error(angle)))
            except ValueError:values.append((angle,None))
        brackets=[(a[0],b[0]) for a,b in zip(values,values[1:]) if a[1] is not None and b[1] is not None and a[1]*b[1]<=0]
        if not brackets:raise ValueError(('No lower contact',frame,values))
        bisect(jaw_error,*brackets[0])
        lower=bone_point(rig,'Jaw',lower_rest)
        lower_hit=tree.find_nearest(lower)[0]
        upper=positions(upper_mesh)[upper_index];lower=positions(lower_mesh)[lower_index]
        neck=positions(sheep)[neck_index]
        vals=[upper,lower,neck,lower_hit]
        for (name,obj),value in zip(probes.items(),vals):obj.location=value;obj.keyframe_insert('location',frame=frame)
        max_contact=max(max_contact,(upper-neck).length,(lower-lower_hit).length)
        key_pose(rig,frame);key_pose(sr,frame)
        for obj in [root,sw]:
            for prop in ['location','rotation_euler']:obj.keyframe_insert(prop,frame=frame)
        compression.keyframe_insert('value',frame=frame)
        sample_meshes=[]
        for mesh in [sheep]+meshes:
            pts=positions(mesh)
            min_floor=min(min_floor,min(p.z for p in pts))
            # All sheep vertices; sampled creature vertices on every frame for manageable references.
            inds=list(range(len(pts))) if mesh==sheep else list(range(0,len(pts),max(1,len(pts)//80)))
            sample_meshes.append(dict(name=mesh.name,indices=inds,vertices=[dict(zip('xyz',pts[i])) for i in inds]))
        records.append(dict(time=t,shape=1,label={1:'grip_start',61:'grip_middle',121:'grip_turn',181:'grip_end'}.get(frame,''),meshes=sample_meshes))
    for o in [root,sw]+list(probes.values()):o.animation_data.action.name='ContactTest_'+o.name
    sheep.data.shape_keys.animation_data.action.name='ContactTest_Wool'
    linear_actions()
    assert max_contact<.0001,max_contact
    assert min_floor>-.001,min_floor
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')))
    export(ROOT/'exports'/(NAME+'.fbx'),True)
    for mesh in meshes+[sheep]:mesh.data.calc_loop_triangles()
    report=dict(name=NAME,source=SOURCE,triangles=sum(len(m.data.loop_triangles) for m in meshes+[sheep]),duration=6,creature_bones=len(rig.data.bones),max_contact=max_contact,min_height=min_floor,
                upper_vertex=upper_index,lower_vertex=lower_index,neck_vertex=neck_index,
                physical_device=False,samples=records)
    (ROOT/'exports'/(NAME+'.json')).write_text(json.dumps(report,separators=(',',':'))+'\n')
    scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=960;scene.render.resolution_y=540
    scene.render.resolution_percentage=100;scene.display.shading.color_type='MATERIAL'
    scene.display.shading.show_cavity=True;scene.display.shading.light='STUDIO'
    scene.camera=camera('RigReviewCamera',(6,6,3.5),(-.6,0,.8),40)
    for frame,label in [(1,'grip_start'),(61,'grip_middle'),(181,'grip_end')]:
        scene.frame_set(frame);scene.render.filepath=str(ROOT/'previews'/f'{NAME}_{label}.png');bpy.ops.render.render(write_still=True)
    scene.camera.location=(2.5,3,1.4);scene.camera.rotation_euler=(Vector((0,1,.4))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.frame_set(1);scene.render.filepath=str(ROOT/'previews'/f'{NAME}_contact_close.png');bpy.ops.render.render(write_still=True)
    print('RIG_CONTACT_OK',json.dumps({k:v for k,v in report.items() if k!='samples'}))

if __name__=='__main__':main()
