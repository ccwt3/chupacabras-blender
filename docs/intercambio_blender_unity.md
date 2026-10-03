> **Referencia histórica del alcance anterior.** Sus resultados se conservan;
> sus próximos pasos y requisitos cinematográficos no son tareas vigentes.
> Consultar el [plan de figura AR](plan_secuencia.md) y el [estado](estado.md).

# Paso 4: contrato de intercambio comprobable

Sesión del 24 de septiembre de 2026. Fuente: `scenes/04_intercambio.blend`;
exportación explícita: `exports/04_intercambio.fbx`. Las demos anteriores se
conservan. La fuente contiene la restricción COPY_LOCATION; el FBX guarda su
resultado horneado. No se requiere Blender instalado para reproducir la app.

## Ajustes y reproducción

- Blender 5.2.2 LTS, metros, escala de unidad 1, 30 fps, fotogramas 1–1201.
  El 1201 es la clave de límite a 40 s; una captura usa 1–1200.
- FBX: -Z hacia delante, Y arriba, unidades del archivo, escala 1,
  `FBX_SCALE_UNITS`, sin `bake_space_transform`, sin leaf bones, sin aplicar
  modificadores de malla para conservar shape keys. Horneado cada fotograma,
  simplificación 0, sin exportar todas las acciones ni las pistas NLA.
- Unity exclusivo 6000.3.22f1: Generic, conversión de ejes horneada, unidades
  del archivo, escala 1, importación de cámara y blend shapes, sin compresión
  de animación ni loop automático. Equivalencia comprobada: Blender (x,y,z)
  → Unity (x,z,y).
- Un Animator en la raíz común evalúa el clip completo; root motion desactivado.
  La raíz de presentación del marcador permanece fuera del clip. El reproductor
  provisional usa Playables; no sustituye la Timeline de producción del paso 17.
- Compresión de lana: shape key `WoolCompression`, importada como blend shape.
  Su curva y sus vértices deformados se comparan con Blender. Este es el método
  elegido para adaptar la oveja en el paso 10.
- Cámara interna importada, lente 40 mm y sensor 36 mm; encuadre horizontal
  16:9 en una RenderTexture de 960 × 540 para revisión. Capa 8 para ficción;
  capa 0 para ventana/marcador de referencia y cámara exterior.
- Ventana provisional 240 × 135 mm: 2.4 veces el lado de detección de 100 mm.
  La imagen de referencia de 512 px se muestra a 320 mm para que sus 160 px
  entre esquinas representen 100 mm. Esta escena no abre la cámara del móvil.

Regeneración: `blender -b -t 4 --python-exit-code 1 --python scripts/intercambio.py`.
Si las salidas existen, el generador se detiene; usar `CHUPA_SUFFIX=_r02` para
conservarlas. `exports/04_intercambio.json` registra 41 muestras independientes
de Blender con posiciones de contacto, vértices deformados y peso de shape key.

En la raíz Unity, `ExchangeBuild.Verify` compara los datos y conserva una escena
nueva `Assets/Scenes/04_Exchange.unity`; `ExchangeBuild.Capture` genera las vistas
con GPU. Usar siempre la ruta exacta de Unity fijada en el estado general. Al repetir, definir
`CHUPA_EXCHANGE_EVIDENCE` a una carpeta nueva: las capturas existentes se conservan.
`bash scripts/verify_sequence.sh` lo hace automáticamente.

## Verificación

La primera importación confirmó clip de 40 s, cubo de 1 m y blend shape presente.
La comparación numérica inicial dio error máximo de contacto 1.34e-7 m,
vértices 3.46e-7 m y peso 1.10e-7. Se corrigió un problema del generador de escena:
el importador no crea necesariamente Animator en la raíz común, por lo que se
crea allí explícitamente. Los informes y logs, incluidos los intentos iniciales,
se conservan en `docs/evidencias/2026-09-24_intercambio/` de Unity.

RenderTexture y reproducción verificadas: el grafo de ejecución conserva
el contacto con error máximo 1.79e-7 m. Una imagen de cuatro colores confirma
las cuatro esquinas UV; la proyección frontal conserva 16:9. Las capturas se
inspeccionaron y las 32 aserciones existentes de seguimiento pasaron.
La reapertura independiente de la fuente comprobó contacto en sus 1201 claves.
El cierre se registra en `estado.md` y en los informes finales. Nada de este paso constituye una nueva prueba física
ni permite atribuir rendimiento móvil a los resultados del Editor.

## Referencias

Blender Foundation. (s. f.). *Export scene operators*. Blender Python API.
https://docs.blender.org/api/3.0/bpy.ops.export_scene.html

Unity Technologies. (s. f.). *ModelImporter*. Unity 6000.3 scripting reference.
https://docs.unity.com/en-us/engine/6000.3/script-reference/unityeditor/modelimporter

Las opciones se contrastaron además con el operador y el importador realmente
instalados; la prueba de archivos exportados prevalece sobre las descripciones.
