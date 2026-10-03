"""F2: nueva fuente de anatomía/pose y comparación; no exporta ni ejecuta F3.

CHUPA_F2_REV=r04 blender -b -t 4 --python-exit-code 1 --python scripts/figura_forma.py
Las salidas existentes se conservan. WORKBENCH hace comparables forma y pose,
no acredita materiales finales ni calidad móvil.
"""
import json
import math
import os
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chupacabras import tube, join, report
from intercambio import camera

ROOT = Path(__file__).resolve().parents[1]
BASE = '09_chupacabras_demacrado_r02'
NAME = 'F2_chupacabras_forma_' + os.environ.get('CHUPA_F2_REV', 'r04')
OUTPUT = ROOT / 'previews' / NAME
SOURCE = ROOT / 'scenes' / (NAME + '.blend')


def apply(obj, modifier):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=modifier.name)


def smoothstep(a, b, x):
    t = max(0, min(1, (x-a)/(b-a)))
    return t*t*(3-2*t)


def pose(p):
    """Continuous spatial deformation keeps all attached details together."""
    x, y, z = p
    # Planted hands are staggered, with diminishing motion towards the shoulders.
    hand = smoothstep(.35, .65, abs(x)) * (1-smoothstep(.20, 1.60, z))
    fore = smoothstep(-.65, .05, y)
    p.y += hand * ((-.23 if x > 0 else .18)*fore + (.09 if x > 0 else -.10)*(1-fore))
    p.x += hand * (.055 if x > 0 else -.025)
    p.z -= .020*hand*fore
    # Alert head turn blends into the neck rather than separating a rigid skull.
    head = smoothstep(.40, .82, y) * smoothstep(.50, .85, z)
    pivot = Vector((0, .48, 1.36))
    q = Matrix.Rotation(math.radians(-12)*head, 3, 'Z') @ (p-pivot) + pivot
    tail = 1-smoothstep(-2.9, -1.45, y)
    q.x += .27*tail
    q.z += .05*tail
    return q


def refine():
    root = bpy.data.objects['ChupacabrasAssetRoot']
    for obj in root.children:
        if obj.type != 'MESH':
            continue
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    # Fuse brow and cheek ridges into the skull instead of leaving pasted blocks.
    ridge = bpy.data.objects['Chupa_Detail_Ridge']
    face = ridge.copy(); face.data = ridge.data.copy(); bpy.context.collection.objects.link(face)
    for obj, keep_face in ((ridge, False), (face, True)):
        bm = bmesh.new(); bm.from_mesh(obj.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if (v.co.y > .70) != keep_face], context='VERTS')
        bm.to_mesh(obj.data); bm.free()
    head = join([bpy.data.objects['Chupa_Head'], face], 'Chupa_Head')
    head.parent = root
    # Union the previously intersecting cranial masses into a sculptable surface.
    mod = head.modifiers.new('CranialUnion', 'REMESH')
    mod.mode = 'VOXEL'; mod.voxel_size = .010
    apply(head, mod)
    mod = head.modifiers.new('CheekTransition', 'SMOOTH')
    mod.factor = .60; mod.iterations = 8
    apply(head, mod)
    mod = head.modifiers.new('FormResolution', 'DECIMATE'); mod.ratio = .48
    apply(head, mod)
    head.data.materials.clear(); head.data.materials.append(bpy.data.materials['Chupa_Skin'])
    # Round the jaw without inflating the thin abdomen or obscuring the ribs.
    jaw = bpy.data.objects['Chupa_Jaw']
    mod = jaw.modifiers.new('JawContinuity', 'REMESH'); mod.mode = 'VOXEL'; mod.voxel_size = .008
    apply(jaw, mod)
    mod = jaw.modifiers.new('JawRelax', 'SMOOTH'); mod.factor = .25; mod.iterations = 2
    apply(jaw, mod)
    for name in ('Chupa_Jaw', 'Chupa_LowerTeeth'):
        for v in bpy.data.objects[name].data.vertices:
            v.co.z += .035*smoothstep(.80, 1.3, v.co.y)
    body = bpy.data.objects['Chupa_Body']
    mod = body.modifiers.new('JointTransitions', 'SMOOTH')
    mod.factor = .35; mod.iterations = 2
    apply(body, mod)
    # Replace only this new source's broad pyramidal spines with curved roots/tips.
    horn = bpy.data.materials['Chupa_Horn']
    for i, (y, z, h) in enumerate([(.44,1.72,.70),(.05,1.93,.77),(-.34,1.82,.67),(-.73,1.53,.52),(-1.08,1.42,.31)]):
        old = bpy.data.objects['Chupa_Crest'+str(i)]
        bpy.data.objects.remove(old, do_unlink=True)
        spine = tube('Chupa_Crest'+str(i),
            [(0,y,z-.08),(0,y-.025,z+.12),(0,y-.08,z+h*.48),(.018,y-.17,z+h*.80),(.03,y-.29,z+h)],
            [(.065,.145),(.058,.12),(.042,.078),(.025,.036),.0015],horn,12)
        spine.parent = root
    # Preserve teeth while replacing the old block-shaped claws in this copy.
    ivory = bpy.data.objects['Chupa_Detail_Ivory']
    bm = bmesh.new(); bm.from_mesh(ivory.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < .4], context='VERTS')
    bm.to_mesh(ivory.data); bm.free()
    claws = [ivory]
    mat = bpy.data.materials['Chupa_Ivory']
    for s in (-1, 1):
        for j in (-1, 0, 1):
            x = s*.89+j*.18; y = 1.22-.04*abs(j)
            claws.append(tube('ForeClaw',[(x,y-.070,.09),(x,y+.035,.11),(x,y+.10,.105),(x,y+.18,.065),(x,y+.22,.055)],
                [.038,.034,.026,.014,.0015],mat,12))
            x = s*.68+j*.12
            claws.append(tube('HindClaw',[(x,-.955,.09),(x,-.86,.105),(x,-.79,.095),(x,-.71,.05),(x,-.67,.055)],
                [.035,.030,.023,.012,.0015],mat,12))
    for claw in claws[1:]:
        front = claw.name.startswith('ForeClaw')
        support_z = min(v.co.z for v in body.data.vertices
                        if abs(v.co.x)>.45 and (v.co.y>0 if front else v.co.y<-.5))
        lift = max(0, support_z+.002-min(v.co.z for v in claw.data.vertices))
        for v in claw.data.vertices:
            v.co.z += lift
    join(claws,'Chupa_Detail_Ivory').parent = root
    # Smooth shading and the same deformation for skin, teeth, eyes and spines.
    for obj in root.children:
        if obj.type == 'MESH':
            for vertex in obj.data.vertices:
                vertex.co = pose(vertex.co.copy())
            for poly in obj.data.polygons:
                poly.use_smooth = True
        elif obj.type == 'EMPTY':
            obj.location = pose(obj.location.copy())
    # Establish a real support plane in this new source, keeping proportions intact.
    minimum = min(v.co.z for v in body.data.vertices)
    for obj in root.children:
        if obj.type == 'MESH':
            for vertex in obj.data.vertices:
                vertex.co.z -= minimum
        elif obj.type == 'EMPTY':
            obj.location.z -= minimum
    return root


VIEWS = [
    ('frente', (0,8,2.1), (0,-.5,1.2), 5.5),
    ('perfil', (8,0,2.1), (0,-.5,1.2), 5.5),
    ('espalda', (0,-8,2.1), (0,-.5,1.2), 5.5),
    ('tres_cuartos', (5,7,3.5), (0,-.5,1.2), 5.5),
    ('inferior', (4,5,-1.6), (0,-.15,1), 4.9),
    ('rostro', (2.1,5,2.0), (0,.95,1.38), 1.65),
]


def configure_review():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x = 1100; scene.render.resolution_y = 850
    scene.render.resolution_percentage = 100
    shade = scene.display.shading
    shade.light = 'STUDIO'; shade.studio_light = 'paint.sl'; shade.color_type = 'MATERIAL'
    shade.show_shadows = True; shade.show_cavity = True; shade.cavity_type = 'BOTH'
    shade.show_specular_highlight = False; shade.background_type = 'WORLD'
    scene.world.color = (.045,.055,.065); scene.view_settings.view_transform = 'Standard'
    cam = scene.camera
    cam.data.type = 'ORTHO'
    return scene, cam


def render_views(label):
    scene, cam = configure_review()
    for name, eye, target, scale in VIEWS:
        cam.location = eye
        cam.rotation_euler = (Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.data.ortho_scale = scale
        scene.render.filepath = str(OUTPUT / (label+'_'+name+'.png'))
        bpy.ops.render.render(write_still=True)


def main():
    if SOURCE.exists() or OUTPUT.exists():
        raise FileExistsError('Choose a new CHUPA_F2_REV; existing deliveries are preserved.')
    OUTPUT.mkdir()
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(BASE+'.blend')), use_scripts=False)
    root = refine()
    info = report(root)
    info.update(source=BASE,stage='F2',mobile_budget_approved=False,uv_rework_pending=True)
    (OUTPUT/'geometry.json').write_text(json.dumps(info,indent=2)+'\n')
    scene, cam = configure_review()
    _, eye, target, scale = VIEWS[3]
    cam.location=eye; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=scale
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
    render_views('forma')
    # Small inspection turntable, not an animation delivered in the app.
    scene, cam = configure_review()
    scene.render.resolution_x=720; scene.render.resolution_y=540
    frames=OUTPUT/'giro_frames'; frames.mkdir()
    cam.data.ortho_scale=5.5
    for frame in range(72):
        angle=math.tau*frame/72+.55
        cam.location=(8*math.sin(angle),8*math.cos(angle)-.5,3.1)
        cam.rotation_euler=(Vector((0,-.5,1.2))-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(frames/f'{frame:04d}.png')
        bpy.ops.render.render(write_still=True)
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes'/(BASE+'.blend')),use_scripts=False)
    render_views('base')
    print('F2_FORM_OK '+json.dumps({'source':str(SOURCE),'triangles':info['triangles'],'physical_device':False}))


if __name__ == '__main__':
    main()
