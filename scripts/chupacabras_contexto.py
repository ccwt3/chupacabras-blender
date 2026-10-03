"""Muestra de volumen/contacto para 8–9 usando cámaras y recorrido del contexto 06.

La oveja es una copia evaluada neutral de Quaternius; el giro rígido se hereda
del bloqueo. No es el rig ni actuación definitivos de los pasos 10–18.
"""
import json
import math
import os
import sys
from pathlib import Path
import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from intercambio import ROOT, export

MODEL=os.environ.get('CHUPA_MODEL','08_chupacabras_forma')
NAME=MODEL+os.environ.get('CHUPA_CONTEXT_SUFFIX','_contexto_r02')


def main():
    for folder,ext in [('scenes','.blend'),('exports','.fbx'),('exports','.json')]:
        if (ROOT/folder/(NAME+ext)).exists(): raise FileExistsError(NAME+ext)
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/07_oveja_r04.blend'),use_scripts=False)
    sheep=bpy.data.objects['Sheep_Quaternius']
    ev=sheep.evaluated_get(bpy.context.evaluated_depsgraph_get())
    vertices=[list(ev.matrix_world@v.co) for v in ev.data.vertices]
    faces=[list(p.vertices) for p in ev.data.polygons]
    indices=[p.material_index for p in ev.data.polygons]
    colors=[(m.name,list(m.diffuse_color)) for m in sheep.data.materials]
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/06_escenario_contexto.blend'),use_scripts=False)
    scene=bpy.context.scene
    # The final long tail cannot hide sideways behind the narrow barn proxy.
    # Turn it upstage during the hidden section; preserve all historic source files.
    creature=bpy.data.objects['CreatureRoot']
    for frame,angle in ((421,-math.pi/2),(451,-math.pi),(600,-math.pi)):
        scene.frame_set(frame)
        creature.rotation_euler.z=angle
        creature.keyframe_insert('rotation_euler',frame=frame)
        creature.location.y=9.3
        creature.keyframe_insert('location',frame=frame)
    # A higher internal landing camera hides the sheep through the anatomical
    # torso instead of relying on the old solid box extending to the ground.
    cam=bpy.data.objects['CinemaCamera']
    attack_camera=tuple(float(v) for v in os.environ.get('CHUPA_ATTACK_CAMERA','0,-6,2.4').split(','))
    assert len(attack_camera)==3 and all(math.isfinite(v) for v in attack_camera)
    for frame in (601,750):
        scene.frame_set(frame)
        cam.location=attack_camera
        cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.keyframe_insert('location',frame=frame)
        cam.keyframe_insert('rotation_euler',frame=frame)
    for obj in list(scene.objects):
        if obj.type=='MESH' and obj.name.startswith(('Creature','Sheep')):
            bpy.data.objects.remove(obj,do_unlink=True)
    with bpy.data.libraries.load(str(ROOT/'scenes'/(MODEL+'.blend')),link=False) as (src,dst):
        dst.objects=[n for n in src.objects if n.startswith(('Chupa','JawPivot','BiteSocket'))]
    for obj in dst.objects: scene.collection.objects.link(obj)
    root=bpy.data.objects['ChupacabrasAssetRoot'];root.parent=bpy.data.objects['CreatureRoot']
    if 'Chupa_Detail_Ivory' in bpy.data.objects:
        # The finished claws extend farther sideways than the neutral hands.
        # Keep that extra reach clear of the wall during the initial stalk.
        for layer in creature.animation_data.action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        if curve.data_path=='location' and curve.array_index==1:
                            for key in curve.keyframe_points:
                                if key.co.x<421:
                                    key.co.y+=.25
                                    key.handle_left.y+=.25
                                    key.handle_right.y+=.25
    data=bpy.data.meshes.new('SheepVolume');data.from_pydata(vertices,[],faces);data.update()
    obj=bpy.data.objects.new('Sheep_Quaternius_Volume',data);scene.collection.objects.link(obj)
    obj.parent=bpy.data.objects['SheepRoot']
    for name,color in colors:
        mat=bpy.data.materials.new(name);mat.diffuse_color=color;data.materials.append(mat)
    for p,index in zip(data.polygons,indices): p.material_index=index
    sheep_root=obj.parent
    # Named landmark in the anterior wool/neck region, to be deformed in step 10.
    neck_local=Vector((0,-.55,.87));bite_local=Vector((0,1.30,1.01))
    for frame in range(637,1202):
        scene.frame_set(frame)
        sheep_root.location=bite_local-sheep_root.rotation_quaternion@neck_local
        sheep_root.keyframe_insert('location',frame=frame)
    bpy.data.objects['Mouth'].location=bite_local
    bpy.data.objects['Neck'].location=neck_local
    max_error=0
    for frame in range(637,1202):
        scene.frame_set(frame);bpy.context.view_layer.update()
        error=(bpy.data.objects['Mouth'].matrix_world.translation-
               bpy.data.objects['Neck'].matrix_world.translation).length
        max_error=max(max_error,error)
    assert max_error<1e-5
    # Conservative barn box at facade/walls, then roof. World AABBs of every
    # actual creature part must stay clear at 30 Hz, including the turn.
    barn_boxes=[((-5.08,4.84,0),(-1.52,6.34,3.04)),
                ((-5.15,4.80,3.0),(-1.45,6.38,4.35))]
    meshes=[o for o in scene.objects if o.type=='MESH' and o.name.startswith('Chupa_')]
    overlaps=[]
    for frame in range(1,1201):
        scene.frame_set(frame);bpy.context.view_layer.update()
        for obj in meshes:
            points=[obj.matrix_world@Vector(c) for c in obj.bound_box]
            lo=[min(v[i] for v in points) for i in range(3)]
            hi=[max(v[i] for v in points) for i in range(3)]
            if any(all(min(hi[i],b[i])-max(lo[i],a[i])>.001 for i in range(3))
                   for a,b in barn_boxes):
                overlaps.append((frame,obj.name))
    assert not overlaps, overlaps[:20]
    export(NAME)
    (ROOT/'exports'/(NAME+'.json')).write_text(json.dumps(dict(
        source=MODEL,frames=565,max_landmark_error=max_error,duration=40,
        neck_landmark=list(neck_local),bite_landmark=list(bite_local),
        barn_aabb_frames=1200,barn_overlaps=overlaps,
        attack_camera=list(attack_camera),
        static_sheep_volume=True,final_rig=False,physical_device=False),indent=2)+'\n')
    print('CHUPACABRAS_CONTEXT_OK',max_error)


if __name__=='__main__': main()
