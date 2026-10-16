**Corrección solicitada tras la prueba física de 0.2.6:** el cuello se estira
y falta recorrido explícito. Se sustituirá la traslación de cabeza por agachado
del cuerpo, con 30 cm libres entre animales al inicio y posición final sobre el
AprilTag. La versión 0.2.6 se conserva como candidata probada, no aceptada.

# Ataque natural y volumen de un metro — 11 de octubre de 2026

Revisión solicitada sobre la entrega 0.2.5: oveja pastando, salto corto,
mordida, impacto y forcejeo sin sangre; giro y regreso caminando antes de
recuperar la respiración. Ambos animales y la trayectoria deben caber en
1 × 1 × 1 m sin cambiar el AprilTag ni las proporciones.

## Modelamiento, animación e integración

Fuente nueva `scenes/ataque_ar_r05.blend` y exportación
`exports/ataque_ar_r05.fbx`. R02, R03 y R04 se conservan; R03/R04 son pruebas
intermedias. R08 mantiene malla, UV y texturas. Se añade un hueso de mandíbula
sobre las islas existentes de mandíbula y dientes inferiores: 17 huesos en
el chupacabras, 24 en la oveja y 112.822 triángulos entre ambos.

A 24 fps: pastoreo y anticipación, salto entre 2,23 y 2,87 s, mordida y caída,
forcejeo que termina a 5,45 s, liberación del cuello y vuelta caminando.
El regreso utiliza una trayectoria continua con apoyos alternos y solución
de dos segmentos por extremidad; el cuerpo vuelve al origen y a su orientación
inicial. A 13,5 s empieza el bucle de respiración de 4 s con la oveja inmóvil.
La animación queda horneada; no hay simulación física ni IK en tiempo real.

El ajuste de Unity mide todos los vértices deformados de ambos clips a 48 Hz,
incluye la rotación de presentación y la cola, y aplica la misma escala uniforme
a todo el conjunto. Reserva margen frente al límite de un metro y centra la
trayectoria en el plano del marcador. El offset se aplica bajo `StaticFigure`,
por lo que el seguimiento sigue controlando exclusivamente el ancla.
Se mantiene el tamaño detector de 0,10 m y los archivos del AprilTag existentes.

La medición utiliza `BakeMesh(..., true)` y transforma sus vértices al espacio
del ancla; Unity documenta que este parámetro compensa la escala del renderer.
[Referencia oficial de Unity 6.3](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/SkinnedMeshRenderer.BakeMesh.html).

Envolvente Unity verificada: **0,900001 × 0,833098 × 0,416073 m**, centrada
sobre el marcador, con escala uniforme **0,14031912**. Se deja un margen de
al menos 5 cm por lado en el eje más ancho; la cola y los giros están incluidos.

Validación de fuente R05: alcance excedido de patas 0, mínimo Z del chupacabras
0, mínimo Z de oveja −6,31e−8 m (redondeo), error máximo de contacto 1,33e−7 m,
deriva final de oveja 0 y diferencia de vértices en la unión del bucle 0.
Reimportación FBX verificada en 13 poses (error máximo 3,24e−6 m), giro sin
discontinuidad y regreso al origen. Clips, geometría, ausencia de movimiento
en el ancla y límites de volumen verificados también en Unity.
Vídeo de revisión: `previews/ataque_ar_r05/secuencia.mp4` (materiales neutros
de Workbench, no representa la iluminación final de Unity).

## Prueba móvil y empaquetado

En curso. No atribuir a esta revisión la aceptación física ni el perfil
registrado anteriormente para la versión 0.2.5.

La envolvente métrica se verifica en coordenadas de Unity. Su correspondencia
exacta con centímetros físicos depende del seguimiento y la calibración de
cámara existente (FOV provisional); no es una medición con cinta en el entorno.
