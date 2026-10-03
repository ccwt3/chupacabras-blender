> **Referencia histórica del alcance anterior.** Sus resultados se conservan;
> sus próximos pasos y requisitos cinematográficos no son tareas vigentes.
> Consultar el [plan de figura AR](plan_secuencia.md) y el [estado](estado.md).

# Paso 5: bloqueo de 40 segundos

El bloqueo usa formas provisionales para fijar espacio, tiempos y cámaras.
No es el modelado del chupacabras ni la oveja definitiva reutilizada. La selección
y licencia de esa oveja siguen en el paso 7. No hay sonido, polvo ni actuación
final: corresponden a pasos posteriores. Las demos de 35 segundos y estática
permanecen intactas.

## Entrega de esta revisión

- Fuente vigente: `scenes/05_blocking_r04.blend`.
- Exportación: `exports/05_blocking_r04.fbx` y referencia numérica `.json`.
- Unity: `Assets/Scenes/05_Blocking_r04.unity`, en la raíz AR acordada.
- Previsualización: `previews/05_blocking_r04.mp4`, renderizada desde Unity.
- Generador: `scripts/blocking.py`, con funciones de `scripts/intercambio.py`.

Las fuentes y escenas de revisiones inicial, R02 y R03 se conservan.
R03 reduce el cuerpo
expuesto durante el acecho, conserva un ojo visible y mejora la lectura de
cabeza/patas y la masa del granero. R04 añade caída de costado y movimiento
sencillo de patas durante el arrastre, manteniendo el cuello en la boca mediante
compensación de la transformación. No se reutilizan como arte definitivo.

## Cronología y espacio

| Tiempo | Bloqueo |
| --- | --- |
| 0–15 s | Oveja mueve la cabeza pastando; criatura asoma detrás del granero. |
| 15–20 s | La criatura y ojos quedan detrás de geometría opaca. |
| 20 s | Corte al plano bajo; el salto comienza detrás de la cámara interna. |
| 20–21.2 s | Trayectoria por encima de la cámara y descenso delante de ella. |
| 21.2–25 s | El volumen de hombros tapa a la oveja sin polvo ni desactivar su malla. |
| 25–31 s | Corte a tres cuartos, apertura y retroceso hacia la izquierda. |
| 31–39 s | Giro amplio y salida derecha; ambos comparten la trayectoria del agarre. |
| 39–40 s | Campo vacío. |
| 40 s | Reinicio directo del reproductor provisional a 0 s. |

Metros en Blender: raíz del par en (0,-1,0) al contacto, (-2.8,-0.8,0)
a 29 s, (-3.5,0.2,0) a 31 s, (-2.3,1.2,0) a 33 s y (14,1.2,0)
a 39 s. El eje vertical es Z en Blender/Y en Unity. La oveja tiene un
punto de cuello a la misma posición que la boca desde el aterrizaje.
La actuación de peso, patas y mordida se refinará en 13–15; no se afirma
que este bloqueo ya cumpla la aceptación de animación final.

La cámara de calma está en (0,-12,4), con lente 35 mm; la de ataque,
en (0,-6,1.1), 32 mm. A 25 s pasa a (7,-7,5), 35 mm, y termina su
apertura a (5,-11,6) a 28 s. Sensor horizontal de 36 mm y ventana 16:9.
La raíz externa del marcador no recibe ninguna de estas curvas.

### Revisión para la actuación final

Después de revisar el video de referencia, el usuario señaló dos rasgos del
bloqueo que se sienten bruscos: el salto repentino de cámara y la entrada de
la criatura desde el eje del lente. R04 conserva ambas decisiones como una
referencia provisional de planificación, no como una indicación obligatoria
para la actuación final. En las escenas 13–14, anticipar el movimiento de la
cámara interna desde antes de los 20 s y usar una entrada desde el lateral o
detrás del granero, dirigiendo el salto hacia la oveja. Mantener el beat a los
20 s, la trayectoria cerca/por encima de la cámara interna, el ocultamiento y
la cámara AR independiente. Ajustar poses y cámara en hitos nuevos; no editar
este archivo histórico.

## Comprobación y límites

Unity evalúa el FBX mediante el mismo grafo Playables usado al reproducir.
Se comparan cámara y trayectoria con los datos Blender, y contacto en 564
instantes a 30 Hz. El clip importado mide 40.0000038 s por representación
float; el reloj utiliza el límite exacto de 40 s, sin sumar un fotograma.
La Timeline definitiva y sus pruebas completas siguen en el paso 17.

Máscaras de render reales a 320 × 180 comprueban todos los fotogramas de
15–20 s, 21.2–25 s y 39–40 s: no aparece ningún píxel blanco de los modelos
que deben estar ocultos. Se exige además que la oveja sea visible antes y
después, y que haya píxeles de ojo durante el acecho. Las máscaras usan la
profundidad real del render, sin partículas ni cambios de visibilidad.

Tres vistas exteriores cambian la perspectiva de la superficie y dejan
idéntica, byte a byte, la imagen interna en 23 s. La prueba de cuatro colores
del paso 4 verifica las cuatro esquinas UV y proporción 16:9. Esto comprueba
la separación de cámaras; no es una prueba física de movimiento del teléfono.

Resultados, capturas y logs en Unity: `docs/evidencias/2026-09-24_blocking_r04/`.
La resolución de revisión 960 × 540 no es presupuesto móvil aprobado.
No se ha instalado esta revisión ni se declara nuevo rendimiento G20/S23.
La conexión de la secuencia al seguimiento real permanece en el paso 20.

## Reproducción

Abrir `05_Blocking_r04.unity` con Unity 6000.3.22f1 y pulsar Play. Se observa
el marcador de referencia y la ventana con geometría animada; no se abre
la cámara física. Abrir el `.blend` para editar las formas y curvas fuente.

Para crear otra revisión sin sobrescribir:

```bash
CHUPA_SUFFIX=_r05 blender -b -t 4 --python-exit-code 1 --python scripts/blocking.py
```

Copiar la exportación nueva a `Assets/Exchange/`, ajustar la ruta/revisión
en `BlockingBuild` y ejecutar `BlockingBuild.Configure` con el Editor exacto.
El generador rechaza una escena de destino existente. En Unity,
`bash scripts/verify_sequence.sh` genera otra carpeta de evidencias con fecha.
`BlockingBuild.CaptureVideo` guarda 480 imágenes a 12 fps; definir
`CHUPA_BLOCKING_EVIDENCE` a una carpeta nueva al repetir la captura.

```bash
ffmpeg -n -framerate 12 -i RUTA_EVIDENCIA/frames/%04d.png \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart SALIDA_NUEVA.mp4
```

`bash scripts/build_blocking.sh` compila una APK de revisión independiente,
con identificador `com.chupacabras.ar.blockingpreview`, sin instalarla.
Los ajustes de identidad anteriores se restituyen al finalizar.
