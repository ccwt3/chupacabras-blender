# Escenario para la ventana cinematográfica — paso 6

Se construye un granero de tablas envejecidas con puertas, travesaños, techo y
juntas; suelo seco con manchas geométricas, hierba dispersa, piedras, bosque en
silueta y luna facetada. Los materiales básicos se reconstruyen en URP. No hay
texturas, pelo, partículas ni luces adicionales en el recurso estático. El
acabado e iluminación definitivos siguen en el paso 12.

## Archivos y reproducción

- `scenes/06_escenario.blend`: fuente de la geometría estática, en metros.
- `exports/06_escenario.fbx` y `.json`: geometría, paleta, límites y conteos.
- `scenes/06_escenario_contexto.blend` y FBX homónimo: revisión del bloqueo para
  comprobar el escenario. Sus animales siguen siendo formas provisionales.
- Unity: `Assets/Environment/` y `Assets/Scenes/06_Environment.unity`.
- Generador: `scripts/escenario.py`; reapertura: `scripts/verificar_escenario.py`.

```bash
CHUPA_SUFFIX=_r02 blender -b -t 4 --python-exit-code 1 --python scripts/escenario.py
blender -b -t 4 --python-exit-code 1 --python scripts/verificar_escenario.py
```

El generador rechaza sobrescribir entregas. Para importar otra revisión en Unity,
adaptar las rutas explícitas de `EnvironmentBuild`; conservar escenas anteriores.
`EnvironmentBuild.Verify` reabre la escena sin guardarla; definir
`CHUPA_ENV_EVIDENCE` a una carpeta nueva antes de repetir las capturas con el
Editor exacto 6000.3.22f1. No usar otra versión del Editor.

## Corrección de distribución

La comprobación inicial encontró intersecciones entre el granero del bloqueo y
los animales al girar, aproximadamente desde 30.5 s. En el nuevo contexto se
desplazan **3.2 m hacia el fondo** el granero y las claves de acecho anteriores a
20 s. Se reduce la profundidad del edificio para mantener separación con el
acecho. Cámaras, salto desde 20 s, contacto, arrastre y salida conservan sus
curvas. No se modifica R04 ni ninguna demo. Esta corrección pertenece a los
recorridos/oclusiones del paso 6, no al refinamiento de actuación.

Se comprueba cada caja de pieza del granero contra las cajas de los personajes
evaluadas en los 1200 fotogramas. La vegetación y piedras se colocan fuera de la
unión del recorrido muestreado a 10 Hz con márgenes de 0.65/0.8 m. Los árboles
quedan al fondo. Manchas de suelo son planas y no obstaculizan el recorrido.

## Costo y límites

**2915 triángulos, 10 mallas y 10 materiales compartidos**, una malla por material.
Este conteo corresponde solo al escenario estático. No es una medición de draw
calls ni de rendimiento en Android. La RenderTexture de revisión sigue en
960 × 540; el presupuesto final requiere medición física en el G20.

La fuente se reabre con Blender 5.2.2 LTS. El contexto conserva 40 s y contacto
en 565 muestras desde el aterrizaje (error máximo 9.83e-7 m). Las pruebas visuales
Unity y su resultado final quedan en `docs/estado.md` y en
`docs/evidencias/2026-09-24_escenario/` de la raíz Unity.

Cierre Unity: pasan las 150 máscaras de criatura oculta, 114 de oveja oculta y
30 del campo vacío; ojo visible durante acecho y oveja antes/después. Capturas
inspeccionadas, incluida la ventana. Pasan también las 32 aserciones existentes
de seguimiento. La legibilidad aquí es de render, no una evaluación física móvil.
