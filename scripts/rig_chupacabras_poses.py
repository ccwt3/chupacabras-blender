"""Prueba de controles FK 11: patas, columna, cola y apertura de mandíbula."""
import json
import math
import os
import sys
from pathlib import Path
import bpy
from mathutils import Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from intercambio import ROOT
from oveja import positions,export
from rig_oveja import key_pose,linear_actions

name='11_rig_chupacabras_poses'+os.environ.get('CHUPA_SUFFIX','')
for d,e in [('scenes','.blend'),('exports','.fbx'),('exports','.json')]:
    if (ROOT/d/(name+e)).exists():raise FileExistsError(name+e)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/11_rigs_contacto.blend'),use_scripts=False)
scene=bpy.context.scene
rig=bpy.data.objects['ChupaRig'];root=bpy.data.objects['ChupacabrasAssetRoot']
sr=bpy.data.objects['SheepRig'];sw=bpy.data.objects['SheepAssetRoot'];sheep=bpy.data.objects['Sheep_Quaternius']
for o in scene.objects:o.animation_data_clear()
for r in [rig,sr]:
    for b in r.pose.bones:b.matrix_basis=Matrix.Identity(4)
sheep.data.shape_keys.animation_data_clear();sheep.data.shape_keys.key_blocks['WoolCompression'].value=0
sw.location=(3,0,.004064235836267471);sw.rotation_euler=(0,0,0)
root.location=(0,0,0);root.rotation_euler=(0,0,0)
rig.animation_data_create();rig.animation_data.action=bpy.data.actions.new('RigTest_CreatureControls_6s')
labels={1:'neutral',31:'crouch',61:'stride_left',91:'back_bend',121:'stride_right',151:'jaw_open',181:'neutral_end'}
for f,label in labels.items():
    scene.frame_set(f)
    for b in rig.pose.bones:b.matrix_basis=Matrix.Identity(4)
    if label=='crouch':
        for side in ('L','R'):
            rig.pose.bones['Arm.'+side].rotation_euler.x=.20
            rig.pose.bones['Forearm.'+side].rotation_euler.x=-.28
            rig.pose.bones['Thigh.'+side].rotation_euler.x=.20
            rig.pose.bones['Shin.'+side].rotation_euler.x=-.30
        rig.pose.bones['Neck'].rotation_euler.x=-.3
    if label.startswith('stride'):
        sign=1 if label.endswith('left') else -1
        for side,s in [('L',sign),('R',-sign)]:
            rig.pose.bones['Arm.'+side].rotation_euler.x=.25*s
            rig.pose.bones['Forearm.'+side].rotation_euler.x=-.10*s
            rig.pose.bones['Thigh.'+side].rotation_euler.x=-.28*s
            rig.pose.bones['Shin.'+side].rotation_euler.x=.15*s
        for i in range(5):rig.pose.bones[f'Tail{i}'].rotation_euler.y=.25*sign
    if label=='back_bend':
        rig.pose.bones['Spine'].rotation_euler=(.12,.18,0)
        rig.pose.bones['Neck'].rotation_euler=(-.30,-.15,0)
        for i in range(5):rig.pose.bones[f'Tail{i}'].rotation_euler.x=.15
    if label=='jaw_open':
        rig.pose.bones['Jaw'].rotation_euler.x=-.55
        rig.pose.bones['Head'].rotation_euler.y=.20
    key_pose(rig,f)
linear_actions()
meshes=[o for o in scene.objects if o.type=='MESH']
creature=[o for o in meshes if o!=sheep]
for f in range(1,182):
    scene.frame_set(f);bpy.context.view_layer.update()
    root.location.z-=min(v.z for m in creature for v in positions(m))
    root.keyframe_insert('location',frame=f)
root.animation_data.action.name='RigTest_CreatureSupport';linear_actions()
records=[]
for f in range(1,182):
    scene.frame_set(f);bpy.context.view_layer.update()
    samples=[]
    for mesh in meshes:
        pts=positions(mesh);inds=list(range(0,len(pts),max(1,len(pts)//80)))
        samples.append(dict(name=mesh.name,indices=inds,vertices=[dict(zip('xyz',pts[i])) for i in inds]))
    records.append(dict(time=(f-1)/30,shape=0,label=labels.get(f,''),meshes=samples))
scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'scenes'/(name+'.blend')))
export(ROOT/'exports'/(name+'.fbx'),True)
(ROOT/'exports'/(name+'.json')).write_text(json.dumps(dict(name=name,duration=6,physical_device=False,samples=records),separators=(',',':'))+'\n')
print('RIG_CONTROLS_OK',name)
