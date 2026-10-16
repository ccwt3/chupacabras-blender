"""AR attack: preserve R08 surface, extend its rig, reuse the CC0 sheep.

Creates a 17.5-second source: grazing/attack/return 0–13.5 s, then a 4 s loop.
Run with a new CHUPA_ATTACK_REV to preserve previous outputs.
"""
import json
import math
import os
import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figura_forma import smoothstep
from rig_contacto import segment_distance
from oveja import positions
from intercambio import camera

ROOT = Path(__file__).resolve().parents[1]
NAME = 'ataque_ar_' + os.environ.get('CHUPA_ATTACK_REV', 'r01')
FPS = 24
METERS = .08
SHEEP_Y = 3.1
LAND_Y = 1.5
REST = 13.5
END = int((REST+4)*FPS)+1
WALK_START, WALK_END = 6.5, 13.0


def pulse(t, start, peak, end):
    return smoothstep(start, peak, t) * (1-smoothstep(peak, end, t))


def extend_rig(mesh, rig):
    bpy.ops.object.select_all(action='DESELECT')
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')
    segments = {}
    for side, sign in [('L', 1), ('R', -1)]:
        points = {
            'Brazo': ((sign*.40,.32,1.65),(sign*.81,.07,1.12)),
            'Antebrazo': ((sign*.81,.07,1.12),(sign*.89,.70,.28)),
            'Mano': ((sign*.89,.70,.28),(sign*.89,1.2,.10)),
            'Muslo': ((sign*.28,-1.15,1.31),(sign*.63,-.92,.88)),
            'Pierna': ((sign*.63,-.92,.88),(sign*.69,-1.40,.41)),
            'Pie': ((sign*.69,-1.40,.41),(sign*.68,-.9,.10)),
        }
        parents = {'Brazo':'Root','Antebrazo':'Brazo.'+side,'Mano':'Antebrazo.'+side,
                   'Muslo':'Root','Pierna':'Muslo.'+side,'Pie':'Pierna.'+side}
        for name, (a,b) in points.items():
            full = name+'.'+side
            bone = rig.data.edit_bones.new(full)
            bone.head, bone.tail = a,b
            bone.parent = rig.data.edit_bones[parents[name]]
            segments[full] = (Vector(a),Vector(b))
    jaw = rig.data.edit_bones.new('Mandibula')
    jaw.head=(.07277,.82235,1.07336);jaw.tail=(.17,1.28,.96336)
    jaw.parent=rig.data.edit_bones['Cabeza']
    bpy.ops.object.mode_set(mode='OBJECT')
    old_names = [g.name for g in mesh.vertex_groups]
    for name in segments: mesh.vertex_groups.new(name=name)
    for v in mesh.data.vertices:
        x,y,z = v.co
        mask = smoothstep(.30,.62,abs(x))*(1-smoothstep(.95,1.65,z))*smoothstep(-2.05,-1.75,y)
        if mask < 1e-5: continue
        side = 'L' if x>0 else 'R'
        names = ('Brazo','Antebrazo','Mano') if y>-.48 else ('Muslo','Pierna','Pie')
        nearest = sorted((segment_distance(v.co,*segments[n+'.'+side]),n+'.'+side) for n in names)[:2]
        original = [(old_names[g.group],g.weight) for g in v.groups if g.group<len(old_names)]
        for name,w in original: mesh.vertex_groups[name].add([v.index],w*(1-mask),'REPLACE')
        weights = [1/max(.04,d)**4 for d,n in nearest]
        for (d,name),w in zip(nearest,weights): mesh.vertex_groups[name].add([v.index],mask*w/sum(weights),'REPLACE')
        # Mobile skin supports four influences; preserve normalized strongest weights.
        groups = sorted([(g.weight,g.group) for g in v.groups],reverse=True)
        total = sum(w for w,i in groups[:4])
        for w,i in groups: mesh.vertex_groups[i].remove([v.index])
        for w,i in groups[:4]: mesh.vertex_groups[i].add([v.index],w/total,'REPLACE')
    # The joined R08 retains disconnected jaw/teeth islands: weight whole islands.
    parents=list(range(len(mesh.data.vertices)))
    def find(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    for edge in mesh.data.edges:
        a,b=map(find,edge.vertices);parents[a]=b
    islands={}
    for v in mesh.data.vertices:islands.setdefault(find(v.index),[]).append(v)
    jaw_group=mesh.vertex_groups.new(name='Mandibula');jaw_vertices=0
    for vs in islands.values():
        low=min(v.co.z for v in vs);high=max(v.co.z for v in vs)
        if low>.85 and max(v.co.y for v in vs)> .9 and ((len(vs)>300 and high<1.2) or (len(vs)==18 and high<1.08) or (len(vs)>100 and high<1.03)):
            for v in vs:
                for g in list(v.groups):mesh.vertex_groups[g.group].remove([v.index])
                jaw_group.add([v.index],1,'REPLACE');jaw_vertices+=1
    assert 900<jaw_vertices<1500,jaw_vertices
    for b in rig.pose.bones: b.rotation_mode='XYZ'


def mesh_floor(obj):
    evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return min((evaluated.matrix_world@Vector(corner)).z for corner in evaluated.bound_box)


def key_object(obj, frame):
    for prop in ('location','rotation_euler','scale'): obj.keyframe_insert(prop,frame=frame)


def return_path(t):
    # Three tangent-connected Beziers make one clockwise walking turn, ending at home.
    u=smoothstep(WALK_START,WALK_END,t)*3
    curves=[((.12,LAND_Y),(.12,2.0),(1.65,1.15),(1.65,.25)),
            ((1.65,.25),(1.65,-.65),(1.1,-1.1),(.55,-1.1)),
            ((.55,-1.1),(0,-1.1),(0,-.6),(0,0))]
    i=min(2,int(u));v=u-i;a,b,c,d=[Vector((*p,0)) for p in curves[i]]
    point=(1-v)**3*a+3*(1-v)**2*v*b+3*(1-v)*v*v*c+v**3*d
    tangent=3*(1-v)**2*(b-a)+6*(1-v)*v*(c-b)+3*v*v*(d-c)
    yaw=-math.atan2(tangent.x,tangent.y)
    if i>=1 and yaw>=0:yaw-=2*math.pi
    return point,yaw


def foot_target(t,rest,phase):
    period=.50
    cycle=(t-WALK_START)/period+phase;k=math.floor(cycle);fraction=cycle-k
    start=max(WALK_START,min(WALK_END,WALK_START+(k-phase)*period))
    end=max(WALK_START,min(WALK_END,WALK_START+(k+1-phase)*period))
    def planted(at):
        p,yaw=return_path(min(WALK_END,at+period*.31))
        return p+Matrix.Rotation(yaw,3,'Z')@rest
    a,b=planted(start),planted(end)
    if start==WALK_START:
        p,yaw=return_path(WALK_START);a=p+Matrix.Rotation(yaw,3,'Z')@rest
    swing=smoothstep(.62,1,fraction)
    target=a.lerp(b,swing)
    target.z+=.16*math.sin(math.pi*swing)
    # Settle the last step on the exact original footprint before the idle loop.
    return target.lerp(rest,smoothstep(WALK_END-.25,REST,t))


def plant_limb(rig,upper,lower,foot,target):
    a=rig.pose.bones[upper];b=rig.pose.bones[lower];c=rig.pose.bones[foot]
    shoulder=a.bone.head_local;elbow=b.bone.head_local;wrist=c.bone.head_local
    local=rig.matrix_world.inverted()@target
    direction=local-shoulder;distance=direction.length
    l1=(elbow-shoulder).length;l2=(wrist-elbow).length
    distance=min(l1+l2-.0001,max(abs(l1-l2)+.0001,distance));direction.normalize()
    along=(l1*l1-l2*l2+distance*distance)/(2*distance)
    pole=elbow-shoulder;pole-=direction*pole.dot(direction);pole.normalize()
    joint=shoulder+direction*along+pole*math.sqrt(max(0,l1*l1-along*along))
    for bone,origin,tip in [(a,shoulder,joint),(b,joint,local)]:
        rot=(bone.bone.tail_local-bone.bone.head_local).rotation_difference(tip-origin)
        matrix=rot.to_matrix().to_4x4()@bone.bone.matrix_local
        matrix.translation=origin;bone.matrix=matrix
        bpy.context.view_layer.update()
    matrix=c.bone.matrix_local.copy();matrix.translation=local;c.matrix=matrix
    return max(0,(local-shoulder).length-l1-l2)


def main():
    for folder,ext in [('scenes','.blend'),('exports','.fbx'),('exports','.json')]:
        if (ROOT/folder/(NAME+ext)).exists(): raise FileExistsError(NAME+ext)
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/chupacabras_nocturno_r08_respira_r02.blend'),use_scripts=False)
    scene=bpy.context.scene
    mesh=bpy.data.objects['Chupacabras_Nocturno']; rig=mesh.modifiers['Respiracion'].object
    root=bpy.data.objects['ChupacabrasAssetRoot']
    breathing=[]
    for f in range(1,98):
        scene.frame_set(f)
        breathing.append({b.name:(b.location.copy(),b.rotation_euler.copy(),b.scale.copy()) for b in rig.pose.bones})
    scene.frame_set(1);rig.animation_data_clear()
    extend_rig(mesh,rig)
    with bpy.data.libraries.load(str(ROOT/'historicos/scenes/07_oveja_r04.blend'),link=False) as (src,dst):
        dst.objects=['SheepAssetRoot','SheepRig','Sheep_Quaternius']
    for obj in dst.objects: scene.collection.objects.link(obj)
    sw=bpy.data.objects['SheepAssetRoot']; sr=bpy.data.objects['SheepRig']; sheep=bpy.data.objects['Sheep_Quaternius']
    for obj in [sw,sr,sheep]: obj.animation_data_clear()
    for b in sr.pose.bones: b.matrix_basis=Matrix.Identity(4);b.rotation_mode='XYZ'
    # A single subdivision softens the archived faceted silhouette at modest cost.
    bpy.context.view_layer.objects.active=sheep
    subdiv=sheep.modifiers.new('Lana_suave','SUBSURF');subdiv.levels=1
    bpy.ops.object.modifier_apply(modifier=subdiv.name)
    for v in sheep.data.vertices:
        weights=sorted(((g.weight,g.group) for g in v.groups),reverse=True)
        total=sum(w for w,i in weights[:4])
        for w,i in weights:sheep.vertex_groups[i].remove([v.index])
        for w,i in weights[:4]:sheep.vertex_groups[i].add([v.index],w/total,'REPLACE')
    for p in sheep.data.polygons:p.use_smooth=True
    for mat in sheep.data.materials:
        mat.use_nodes=True
        bsdf=mat.node_tree.nodes.get('Principled BSDF')
        if bsdf:bsdf.inputs['Roughness'].default_value=.94
    sequence=bpy.data.objects.new('AttackSequence',None);scene.collection.objects.link(sequence)
    root.parent=sequence;sw.parent=sequence
    scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=END
    sheep_rest=positions(sheep)
    neck_index=min(range(len(sheep_rest)),key=lambda i:(sheep_rest[i]-Vector((-.16,-.57,.87))).length)
    floor=[];contact=[];snapshots={};feet=[];reach=[];chupa_floor=[];head_translation=[]
    start_y=None;initial_gap=None
    for side,phase in [('L',0),('R',.5)]:
        for upper,lower,foot,offset in [('Brazo','Antebrazo','Mano',0),('Muslo','Pierna','Pie',.25)]:
            names=[n+'.'+side for n in (upper,lower,foot)]
            feet.append((*names,rig.data.bones[names[2]].head_local.copy(),(phase+offset)%1))
    for f in range(1,END+1):
        t=(f-1)/FPS;scene.frame_set(f)
        for b in rig.pose.bones:b.matrix_basis=Matrix.Identity(4)
        for b in sr.pose.bones:b.matrix_basis=Matrix.Identity(4)
        for name,(loc,rot,scale) in breathing[round((max(t-REST,0) if t>=REST else t)%4*FPS)].items():
            b=rig.pose.bones[name];b.location=loc;b.rotation_euler=rot;b.scale=scale
        rig.pose.bones['Cabeza'].location=(0,0,0)
        crouch=pulse(t,1.55,2.2,2.55)
        air=max(0,1-((t-2.55)/.32)**2) if 2.23<t<2.87 else 0
        forward=smoothstep(2.23,2.87,t)
        impact=pulse(t,2.83,2.98,3.25)
        roll=smoothstep(3.0,3.85,t)
        struggle=pulse(t,3.15,3.8,5.45)
        graze=1-smoothstep(1.95,2.65,t)
        sw.rotation_euler=(.035*struggle*math.sin(t*15),math.pi/2*roll,.045*struggle*math.sin(t*12))
        sw.location=(-.45+.12*roll,SHEEP_Y+.12*roll,0)
        sr.pose.bones['Shoulders'].rotation_euler.x=(-1.3+.025*math.sin(t*3))*graze
        sr.pose.bones['Neck'].rotation_euler.x=(-.8+.045*math.sin(t*2))*graze-.24*roll
        sr.pose.bones['Head'].rotation_euler=(.6*graze+.14*roll,.07*math.sin(t*2)*graze,.06*struggle*math.sin(t*13))
        for side,phase in [('L',0),('R',math.pi)]:
            sr.pose.bones['FrontFoot.'+side].location.y=-.2*roll-.38*struggle*(1+math.sin(t*16+phase))
            sr.pose.bones['BackFoot.'+side].location.x=.12*roll+.22*struggle*math.sin(t*13+phase)
        bpy.context.view_layer.update();sw.location.z-=min(v.z for v in positions(sheep))
        root.location=(0,0,0);root.rotation_euler=(0,0,0)
        if start_y is None:
            bpy.context.view_layer.update()
            start_y=min(v.y for v in positions(sheep))-max(v.y for v in positions(mesh))-.30/METERS
            initial_gap=.30
        grip=smoothstep(2.8,3.15,t)*(1-smoothstep(5.5,6.3,t))
        root.location=(.12*forward,start_y+(LAND_Y-start_y)*forward,.50*air-.24*crouch-.50*grip)
        rig.pose.bones['Torax'].rotation_euler.x=.10*grip+.06*impact
        rig.pose.bones['Torax'].rotation_euler.y=.025*struggle*math.sin(t*12)
        rig.pose.bones['Cola'].rotation_euler.x+=.08*air
        for side in ('L','R'):
            rig.pose.bones['Brazo.'+side].rotation_euler.x=-.38*air
            rig.pose.bones['Antebrazo.'+side].rotation_euler.x=.65*air
            rig.pose.bones['Muslo.'+side].rotation_euler.x=.30*air
            rig.pose.bones['Pierna.'+side].rotation_euler.x=-.48*air
            rig.pose.bones['Mano.'+side].rotation_euler.x=-.18*air
        head=rig.pose.bones['Cabeza']
        bite_local=head.bone.matrix_local.inverted()@Vector((.1705,1.2821,.9634))
        target=positions(sheep)[neck_index]
        bpy.context.view_layer.update()
        if grip>0:
            # Move and lower the whole body into reach; never translate or stretch the neck.
            matrix=rig.matrix_world@head.matrix
            length=(matrix.to_3x3()@bite_local).length
            dx=target.x-matrix.translation.x;dz=target.z-matrix.translation.z
            horizontal=math.sqrt(max(.01,length*length-dx*dx-dz*dz))
            root.location.y+=grip*(target.y-matrix.translation.y-horizontal)
            bpy.context.view_layer.update()
        if air==0 and t<WALK_START:
            stance=Vector((0,start_y,0)) if t<2.23 else Vector((.12,LAND_Y,0))
            for upper,lower,foot,rest,phase in feet:
                reach.append(plant_limb(rig,upper,lower,foot,stance+rest))
        if t>=WALK_START:
            point,yaw=return_path(t);root.location=point;root.rotation_euler.z=yaw
            if t<REST:
                root.location.z+=.025*math.sin((t-WALK_START)*math.tau/.50*2)*pulse(t,WALK_START,9,REST)
                bpy.context.view_layer.update()
                for upper,lower,foot,rest,phase in feet:reach.append(plant_limb(rig,upper,lower,foot,foot_target(t,rest,phase)))
                rig.pose.bones['Torax'].rotation_euler.y+=.025*math.sin((t-WALK_START)*math.tau/.50)*pulse(t,WALK_START,9,REST)
                rig.pose.bones['Cola'].rotation_euler.z+=.06*math.sin((t-WALK_START)*math.tau/.50-.8)*pulse(t,WALK_START,9,REST)
        rig.pose.bones['Mandibula'].rotation_euler.x=-.30*pulse(t,1.95,2.65,3.05)+.11*grip
        bpy.context.view_layer.update()
        if grip>0:
            matrix=rig.matrix_world@head.matrix
            direction=matrix.to_3x3()@bite_local
            rotation=direction.rotation_difference(target-matrix.translation)
            from mathutils import Quaternion
            rotated=Quaternion().slerp(rotation,grip).to_matrix().to_4x4()@matrix
            rotated.translation=matrix.translation
            head.matrix=rig.matrix_world.inverted()@rotated
            bpy.context.view_layer.update()
        head_translation.append(head.location.length)
        root.location.z-=min(0,mesh_floor(mesh))
        bpy.context.view_layer.update()
        if 3.15<=t<=5.5:
            bite=rig.matrix_world@head.matrix@bite_local
            contact.append((target-bite).length)
        key_object(root,f);key_object(sw,f)
        for arm in [rig,sr]:
            for b in arm.pose.bones:key_object(b,f)
        if f in (1,49,61,73,85,97,121,157,193,229,265,301,325,373,421):
            vv=positions(mesh);ss=positions(sheep)
            assert abs(mesh_floor(mesh)-min(v.z for v in vv))<1e-5
            snapshots[f]={'chupa_bounds':[[min(v[i] for v in vv),max(v[i] for v in vv)] for i in range(3)],'sheep_bounds':[[min(v[i] for v in ss),max(v[i] for v in ss)] for i in range(3)]}
        floor.append(min(v.z for v in positions(sheep)))
        chupa_floor.append(mesh_floor(mesh))
    for obj in (root,rig,sw,sr):
        obj.animation_data.action.name='Ataque_'+obj.name
        for layer in obj.animation_data.action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for key in curve.keyframe_points:key.interpolation='LINEAR'
    scene.frame_set(int(REST*FPS)+1);end_sheep=positions(sheep);end_chupa=positions(mesh)
    scene.frame_set(END)
    sheep_drift=max((a-b).length for a,b in zip(end_sheep,positions(sheep)))
    loop_seam=max((a-b).length for a,b in zip(end_chupa,positions(mesh)))
    print('CONTACT_DIAGNOSTICS',dict(contact=max(contact),reach=max(reach),head_translation=max(head_translation),floor=min(chupa_floor)),flush=True)
    assert min(floor)>-1e-4 and min(chupa_floor)>-1e-4,(min(floor),min(chupa_floor))
    assert max(reach)<.001,max(reach)
    assert sheep_drift<1e-5 and loop_seam<1e-4,(sheep_drift,loop_seam)
    assert max(contact)<.06,max(contact)
    assert max(head_translation)<1e-5,max(head_translation)
    for obj in (mesh,sheep):
        assert all(abs(sum(g.weight for g in v.groups)-1)<1e-4 for v in obj.data.vertices)
    assert all(sum(g.weight for g in v.groups if mesh.vertex_groups[g.group].name.startswith(('Muslo','Pierna','Pie')))<1e-5 for v in mesh.data.vertices if v.co.y<-2.05),'Tail must not follow leg flexion'
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in (sequence,root,rig,mesh,sw,sr,sheep):obj.select_set(True)
    bpy.context.view_layer.objects.active=sequence
    bpy.ops.export_scene.fbx(filepath=str(ROOT/'exports'/(NAME+'.fbx')),use_selection=True,object_types={'MESH','EMPTY','ARMATURE'},axis_forward='-Z',axis_up='Y',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=False,use_mesh_modifiers=False,add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,path_mode='STRIP')
    for obj in (mesh,sheep):obj.data.calc_loop_triangles()
    report=dict(name=NAME,fps=FPS,duration=REST+4,attack_end=REST,loop_start_frame=int(REST*FPS)+1,loop_end_frame=END,chupa_triangles=len(mesh.data.loop_triangles),sheep_triangles=len(sheep.data.loop_triangles),chupa_bones=len(rig.data.bones),sheep_bones=len(sr.data.bones),min_sheep_z=min(floor),max_contact_error=max(contact),sheep_final_drift=sheep_drift,loop_seam=loop_seam,snapshots=snapshots,max_foot_reach_excess=max(reach),min_chupa_z=min(chupa_floor),max_head_translation=max(head_translation),uniform_scale=METERS,initial_gap_m=initial_gap,start_y=start_y,final_root_xy=[0,0],physical_device=False)
    (ROOT/'exports'/(NAME+'.json')).write_text(json.dumps(report,indent=2)+'\n')
    print('ATTACK_OK',json.dumps({k:v for k,v in report.items() if k!='snapshots'}))

if __name__=='__main__':main()
