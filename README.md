**Revisión 0.2.8 / 208:** ampliación uniforme ×1,375 de modelos y recorrido;
reinicio completo al recuperar el marcador. AprilTag sin cambios.
[Detalle y verificaciones](docs/ataque_natural_1m.md). Instalada limpiamente en Moto G20; pruebas Unity y empaquetado correctos.
Escala, recorrido y reinicio aceptados en Moto G20 («todo bien 10/10»).
29,33 fps durante tres minutos; segundo plano correcto y reinstalación final
limpia del mismo APK derivado del AAB.
El usuario aceptó el movimiento de 0.2.7; versiones anteriores preservadas.

**Entrega del 11 de octubre — 0.2.5 / 205:** chupacabras y oveja en 3D, ataque
y reposo final, probados en Moto G20. AAB y APK derivado listos.
[Avance y verificación de la nueva entrega](docs/ataque_ar.md).
La sección F7 siguiente documenta la entrega previa preservada.

# Chupacabras — fuentes Blender

Actualización de la aplicación (10 de octubre): se añade una pantalla de inicio
y se retira el modo de desarrollo en la versión 0.2.3. [Cambios y validación](../../unity/chupacabras/docs/interfaz_inicio.md).
La entrega F7 descrita a continuación conserva su APK original y sus pruebas físicas.

El alcance vigente es una **figura del chupacabras sobre un marcador AprilTag**.
**F1–F7 completadas como demo funcional en Moto G20**. Nocturno R08 conserva
su apariencia y usa respiración R02, aceptada tras la prueba física.
[Entrega y resultados F7](docs/figura_ar_f7.md): 28,53 fps de media durante
310 s; no alcanza 30 fps sostenidos. Fuentes, APK, marcador y guía en
`entregas/F7_Nocturno_R08_20261006/` y su archivo `.tar.gz`.

- [Estado y punto exacto de retoma](docs/estado.md).
- [Prueba G20 y correcciones F5–F6](docs/figura_ar_f5_f6.md).
- [Entrega F3–F4, vistas y errores corregidos](docs/figura_ar_f3_f4.md).
- [Plan vigente y aceptación](docs/plan_secuencia.md).
- [Ficha visual](docs/ficha_produccion.md).
- [Aplicación Unity](../../unity/chupacabras/README.md).
- [Modelos realmente usados y separación de históricos](docs/modelos_vigentes_unity.md):
  copias verificadas en `../chupacabras_models/vigentes/`.
- [Archivo de modelos históricos](docs/modelos_historicos.md): 131 archivos
  trasladados a `historicos/`, conservando sus rutas relativas.
- [Separación para liberar espacio en Blender y Unity](docs/separacion_espacio.md):
  modelos, recursos y builds antiguos agrupados; versión final preservada.

Fuente exportable actual: `scenes/chupacabras_nocturno_r08_respira_r02.blend`, con texturas
PBR y respiración de cuatro segundos. [Vista](previews/chupacabras_nocturno_r08/tres_cuartos.png) ·
[Respiración final](previews/chupacabras_nocturno_r08_respira_r02/respiracion.mp4).
Se conservan `scenes/F2_chupacabras_forma_r04.blend` y la entrega F3 anterior;
la escena F4 R02 mantiene su presentación y seguimiento. [Entrega anterior F1–F2](docs/figura_ar_f1_f2.md).
`scenes/` conserva las dos fuentes Nocturno vigentes y F2 R04, necesaria para
regenerar Nocturno. Los demás modelos de trabajo están ahora en `historicos/`.

Para revisar la actuación histórica: `historicos/scenes/14_ataque_r07.blend` o
`historicos/previews/14_ataque_r07.mp4` (0–25 s, no corto definitivo ni entrega nueva).
Las [demos lowpoly](docs/demo_lowpoly.md) y [animada](docs/demo_animada.md)
conservan sus alcances independientes.
