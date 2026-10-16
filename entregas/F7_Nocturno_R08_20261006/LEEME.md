# Nocturno R08 — demo AR, F7

**F7 completada el 6 de octubre de 2026 como demo funcional aceptada en Moto G20.**

## Uso en Moto G20

1. Instalar `APK/F6_figure_20261006_181916.apk` y abrir Chupacabras — Figura AR.
2. Conceder cámara y apuntar la cámara trasera al marcador existente, bien iluminado y sin reflejos.
3. Mantener visibles sus esquinas y mover el teléfono para observar la figura y su respiración de cuatro segundos.
4. Al retirar el marcador se oculta la figura. Volver a enfocarlo permite recuperarla; lo mismo tras regresar del segundo plano.
5. Si se denegó cámara, autorizarla en Ajustes de la app y pulsar Reintentar.

Marcador: `Unity/marker/03_marker_carta.pdf`, AprilTag tagStandard41h12 ID 0;
100 mm entre esquinas de detección y dibujo de 180 mm. Reutilizar la impresión existente.
La proyección usa FOV provisional de 60°; no implica escala física calibrada.

## Identificación

APK 0.2.2, código 202; paquete `com.chupacabras.ar.figure`; 55.348.110 bytes.
SHA-256: `7db6358cdb13c37467a3d42f76d163ef8359c0ef25583441065ed5b869863aae`.
El nombre F6 y la versión se conservan para entregar exactamente los bytes probados con R08 y respiración R02.
No confundir con la APK anterior de 41.621.707 bytes, también 0.2.2.
Es una build de desarrollo para demo, no una publicación de tienda.

## Inventario

- `APK/`: candidata íntegra, sin recompilar después de la prueba.
- `Blender/scenes/chupacabras_nocturno_r08_respira_r02.blend`: fuente editable vigente con respiración perceptible.
- `Blender/scenes/chupacabras_nocturno_r08.blend`: revisión original preservada; misma geometría y texturas.
- `Blender/scenes/F2_chupacabras_forma_r04.blend`: base del generador de R08.
- `Blender/exports/`: FBX, cuatro mapas 2K y manifiesto de autoría.
- `Blender/scripts/`: generadores y verificadores existentes; los scripts históricos pueden requerir fuentes históricas conservadas en el repositorio original.
- `Blender/previews/`: vistas, respiración y comprobaciones de fuente.
- `Unity/Assets`, `Packages`, `ProjectSettings`: proyecto editable completo, con recursos históricos preservados; solo la escena F4 entra en la build de figura.
- `Unity/scripts/`: compilación y verificadores; `Unity/docs/licenses/`: avisos AprilTag; `Unity/marker/`: marcador y sus fuentes.
- `evidencias/candidata_original/`: APK inicial, conservada para trazabilidad; el defecto de respiración fue corregido.
- `evidencias/F7/`: pruebas de ambas candidatas, build R02, perfiles completos, aceptación y limpieza.
- `manifest.json` y `SHA256SUMS`: inventario e integridad de todos los archivos.
- `evidencias/compilacion_R08/`: compilación original, comprobaciones y estados sintéticos. No sustituye evidencia física.

## Reproducción

Abrir `Unity/` exclusivamente en Unity 6000.3.22f1, escena `Assets/Scenes/F4_FiguraAR_r02.unity`.
Desde esa carpeta: `CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh`.
Los scripts existentes usan la ruta del Editor de este equipo; para otro equipo debe instalarse la misma versión y adaptar esa ruta.
Library, Temp, SDK, Editor y credenciales no se distribuyen. La resolución inicial de dependencias requiere caché o red y licencia Unity válida.
Una recompilación genera otra APK: no hereda automáticamente el hash ni la validación física de esta entrega.

Blender verificado con 5.2.2 LTS. Desde `Blender/`:
`CHUPA_ART_REV=r08_respira_r02 blender -b -t 2 --python-exit-code 1 --python scripts/verificar_nocturno.py`.
La corrección se reproduce desde R08 con `scripts/refinar_respiracion_nocturno.py` en un destino sin R02; el script rechaza sobrescribirla.
Para generar otra revisión artística, seguir `Blender/docs/rediseno_nocturno.md` usando otro identificador, sin sobrescribir R08.

## Autoría y licencias

Nocturno R08 y sus mapas procedurales son recursos originales del proyecto según `Blender/exports/chupacabras_nocturno_r08/manifest.json`; no se añaden imágenes de referencia ajenas.
Ese manifiesto acredita procedencia, pero no declara una nueva licencia general del proyecto.
AprilTag conserva sus avisos en `Unity/docs/licenses/`, y el paquete embebido conserva su LICENSE.
Los recursos históricos de oveja incluidos en las fuentes conservan `Unity/Assets/Sheep/License_Quaternius.txt`; no forman parte de la escena AR vigente.
Los paquetes Unity conservan sus versiones y están sujetos a sus términos originales. No se reasignan licencias.

## Límites

APK final: 310 s a **28,53 fps**, p95 49,98 ms y máximo 83,30 ms; 2530/2530 muestras con figura visible.
**No alcanza 30 fps sostenidos.** El usuario aceptó ese resultado como suficiente para la demo.
Memoria PSS 401,15 → 386,33 MiB; batería 37,9 → 39,4 °C con USB; estado térmico reportado 0.
Apariencia, respiración corregida, apoyo, pérdidas/recuperación y reanudación comprobados en G20.
Se retiró la instalación de pruebas; paquete/proceso/datos externos ausentes. No había instalación previa.
Informe detallado: `Blender/docs/figura_ar_f7.md`. Datos brutos: `evidencias/F7/`.
Los informes históricos conservan fechas y resultados de sus revisiones; no sustituyen este cierre.
S23 no probado. Sin validación de uso durante horas, calibración exacta ni ejecución Android con páginas de 16 KB.

## Comprobar integridad

Desde la raíz de esta carpeta: `sha256sum -c SHA256SUMS`.
Para la APK sola: `sha256sum APK/F6_figure_20261006_181916.apk`.
El hash del archivo `.tar.gz` se entrega en el archivo hermano `.tar.gz.sha256`.

La estructura de este paquete es `Blender/` + `Unity/`; algunos enlaces históricos
entre repositorios o a entregas antiguas solo aplican a las rutas de trabajo originales.
Esta guía y el informe F7 son las entradas portables de la entrega. Los archivos
históricos que no se necesitan para reabrir/compilar la figura permanecen en los
repositorios originales; no fueron eliminados ni sustituidos.
