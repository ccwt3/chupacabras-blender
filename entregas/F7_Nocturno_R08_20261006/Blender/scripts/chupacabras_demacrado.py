"""Revisión solicitada de 8/9: piel sobre huesos; conserva fuentes y silueta.

CHUPA_SUFFIX=_r01 blender -b -t 4 --python-exit-code 1 --python
scripts/chupacabras_demacrado.py -- 8  (después -- 9)
"""
import json
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chupacabras import anatomy, detail, ellipsoid, join, tube, unwrap, report, views
from intercambio import ROOT, camera

SUFFIX = os.environ.get('CHUPA_SUFFIX', '_r01')
NAMES = {8: '08_chupacabras_demacrado', 9: '09_chupacabras_demacrado'}


def lean_body(root):
    skin = bpy.data.materials['Chupa_Skin']
    bpy.data.objects.remove(bpy.data.objects['Chupa_Body'], do_unlink=True)
    parts = [ellipsoid('Ribcage', (0, -.02, 1.51), (.43, .78, .49), skin),
             ellipsoid('HollowAbdomen', (0, -.72, 1.40), (.205, .56, .24), skin),
             ellipsoid('BonyPelvis', (0, -1.15, 1.31), (.30, .40, .28), skin),
             ellipsoid('LeanNeck', (0, .51, 1.42), (.265, .47, .31), skin)]
    for s in (-1, 1):
        parts.append(ellipsoid('Scapula', (s*.36, .04, 1.67), (.155, .40, .34), skin))
        parts.append(tube('Foreleg', [(s*.40,.32,1.65),(s*.81,.07,1.12),
                         (s*.87,.27,.81),(s*.89,.70,.28),(s*.89,.83,.13)],
                         [.155,.115,.081,.060,.085], skin, 12))
        parts.append(ellipsoid('Elbow', (s*.81,.07,1.12), (.14,.13,.14), skin))
        parts.append(ellipsoid('Palm', (s*.89,.86,.14), (.17,.24,.075), skin))
        parts.append(tube('Hindleg', [(s*.28,-1.15,1.31),(s*.63,-.92,.88),
                         (s*.69,-1.40,.41),(s*.68,-1.32,.14)],
                         [.17,.14,.066,.060], skin, 12))
        parts.append(ellipsoid('Hock', (s*.69,-1.40,.41), (.083,.088,.092), skin))
        parts.append(ellipsoid('Hindfoot', (s*.68,-1.17,.12), (.16,.29,.075), skin))
        for j in (-1,0,1):
            x=s*.89+j*.13
            parts.append(tube('Finger', [(x,.89,.14),(x+j*.035,1.09,.105),
                             (x+j*.05,1.22-.04*abs(j),.09)], [.052,.040,.028],skin))
            x=s*.68+j*.12
            parts.append(tube('Toe',[(x,-1.15,.12),(x,-.89,.085)],[.048,.030],skin))
        # Ribs emerge from the thoracic surface and fuse into it: no floating bones.
        for y in (-.59,-.42,-.25,-.08,.09,.26):
            ring=math.sqrt(1-((y+.02)/.78)**2)
            points=[]
            for j in range(13):
                a=.18+j*2.65/12
                points.append((s*(.43*ring*math.sin(a)+.013),
                               y+.055*math.sin(a), 1.51+.49*ring*math.cos(a)))
            parts.append(tube('SubcutaneousRib',points,[.027]*len(points),skin,8))
        parts.append(tube('ScapularEdge',[(s*.29,-.27,1.85),(s*.47,.02,1.88),
                                         (s*.42,.32,1.59)],[.05,.047,.025],skin))
        parts.append(tube('IliacCrest',[(s*.15,-1.40,1.43),(s*.29,-1.18,1.52),
                                      (s*.23,-.96,1.43)],[.045,.047,.025],skin))
    parts.append(tube('Tail',[(0,-1.37,1.31),(.03,-1.85,1.10),(.12,-2.28,.79),
                            (.30,-2.72,.62),(.56,-3.03,.83),(.74,-3.14,1.14)],
                            [.14,.11,.073,.048,.028,.012],skin,12))
    body=join(parts,'Chupa_Body');body.parent=root
    mod=body.modifiers.new('SkinUnion','REMESH');mod.mode='VOXEL';mod.voxel_size=.018
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=body.modifiers.new('SkinRelax','SMOOTH');mod.factor=.55;mod.iterations=2
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=body.modifiers.new('SurfaceBudget','DECIMATE');mod.ratio=.23
    bpy.ops.object.modifier_apply(modifier=mod.name)
    body.data.materials.clear();body.data.materials.append(skin)
    # Keep the tall crest but sink its roots into the slimmer back/neck.
    for obj in root.children:
        if obj.name.startswith('Chupa_Crest'):
            low=min(v.co.z for v in obj.data.vertices)
            for v in obj.data.vertices:
                v.co.x*=.70
                v.co.z-=.13*max(0,1-(v.co.z-low)/.30)


def lean_face(root):
    # One continuous mapping includes sockets, brow, teeth and jaw together.
    # Y/Z of the bite landmarks remain unchanged; X narrows the skull and snout.
    for obj in root.children:
        if obj.type!='MESH' or obj.name=='Chupa_Body' or obj.name.startswith('Chupa_Crest'):
            continue
        bpy.ops.object.select_all(action='DESELECT');obj.select_set(True)
        bpy.context.view_layer.objects.active=obj
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
        for v in obj.data.vertices:
            p=v.co
            if p.y>.75 and p.z>.65 or obj.name.startswith(('Chupa_Head','Chupa_Jaw','Chupa_Ear','Chupa_Eye')):
                p.x*=.76
                # Hollow cheeks below the zygomatic ridge, preserving the teeth.
                if obj.name=='Chupa_Head':
                    hollow=math.exp(-((p.y-.88)/.22)**2-((p.z-1.24)/.14)**2)
                    p.x*=1-.24*hollow


def finish(root):
    detail(root)
    mouth=bpy.data.materials['Chupa_Mouth']
    sockets=[]
    for s in (-1,1):
        eye=bpy.data.objects['Chupa_Eye'+str(s)]
        eye.scale=(.80,.85,.66)
        eye.location.y+=.028
        socket=ellipsoid('OrbitalHollow',(s*.265,1.015,1.43),(.116,.066,.098),mouth)
        socket.rotation_euler.z=s*-.35
        sockets.append(socket)
    join(sockets,'Chupa_HeadSockets').parent=root
    # Sparse fur must not recreate the broad mantle of the earlier model.
    for obj in root.children:
        if obj.name.startswith('Chupa_Detail'):
            for v in obj.data.vertices:
                if -.8<v.co.y<.75 and v.co.z>1.30:
                    v.co.x*=.64
    lean_face(root)
    colors={'Skin':(.19,.205,.18),'Ridge':(.28,.29,.25),'Mouth':(.025,.018,.025),
            'Horn':(.075,.085,.080),'Ivory':(.53,.50,.36),'Eye':(1,.64,.045)}
    for name,color in colors.items():
        bpy.data.materials['Chupa_'+name].diffuse_color=(*color,1)


def main():
    step=int(sys.argv[sys.argv.index('--')+1]);name=NAMES[step]+SUFFIX
    for folder,ext in [('scenes','.blend'),('exports','.fbx'),('exports','.json')]:
        if (ROOT/folder/(name+ext)).exists():raise FileExistsError(name+ext)
    if step==8:
        scene,root=anatomy();lean_body(root)
        # Face is narrowed in step 9 together with its new details.
    else:
        source=os.environ.get('CHUPA_FORM',NAMES[8]+SUFFIX)
        bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(source+'.blend')),use_scripts=False)
        scene=bpy.context.scene;root=bpy.data.objects['ChupacabrasAssetRoot'];finish(root)
    unwrap(root)
    info=report(root);info.update(revision='demacrado',triangle_budget=40000,
                                source='chupacabras.anatomy' if step==8 else source,
                                rig_revalidation_required=True)
    assert info['triangles']<info['triangle_budget']
    (ROOT/'exports'/(name+'.json')).write_text(json.dumps(info,indent=2)+'\n')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [root]+list(root.children):obj.select_set(True)
    bpy.ops.export_scene.fbx(filepath=str(ROOT/'exports'/(name+'.fbx')),use_selection=True,
        object_types={'MESH','EMPTY'},axis_forward='-Z',axis_up='Y',apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=False,bake_anim=False)
    cam=camera('LeanReviewCamera',(5,7,3.5),(0,-.5,1.2));scene.camera=cam
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'scenes'/(name+'.blend')))
    views(scene,name)
    print('LEAN_CREATURE_OK '+json.dumps(dict(name=name,triangles=info['triangles'])))


if __name__=='__main__':main()
