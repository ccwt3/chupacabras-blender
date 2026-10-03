# Revisión demacrada: rig y aspecto, pasos 11–12

Continuación del 2 de octubre de 2026 (logs también fechados 3 de octubre UTC).
Fuente: `scenes/09_chupacabras_demacrado_r02.blend`. Esta sesión retoma 11 y
12; no inicia actuación 13–14. Los hitos anteriores se conservan.

## Rig y contacto

`11_rigs_contacto_demacrado_r01` contiene 23 huesos, 30.880 triángulos del
chupacabras y 612 de la oveja. Se reasignan pesos por posición sobre la nueva
malla; hombros, pelvis y nacimiento de cola siguen las articulaciones revisadas.
Cabeza, cuencas y ojos quedan rígidos sobre Head; mandíbula y dientes inferiores
siguen Jaw. Se comprueba normalización y un máximo de dos influencias por
vértice del chupacabras. Los materiales y la geometría de la fuente se conservan.

Los contactos se buscan otra vez sobre la geometría: vértice superior **174**,
inferior **35**, cuello **174**. No se copian los antiguos 175/36. La oveja
conserva las 612 caras trianguladas antes de deformar y resolver el agarre,
incluido el solapamiento heredado de Quaternius. El contacto se hornea en
Blender; no se añade un solver al móvil.

Dos muestras independientes de seis segundos, 30 fps, claves 1–181:

- `scenes/11_rigs_contacto_demacrado_r01.blend`: agarre ya establecido,
  pataleo y desplazamiento conjunto; no son pasos de arrastre finales.
- `scenes/11_rig_chupacabras_poses_demacrado_r01.blend`: neutral, flexión,
  zancadas alternas, columna/cola y mandíbula abierta.

FBX/JSON homónimos en `exports/`, contactos de superficie en `_surface.json`.
Vídeo de contacto: `previews/11_rigs_contacto_demacrado_r01.mp4`, seis segundos,
960 × 540, 15 fps. PNG de inicio/medio/final y detalle de boca en `previews/`.
Los 90 PNG intermedios son regenerables y se excluyen de Git.

Reapertura Blender: 181 cuadros por muestra, sin discrepancias contra la
referencia guardada, áreas triangulares positivas, pesos normalizados y apoyo.
Contacto máximo 0,001016 mm; distancia a superficie 0,001014 mm. Salto máximo
entre muestras de contacto 19,74 mm, inferior al umbral existente de 30 mm.
Estos valores son pruebas geométricas, no precisión física de AR.
Se compararon directamente las 18 mallas en reposo contra el acabado R02
(error cero) y caras, coordenadas y shape keys de oveja contra R03 (idénticas).
Comprobación reproducible: `docs/evidencias/2026-10-02_rigs_demacrado/comprobar_fuentes.py`.

Unity importa en `Assets/Rigs/`, con escenas homónimas en `Assets/Scenes/`.
El verificador utiliza el número de triángulos documentado para cada entrega;
conserva 11.162 como expectativa de los rigs anteriores. No se aumenta una
tolerancia para hacer pasar la malla nueva. Contacto Unity: 181 cuadros,
259.735 puntos comparados, error máximo de vértice 0,02780 mm y contacto con
triángulos de lana 0,001396 mm. Raíz AR comprobada también con pose exterior
distinta de identidad. Controles Unity: 181 cuadros, 222.811 puntos, error
máximo 0,009343 mm. Resultados completos en las evidencias de ambas raíces.

## Reproducción

Desde la raíz Blender, usar sufijos nuevos; los generadores rechazan entregas
existentes:

```bash
CHUPA_MODEL=09_chupacabras_demacrado_r02 CHUPA_SUFFIX=_demacrado_r02 blender -b -t 4 --python-exit-code 1 --python scripts/rig_contacto.py
CHUPA_RIG=11_rigs_contacto_demacrado_r02 blender -b -t 4 --python-exit-code 1 --python scripts/verificar_rigs.py
CHUPA_CONTACT_SOURCE=11_rigs_contacto_demacrado_r02 CHUPA_SUFFIX=_demacrado_r02 blender -b -t 4 --python-exit-code 1 --python scripts/rig_chupacabras_poses.py
CHUPA_RIG=11_rig_chupacabras_poses_demacrado_r02 blender -b -t 4 --python-exit-code 1 --python scripts/verificar_rigs.py
CHUPA_RIG=11_rigs_contacto_demacrado_r02 blender -b -t 4 --python-exit-code 1 --python scripts/preview_rigs.py
ffmpeg -v error -n -framerate 15 -i previews/11_rigs_contacto_demacrado_r02_frames/%04d.png -c:v libx264 -crf 20 -pix_fmt yuv420p previews/11_rigs_contacto_demacrado_r02.mp4
```

Copiar los FBX/JSON y `_surface.json` a `Assets/Rigs/` de Unity; ejecutar
`RigBuild.Configure` con `CHUPA_RIG` y `CHUPA_RIG_EVIDENCE` nuevos usando
exclusivamente `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`.
`RigBuild.Verify` reabre la escena guardada. El modo por defecto de todos los
scripts conserva sus fuentes históricas.

## Aspecto preparado en Unity

Entrega vigente: `Assets/Scenes/12_AppearanceAR_demacrado_r02.unity` y
`Assets/Appearance12DemacradoR02/AppearanceStudy.prefab`, en la raíz Unity.
Se sustituye la criatura en figura exterior, pastoreo y contacto, preservando
la colocación centrada de R05. Materiales propios mantienen la paleta seca de
la fuente y las cuencas oscuras. El primer intento conservó la capa de cine
del prefab y falló la comprobación de capa exterior; se corrigió la sustitución
para heredar la capa del objeto reemplazado. R01 fallida queda como diagnóstico.

R02 pasa tres planos, tres perspectivas, geometría/capas, centrado de figura,
panel lateral fuera del dibujo y cámara interna independiente (mismos píxeles
antes/después de mover la raíz AR). Play Mode sintético pasa adquisición,
pérdida, pausa y recuperación. Las capturas fueron inspeccionadas; no son prueba
de brillo ni rendimiento en el teléfono.

APK nueva: `builds/android/12_appearance_20261003_012410.apk`, **0.0.15**,
41.400.738 bytes, SHA-256
`b10e73187f762d6691ecea2319fcb8f1676df37283531bee41d4bafaae5ae4a5`.
BuildReport Unity 6000.3.22f1: 0 errores/0 advertencias. Firma, CAMERA, ARM64
y ocho bibliotecas/empaquetado alineados a 16 KB comprobados. Esto no demuestra
ejecución en un sistema Android con páginas de 16 KB.

La APK 0.0.14 anterior y el marcador carta conservan sus hashes.
**M#[6] pendiente**: revisión real de ojos, costillas, espinas, dientes, lana y
brillo en G20. Guía y comandos:
[pasos11_12_demacrado.md](/home/cacawatin/code/unity/chupacabras/docs/pasos11_12_demacrado.md).
M#[4] conserva su cierre histórico; M#[5] permanece reservada para el paso 20.

## Límites de cierre

Producción definitiva: 40 s; demo independiente: 35 s. Estas muestras de seis
segundos solo validan el rig. No resuelven locomoción final, cámara continua ni
salto/ataque. No sustituyen una revisión del aspecto en el G20. Consultar
`estado.md` para la APK, acción manual y punto vigente de reanudación.
