> **Referencia histórica del alcance anterior.** Sus resultados se conservan;
> sus próximos pasos y requisitos cinematográficos no son tareas vigentes.
> Consultar el [plan de figura AR](plan_secuencia.md) y el [estado](estado.md).

# Calma y ataque: pasos 13–14

Sesión del 2 de octubre de 2026. El usuario autoriza aplazar **12.2–12.3 /
M#[6]** para producir 13 y 14. No se ejecutan 15–24 y no se declara aceptación
física del aspecto demacrado. Se mantienen ambas raíces, Unity **6000.3.22f1**,
Blender como fuente, AprilTag y la producción definitiva de **40 s**.

## Fuentes y alcance

Se reutiliza `11_rigs_contacto_demacrado_r01.blend`: 23 huesos del chupacabras,
la oveja Quaternius CC0 de 24 huesos y sus 612 triángulos fijos. No se alteran
pesos, topología ni escala de ninguno de los personajes. Se añade el escenario
`06_escenario.blend`. Los materiales de las escenas Unity referencian el aspecto
preparado en `Assets/Appearance12DemacradoR02/`; no se cambia el hito 12.

- `scenes/13_calma_r07.blend`: rango activo 1–601, **0–20 s**.
- `scenes/14_ataque_r07.blend`: rango activo 1–751, **0–25 s**, con el mismo
  comienzo para comprobar continuidad. No contiene el arrastre 25–40 s.
- FBX y referencias numéricas homónimas en `exports/` y `Assets/Acting/`.
- Escenas Unity homónimas en `Assets/Scenes/`, con ventana de 960 × 540,
  geometría en tiempo real y cámara exterior de revisión independiente.
- `previews/13_calma_r07.mp4` y `previews/14_ataque_r07.mp4`: evidencias de los
  rangos anteriores; no sustituyen las escenas ni son el corto final.

El rango activo del hito 13 termina en 20 s; sus acciones conservan las claves
posteriores compartidas con 14 para continuar la autoría. Los clips FBX se
recortan al rango activo. Las vistas usan el reproductor `RigPreview` existente,
con un solo clip para ambos personajes/cámara; la Timeline de 40 s es el paso 17.
La conexión del corto al seguimiento real permanece en el paso 20.

## Actuación y correcciones

El pastoreo combina variaciones de cuello/cabeza con frecuencias distintas y
una vista ligeramente oblicua de la oveja. El acecho conserva el ojo visible
junto al granero. La retirada retrocede antes de girar, para que la cola no
atraviese las tablas, y termina a los 15 s. Se añaden pasos y compensación de
apoyo; no se desactivan cuerpo ni ojos para ocultarlos.

La cámara empieza a avanzar a los 18,5 s, eleva la mirada para anticipar el
salto y vuelve hacia el aterrizaje con curvas continuas. La criatura despega
a los 20 s desde detrás del granero, supera el techo, cruza cerca/por encima
del lente interno y aterriza a los 21,2 s. Hay recogida/extensión de patas,
compresión de impacto, caída de la oveja y forcejeo hasta los 25 s. La caída
compensa lateralmente el giro para quedar detrás del cuerpo del atacante.
No hay polvo, sangre, mallas auxiliares de ocultación ni curvas de visibilidad.
El agarre sostenido y las pisadas del arrastre corresponden al paso 15.

Se conservaron revisiones de diagnóstico: R01 mostró roce de cola con granero,
encuadre insuficiente del salto y caída expuesta; R02 corrigió la retirada;
R03 mostró la entrada del salto y redujo la exposición a tres cuadros; R04
corrigió el despeje del edificio. R05 mejora la lectura oblicua y deja una exposición residual de cuatro
píxeles en un cuadro; R06 amplió demasiado ese desplazamiento. El diagnóstico `ActingBuild.SearchFall`
midió 16 variantes sobre el render importado; R07 aplica una compensación
lateral menor y un avance de hasta 10 cm durante la caída. Ninguna revisión fallida se considera aceptada. Sus derivados R01–R06 se
conservan localmente y se excluyen de Git; los logs, informes y capturas de
diagnóstico sí se versionan. R07 es la entrega reproducible versionada.

## Verificación y reproducción

Generador único `scripts/actuacion.py`; usar un sufijo **nuevo** para no
sobrescribir entregas:

```bash
CHUPA_SUFFIX=_r08 blender -b -t 4 --python-exit-code 1 --python scripts/actuacion.py
CHUPA_ACTING=14_ataque_r08 blender -b -t 4 --python-exit-code 1 --python scripts/verificar_actuacion.py
CHUPA_ACTING=13_calma_r08 blender -b -t 4 --python-exit-code 1 --python scripts/verificar_actuacion.py
```

El verificador reabre Blender, contrasta vértices contra la referencia,
comprueba apoyo, continuidad de posición/rotación de cámara, despegue/aterrizaje,
ausencia de vértices dentro del volumen conservador de paredes/techo y misma
animación 0–20 s en ambos hitos. La comprobación del edificio no es un solver
de colisiones exhaustivo de triángulos. La inspección visual complementa
las comprobaciones numéricas; no certifica gusto estético del usuario.

En Unity, copiar FBX/JSON a `Assets/Acting/`, usar `CHUPA_ACTING` y ejecutar
`ActingBuild.Configure` únicamente para una escena nueva. `ActingBuild.Verify`
reabre una escena existente y evalúa mediante Playables, comparando los mismos
vértices importados durante toda la animación. No sustituye evaluación por
`SampleAnimation` en las pruebas. Comprueba máscaras de profundidad a 960 × 540
cada 1/30 s: criatura 15–20 s y oveja 21,2–25 s, con control positivo al retirar
al atacante solo durante la prueba. Comprueba que mover la referencia AR y
cámara exterior deja idénticos los píxeles de la cámara interna, y ejecuta las
32 aserciones existentes de seguimiento.

`ActingBuild.CaptureVideo` captura 15 fps. Invocar siempre el Editor exacto:

```bash
CHUPA_ACTING=14_ataque_r07 CHUPA_ACTING_EVIDENCE=docs/evidencias/actuacion/revision_nueva \
/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity \
  -batchmode -quit -job-worker-count 2 -projectPath /home/cacawatin/code/unity/chupacabras \
  -executeMethod ActingBuild.Verify -logFile /tmp/chupacabras_actuacion.log
```

Resultados y capturas: `docs/evidencias/2026-10-02_actuacion/` en Blender y
`docs/evidencias/actuacion/` en Unity. Consultar `estado.md` para las cifras
finales y pruebas pendientes. Los PNG intermedios de vídeo son regenerables.

## Validación física aplazada

La APK **0.0.15**, el marcador carta y la guía M#[6] existentes se conservan.
No se necesita conectar el G20 para estos pasos ni se solicita otra acción
manual. M#[6] sigue pendiente de reanudación expresa, con APK/marcador/guía
preparados. Su resultado permitirá cerrar lectura/brillo reales del paso 12;
las capturas actuales no acreditan eso ni rendimiento sostenido, calibración,
Android de 16 KB o funcionamiento en el S23.

Para codificar la captura de 14 (desde la raíz Blender):

```bash
ffmpeg -v error -n -framerate 15 -i /home/cacawatin/code/unity/chupacabras/docs/evidencias/actuacion/14_ataque_r07/frames/%04d.png -frames:v 375 -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart previews/14_ataque_r07.mp4
```

El vídeo de 13 usa los primeros 300 cuadros de esa captura, después de comprobar
que el tramo común coincide en ambos hitos y de verificar ambas importaciones.
Cambiar `-frames:v 375` a `300` y la salida a `13_calma_r07.mp4`. FFmpeg `-n`
impide sobrescrituras. `14_ataque_r07_salto.png` reúne 24 muestras desde 19,8 s
para inspeccionar entrada, cruce y aterrizaje. FFprobe confirma ambos MP4.
