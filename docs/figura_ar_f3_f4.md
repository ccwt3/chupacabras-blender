# Figura AR: malla y superficie F3, integración F4

Trabajo del 3 de octubre de 2026. Alcance: las dos etapas autorizadas F3 y F4;
la validación física F5 no forma parte de esta sesión. Continuidad canónica en
[estado](estado.md), requisitos en [plan](plan_secuencia.md).

## Malla y superficie

Fuente de forma preservada: `scenes/F2_chupacabras_forma_r04.blend`.
La nueva entrega se genera con `scripts/figura_superficie.py` y se comprueba
independientemente con `scripts/verificar_figura_superficie.py`.

La reducción actúa en cuerpo, cráneo y mandíbula, conservando los detalles de
silueta. De 88.952 triángulos F2 pasa a **34.026**, una reducción del **61,7 %**.
La base F1 tenía 30.880 triángulos: F3 tiene un 10,2 % más que aquella base,
pero conserva los cambios de forma F2. Ninguna cifra es un presupuesto móvil
aprobado. Las 18 mallas y seis materiales se consolidan en **una malla y un
material**, con la pose fija, sin huesos, Animator ni clips.

Distancia bidireccional de los vértices a la superficie antes/después de la
reducción, en metros de autoría: cuerpo 0,003595; cráneo 0,001887;
mandíbula 0,000977. Es una medida muestreada, no una distancia de Hausdorff
continua ni una garantía visual. Con la escala Unity 0,045, el máximo equivale
a unos 0,162 mm en el espacio virtual del marcador.

La UV conserva cortes automáticos relajados por desenvolvimiento angular,
islas con superficie y grosor suficientes para recibir muestras y padding de
horneado. Se triangula antes del bake para conservar la base tangente en Unity.
No se añade escultura de alta resolución: la forma F2 sigue separada y el
detalle fino de piel se genera en nodos y se hornea a mapas originales.

| Mapa 2048 × 2048 | Uso |
| --- | --- |
| BaseColor | sRGB, pigmentación sin iluminación horneada. |
| Normal | Lineal, tangente +Y; textura normal en URP. |
| Roughness | Lineal, fuente Blender; no se copia a Unity. |
| MetallicSmoothness | Lineal, R=0 metálico; alfa=1−rugosidad para URP Lit. |

Android recibe tres mapas con mipmaps, ASTC 6×6 y lectura CPU desactivada.
La estimación de esos mapas con mipmaps es **7,14 MiB** en ASTC; sería **64 MiB**
si los tres se descomprimieran como RGBA32. No incluye framebuffer, cámara,
detector, malla, buffers temporales ni memoria total del proceso. La compresión
configurada no sustituye una medición en el G20.

Autoría: texturas procedurales creadas para este proyecto por el agente, a partir
de los nodos descritos en el generador. Mapas nuevos bajo CC0-1.0 según el
manifiesto de exportación. No se descargaron texturas ni se empaquetaron imágenes
de referencia. Esto no cambia la licencia de otras fuentes del repositorio.

## Integración

F4 reutiliza `TrackingProbe`, `FigurePreview`, la ruta de compilación y el
verificador APK de F1. `CHUPA_FIGURE_STAGE=F4` selecciona la nueva escena,
carpeta de recursos y versión; sin esa variable se conserva el comportamiento F1.
`FigureSurface.cs` prepara el FBX, mapas URP Lit y capturas comparables.

La nueva figura mantiene posición, rotación y escala de `StaticFigure` de F1.
La iluminación local emplea dos luces direccionales cálida/fría y ambiente plano
neutro; no añade sombras, suelo, cielo, reflejos de un escenario, cámaras internas
ni contenido cinematográfico. Los ojos se distinguen por color y rugosidad, sin
emisión ni efectos. Fondos claros/oscuros sintéticos son evidencia de contraste,
no sustituyen la cámara real.

Los originales F1, F2 y las escenas históricas se conservan. Los tres cambios
ajenos preparados en Unity (GraphicsSettings, QualitySettings y
PackageManagerSettings) se comparan con el inventario inicial.

## Errores encontrados y corrección

Las primeras revisiones de superficie mostraron pequeños triángulos negros.
La geometría cerrada no era suficiente para detectar este defecto: había islas
UV menores que un píxel que no recibían muestras. Aumentar padding no lo
resolvió; el desenvolvimiento angular por sí solo tampoco. Se corrigió el tamaño
mínimo de islas, incluyendo grosor para islas estrechas, antes de volver a hornear.
El verificador de cobertura detectó 210, 169 y finalmente un triángulo sin muestra
en los intentos anteriores. Fuentes y logs de esos intentos se conservan.

Blender 5.2.2 emite avisos de futura retirada de `use_nodes` en Blender 6.0;
son avisos de API, no fallos de exportación en la versión instalada.

## Reproducción y validación

Elegir una revisión nueva para conservar las entregas existentes:

```bash
CHUPA_F3_REV=r06 blender -b -t 4 --python-exit-code 1 --python scripts/figura_superficie.py
CHUPA_F3_REV=r06 blender -b -t 4 --python-exit-code 1 --python scripts/verificar_figura_superficie.py
```

Unity usa exclusivamente `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`.
La candidata se reproduce desde la raíz Unity con:

```bash
CHUPA_FIGURE_STAGE=F4 bash scripts/build_figure.sh
```

La escena existente se conserva; otra fuente requiere una nueva revisión de
recursos/escena, no sobrescribir una entrega. El script genera evidencia y APK
con destinos nuevos. No instala ni ejecuta la aplicación en teléfono.

Las comprobaciones de F3 incluyen reapertura independiente, topología cerrada,
UV/coordenadas finitas, cobertura de bake en centros de triángulos, mapas y
convenciones, inversión rugosidad/suavidad y reimportación FBX con comparación de
vértices. No son pruebas exhaustivas de autointersecciones o de todos los niveles
mip. Las seis vistas y comparación de forma constituyen una revisión visual aparte.

Entrega Blender: [fuente R05](../scenes/F3_chupacabras_superficie_r05.blend),
[FBX](../exports/F3_chupacabras_superficie_r05.fbx),
[mapas y manifiesto](../exports/F3_chupacabras_superficie_r05/manifest.json),
[seis vistas](../previews/F3_chupacabras_superficie_r05/seis_vistas.png),
[comparación de forma](../previews/F3_chupacabras_superficie_r05/comparacion_forma.png)
y [checks](../previews/F3_chupacabras_superficie_r05/reopen_checks.json).
La reapertura y el FBX pasaron; el centro UV de cada triángulo recibe textura.
Los intentos R01–R04 permanecen locales; sus logs comprimidos conservan los fallos.
`resumen_figura.py` ahora permite importar su función de montaje sin ejecutar
el resumen F2, que conserva su comportamiento al invocarlo como script.

La primera verificación Unity falló al comparar los ejes de `Mesh.bounds` con
los de otra ruta de intercambio. Este FBX conserva XY de Blender y Z invertida
en la malla; la transformación existente de F1 la coloca sobre el marcador.
El verificador compara ahora los límites en el espacio de la raíz y las vistas
usan esa misma conversión. No se giró la figura para satisfacer el test.

El diagnóstico visual también encontró una captura inicial sobreexpuesta al
cambiar de pipeline en Editor: las siguientes capturas con el mismo material
recuperan el aspecto normal. El capturador F4 hace una pasada de inicialización
antes de guardar la imagen; el material PBR permanece conectado. La ejecución
sintética comprueba por separado la presentación durante seguimiento.

La revisión visual Unity R01 expuso una transición oscura demasiado abrupta en
el muslo. Se compararon 26.063 vértices importados con las esquinas Blender:
todas las normales coinciden (producto escalar mínimo 0,9999998); no hubo
inversiones de signo tangente. Un vértice presentó discrepancia tangente
(producto escalar 0,90); el resto superó 0,99. Las capturas sin normales,
sin texturas y sin iluminación separaron ese problema de la UV: la transición
persistía sin mapas y desaparecía sin luces. R02 orienta ambas luces desde
arriba en el espacio real de la figura, eleva el ambiente neutro y conserva la
luz de relleno por píxel, que ya estaba activa en F1. R01 y su APK quedan como intento conservado.

Al preparar R02 hubo un error de compilación: el ajuste público de luces
adicionales es de solo lectura en Unity 6000.3.22f1. Se comprobó en el código del paquete instalado que el modo por píxel ya
estaba activo. El código final lo comprueba y lo conserva; no necesita escribir
esa propiedad. La corrección efectiva es la dirección de las luces y el ambiente.
El intento fallido y el diagnóstico quedan en los logs.


## Entrega y resultados finales

- Fuente Blender F3 **R05**, FBX estático y atlas PBR: 34.026 triángulos,
  una malla/material. Reapertura, UV/cobertura y reimportación FBX correctas.
- Unity: `Assets/Scenes/F4_FiguraAR_r02.unity` y
  `Assets/FiguraAR/F4_r02/Figure.prefab`. Mismos centrado, escala 0,045 y pose
  de anclaje F1; 26.063 vértices tras separación por UV/tangentes en importación.
- APK **0.2.0**, código 200, paquete `com.chupacabras.ar.figure`:
  `F4_figure_20261003_172936.apk`, **42,421,014 bytes**.
- SHA-256: `e5acda3e837a7054aff879d64de176599695ffc6c73b315b868c9cb2fd268104`.
- [Build, runtime y verificación APK](../../../unity/chupacabras/docs/evidencias/F4_20261003_172800/):
  32 aserciones existentes y ocho estados sintéticos correctos, misma instancia
  y escala, reloj narrativo cero. Sin Animator/Timeline/cámaras de cine en ejecución.
- BuildReport: cero errores y cero advertencias. Firma, permiso de cámara,
  ARM64, alineación ZIP/ELF de 16 KB comprobados. Ocho bibliotecas nativas.
  No acredita ejecución real en Android de páginas de 16 KB.
- `packed_assets.txt` contiene la nueva malla y mapas; no recursos cinematográficos.
  El tamaño de BuildReport incluye otras salidas y no es el tamaño de la APK.
- [Regresión F1](../../../unity/chupacabras/docs/evidencias/F4_regresion_F1_20261003/):
  escena original, 30.880 triángulos, tres composiciones y 32 checks correctos.
- [Vistas finales](../../../unity/chupacabras/docs/evidencias/F4_revision_visual_20261003/):
  frente, perfil, espalda, tres cuartos, inferior y rostro; fondos sintéticos claro
  y oscuro. Su encuadre iguala la escala ortográfica horizontal de Blender.

Juicio visual del agente: la reducción mantiene la silueta y apoyos de F2;
la piel muestra variación y relieve fino, con rugosidad diferenciada en ojos,
dientes y cresta. No se observan huecos del horneado ni uniones de atlas negras
en las vistas finales. Persisten planos anatómicos angulosos de la fuente F2:
el resultado sigue siendo estilizado y no se declara fotorrealismo ni aprobación
estética del usuario. Las luces de estudio Blender y luces móviles Unity son
diferentes; la comparación comprueba forma/mapas, no identidad de cada píxel.
Brillo real, fps, memoria total, seguimiento físico y aceptación visual siguen
pendientes de F5. **No se conectó ni instaló en ningún teléfono.**

[Resumen de seis vistas Unity](../previews/F3_chupacabras_superficie_r05/unity_seis_vistas.png)
y [comparación Blender/Unity](../previews/F3_chupacabras_superficie_r05/comparacion_blender_unity.png).
El verificador final volvió a pasar con las cámaras equivalentes. Su último
cambio solo ajusta capturas de Editor; no cambia los assets ni el código runtime
de la APK candidata. No se recompila por un cambio exclusivo de evidencia.

Se comprobaron sintaxis Python/shell y espacios finales de los cambios. No hay
linter ni suite general Blender configurados; se ejecutaron los verificadores
F3 y los checks existentes de Unity. Los ajustes previos se conservaron por
hash. Los temporales `.utmp` versionados que Unity regeneró se restauraron solo
si su estado inicial coincidía con HEAD, guardando copia de lo generado.
No se borraron fuentes ni se hicieron commits/push.
