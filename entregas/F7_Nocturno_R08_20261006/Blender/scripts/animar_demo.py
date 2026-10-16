"""Anima la demo existente sin sobrescribirla; movimientos por piezas rígidas.

Uso: blender -b -t 6 --python-exit-code 1 --python scripts/animar_demo.py
"""

import math
from pathlib import Path

import bpy
from mathutils import Euler, Vector


ROOT = Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT / "scenes/demo_lowpoly.blend"))
scene = bpy.context.scene
scene.name = "Demo animada • 35 segundos"
scene.render.fps = 24
scene.render.fps_base = 1
scene.frame_start, scene.frame_end = 1, 840
scene.frame_set(1)
sheep = bpy.data.collections["03 • Oveja PROXY"]
beast = bpy.data.collections["04 • Chupacabras BORRADOR"]
controls = bpy.data.collections.new("07 • Controles de animación")
scene.collection.children.link(controls)


def parent_preserving(obj, parent):
    world = obj.matrix_world.copy()
    obj.parent = parent
    obj.matrix_world = world


def pivot(name, position, objects=(), parent=None):
    obj = bpy.data.objects.new(name, None)
    controls.objects.link(obj)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = 0.25
    obj.location = position
    bpy.context.view_layer.update()
    if parent:
        parent_preserving(obj, parent)
    bpy.context.view_layer.update()
    for child in objects:
        parent_preserving(child, obj)
    bpy.context.view_layer.update()
    return obj


def smooth(a, b, t):
    u = max(0.0, min(1.0, (t - a) / (b - a)))
    return u * u * (3 - 2 * u)


def key(obj, frame):
    obj.keyframe_insert("location", frame=frame)
    obj.keyframe_insert("rotation_euler", frame=frame)


sheep_parts = list(sheep.objects)
beast_parts = list(beast.objects)
wolf_root = pivot("Chupacabras • recorrido", (2.2, 0.6, 0), beast_parts)
sheep_root = pivot("Oveja • recorrido", (-2, -1.15, 1), sheep_parts)
sheep_head = pivot("Oveja • pastoreo", (-2.6, -1.15, 0.91),
                   [o for o in sheep_parts if o.name.startswith(("Cabeza", "Oreja"))], sheep_root)
wolf_head = pivot("Chupacabras • cabeza", (1.22, 0.6, 1.65),
                 [o for o in beast_parts if o.name.startswith(
                     ("Cuello", "Cráneo", "Hocico", "Mandíbula", "Oreja", "Ojo", "Colmillo"))], wolf_root)
mouth = pivot("Contacto • mordida", (0.19, 0.52, 1.25), parent=wolf_head)
tail = pivot("Chupacabras • cola", (3.35, 0.65, 1.72),
             [o for o in beast_parts if o.name.startswith("Cola")], wolf_root)

wolf_legs = []
for fore in (True, False):
    for side in (-1, 1):
        parts = []
        for obj in beast_parts:
            if not obj.name.startswith(("Extremidad", "Pata con", "Garra")):
                continue
            point = obj.matrix_world.translation - Vector((2.2, 0.6, 0))
            if (point.x < 0) == fore and (point.y < 0) == (side < 0):
                parts.append(obj)
        pos = (2.2 + (-0.75 if fore else 0.83), 0.6 + side * 0.37, 1.6 if fore else 1.5)
        control = pivot(f"Pata criatura • {'delantera' if fore else 'trasera'} {side}", pos, parts, wolf_root)
        wolf_legs.append((control, (0 if fore else math.pi) + (0 if side < 0 else math.pi)))

sheep_legs = []
for i, obj in enumerate(o for o in sheep_parts if o.name.startswith("Pata oveja")):
    pos = obj.matrix_world.translation.copy()
    pos.z = 0.7
    sheep_legs.append(pivot(f"Pata oveja • {i + 1}", pos, [obj], sheep_root))

# Pose sin deformación elástica: curvas de posición y rotación sobre pivotes.
head_base = sheep_head.location.copy()
wolf_start = Vector((3.0, 1.05, 0))
wolf_launch = Vector((1.3, 0.15, 0))
wolf_land = Vector((-0.3, -1.3, 0))
sheep_start = Vector((-2, -1.15, 1))
neck_local = Vector((-0.62, -0.05, -0.12))
frames = sorted(set(range(1, 842, 2)) | {360, 361, 385, 433, 793, 840, 841})

for frame in frames:
    t = (frame - 1) / 24
    moving = t < 13.5 or 18 <= t < 33
    stride = t * (3.1 if t < 15 else 4.4)
    if t < 15:
        approach = smooth(0, 13.5, t)
        wolf_root.location = wolf_start.lerp(wolf_launch, approach)
        wolf_root.location.y += 0.24 * math.sin(t * 0.6) * (1 - smooth(12, 15, t))
        wolf_root.location.z = (0.035 * math.sin(stride * 2) if moving else 0) - 0.12 * smooth(14.2, 15, t)
    elif t < 16:
        u = t - 15
        wolf_root.location = wolf_launch.lerp(wolf_land, smooth(15, 16, t))
        wolf_root.location.z = 1.15 * math.sin(math.pi * u) - 0.12 * (1 - u)
    elif t < 18:
        wolf_root.location = wolf_land.copy()
        wolf_root.location.z = 0.035 * math.sin((t - 16) * 19) - 0.07 * (1 - smooth(16, 18, t))
    else:
        wolf_root.location = wolf_land.lerp(Vector((4.2, -0.3, 0)), smooth(18, 33, t))
        wolf_root.location.z = 0.025 * math.sin(stride * 2) if moving else 0
    wolf_root.rotation_euler = (0, 0, 0.07 * math.sin(t * 0.7) * (1 - smooth(13, 15, t)))
    wolf_head.rotation_euler = (0, -0.32 * smooth(15.6, 16.5, t),
                               0.065 * math.sin(t * 1.6) * (1 - smooth(14, 15, t)))
    tail.rotation_euler = (0, 0.09 * math.sin(t * 1.5), 0.16 * math.sin(t * 1.8))
    for leg, phase in wolf_legs:
        swing = (0.15 if t < 15 else -0.19) * math.sin(stride + phase) if moving else 0
        if 15 <= t < 16:
            swing += 0.45 * math.sin(math.pi * (t - 15) + phase * 0.25)
        leg.rotation_euler = (0, swing, 0)
        key(leg, frame)
    key(wolf_root, frame)
    key(wolf_head, frame)
    key(tail, frame)

    fall = smooth(16, 17.4, t)
    sheep_root.rotation_euler = (fall * 1.26, 0, fall * math.pi)
    sheep_head.location = head_base.copy()
    sheep_head.rotation_euler = (0, (0.13 + 0.17 * math.sin(t * 2.7)) * (1 - fall),
                                  0.07 * math.sin(t * 1.2) * (1 - fall))
    # Calcular la posición del cuello a partir de la boca, evitando separación al arrastrar.
    bpy.context.view_layer.update()
    bitten_position = mouth.matrix_world.translation - sheep_root.rotation_euler.to_matrix() @ neck_local
    sheep_root.location = sheep_start.lerp(bitten_position, fall)
    if t < 16:
        sheep_root.location.z += 0.017 * math.sin(t * 3)
    for i, leg in enumerate(sheep_legs):
        struggle = 0.38 * math.sin(t * 9 + i * math.pi / 2) * fall * (1 - smooth(28, 33, t))
        leg.rotation_euler = (0.12 * math.sin(t * 7 + i) * fall, struggle, 0)
        key(leg, frame)
    key(sheep_root, frame)
    key(sheep_head, frame)

# Interpolación lineal para que las curvas horneadas no introduzcan sobrepasos.
for obj in controls.objects:
    if not obj.animation_data or not obj.animation_data.action:
        continue
    action = obj.animation_data.action
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for point in curve.keyframe_points:
                        point.interpolation = "LINEAR"

for name, frame in [("Pastoreo y acecho", 1), ("ATAQUE • 15 s", 361),
                    ("Impacto • 16 s", 385), ("Arrastre • 18 s", 433), ("Final • 33 s", 793)]:
    scene.timeline_markers.new(name, frame=frame)

# Comprobar contacto durante todo el arrastre y duración real del borrador.
for frame in (433, 481, 601, 721, 793, 840):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    neck = sheep_root.matrix_world @ neck_local
    assert (neck - mouth.matrix_world.translation).length < 0.001, (frame, "Se perdió el agarre")
assert (scene.frame_end - scene.frame_start + 1) / scene.render.fps == 35
assert scene.timeline_markers["ATAQUE • 15 s"].frame == 361
scene.frame_set(1)
scene.render.resolution_x, scene.render.resolution_y = 640, 480
scene.cycles.samples = 8
scene.render.engine = "CYCLES"
scene["demo_timing"] = "35 s: pastoreo/acecho 0–15, ataque 15–18, arrastre 18–33, cierre 33–35"
scene["demo_scope"] = "Piezas rígidas, sin rig final, audio, Unity ni AR"
stem = "demo_ataque_arrastre"
index = 1
while (ROOT / "scenes" / f"{stem}.blend").exists():
    stem = f"demo_ataque_arrastre_{index:02d}"
    index += 1
scene.render.filepath = str(ROOT / "previews" / f"{stem}.png")
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "scenes" / f"{stem}.blend"))
print(f"ANIMATION_OK: {stem}, 35 s, ataque 15 s, contacto verificado")
