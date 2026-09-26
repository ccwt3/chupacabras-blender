# Rigs y muestra de contacto — pasos 10 y 11

## Paso 10: oveja

Fuente: `scenes/07_oveja_r04.blend`, Sheep de Quaternius, CC0. Se conservan
307 vértices, 612 triángulos, 24 huesos, cuatro IK y los pesos normalizados
hasta cuatro influencias. No se reconstruye el recurso ni se cambia su licencia.

Nueva fuente: `scenes/10_rig_oveja.blend`; FBX/JSON homónimos en `exports/`.
La muestra independiente dura **8 segundos** (1–241 a 30 fps). No sustituye
la secuencia definitiva de 40 s ni la demo histórica de 35 s.

Se añade `WoolCompression`, localizada en 66 vértices de lana alrededor del
cuello; cabeza, piel y patas conservan su forma. Se ensayan reposo, pastoreo
con hocico a 18,5 mm del suelo, giro de cabeza, forcejeo a ambos lados, caída
lateral con compresión y pataleo. Las cuatro IK originales siguen editables;
FBX hornea sus resultados. La altura de apoyo se corrige en los 241 cuadros,
incluidas las transiciones. Estas poses prueban el rig; la actuación y los
pasos definitivos corresponden a 13–15.

Generación sin sobrescritura:

```bash
ALSOFT_DRIVERS=null blender -b --disable-autoexec -t 4 --python-exit-code 1 --python scripts/rig_oveja.py
ALSOFT_DRIVERS=null blender -b --disable-autoexec -t 4 --python-exit-code 1 --python scripts/verificar_rigs.py
```

`CHUPA_SUFFIX` permite generar una revisión nueva. La reapertura compara
vértices evaluados, apoyo, áreas de triángulos, duración y número de influencias.
La verificación Unity compara las deformaciones del FBX mediante Playables y
BakeMesh; además revisa la curva del blend shape y la independencia de la raíz
AR de referencia. Es una escena de revisión local, sin seguimiento físico.

Evidencia de trabajo en `docs/evidencias/2026-09-24_rigs/`. Resultados vigentes y
estado de aceptación se registran en `docs/estado.md` al cierre.

## Paso 11: chupacabras y agarre

Fuente original: `scenes/09_chupacabras_acabado.blend`, conservada intacta.
Se añaden **23 huesos FK**: raíz de locomoción, pelvis, columna, cuello,
cabeza, mandíbula, cinco segmentos de cola y tres huesos por extremidad.
La malla del cuerpo mezcla como máximo dos influencias; ojos, cabeza,
mandíbula y dientes inferiores tienen asignaciones específicas. Se conservan
10.550 triángulos, 17 mallas y los materiales/UV del acabado.

Dos muestras complementarias del mismo paso:

- `scenes/11_rig_chupacabras_poses.blend`: seis segundos, poses neutral,
  flexión de patas, zancada izquierda/derecha, espalda, cola y mandíbula.
  La oveja neutral al lado sirve de escala. No es un ciclo final de caminar.
- **`scenes/11_rigs_contacto_r03.blend`**: seis segundos, agarre establecido,
  pataleo de oveja, columna/cola y desplazamiento lateral conjunto de 1,5 m.
  La oveja queda de costado, apoyada en el suelo y con lana comprimida.
  No escenifica todavía el ataque, cierre inicial del agarre ni pasos de
  arrastre sincronizados. Esas actuaciones pertenecen a 14–15.

El agarre usa un vértice real de colmillo superior (175), uno de diente
inferior (36) y un vértice del cuello (174). El generador resuelve la inclinación
del cuello y la apertura mandibular sobre la superficie deformada mediante
búsqueda acotada; hornea el resultado cada fotograma. No hay restricciones
circulares ni solver en ejecución móvil. `SequenceRoot` contiene ambos rigs;
la raíz AR de Unity es un padre independiente y se ensaya también con una
pose/escala exterior distinta de identidad.

**Corrección R03:** la primera prueba numérica comparaba vértices y marcadores
correctamente, pero una prueba adicional contra triángulos importados detectó
5,31 mm de separación. Los polígonos de la oveja (282 quads, 42 triángulos y dos
pentágonos) se dividían de forma distinta al deformarse/exportarse. R03 fija las
diagonales en la copia de la oveja antes de resolver el contacto: mismos
307 vértices, 612 triángulos y shape key. Este orden debe conservarse al producir
las actuaciones finales. La primera fuente, FBX, clip y resultados fallidos
quedan como diagnóstico; no usar su contacto como entrega aceptada.

La operación estándar de triangulación en modo edición (R02) descartaba una
cara. R03 reconstruye las 612 caras desde los índices de loop y conserva
vértices, pesos, UV, materiales y compresión. La oveja original tiene una arista
con más de dos caras; su teselación conserva ese solapamiento heredado,
representado en tres aristas, sin bordes abiertos ni vértices sueltos. No se
afirma que el recurso sea manifold. Las fuentes anteriores siguen intactas.

```bash
CHUPA_SUFFIX=_r04 ALSOFT_DRIVERS=null blender -b --disable-autoexec -t 4 --python-exit-code 1 --python scripts/rig_contacto.py
CHUPA_RIG=11_rigs_contacto_r04 ALSOFT_DRIVERS=null blender -b --disable-autoexec -t 4 --python-exit-code 1 --python scripts/verificar_rigs.py
CHUPA_RIG=11_rigs_contacto_r04 ALSOFT_DRIVERS=null blender -b --disable-autoexec -t 4 --python-exit-code 1 --python scripts/preview_rigs.py
ffmpeg -v error -n -framerate 15 -i previews/11_rigs_contacto_r04_frames/%04d.png -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart previews/11_rigs_contacto_r04.mp4
```

El verificador de Blender genera además `exports/<nombre>_surface.json` desde
una reapertura independiente. Unity compara esos puntos con dientes realmente
deformados y mide su distancia a los triángulos de la lana importada. No basta
que coincidan dos empties. Las capturas fuerzan recálculo de matrices de skin
por render para evitar repetir una pose anterior. Iluminación y piso de las
escenas 10–11 sirven solo para inspección; no completan el paso 12.

En Unity: FBX, JSON, materiales y prefabs en `Assets/Rigs/`; escenas homónimas
en `Assets/Scenes/`. `RigPreview` reproduce la duración propia del clip mediante
un reloj único; no modifica `SequencePreview` ni su contrato de 40 segundos.
`RigBuild` configura y verifica con Unity **6000.3.22f1**. No se necesita APK
nueva ni acceso al teléfono para estas aceptaciones de rig/importación.
