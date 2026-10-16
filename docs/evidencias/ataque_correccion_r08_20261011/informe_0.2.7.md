# Ataque natural, separación y volumen — 11 de octubre de 2026

Revisión sobre la primera secuencia AR: pastoreo, salto con desplazamiento,
mordida y forcejeo sin sangre; giro y regreso caminando, con toda la actuación
dentro de 1 × 1 × 1 m y el mismo AprilTag.

## Corrección tras la prueba física

El usuario vio la secuencia 0.2.6 completa, pero detectó estiramiento del cuello
y pidió 30 cm de separación inicial, un traslado A → B claro y que el estado
final quedara sobre el marcador. Esa candidata se conserva, no se considera
aceptada y su perfil de 29,98 fps pertenece exclusivamente a 0.2.6.

Fuente corregida: `scenes/ataque_ar_r08.blend`, `exports/ataque_ar_r08.fbx`.
El contacto se consigue bajando y colocando todo el cuerpo, flexionando las
patas mediante IK horneado y rotando la cabeza: no se añade traslación de
cabeza ni se estira el cuello. La oveja permanece apoyada en el suelo.
Se corrigieron los pesos de la cola para que flexionar las patas traseras no
arrastrara sus vértices. El giro de regreso conserva dirección y velocidad
continuas entre tramos.

La separación inicial libre es de **30 cm** a lo largo de la dirección del
ataque; el salto desplaza la raíz aproximadamente **35,8 cm** desde A hasta B.
A está fuera del AprilTag. La posición final de la raíz es **(0, 0)** sobre el
marcador, distinta de A. Ambos animales usan una sola escala uniforme de 0,08,
y se presenta la trayectoria en diagonal para alojarla dentro del volumen.
El tamaño de detección del AprilTag sigue siendo **0,10 m**; sus archivos y
el código de seguimiento se conservan byte por byte.

Pastoreo, anticipación, salto entre 2,23 y 2,87 s, caída con mordida, forcejeo,
liberación y recorrido de regreso. A **13,5 s** comienza la respiración de
cuatro segundos en bucle; la oveja queda inmóvil. Perder el marcador pausa y
oculta la escena; recuperarlo continúa. Volver a Inicio reinicia la actuación.

Nocturno R08 conserva malla, UV y texturas; el rig incorpora mandíbula y patas.
**112.822 triángulos**, 17 huesos del chupacabras y 24 de la oveja. Las poses se
hornean: no se ejecuta IK ni simulación física durante la reproducción móvil.

## Comprobaciones

Fuente R08: exceso de alcance de patas 0; traslación máxima de cabeza
1,19e−7 unidades (redondeo); apoyo sobre suelo dentro de tolerancia numérica;
máximo error de contacto de mordida **2,85 mm** tras aplicar la escala uniforme;
oveja inmóvil y unión del bucle sin diferencia de vértices. Reimportación FBX
verificada en 13 poses, error máximo 2,35e−6 unidades de autoría. Regreso al
marcador y giro sin discontinuidades verificados.

Unity comprueba los vértices deformados de ambos clips a 48 Hz, incluyendo
la cola y los giros. Comprueba también el espacio libre inicial de 30 cm,
la raíz final sobre el AprilTag y la escala uniforme. La envolvente final
medida es **0,583107 × 0,665988 × 0,255559 m**, completamente dentro del
cubo de un metro sobre el marcador. Se verificaron también los 32 controles
de seguimiento y los clips de ataque/reposo.
La medición usa `BakeMesh(..., true)` y convierte al espacio del ancla;
[documentación de Unity 6.3](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/SkinnedMeshRenderer.BakeMesh.html).

Vídeo: `previews/ataque_ar_r08/secuencia.mp4`, con materiales neutros de
Workbench para revisión del movimiento; la aplicación conserva sus materiales.

## Móvil y empaquetado

El usuario confirmó la mejora del movimiento en 0.2.7 y solicitó después
mayor escala y reinicio al recuperar el marcador, implementados en 0.2.8.
Perfil de 181,28 s: 29,662 fps, mediana 33,323 ms y p95 33,563 ms.

La medida virtual se verifica en Unity. Su correspondencia exacta con el
entorno físico depende de la calibración y del seguimiento existentes (FOV
provisional); no equivale a una medición con cinta en el entorno.
