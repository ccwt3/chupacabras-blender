"""Adapta Sheep de Quaternius (CC0), sin reconstruir su malla ni ampliar el rig.

Entrega editable y muestra horneada de aptitud de poses; el rig final es paso 10.
"""
import json
import math
import os
import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from intercambio import ROOT, empty

NAME='07_oveja'+os.environ.get('CHUPA_SUFFIX','')
SOURCE=ROOT/'assets/oveja/original/Farm Animals by @Quaternius/Blends/Sheep.blend'


def positions(obj):
    ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return [ev.matrix_world@v.co for v in ev.data.vertices]


def bbox(points):
    return [[min(p[i] for p in points) for i in range(3)],
            [max(p[i] for p in points) for i in range(3)]]


def export(path,animated):
    bpy.ops.export_scene.fbx(filepath=str(path),object_types={'MESH','ARMATURE','EMPTY'},
        axis_forward='-Z',axis_up='Y',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',
        bake_space_transform=False,add_leaf_bones=False,use_mesh_modifiers=False,
        bake_anim=animated,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,
        bake_anim_force_startend_keying=True,bake_anim_step=1,bake_anim_simplify_factor=0)


def main():
    for folder,ext in [('scenes','.blend'),('exports','.fbx'),('exports','.json'),('exports','_poses.fbx')]:
        if (ROOT/folder/(NAME+ext)).exists(): raise FileExistsError(NAME+ext)
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
    scene=bpy.context.scene
    scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
    scene.render.fps=30; scene.frame_start=1;scene.frame_end=181
    rig=bpy.data.objects['Armature']; sheep=bpy.data.objects['Sheep']
    rig.name='SheepRig'; sheep.name='Sheep_Quaternius'
    # Bound skinning cost explicitly to four influences, matching mobile import.
    pruned_vertices=0
    for vertex in sheep.data.vertices:
        weights=sorted([(g.group,g.weight) for g in vertex.groups if g.weight>0],key=lambda p:p[1],reverse=True)
        if len(weights)>4: pruned_vertices+=1
        for group,weight in weights[4:]: sheep.vertex_groups[group].remove([vertex.index])
        total=sum(weight for group,weight in weights[:4])
        for group,weight in weights[:4]: sheep.vertex_groups[group].add([vertex.index],weight/total,'REPLACE')
    original_actions=[dict(name=a.name,frames=list(a.frame_range)) for a in bpy.data.actions]
    for a in bpy.data.actions: a.use_fake_user=True
    rig.animation_data.action=None
    for track in rig.animation_data.nla_tracks: track.mute=True
    for bone in rig.pose.bones: bone.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()
    original_bounds=bbox(positions(sheep))
    scale=1.18/(original_bounds[1][2]-original_bounds[0][2])
    wrapper=empty('SheepAssetRoot');rig.parent=wrapper
    wrapper.scale=(scale,)*3; wrapper.location.z=-original_bounds[0][2]*scale
    wool=sheep.data.materials[0]; dark=sheep.data.materials[1]
    for mat,color in [(wool,(.78,.74,.61,1)),(dark,(.065,.055,.045,1))]:
        mat.diffuse_color=color; mat.use_nodes=True
        mat.node_tree.nodes.clear()
        bsdf=mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        output=mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
        mat.node_tree.links.new(bsdf.outputs['BSDF'],output.inputs['Surface'])
        if bsdf:
            bsdf.inputs['Base Color'].default_value=color
            bsdf.inputs['Roughness'].default_value=.85
    wool.name='Sheep_Wool';dark.name='Sheep_Dark'
    # Unused legacy editor texture points to the author's machine; keep no dependency.
    for image in list(bpy.data.images):
        if image.source=='FILE': bpy.data.images.remove(image)
    for poly in sheep.data.polygons: poly.use_smooth=False
    scene.frame_set(1);bpy.context.view_layer.update()
    rest_bounds=bbox(positions(sheep))
    assert abs(rest_bounds[1][2]-rest_bounds[0][2]-1.18)<1e-5
    assert abs(rest_bounds[0][2])<1e-5
    sheep.data.calc_loop_triangles()
    # Preserve the native action library and constraints in the editable source.
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'scenes'/(NAME+'.blend')))
    export(ROOT/'exports'/(NAME+'.fbx'),False)
    # Sample existing usable poses plus a head/neck turn. No new bones/weights.
    native=bpy.data.actions['Death']
    rig.animation_data.action=native
    scene.frame_set(26);bpy.context.view_layer.update()
    fall={b.name:b.matrix_basis.copy() for b in rig.pose.bones}
    rig.animation_data.action=None
    action=bpy.data.actions.new('AptitudeOnly_6s'); rig.animation_data.action=action
    samples=[]
    for frame,label in [(1,'neutral'),(61,'grazing'),(121,'native_death'),(181,'neutral_end')]:
        scene.frame_set(frame)
        wrapper.location.z=-original_bounds[0][2]*scale
        for bone in rig.pose.bones:
            bone.matrix_basis=fall[bone.name] if frame==121 else Matrix.Identity(4)
        if frame==61:
            # Local X folds shoulders and neck down toward the grass.
            for name,angle in [('Shoulders',-.50),('Neck',-.62),('Head',.2)]:
                b=rig.pose.bones[name]; b.rotation_mode='QUATERNION'
                b.rotation_quaternion=Matrix.Rotation(angle,4,'X').to_quaternion()
        bpy.context.view_layer.update()
        for bone in rig.pose.bones:
            bone.keyframe_insert('location',frame=frame)
            bone.keyframe_insert('rotation_quaternion' if bone.rotation_mode=='QUATERNION' else 'rotation_euler',frame=frame)
            bone.keyframe_insert('scale',frame=frame)
        verts=positions(sheep)
        # The native death pose sinks 5 cm into the floor at this scale.
        # Correct only this aptitude sample's global support height.
        floor_offset=max(0,-min(v.z for v in verts))
        wrapper.location.z+=floor_offset
        wrapper.keyframe_insert('location',frame=frame)
        bpy.context.view_layer.update()
        verts=positions(sheep)
        assert all(math.isfinite(c) for v in verts for c in v)
        samples.append(dict(time=(frame-1)/30,label=label,bounds=bbox(verts),
                            vertices=[dict(zip('xyz',v)) for v in verts]))
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for k in curve.keyframe_points:k.interpolation='LINEAR'
    scene.frame_set(1)
    export(ROOT/'exports'/(NAME+'_poses.fbx'),True)
    report=dict(author='Quaternius',license='CC0-1.0',source=str(SOURCE.relative_to(ROOT)),
        original_vertices=len(sheep.data.vertices),triangles=len(sheep.data.loop_triangles),
        bones=len(rig.data.bones),materials=2,uniform_scale=scale,rest_bounds=rest_bounds,
        facing='-Y Blender / -Z Unity',native_actions=original_actions,
        pruned_vertices=pruned_vertices,max_influences=4,shape_keys=False,rig_final=False,physical_device=False,samples=samples)
    (ROOT/'exports'/(NAME+'.json')).write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
