# Figura AR: prueba física F5 y correcciones F6

Sesión del 3 de octubre de 2026, iniciada por petición del usuario con el móvil
conectado. **F5 y F6 cerradas como demo AR funcional, según la aclaración final del usuario.**

## Preparación

Se conserva la candidata F4 R02, versión 0.2.0 / código 200, paquete
`com.chupacabras.ar.figure`. SHA-256:
`e5acda3e837a7054aff879d64de176599695ffc6c73b315b868c9cb2fd268104`.
Firma, ZIP/ELF y ARM64 se volvieron a verificar antes de instalarla.
Moto G20 con Android 11/API 30, ARM64 y páginas de 4096 bytes. Esto no es una
prueba de ejecución con páginas de 16 KB. El paquete no existía antes de esta
sesión; retirar solamente esta instalación al terminar la prueba.

Inventario de ambos repositorios y estado previo conservados en
`evidencias/2026-10-03_figura_f5_f6/`. Se mantienen los cambios anteriores de
F3/F4 y los ajustes de Unity que ya estaban preparados en el índice.

## Método y límites

`scripts/perfil_figura_g20.py` recoge las marcas de presentación de la
SurfaceView propia cada tres segundos, memoria/temperatura/CPU cada treinta
segundos y los CSV/logs de nuestra aplicación. Identifica un único G20 y una
única superficie antes de comenzar; crea un destino nuevo sin sobrescribir
otra medición. No cambia ajustes del teléfono.

La medición de cinco minutos comienza después de colocar el teléfono con el
marcador y la figura visibles. Los tiempos de presentación de SurfaceFlinger
se distinguen del contador suavizado de Unity y de la frecuencia de detección.
Ni esos tiempos ni `dumpsys cpuinfo` proporcionan tiempos de ejecución GPU.
La carga USB y el muestreo ADB forman parte de las condiciones del ensayo.

Reproducción desde la raíz Blender, con ADB autorizado:

```bash
python scripts/perfil_figura_g20.py docs/evidencias/NUEVA_MEDICION --seconds 310
```

## Revisión visual del usuario

El usuario respondió «Se ve bien y recupera correctamente» tras las instrucciones
para revisar frente/lados/cerca, tres pérdidas/recuperaciones, giro y salida a
Inicio/reanudación. No comunicó defectos de forma, piel, iluminación, tamaño o
temblor. La aceptación es de esta candidata en las condiciones observadas.
La captura `perfil_inicio.png` muestra una sola figura sobre la impresión.

## Regresión de ID incorrecto

Se amplía `FigurePreview` de Unity conservando sus ocho estados anteriores y
agregando ID incorrecto/recuperación de ID correcto. Antes de usar el patrón,
el detector real debe reconocer exactamente ID 1; así se evita confundir una
imagen ilegible con una prueba de filtrado. También se comprueban instancia,
escala y ausencia de elementos cinematográficos en ambos estados nuevos.
No cambia el código runtime, los assets de la escena ni la APK candidata.

El patrón `docs/fixtures/tag41h12_id1.png` del proyecto Unity se generó con
`apriltag_to_image` de la biblioteca Linux ya instalada, tagStandard41h12 ID 1;
9 × 9 celdas ampliadas sin interpolación a 288 × 288 y margen blanco hasta
512 × 512. Referencia de interfaz: AprilRobotics. (s. f.). *apriltag.h* [Código
fuente]. GitHub. https://github.com/AprilRobotics/apriltag/blob/master/apriltag.h
Licencia nativa existente: `docs/licenses/AprilTag-native.txt` en Unity.
Es una comprobación sintética de la ruta real de detección; no una segunda
impresión ni una prueba física de otro marcador.

## Perfil físico de la candidata F4 R02

Resultado bruto y resumen en `evidencias/2026-10-03_figura_f5_f6/perfil_f4/`.
La presentación se observó durante **309,98 s**, con **9301 intervalos** únicos.
Se descarta la historia anterior al último timestamp de la primera consulta de
SurfaceFlinger; se deduplica la segunda columna (presentación real), se ordena
y se calculan diferencias consecutivas. Percentiles por rango más próximo.

| Medida | Resultado |
| --- | --- |
| Presentación media | 30,005 fps |
| Media por minuto, cinco minutos | 30,001 / 30,001 / 30,001 / 30,010 / 30,010 fps |
| Intervalo de presentación mediano / p95 / p99 | 33,323 / 33,421 / 33,599 ms |
| Mayor intervalo | 49,979 ms |
| Intervalos >40 ms / >50 ms / >100 ms | 6 / 0 / 0 |
| Figura visible, CSV entre 243,038 y 546,923 s | 2499 de 2499 muestras; 303,885 s |
| Frecuencia efectiva del detector | 15,009 Hz |
| Preparación de imagen, mediana / p95 / máximo | 2,930 / 15,664 / 21,468 ms |
| Detector, mediana / p95 / máximo | 12,065 / 15,082 / 19,565 ms |
| Memoria PSS mínima–máxima | 409917–413343 KiB, aproximadamente 400,3–403,7 MiB |
| PSS inicio → 300 s | 413343 → 410469 KiB |
| Batería inicio → 300 s | 38,0 → 38,5 °C, carga USB activa |
| SoC / GPU, rango de sensores | 56,776–63,510 / 53,686–59,830 °C |
| Estado térmico Android | 0 en las once lecturas |

La captura real fue 320 × 240, orientación reportada 90°, FOV provisional 60°,
tag configurado de 100 mm. La figura permaneció visible en todo el tramo CSV
interior a la medición. No se detectó degradación de cuadros ni crecimiento
continuo de PSS durante este ensayo; no acredita una exposición de horas.

`dumpsys cpuinfo` mostró ventanas de 48 % y 65 % para el proceso, repetidas
entre consultas: se conservan como diagnóstico, no como perfil de CPU por
cuadro ni porcentaje de todo el teléfono. No se obtuvo tiempo GPU por cuadro.
RSS y swap PSS están en el resumen bruto; memoria PSS no es el tamaño de los
mapas ni debe confundirse con la estimación ASTC de F3.

## Defecto físico F6: bucle al denegar cámara

La primera prueba de denegación no quedó denegada: el permiso terminó aceptado;
se conservó como arranque frío sin red. En el segundo intento el usuario confirmó
«Denegado». Android mostró `granted=false` y `USER_FIXED`, pero la app alternó
pausa/reanudación repetidamente y mantuvo «Esperando permiso de cámara…».
`denegado_logcat.txt`, las capturas y `fallo_permiso_files/` conservan el fallo.
Este fallo invalidó el cierre inicial; se corrigió y repitió físicamente en la APK F6.

Causa: el diálogo de permisos pausa la actividad; `OnApplicationPause(true)`
cancela las corrutinas. Al reanudar, se llamaba otra vez a `OpenCamera`, que
solicitaba de nuevo el permiso. Esto repite el ciclo incluso tras la denegación
persistente. La corrección distingue apertura explícita de reanudación:
`OpenCamera(false)` comprueba el permiso al reanudar sin volver a solicitarlo.
Inicio y Reintentar conservan la solicitud explícita. La recuperación normal
con permiso concedido mantiene la misma ruta de cámara.

También se oculta el quad de cámara mientras no hay imagen, para eliminar el
rectángulo blanco observado durante la denegación. Son cambios compartidos de
`TrackingProbe`; se vuelven a verificar F4/F6 y F1. No cambian malla, texturas,
iluminación, detector ni paquetes. Se conserva la fuente runtime anterior.

La primera candidata corregida es **F6 0.2.1 / código 201**, mismo identificador de paquete
y escena F4 R02. `CHUPA_FIGURE_STAGE=F6` selecciona su versión y destino APK;
las opciones F1/F4 y sus versiones siguen disponibles. El verificador reconoce
los tres destinos. La corrección exige perfil físico nuevo de la APK final.

Incidencia del procedimiento: `pm set-permission-flags` no está disponible en
este Android. No cambió banderas por esa orden; la denegación se hizo mediante
el diálogo normal y respuesta del usuario. No se alteraron permisos ajenos.

## Regresión física de la corrección

APK `F6_figure_20261003_211921.apk`, **41.623.751 bytes**, versión 0.2.1,
código 201, SHA-256
`cb41903727ab7a8d053286834114b7c9b7e6df398d997ffd35a3ceaca3f529a4`.
BuildReport: cero errores y cero advertencias. Firma, permiso de cámara, ARM64,
ZIP/ELF de 16 KB y dependencias verificadas de nuevo; el G20 sigue usando páginas
reales de 4096 bytes. Evidencia: `build_f6_r01/`.

- Permiso denegado persistente: `granted=false`, `USER_FIXED`, aviso «Cámara
  denegada. Autorízala en Ajustes y pulsa Reintentar.», sin figura ni quad blanco.
- Reintentar todavía denegado: vuelve al mismo aviso, sin bucle. El log anterior
  contenía 207 pares de pausa/reanudación en la ventana retenida; el corregido
  conserva dos pausas y tres reanudaciones durante arranque y reintento. Son
  ventanas diferentes, usadas para diagnosticar repetición, no un benchmark.
- Permiso restablecido por ADB y botón Reintentar: vuelve la cámara y se detecta
  el tag en el mismo proceso, figura visible y reloj narrativo cero.
- Inicio durante dos segundos y retorno: reaparece la figura; captura y log
  propios conservados. Después se fuerza parada de nuestra app y se verifica
  arranque frío con cámara concedida, figura visible y **sin red activa**.
- El usuario confirmó «Sin red, visible» para F4; para F6 constan modo avión,
  `Active default network: none`, captura y CSV visibles tras el arranque frío.
  No se modificaron redes por ADB. El usuario activó el modo avión para el ensayo.
- Las 32 comprobaciones y diez estados sintéticos pasan con F6. F1 también pasa
  los diez estados usando la corrección compartida. El ID 1 y el timeout se
  verificaron sintéticamente; no se presentan como nuevo marcador físico ni
  desconexión física del sensor.

## Perfil F6 0.2.1 y giro físico

El segundo perfil recogió 310,00 s. Mediana/p95/p99 de presentación:
33,323 / 33,409 / 33,573 ms. El promedio bruto es **29,607 fps**, porque incluye
una interrupción de 4,132 s coincidente con un gesto desde la parte superior
(15:28:23.959) y pérdida/recuperación del foco de Android (15:28:24.984–28.999).
Se conserva íntegro el dato; no se declara este intervalo como ejecución
continua en primer plano. La correlación es consistente con abrir el panel de
Android, no demuestra un bloqueo del renderizador. Sin ese único intervalo
identificado quedan 305,867 s de presentación activa a **30,003 fps**.

CSV interior: 2513/2514 muestras visibles durante 307,900 s. La muestra oculta
sigue al hueco de registro entre 304,740 y 308,931 s; después recupera. No se
atribuye a una pérdida espontánea del tag ni se oculta al informar el resultado.
El primer resumen rechazó la hipótesis demasiado estricta de 100 % de muestras
visibles; se investigó la interrupción y se conservó el resumen bruto.

PSS: 445162 → 449365 KiB, máximo 449873; subida inicial seguida de fluctuaciones.
Heap nativo asignado: 201081 → 198102 KiB. Batería: 35,2 → 36,9 °C; estado térmico
0 en doce lecturas. No se observó crecimiento continuo del heap ni degradación
térmica durante el intervalo, sin afirmar ausencia de fugas a largo plazo.
La app acababa de arrancar y estaba sin red; F4 llevaba más calentamiento y
conexión. Las diferencias entre perfiles no son una comparación controlada de
optimización. No se modificaron recursos visuales ni calidad gráfica.

El teléfono tenía giro automático desactivado. El usuario lo activó para la
prueba y respondió «Todo listo y si todo se ve bien». El CSV físico posterior
registra 90° → 0° → 90° → 0° y detección válida en ambas orientaciones. Las imágenes
de cámara horizontal/vertical y el log están en `final_files/` y
`f6_final_logcat.txt`.

## Última corrección y criterio de cierre

Durante ese giro, el botón Captura reveló un defecto menor: Android añadía
`persistentDataPath` a una ruta que ya lo incluía. Se guardaba la cámara, pero
fallaba la captura de pantalla. F6 **0.2.2 / código 202** pasa una ruta relativa
solo en Android; Editor conserva su ruta absoluta. No cambia el flujo AR.
Fuentes previas y nuevas, APK 0.2.1 y evidencias se conservan.

El usuario aclaró: «con que funcione el AR es mas que suficiente, no es una app comercial».
El cierre se ajusta a **demo AR funcional**, con los arreglos ya hechos. Se
suspende la repetición de cinco minutos propuesta para 0.2.2: su verificación
final es de instalación, arranque, detección y presentación. Las mediciones
anteriores conservan sus versiones y límites; no se atribuyen a la APK 0.2.2.
No se abre trabajo adicional de pulido ni F7 en esta sesión.

El recopilador `scripts/perfil_figura_g20.py` y el resumidor
`scripts/resumir_perfil_figura.py` usan solo biblioteca estándar y ADB existente.
Este último conserva todos los huecos y pérdidas: se comprobó contra el perfil
interrumpido que reproduce 29,607 fps, el hueco >4 s y las 2513/2514 muestras.
No elimina atípicos para hacer aprobar el resultado. Para perfiles con extremos
registrados se puede reproducir el resumen así:

```bash
python scripts/resumir_perfil_figura.py docs/evidencias/2026-10-03_figura_f5_f6/perfil_f6
```

## Cierre

Candidata final: `builds/android/F6_figure_20261003_213520.apk` en Unity,
**0.2.2 / código 202**, **41.621.707 bytes**, SHA-256
`d8448556ee2529bd8ee130c75d26e424b1ec98106f04f196cdf65574e4cfabbd`.
BuildReport: cero errores y advertencias; 32 checks y diez estados correctos;
firma, permisos, ABI y alineación verificados. Evidencia `build_f6_r02/`.

Instalada y abierta en frío en G20: figura única visible y detección activa,
reloj narrativo cero. `f6_r02_ar.png` muestra el resultado. El botón Captura
ya guarda ambos archivos: `213853_296_camera.png` y `213853_296_screen.png`,
conservados en `f6_r02_files/`. Esto confirma la corrección de ruta en Android.
No se repitió el perfil largo de esta APK por la prioridad indicada por el usuario.

Limpieza: `adb uninstall com.chupacabras.ar.figure` devolvió `Success`;
paquete y proceso ausentes y directorio externo inexistente. `cleanup.txt`
conserva la comprobación. Esa app no estaba instalada al iniciar; no se retiró
ninguna otra app. Ya se puede desconectar el móvil. El usuario puede restaurar
sus preferencias de red/giro si todavía no lo hizo; el agente no las cambió.

Se conservan fuentes, escenas, APK y evidencias previas. Los tres ajustes ajenos
del índice Unity y los assets F4 mantienen sus hashes iniciales. Se restauraron
solo temporales CMake que inicialmente eran idénticos a HEAD, con copia local
de los generados y registro. `.gitignore` excluye esas copias de compilación,
no los informes. Sintaxis Python/shell y `git diff --check` verificados. No hay
linter general configurado; se ejecutaron los verificadores existentes relevantes.
No se hicieron commits ni push. F7 no se inicia; S23 pendiente.
