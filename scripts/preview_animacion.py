"""Previsualización económica: 420 imágenes Workbench a 12 fps, 35 s.

Abrir demo_ataque_arrastre.blend con Blender y ejecutar este script en background.
Conserva el .blend y las imágenes previas; usa una carpeta nueva en cada ejecución.
"""

from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
scene = bpy.context.scene
assert scene.frame_end == 840 and scene.render.fps == 24
output = ROOT / "previews" / "animacion_frames"
index = 1
while output.exists():
    output = ROOT / "previews" / f"animacion_frames_{index:02d}"
    index += 1
output.mkdir()
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x, scene.render.resolution_y = 640, 480
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.display.shading.light = "STUDIO"
scene.display.shading.studiolight_rotate_z = 0.4
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.background_type = "WORLD"
scene.world.color = (0.035, 0.055, 0.10)
for index, frame in enumerate(range(1, 841, 2), 1):
    scene.frame_set(frame)
    scene.render.filepath = str(output / f"{index:04d}.png")
    bpy.ops.render.render(write_still=True)
print(f"PREVIEW_OK: {output}; 420 imágenes, codificar a 12 fps")
