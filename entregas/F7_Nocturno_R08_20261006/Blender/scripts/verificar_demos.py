"""Reabre las demos y comprueba sus datos sin guardar ni renderizar.

Uso: blender -b -t 6 --python-exit-code 1 --python scripts/verificar_demos.py
Imprime un informe JSON entre DEMOS_JSON_BEGIN y DEMOS_JSON_END.
"""

import json
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
report = {"blender": bpy.app.version_string, "escenas": []}
for filename in ("demo_lowpoly.blend", "demo_ataque_arrastre.blend"):
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / "scenes" / filename))
    scene = bpy.context.scene
    assert scene.camera is not None, "Falta cámara activa"
    item = {
        "archivo": f"scenes/{filename}",
        "objetos": len(scene.objects),
        "camara": scene.camera.name,
        "resolucion": [scene.render.resolution_x, scene.render.resolution_y],
        "fps": scene.render.fps / scene.render.fps_base,
        "rango": [scene.frame_start, scene.frame_end],
    }
    if filename == "demo_lowpoly.blend":
        assert len(scene.objects) == 328
        assert item["resolucion"] == [1200, 900]
    else:
        assert item["rango"] == [1, 840] and item["fps"] == 24
        item["duracion_s"] = (scene.frame_end - scene.frame_start + 1) / item["fps"]
        assert item["duracion_s"] == 35
        assert scene.timeline_markers["ATAQUE • 15 s"].frame == 361
        item["ataque_s"] = (361 - scene.frame_start) / item["fps"]
        root = bpy.data.objects["Oveja • recorrido"]
        mouth = bpy.data.objects["Contacto • mordida"]
        item["contacto"] = []
        for frame in (433, 481, 601, 721, 793, 840):
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            neck = root.matrix_world @ Vector((-0.62, -0.05, -0.12))
            error = (neck - mouth.matrix_world.translation).length
            assert error < 0.001, (frame, "Se perdió el agarre", error)
            item["contacto"].append({"fotograma": frame, "error_unidades": error})
    report["escenas"].append(item)

print("DEMOS_JSON_BEGIN")
print(json.dumps(report, indent=2, ensure_ascii=False))
print("DEMOS_JSON_END")
