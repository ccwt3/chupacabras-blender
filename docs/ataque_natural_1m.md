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

En 0.2.7, la separación inicial libre era de **30 cm** a lo largo de la dirección del
ataque; el salto desplaza la raíz aproximadamente **35,8 cm** desde A hasta B.
A está fuera del AprilTag. La posición final de la raíz es **(0, 0)** sobre el
marcador, distinta de A. En 0.2.7 ambos animales usaban escala uniforme de 0,08,
y se presenta la trayectoria en diagonal para alojarla dentro del volumen.
El tamaño de detección del AprilTag sigue siendo **0,10 m**; sus archivos y
el código de seguimiento se conservan byte por byte.

Pastoreo, anticipación, salto entre 2,23 y 2,87 s, caída con mordida, forcejeo,
liberación y recorrido de regreso. A **13,5 s** comienza la respiración de
cuatro segundos en bucle; la oveja queda inmóvil. En 0.2.8 perder el marcador
oculta la escena y prepara su reinicio; recuperarlo vuelve al pastoreo y repite
el ataque completo. Volver de segundo plano o de Inicio también reinicia.

Nocturno R08 conserva malla, UV y texturas; el rig incorpora mandíbula y patas.
**112.822 triángulos**, 17 huesos del chupacabras y 24 de la oveja. Las poses se
hornean: no se ejecuta IK ni simulación física durante la reproducción móvil.

## Ampliación 0.2.8 y reinicio

El usuario aceptó el movimiento de 0.2.7 y pidió ampliar la escena a 80–100 cm
por lado, conservando **todas** las proporciones, incluida la distancia A → B.
Se mantiene el FBX R08 byte por byte y se cambia únicamente la escala uniforme
de presentación de 0,08 a 0,11 (×1,375). Por eso el espacio libre inicial pasa
a **41,25 cm** y el salto a unos **49,2 cm**. La altura sigue siendo proporcional;
no se aumenta por separado. El AprilTag conserva 10 cm y la raíz final sigue
sobre él. La envolvente tiene aproximadamente **80,2 × 91,6 × 35,1 cm**; se
verifica el ancho total de la envolvente, sin exigir que el marcador esté en
su centro geométrico.

`AttackPlayback.OnDisable` prepara el reinicio con el mecanismo existente.
Las pruebas de recuperación ahora exigen volver a `Ataque` desde el principio;
una pérdida se provoca desde `Reposo` para detectar una reanudación incorrecta.
Se revisan también tiempo de cámara agotado, segundo plano e ID incorrecto.
No se regeneran modelos ni curvas: se preserva la actuación aceptada.

## Comprobaciones históricas 0.2.7

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

0.2.7 / 207: el usuario confirmó que el movimiento se ve mejor. Perfil de
181,28 s: 29,662 fps; mediana 33,323 ms, p95 33,563 ms, mismo proceso.
Estos resultados pertenecen exclusivamente a 0.2.7.

0.2.8 / 208: pasaron los 32 controles de seguimiento, los 14 estados de
reproducción/interfaz y la verificación geométrica a 48 Hz. Envolvente exacta:
**0,801772 × 0,915733 × 0,351394 m**, espacio inicial **0,4125 m** y raíz final
sobre el marcador. FBX y código de seguimiento idénticos por SHA-256 a 0.2.7.
AAB firmado **0.2.8 / 208** y APK universal generada desde ese AAB mediante
bundletool; validación de bundle, firma, ARM64, alineación y configuración
release correctas. Instalación limpia en Moto G20 realizada: 0.2.7 retirada,
datos borrados y directorios propios sin restos. SHA-256 del APK instalado
idéntico al entregado: `c21908ed5de43ff079b22d1d480246d3ce24e3c4fb23a67b7535b894ef63b53a`.
El usuario confirmó la prueba física de tamaño, proporciones, recorrido y
reinicio al tapar y recuperar el marcador: **«todo bien 10/10»**.
Prueba física 0.2.8 completada: **180,70 s a 29,327 fps** de media;
mediana **33,323 ms**, p95 **33,607 ms**, máximo **83,308 ms**. Mismo proceso,
sin coincidencias de excepciones de ejecución/crashes en el log capturado.
La cámara y ambos actores se observaron en capturas del inicio, minuto uno
y tramo final; no es una garantía de seguimiento perfecto en cada fotograma.

PSS: **400,47 → 371,89 MiB**; swap PSS: **15,56 → 154,02 MiB**. La bajada de
PSS no demuestra una reducción del consumo total: aumentó la memoria paginada.
No se hizo una prueba prolongada de estabilidad de memoria. Temperatura de
batería por Android: **41,3 → 41,2 °C**, con USB conectado.

Segundo plano/reanudación correctos: mismo proceso, cámara reabierta y escena
visible. La captura de recuperación muestra el ataque repetido. Después se
borraron los datos, se desinstaló la aplicación de pruebas y se reinstaló la
APK final entregada, sin recompilar. Su SHA-256 coincide con la APK aceptada y
medida. Las carpetas propias quedaron limpias; no se tocaron otras aplicaciones.
La aplicación final queda abierta en Inicio y solicitará de nuevo la cámara.

Evidencia: `docs/evidencias/ataque_escala_r09_20261011/physical_validation.json`,
`profile_180s/`, `lifecycle/`, `install_final/` y `user_acceptance.json`.
Entrega final en
`entregas/Ataque_Natural_AR_0.2.8_20261011/`.

Por instrucción del usuario, antes de cada instalación se borran los datos del
paquete `com.chupacabras.ar.figure`, se desinstala sin conservar datos y se
comprueba la ausencia de sus directorios Android/data, Android/obb y
Android/media. Solo se eliminan restos de esos directorios propios si existen;
no se modifican otras aplicaciones ni archivos ajenos al proyecto.

La medida virtual se verifica en Unity. Su correspondencia exacta con el
entorno físico depende de la calibración y del seguimiento existentes (FOV
provisional); no equivale a una medición con cinta en el entorno.
