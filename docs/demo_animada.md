> **Demo independiente conservada.** Las referencias al corto definitivo de
> 40 s describen el alcance anterior, sustituido por el [plan de figura AR](plan_secuencia.md).
> Esta demo no es la nueva entrega. Ver [estado](estado.md).

# Demo animada: ataque y arrastre

Se añadió una animación de **35 segundos** a los modelos del borrador estático, conservando intacto `scenes/demo_lowpoly.blend`. Es una prueba sencilla de actuación y tiempos; no ejecuta la producción definitiva ni cambia sus 40 segundos acordados.

| Tiempo | Acción |
| --- | --- |
| 0–15 s | La oveja mueve la cabeza pastando; el chupacabras merodea, se aproxima y prepara el salto. |
| 15–16 s | Salto hacia la oveja. |
| 16–18 s | Impacto, giro y caída de la oveja; el atacante baja la cabeza para sujetarla. |
| 18–33 s | El chupacabras retrocede arrastrándola por el cuello, con pasos simples y forcejeo de patas. |
| 33–35 s | Cierre en la última posición. |

Los movimientos usan pivotes y piezas rígidas con keyframes, sin rig deformable, simulaciones ni detalle fino. El punto del cuello sigue el punto de mordida para conservar el agarre durante el arrastre. La cámara permanece fija para facilitar la revisión. No se añadió audio, polvo, Unity ni AR. La demo termina con los personajes dentro del escenario; no intenta reproducir la salida de campo del corto final.

## Archivos y reproducción

- `scenes/demo_ataque_arrastre.blend`: escena animada editable, 24 fps, fotogramas 1–840.
- `previews/demo_ataque_arrastre.mp4`: previsualización ligera Workbench, 640 × 480, 12 fps, duración de 35 s. Su iluminación es de revisión; el `.blend` conserva las luces nocturnas y Cycles.
- `scripts/animar_demo.py`: añade animación al borrador original y guarda una nueva versión.
- `scripts/preview_animacion.py`: genera 420 imágenes de previsualización, tomando un fotograma de cada dos de la escena.

En Blender, abrir el archivo animado y pulsar **Espacio** con el cursor sobre la vista 3D. La línea de tiempo contiene marcadores de pastoreo, ataque, impacto, arrastre y cierre. Volver al fotograma 1 para reproducir desde el inicio.

## Regeneración

Desde la carpeta del proyecto:

```bash
blender -b -t 6 --python-exit-code 1 --python scripts/animar_demo.py
blender -b scenes/demo_ataque_arrastre.blend -t 6 --python-exit-code 1 --python scripts/preview_animacion.py
ffmpeg -n -framerate 12 -i previews/animacion_frames/%04d.png -c:v libx264 -crf 22 -pix_fmt yuv420p -movflags +faststart previews/demo_ataque_arrastre.mp4
```

Los generadores añaden sufijos si ya existen las salidas; ajustar las rutas a la versión recién generada. FFmpeg usa `-n` para no sobrescribir videos existentes.

## Verificación

El generador completó las comprobaciones de duración de 35 s, ataque en el segundo 15 y coincidencia entre boca y cuello en seis momentos del arrastre, incluyendo el final. La escena se reabrió correctamente para renderizar una vista de revisión del arrastre.

Se renderizaron las 420 imágenes y se inspeccionaron inicio, salto, caída, arrastre y cierre. FFprobe confirmó video H.264, 640 × 480, 12 fps, 420 fotogramas y duración exacta de 35 segundos. No hay suite de tests ni linter configurados en este proyecto.
