# F5/F6: validación G20 y corrección de permisos

3 de octubre de 2026. [Informe físico y estado de la sesión](../../Blender/docs/figura_ar_f5_f6.md).

La APK F4 0.2.0 mantuvo 30,005 fps de presentación durante 309,98 segundos,
con figura visible en las 2499 muestras de un tramo interior de 303,885 s.
El usuario aprobó el aspecto y la recuperación. La prueba de permiso denegado
posterior descubrió un bucle real de pausa/reanudación; por ello ese resultado
no basta para cerrar F6.

`TrackingProbe` solicita cámara al iniciar o al pulsar Reintentar; al reanudar
solo comprueba el permiso. Así el diálogo Android no inicia otra solicitud al
regresar. El fondo de cámara se oculta cuando no hay imagen, evitando el quad
blanco observado durante la denegación. No cambia el detector, la malla,
materiales, luces, escala ni paquetes.

`CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh` genera versión 0.2.2,
código 202 y nombre F6 con timestamp, reutilizando escena/prefab F4 R02.
La opción por defecto sigue siendo F1; F4 conserva su selección anterior.
Las APK anteriores permanecen. Los cambios runtime requieren repetir permiso,
reanudación y cinco minutos sobre la candidata nueva antes de aprobarla.

`FigurePreview` conserva sus ocho estados y añade ID incorrecto y recuperación:
primero exige que el detector reconozca realmente el ID 1. Usa
`docs/fixtures/tag41h12_id1.png`, generado con `apriltag_to_image` de la
biblioteca AprilTag Linux ya instalada; tagStandard41h12, 9×9 celdas, escala
nearest de 32 y margen blanco hasta 512×512. No se empaqueta como recurso de la
aplicación. Conserva la licencia `docs/licenses/AprilTag-native.txt`.

Referencia de generación: AprilRobotics. (s. f.). *apriltag.h* [Código fuente].
GitHub. https://github.com/AprilRobotics/apriltag/blob/master/apriltag.h

Todas las evidencias F5/F6 se guardan en el repositorio Blender,
`docs/evidencias/2026-10-03_figura_f5_f6/`; las comprobaciones generales de
tracking también generan sus JSON habituales dentro de Unity. El perfil ADB
reproducible está en `scripts/perfil_figura_g20.py` del repositorio Blender.

## Cierre acordado

El usuario indicó que basta con AR funcional y no es una app comercial.
Se cierra con **0.2.2**: arranque frío, marcador/figura y Captura verificados
realmente en G20. Captura usa ruta relativa en Android porque Unity añade el
directorio persistente; antes duplicaba la ruta. Editor conserva ruta absoluta.
Build final, firma, ABI, alineación y pruebas existentes pasan. No se repite otro
perfil largo por este detalle; los de 0.2.0/0.2.1 conservan sus límites en el informe.
La app fue desinstalada y la limpieza comprobada. Siguiente etapa F7, sin iniciarla.
