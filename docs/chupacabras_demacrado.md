# Chupacabras demacrado — revisión de pasos 8 y 9

2 de octubre de 2026, México (los logs finales usan también 3 de octubre UTC).

El usuario pidió conservar la forma general y reducir el aspecto fornido/de
jabalí, acercándolo a las referencias iniciales: más demacrado, esquelético y
tenebroso, permitiendo mayor cantidad de polígonos. Esta corrección reabre
8–9 y ocupa los dos pasos principales de esta sesión. **No se ejecutaron 13–14.**
No se encontraron archivos AGENTS.md en las raíces ni ancestros consultados;
se aplicaron las instrucciones proporcionadas en la conversación.

## Entregas

- Forma: `scenes/08_chupacabras_demacrado_r01.blend`.
- Acabado vigente: **`scenes/09_chupacabras_demacrado_r02.blend`**.
- FBX y JSON homónimos en `exports/`; cuatro vistas por versión en `previews/`.
- Contextos vigentes de ambas fuentes: **`_contexto_r03.blend` / `.fbx`**.
- Giro de inspección: `previews/09_chupacabras_demacrado_r02_giro.mp4`,
  H.264, 960×720, 12 fps, 120 cuadros, **10 segundos**. Es una inspección del
  modelo, no otro corto ni la animación definitiva.
- Capturas importadas: `previews/09_chupacabras_demacrado_r02_unity_*.png`.
- Unity: `Assets/Creature/<nombre>/Chupacabras.prefab`, materiales, FBX/JSON y
  escenas `Assets/Scenes/<nombre>_contexto_r03.unity`.
- Evidencia Blender: `docs/evidencias/2026-10-02_demacrado/`.
- Evidencia Unity: `docs/evidencias/2026-10-02_demacrado_{forma_r03,acabado,fullres}/`.

El acabado R01, contextos R02 y búsquedas de cámara quedan conservados como
iteraciones. R01 ya adelgaza el cuerpo; R02 añade cuencas oscuras y ojos más
recogidos. No se reemplazaron fuentes, APK, prefabs ni escenas de hitos anteriores.

## Qué cambió y por qué

Se reduce el tórax, se eleva/hunde el abdomen, se estrechan pelvis y cuello y se
adelgazan brazos, muslos, cola y dedos. Codos, corvejones, crestas ilíacas y
escápulas sobresalen de la piel. Las costillas se fusionan con el tórax mediante
remallado: no son huesos flotantes ni una textura dependiente del renderizador.
Se conserva la postura cuadrúpeda baja, arco del lomo, cresta alta, manos,
garras, cola y mandíbula separada.

El rostro se estrecha, se hunden las mejillas y se añaden cuencas oscuras,
con ojos amarillos más pequeños bajo las cejas. Se reduce la anchura del manto
de mechones para que no reconstruya el volumen descartado. Materiales sólidos
compartidos, UV 0–1, sin pelo simulado, nuevas dependencias ni texturas externas.

| Medida | Anterior | Revisión |
| --- | ---: | ---: |
| Volumen de la malla corporal cerrada | 2,839689 m³ | 1,271362 m³ |
| Triángulos, acabado completo | 10.550 | 30.880 |
| Mallas / materiales, acabado | 17 / 6 | 18 / 6 |

La reducción de volumen es **55,23 %**. Incluye tronco, extremidades y cola de
`Chupa_Body`, no cabeza/espinas/dientes. Es una comparación geométrica, no una
estimación de peso ni rendimiento. Se acepta más geometría por instrucción del
usuario; 40.000 es un tope local de generación, **no presupuesto móvil medido**.
Forma neutral: 28.240 triángulos/12 mallas.

## Encuadre y aceptación

La cámara antigua `(0,-6,2.4)` dejaba ver parte de la oveja con el nuevo cuerpo:
solo 5/114 cuadros completamente ocultos. El fallo se conserva en la evidencia
`demacrado_forma` de Unity. La búsqueda de posición identificó una solución con
cámara Blender **`(0.3,-4,2.8)`**, mirando a `(0,0,0.95)`; Unity `(0.3,2.8,-4)`.
Los contextos R03 acercan esa cámara interna. No se engordó al personaje, no se
ocultó ni redujo la oveja, no se añadió polvo/pantallas y no se animó la cámara AR.

Este es un **contexto de volumen heredado del bloqueo**, no la actuación de
13–15. Conserva sus cortes históricos, oveja rígida elevada durante arrastre y
puntos de contacto provisionales. El encuadre cercano demuestra ocultamiento;
la anticipación continua y entrada lateral del ataque siguen pendientes en
13–14. No presentar el contexto como corto final ni como rig aprobado.

## Verificaciones

- Blender 5.2.2 LTS: reapertura independiente de forma R01 y acabados R01/R02;
  mallas cerradas/manifold, caras no degeneradas, UV finitos y escala métrica.
  Fuentes históricas 08 R03/09 y ambas demos también pasan sus verificadores.
- Ambos contextos: 1.200 cuadros sin solapamientos AABB con granero; 565
  muestras de referencias de contacto, máximo 0,0000009903 m en Blender.
- Unity **6000.3.22f1**, reapertura de escenas guardadas: duración 40 s,
  geometría/materiales/UV/ejes y escala coincidentes. Error máximo de límites
  0,0000004299 m; referencias de contacto 0,0000023961 m.
- Forma y acabado a 320×180: 150/150 cuadros de criatura oculta (15–20 s),
  114/114 de oveja oculta (21,2–25 s), 30/30 vacíos (39–40 s). Los ojos del
  acabado ocupan solo **1 píxel** en la vista lejana de revisión: lectura móvil
  por revalidar en 12; no extrapolar que se verán bien en el teléfono.
- `LeanCameraCheck.Verify`: 264 cuadros a **960×540**, cero píxeles visibles
  de los objetivos ocultos. Control positivo: al retirar únicamente el
  oclusor en la prueba, la oveja produce 12.809 píxeles visibles. Esto descarta
  pasar por haber desactivado la oveja o haberla sacado del encuadre.
- 32 aserciones existentes de seguimiento correctas en cada verificación de
  importación; C# compilado por el Editor exacto, Python compilado y
  clang-format correcto. No hay suite/linter Python configurado.
- FFprobe confirma el giro de 10 s. Se inspeccionaron vistas Blender, rostro,
  tres cuartos y ataque Unity. Los PNG intermedios del giro quedan en disco,
  excluidos de Git por ser regenerables; MP4, vistas y scripts se versionan.
- SHA-256: **844 archivos históricos** y tres configuraciones ajenas de Unity
  sin cambios. No se conectó ni instaló nada en el teléfono; no se generó APK.

Avisos del Editor: cierre de PlayableGraph, SDL/Vulkan y resolución del SDK
.NET en los logs; no impidieron compilar ni pasar las verificaciones finales.
El fallo de aceptación de la primera cámara sí fue real y queda separado.

## Reproducción

Desde la raíz Blender; sufijos nuevos evitan sobrescrituras:

```bash
CHUPA_SUFFIX=_r03 blender -b -t 4 --python-exit-code 1 --python scripts/chupacabras_demacrado.py -- 8
CHUPA_SUFFIX=_r03 blender -b -t 4 --python-exit-code 1 --python scripts/chupacabras_demacrado.py -- 9
CHUPA_MODEL=09_chupacabras_demacrado_r03 blender -b -t 4 --python-exit-code 1 --python scripts/verificar_chupacabras.py
CHUPA_MODEL=09_chupacabras_demacrado_r03 CHUPA_CONTEXT_SUFFIX=_contexto_r03 CHUPA_ATTACK_CAMERA=0.3,-4,2.8 blender -b -t 4 --python-exit-code 1 --python scripts/chupacabras_contexto.py
CHUPA_PREVIEW_SUFFIX=_verificacion blender -b -t 4 --python-exit-code 1 --python scripts/preview_demacrado.py
ffmpeg -v error -n -framerate 12 -i previews/09_chupacabras_demacrado_r02_verificacion_giro_frames/%04d.png -c:v libx264 -crf 20 -pix_fmt yuv420p previews/09_chupacabras_demacrado_r02_verificacion_giro.mp4
```

Para reproducir exactamente el acabado R02, usar `CHUPA_FORM=08_chupacabras_demacrado_r01`
y un sufijo de salida nuevo. La fuente R01 de forma se conserva intacta.
Para Unity, copiar el FBX estático, su JSON y el FBX de contexto a un directorio
nuevo en `Assets/Creature/<nombre>/`, como indica `docs/chupacabras_modelo.md`.
Ejecutar `CreatureBuild.Configure` con `CHUPA_MODEL`,
`CHUPA_CONTEXT_SUFFIX=_contexto_r03` y `CHUPA_CREATURE_EVIDENCE` nuevos,
siempre con la ruta exacta del Editor acordado. Para reabrir las escenas actuales,
usar `CreatureBuild.Verify`; la prueba adicional actual es `LeanCameraCheck.Verify`.
`LeanCameraCheck.Run` reproduce la búsqueda diagnóstica sobre el contexto R02;
sus CSV son diagnósticos, no cambian escenas guardadas.

## Continuidad y límites

8–9 revisados técnicamente, sin atribuir aprobación visual posterior al usuario.
Antes de 13–14 hay que **reabrir 11** para asignar/verificar pesos y contacto con
la topología nueva, y **12** para llevarla a los materiales/composición R05.
La oveja y su triangulación R03 no cambian. El rig anterior no debe copiarse
por índices de vértice: cuerpo, rostro y nueva malla orbital tienen otra topología.

M#[4] permanece resuelta para 0.0.14/modelo anterior. La nueva estética no se ha
probado físicamente ni tiene APK propia. Conservar seguimiento, colocación
centrada sobre el símbolo y panel lateral. Preparar cualquier futura prueba
antes de solicitar intervención; M#[5] sigue reservada al paso 20. Ninguna
acción manual necesaria pendiente ahora.

## Referencias

Referencias visuales aportadas por el usuario. (s. f.). *Chupacabras 1–3*
[Imágenes; autoría/publicación no identificadas]. Archivos `references/chupacabras1.jpg`,
`chupacabras2.jpg` y `chupacabras3.jpg`. Inspeccionadas, no usadas como texturas.

Quaternius. (s. f.). *Farm animals* [Modelos 3D, CC0 1.0].
https://quaternius.com/packs/farmanimals.html
