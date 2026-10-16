"""Borrador estático editable. Ejecutar: blender -b -t 6 --python este_archivo.py.

Trabaja en una escena nueva y conserva entregas existentes mediante sufijos.
La oveja es un marcador de volumen provisional, no el modelo de producción.
"""

import math
import random
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
random.seed(12)
scene = bpy.data.scenes.new("Demo • Noche del chupacabras")
bpy.context.window.scene = scene


def material(name, color, emission=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = 0.88
    if emission:
        shader.inputs["Emission Color"].default_value = (*color, 1)
        shader.inputs["Emission Strength"].default_value = emission
    return mat


def collection(name):
    result = bpy.data.collections.new(name)
    scene.collection.children.link(result)
    return result


def finish(obj, name, mat, group):
    obj.name = name
    for previous in list(obj.users_collection):
        previous.objects.unlink(obj)
    group.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def box(name, position, scale, mat, group, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    obj = finish(bpy.context.object, name, mat, group)
    obj.scale = scale
    obj.rotation_euler = rotation
    return obj


def ico(name, position, scale, mat, group, subdivisions=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1, location=position)
    obj = finish(bpy.context.object, name, mat, group)
    obj.scale = scale
    return obj


def segment(name, start, end, radius, mat, group, tip=None, vertices=6):
    direction = Vector(end) - Vector(start)
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices, radius1=radius,
        radius2=radius * 0.75 if tip is None else tip,
        depth=direction.length, location=(Vector(start) + Vector(end)) / 2,
    )
    obj = finish(bpy.context.object, name, mat, group)
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    return obj


def mesh(name, vertices, faces, mat, group):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    group.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


ground = collection("01 • Tierra y vegetación")
barn = collection("02 • Granero")
sheep = collection("03 • Oveja PROXY")
beast = collection("04 • Chupacabras BORRADOR")
sky = collection("05 • Luna y fondo")
stage = collection("06 • Cámara y luces")

earth = material("Tierra • pizarra cálida", (0.13, 0.115, 0.105))
edge = material("Canto de tierra", (0.065, 0.065, 0.082))
grass = material("Hierba seca • salvia", (0.22, 0.25, 0.19))
stone = material("Piedra azul", (0.16, 0.20, 0.26))
woods = [material(f"Madera {i}", (0.13 + i * 0.023, 0.075 + i * 0.012, 0.045 + i * 0.009)) for i in range(4)]
roof = material("Tejado oscuro", (0.075, 0.095, 0.13))
black = material("Interior del granero", (0.007, 0.009, 0.015))
wool = material("Lana marfil facetada", (0.73, 0.70, 0.56))
face = material("Cabeza y patas de oveja", (0.07, 0.085, 0.095))
hide = material("Piel • carbón azulado", (0.045, 0.068, 0.088))
fur = material("Mechones y espinas", (0.09, 0.125, 0.15))
claw = material("Garras y colmillos", (0.36, 0.40, 0.36))
eyes = material("Ojos • amarillo encendido", (1, 0.56, 0.018), 4)
moon = material("Luna • crema fría", (0.74, 0.85, 1), 2)
pine = material("Árboles índigo", (0.025, 0.055, 0.095))

# Una base recortada ayuda a leer el conjunto como un pequeño escenario.
box("Base de tierra", (0, 1, -0.3), (14, 11, 0.6), edge, ground)
box("Superficie", (0, 1, 0.01), (13.95, 10.95, 0.12), earth, ground)
for i in range(65):
    x, y = random.uniform(-6.5, 6.5), random.uniform(-3.8, 6)
    if -4.8 < x < -1.2 and 1.1 < y < 4.8:
        continue
    for j in range(3):
        a = j * 2.1
        h = random.uniform(0.18, 0.42)
        mesh(f"Mata {i:02d}-{j}", [(x - 0.09, y, 0.08), (x + 0.09, y + 0.035, 0.08),
             (x + math.cos(a) * 0.17, y + math.sin(a) * 0.17, h)], [(0, 1, 2)], grass, ground)
for i in range(15):
    ico("Piedra", (random.uniform(-6, 6), random.uniform(-3, 5.5), 0.14),
        (0.24, 0.18, 0.15), stone, ground)

# Granero: tablas individuales, puerta abierta y cubierta a dos aguas.
bx, by = -3.1, 3.1
box("Oscuridad interior", (bx, by, 1.3), (3.3, 2.9, 2.6), black, barn)
for i in range(12):
    x = bx - 1.65 + i * 0.3
    height = 2.5 if abs(x - bx) > 0.65 else 0.6
    z = height / 2 if height > 1 else 2.23
    box("Tabla frontal", (x, by - 1.48, z), (0.28, 0.12, height), woods[i % 4], barn)
for i in range(11):
    for side in (-1, 1):
        box("Tabla lateral", (bx + side * 1.74, by - 1.4 + i * 0.28, 1.25),
            (0.12, 0.26, 2.5), woods[(i + 1) % 4], barn)
mesh("Frontón", [(bx - 1.8, by - 1.51, 2.5), (bx + 1.8, by - 1.51, 2.5),
     (bx, by - 1.51, 3.65)], [(0, 1, 2)], woods[1], barn)
for side in (-1, 1):
    box("Faldón de tejado", (bx + side * 0.96, by, 3.12), (2.35, 3.5, 0.16),
        roof, barn, (0, side * 0.54, 0))
for side in (-1, 1):
    box("Jamba", (bx + side * 0.75, by - 1.58, 1), (0.13, 0.15, 2), woods[3], barn)
box("Dintel", (bx, by - 1.58, 2.04), (1.65, 0.15, 0.15), woods[3], barn)
segment("Travesaño inclinado", (bx + 0.95, by - 1.61, 0.2), (bx + 1.6, by - 1.61, 2.25),
        0.065, woods[3], barn, vertices=4)

# Oveja provisional: únicamente sirve para composición y escala.
sx, sy = -2.0, -1.15
for x in (-0.5, 0.5):
    for y in (-0.26, 0.26):
        segment("Pata oveja proxy", (sx + x, sy + y, 0.7), (sx + x + 0.08, sy + y, 0.12),
                0.105, face, sheep)
ico("Volumen de lana", (sx, sy, 1), (0.92, 0.53, 0.62), wool, sheep, 2)
for x, y, z in [(-0.45, -0.25, 1.3), (0.15, -0.4, 1.15), (0.52, 0, 1.2)]:
    ico("Facetas de lana", (sx + x, sy + y, z), (0.43, 0.3, 0.35), wool, sheep)
ico("Cabeza inclinada", (sx - 0.89, sy - 0.12, 0.65), (0.33, 0.26, 0.4), face, sheep)
for y in (-0.36, 0.16):
    ico("Oreja oveja", (sx - 0.8, sy + y, 0.9), (0.23, 0.13, 0.1), face, sheep)

# Chupacabras original de primitivas: postura baja, lomo arqueado y espinas.
origin = Vector((2.2, 0.6, 0))


def p(x, y, z):
    return origin + Vector((x, y, z))


ico("Tórax", p(-0.2, 0, 1.55), (1.03, 0.48, 0.72), hide, beast, 2)
ico("Cadera alta", p(0.75, 0.03, 1.6), (0.68, 0.4, 0.57), hide, beast)
ico("Hombros", p(-0.83, 0, 1.56), (0.52, 0.52, 0.68), hide, beast, 2)
ico("Cuello inclinado", p(-1.13, -0.02, 1.55), (0.5, 0.35, 0.46), hide, beast)
ico("Cráneo", p(-1.53, -0.05, 1.56), (0.48, 0.33, 0.42), hide, beast, 2)
ico("Hocico", p(-1.91, -0.08, 1.38), (0.38, 0.24, 0.22), hide, beast)
ico("Mandíbula", p(-1.88, -0.075, 1.14), (0.34, 0.20, 0.12), hide, beast)
for y in (-0.23, 0.22):
    segment("Oreja puntiaguda", p(-1.4, y, 1.8), p(-1.17, y * 1.65, 2.35),
            0.18, hide, beast, tip=0)
    ico("Ojo amarillo", p(-1.69, y * 1.39, 1.65), (0.115, 0.065, 0.093), eyes, beast, 2)
    segment("Colmillo", p(-2.02, y * 0.83, 1.36), p(-2.03, y * 0.83, 1.16),
            0.055, claw, beast, tip=0)
for y in (-0.37, 0.37):
    near = y < 0
    arm = [p(-0.75, y, 1.6), p(-0.92, y * 1.4, 0.83), p(-1.28 if near else -0.8, y * 1.8, 0.22)]
    leg = [p(0.83, y, 1.5), p(1.2, y * 1.25, 0.88), p(0.79, y * 1.5, 0.48), p(1.07, y * 1.7, 0.17)]
    for points, radii in ((arm, (0.23, 0.14)), (leg, (0.27, 0.16, 0.1))):
        for a, b, radius in zip(points, points[1:], radii):
            segment("Extremidad angulosa", a, b, radius, hide, beast)
        toe = points[-1]
        ico("Pata con garras", toe, (0.27, 0.2, 0.13), hide, beast)
        for offset in (-0.11, 0, 0.11):
            segment("Garra", toe + Vector((-0.16, offset, 0)), toe + Vector((-0.37, offset, -0.06)),
                    0.045, claw, beast, tip=0)
for i in range(9):
    x = -1.0 + i * 0.25
    z = 2.0 + 0.15 * math.sin(i * 0.4)
    segment("Espina dorsal", p(x, 0.04, z), p(x + 0.3, 0.05, z + 0.62 - i * 0.035),
            0.15 - i * 0.006, fur, beast, tip=0)
for y in (-0.33, 0.33):
    for i in range(4):
        segment("Mechón de cuello", p(-0.75 + i * 0.17, y, 1.9),
                p(-0.5 + i * 0.17, y * 1.55, 2.15), 0.11, fur, beast, tip=0)
tail = [p(1.15, 0.05, 1.72), p(1.9, 0.15, 1.4), p(2.5, 0.38, 1.15), p(2.95, 0.55, 1.45)]
for i in range(3):
    segment("Cola", tail[i], tail[i + 1], 0.19 - 0.05 * i, hide, beast, tip=0.13 - 0.05 * i)

for x, y, height in [(-6, 5.3, 4), (-5, 6, 4.8), (0.3, 6, 3.7), (5.5, 5.4, 4.5), (6.3, 4.5, 3.2)]:
    segment("Tronco", (x, y, 0), (x, y, height), 0.13, woods[0], sky)
    for fraction in (0.43, 0.63, 0.8):
        segment("Pino geométrico", (x, y, height * fraction - 0.7), (x, y, height * fraction + 1.1),
                (1.2 - fraction) * 1.4, pine, sky, tip=0, vertices=7)
ico("Luna llena lowpoly", (2.0, 6.1, 6.7), (0.82, 0.82, 0.82), moon, sky, 2)

world = bpy.data.worlds.new("Noche índigo")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.035, 0.055, 0.15, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.4
scene.world = world


def light(name, position, energy, color, size, target):
    data = bpy.data.lights.new(name, "AREA")
    data.energy, data.color, data.shape, data.size = energy, color, "DISK", size
    obj = bpy.data.objects.new(name, data)
    stage.objects.link(obj)
    obj.location = position
    aim(obj, target)


light("Luz de luna", (1, 5, 9), 1750, (0.45, 0.63, 1), 3, (0, 0, 0))
light("Relleno de lectura", (-4, -5, 6), 850, (0.63, 0.72, 1), 6, (0, 1, 1))
light("Contorno de criatura", (6, 2, 5), 1250, (0.35, 0.67, 0.82), 3, (2, 0, 1))

camera_data = bpy.data.cameras.new("Cámara • composición general")
camera = bpy.data.objects.new("Cámara • composición general", camera_data)
stage.objects.link(camera)
camera.location = (10, -17, 11)
aim(camera, (0, 1.4, 2))
camera_data.type = "ORTHO"
camera_data.ortho_scale = 17.5
scene.camera = camera
scene.render.engine = "CYCLES"
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX"
scene.render.film_transparent = False

# Dejar una vista útil al abrir el archivo, con objetos organizados por colección.
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == "VIEW_3D":
            area.spaces.active.region_3d.view_perspective = "CAMERA"
for obj in bpy.context.selected_objects:
    obj.select_set(False)

(ROOT / "scenes").mkdir(exist_ok=True)
(ROOT / "previews").mkdir(exist_ok=True)
stem = "demo_lowpoly"
index = 1
while (ROOT / "scenes" / f"{stem}.blend").exists() or (ROOT / "previews" / f"{stem}.png").exists():
    stem = f"demo_lowpoly_{index:02d}"
    index += 1
scene.render.filepath = str(ROOT / "previews" / f"{stem}.png")
assert len(beast.objects) > 30 and scene.camera is not None
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "scenes" / f"{stem}.blend"))
bpy.ops.render.render(write_still=True)
print(f"DEMO_OK: {stem}; objetos={len(scene.objects)}")
