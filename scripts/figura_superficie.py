"""F3: malla estática, atlas PBR original y vistas; conserva entregas existentes.

CHUPA_F3_REV=r05 blender -b -t 4 --python-exit-code 1 --python scripts/figura_superficie.py
"""
import json
import math
import os
import sys
from pathlib import Path

import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figura_forma import VIEWS, apply
from chupacabras import join

ROOT = Path(__file__).resolve().parents[1]
NAME = 'F3_chupacabras_superficie_' + os.environ.get('CHUPA_F3_REV', 'r05')
OUT = ROOT / 'previews' / NAME
TEX = ROOT / 'exports' / NAME
SIZE = 2048


def ramp(nodes, links, socket, colors, label):
    node = nodes.new('ShaderNodeValToRGB'); node.label = label
    for element, color in zip(node.color_ramp.elements, colors):
        element.color = (*color, 1)
    links.new(socket, node.inputs[0])
    return node.outputs['Color']


def surface(mat):
    """Object-space fields bake continuously across UV seams; no reference images."""
    mat.use_nodes = True; mat.use_fake_user = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    coord = nodes.new('ShaderNodeTexCoord')
    noise = nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 5
    noise.inputs['Detail'].default_value = 4
    links.new(coord.outputs['Object'], noise.inputs['Vector'])
    skin = mat.name in ('Chupa_Skin', 'Chupa_Ridge')
    eye = mat.name == 'Chupa_Eye'
    base = tuple(mat.diffuse_color[:3])
    if skin:
        colors = ((.075, .083, .058), (.24, .225, .165))
        roughness = (.62, .88)
    elif eye:
        colors = ((.28, .12, .008), (.8, .48, .035)); roughness = (.16, .24)
    else:
        colors = (tuple(c*.55 for c in base), tuple(c*1.05 for c in base))
        roughness = (.35, .60) if mat.name == 'Chupa_Ivory' else (.5, .8)
    links.new(ramp(nodes, links, noise.outputs['Fac'], colors, 'Original pigment'), bsdf.inputs['Base Color'])
    links.new(ramp(nodes, links, noise.outputs['Fac'], [(v,)*3 for v in roughness], 'Dryness'), bsdf.inputs['Roughness'])
    if not eye:
        fine = nodes.new('ShaderNodeTexNoise'); fine.inputs['Scale'].default_value = 95 if skin else 55
        fine.inputs['Detail'].default_value = 3; fine.inputs['Roughness'].default_value = .7
        links.new(coord.outputs['Object'], fine.inputs['Vector'])
        bump = nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .32
        bump.inputs['Distance'].default_value = .012 if skin else .004
        links.new(fine.outputs['Fac'], bump.inputs['Height'])
        links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])


def bake(obj, label, kind, color_space):
    image = bpy.data.images.new(label, width=SIZE, height=SIZE, alpha=False)
    image.colorspace_settings.name = color_space
    for mat in obj.data.materials:
        nodes = mat.node_tree.nodes
        node = nodes.new('ShaderNodeTexImage'); node.image = image
        nodes.active = node
    bpy.ops.object.bake(type=kind)
    image.filepath_raw = str(TEX / (label + '.png')); image.file_format = 'PNG'; image.save()
    return image


def minimum_island_footprint(obj):
    """Reserve texels for tiny disconnected charts instead of leaving them unbaked."""
    bm = bmesh.from_edit_mesh(obj.data); uv = bm.loops.layers.uv.active
    remaining = set(bm.faces)
    while remaining:
        faces = [remaining.pop()]; pending = faces.copy()
        while pending:
            for edge in pending.pop().edges:
                if edge.seam: continue
                for face in edge.link_faces:
                    if face in remaining:
                        remaining.remove(face); faces.append(face); pending.append(face)
        loops = [loop for face in faces for loop in face.loops]
        area = 0
        for face in faces:
            a,b,c = [loop[uv].uv for loop in face.loops]
            area += abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))/2
        perimeter = sum((loop[uv].uv-loop.link_loop_next[uv].uv).length
                        for loop in loops if loop.edge.seam or loop.edge.is_boundary)
        # Area alone misses long needle-shaped islands: reserve an interior radius too.
        scale = max(math.sqrt(64/SIZE**2/max(area,1e-14)),
                    2/SIZE * perimeter/max(2*area,1e-14))
        if scale > 1:
            center = sum((loop[uv].uv.copy() for loop in loops), Vector((0,0)))/len(loops)
            for loop in loops: loop[uv].uv = center+(loop[uv].uv-center)*scale
    bmesh.update_edit_mesh(obj.data)


def render_views(label, workbench=False):
    scene = bpy.context.scene; cam = scene.camera
    scene.render.engine = 'BLENDER_WORKBENCH' if workbench else 'CYCLES'
    scene.render.resolution_x = 1100; scene.render.resolution_y = 850
    scene.render.resolution_percentage = 100
    if workbench:
        shade = scene.display.shading
        shade.light = 'STUDIO'; shade.studio_light = 'paint.sl'; shade.color_type = 'MATERIAL'
        shade.show_shadows = True; shade.show_cavity = True; shade.cavity_type = 'BOTH'
        shade.show_specular_highlight = False; shade.background_type = 'WORLD'
    for name, eye, target, scale in VIEWS:
        cam.location = eye
        cam.rotation_euler = (Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.data.type = 'ORTHO'; cam.data.ortho_scale = scale
        scene.render.filepath = str(OUT / (label+'_'+name+'.png'))
        bpy.ops.render.render(write_still=True)


def main():
    blend = ROOT/'scenes'/(NAME+'.blend'); fbx = ROOT/'exports'/(NAME+'.fbx')
    if any(p.exists() for p in (blend, fbx, OUT, TEX)):
        raise FileExistsError('Choose a new CHUPA_F3_REV; existing deliveries are preserved.')
    OUT.mkdir(); TEX.mkdir()
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'scenes/F2_chupacabras_forma_r04.blend'), use_scripts=False)
    root = bpy.data.objects['ChupacabrasAssetRoot']
    meshes = [o for o in root.children if o.type == 'MESH']
    reduction = {}
    for obj in meshes:
        if obj.name not in ('Chupa_Head', 'Chupa_Jaw', 'Chupa_Body'):
            continue
        original = [v.co.copy() for v in obj.data.vertices]
        tree = BVHTree.FromPolygons(original, [list(p.vertices) for p in obj.data.polygons])
        mod = obj.modifiers.new('MobileResolution', 'DECIMATE')
        mod.ratio = {'Chupa_Head':.19, 'Chupa_Jaw':.15, 'Chupa_Body':.72}[obj.name]
        apply(obj, mod)
        reduced = BVHTree.FromPolygons([v.co.copy() for v in obj.data.vertices], [list(p.vertices) for p in obj.data.polygons])
        deviations = [tree.find_nearest(v.co)[3] for v in obj.data.vertices]
        deviations += [reduced.find_nearest(v)[3] for v in original]
        reduction[obj.name] = {'max_surface_distance_m': max(deviations)}
        assert max(deviations) < .016, (obj.name, max(deviations))
    # Keep equal-camera/equal-light geometry evidence before changing the surface.
    render_views('malla', workbench=True)
    obj = join(meshes, 'Chupa_F3_Surface'); obj.parent = root
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    # Triangulate before tangent-space baking so Blender/Unity use the same triangles.
    mod = obj.modifiers.new('ExportTriangles', 'TRIANGULATE'); apply(obj, mod)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=.012, area_weight=.5)
    # Projection establishes cuts; unwrap relaxes skinny projected triangles before baking.
    bpy.ops.uv.seams_from_islands()
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=.012)
    bpy.ops.uv.average_islands_scale()
    for _ in range(3):
        minimum_island_footprint(obj)
        bpy.ops.uv.pack_islands(rotate=True, margin=.003)
    bpy.ops.object.mode_set(mode='OBJECT')
    for mat in obj.data.materials:
        surface(mat)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.bake.margin = 16; scene.render.bake.margin_type = 'EXTEND'
    scene.render.bake.use_selected_to_active = False
    scene.render.bake.use_pass_direct = False; scene.render.bake.use_pass_indirect = False
    scene.render.bake.use_pass_color = True
    scene.render.bake.normal_space = 'TANGENT'
    albedo = bake(obj, 'BaseColor', 'DIFFUSE', 'sRGB')
    rough = bake(obj, 'Roughness', 'ROUGHNESS', 'Non-Color')
    normal = bake(obj, 'Normal', 'NORMAL', 'Non-Color')
    # URP Lit metallic map uses R=metallic (zero here), A=1-roughness.
    pixels = np.empty(SIZE*SIZE*4, dtype=np.float32); rough.pixels.foreach_get(pixels)
    pixels = pixels.reshape(-1,4); smooth = 1-pixels[:,0].copy()
    pixels[:,:3] = 0; pixels[:,3] = smooth
    mask = bpy.data.images.new('MetallicSmoothness', width=SIZE, height=SIZE, alpha=True)
    mask.colorspace_settings.name = 'Non-Color'; mask.pixels.foreach_set(pixels.ravel())
    mask.filepath_raw = str(TEX/'MetallicSmoothness.png'); mask.file_format = 'PNG'; mask.save()
    mat = bpy.data.materials.new('F3_Surface'); mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    for img, socket in ((albedo,'Base Color'), (rough,'Roughness')):
        node = nodes.new('ShaderNodeTexImage'); node.image = img
        links.new(node.outputs['Color'], bsdf.inputs[socket])
    node = nodes.new('ShaderNodeTexImage'); node.image = normal
    normal_node = nodes.new('ShaderNodeNormalMap')
    links.new(node.outputs['Color'], normal_node.inputs['Color']); links.new(normal_node.outputs['Normal'], bsdf.inputs['Normal'])
    for poly in obj.data.polygons: poly.material_index = 0
    obj.data.materials.clear(); obj.data.materials.append(mat)
    # Neutral studio environment exists only in Blender review, never in the FBX.
    for light in [o for o in scene.objects if o.type == 'LIGHT']:
        bpy.data.objects.remove(light, do_unlink=True)
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get('Background').inputs[0].default_value = (.16,.18,.21,1)
    scene.world.node_tree.nodes.get('Background').inputs[1].default_value = .65
    for name, location, energy, size in [('Key',(3,4,6),850,4), ('Fill',(-4,1,3),550,4), ('Rim',(1,-4,4),700,3)]:
        data = bpy.data.lights.new(name,'AREA'); data.energy = energy; data.shape = 'DISK'; data.size = size
        light = bpy.data.objects.new(name,data); scene.collection.objects.link(light); light.location = location
        light.rotation_euler = (Vector((0,-.5,1.2))-light.location).to_track_quat('-Z','Y').to_euler()
    scene.view_settings.view_transform = 'Standard'
    bpy.ops.object.select_all(action='DESELECT'); root.select_set(True); obj.select_set(True)
    bpy.ops.export_scene.fbx(filepath=str(fbx), use_selection=True, object_types={'MESH','EMPTY'},
        axis_forward='-Z', axis_up='Y', apply_unit_scale=True, apply_scale_options='FBX_SCALE_UNITS',
        bake_space_transform=False, bake_anim=False, use_mesh_modifiers=False, path_mode='STRIP')
    for img in (albedo,rough,normal,mask): img.filepath = bpy.path.relpath(img.filepath, start=str(blend.parent))
    _, eye, target, scale = VIEWS[3]
    scene.camera.location = eye; scene.camera.rotation_euler = (Vector(target)-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.camera.data.ortho_scale = scale
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    obj.data.calc_loop_triangles()
    info = dict(stage='F3', source='F2_chupacabras_forma_r04', triangles=len(obj.data.loop_triangles),
        meshes=1, materials=1, atlas_size=SIZE, reduction=reduction, physical_device=False,
        maps={'BaseColor':'sRGB; RGB pigment, no baked lighting', 'Normal':'linear; tangent +Y/OpenGL',
              'Roughness':'linear; Blender source, not copied to Android', 'MetallicSmoothness':'linear; R=0, A=1-roughness'},
        texture_memory_mib={'runtime_RGBA32_with_mips':64, 'runtime_ASTC_6x6_with_mips_estimate':7.14},
        authorship='Original procedural surface authored in this project; no third-party textures or reference images distributed.',
        license='CC0-1.0 for the new procedural texture maps', mobile_budget_approved=False)
    (TEX/'manifest.json').write_text(json.dumps(info,indent=2)+'\n')
    render_views('pbr')
    print('F3_SURFACE_OK '+json.dumps(info))


if __name__ == '__main__': main()
