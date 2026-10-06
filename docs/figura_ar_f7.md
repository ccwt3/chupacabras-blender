# F7 — revisión final de Nocturno R08

**F7 completada el 6 de octubre de 2026 como demo funcional en Moto G20.**
Se corrigió la respiración imperceptible conservando el personaje R08 y el funcionamiento de la app.
El usuario aceptó la candidata final como demo con el rendimiento real de **28,53 fps**, por debajo de 30 fps sostenidos.
Entrega: `entregas/F7_Nocturno_R08_20261006/`; archivo distribuible hermano `.tar.gz`.
Guía e inventario en `LEEME.md`; hashes por archivo en `SHA256SUMS`; identificación y resultados en `manifest.json`.


## Candidata de partida y preservación

Unity `builds/android/F6_figure_20261003_222832.apk`, 0.2.2 / 202,
55.348.110 bytes, paquete `com.chupacabras.ar.figure`.
SHA-256 comprobado: `0bf9b53293e4035d2decba069845bace2afc0c8330f8a77ad131b333a47b3e16`.
Firma, permiso de cámara, ARM64 y ZIP/ELF comprobados con el verificador existente.
Moto G20, Android 11, ARM64, páginas de 4096 bytes; carga USB activa.
No existían el paquete ni su carpeta externa al comenzar. Se retiró solo esta instalación al finalizar.

## Revisión de partida

Captura `revision_01.png` y video `revision.mp4` (9,736 s) en
`evidencias/2026-10-06_f7/`: figura única, piel oscura, ojos, dientes y cresta
visibles sobre la impresión existente, con cambios de encuadre y orientación.
El video por sí solo no acredita percepción suficiente de respiración.

Respuesta del usuario: «La percepcion de que esta respirando  es nula o no parece,
se ve mas estitico, de ahi en fuera esta bien».
Se registra como defecto del personaje que impide cerrar la animación;
no se interpreta la ausencia de otros defectos como aprobación de esa respiración.

## Verificación de fuentes

Blender 5.2.2 LTS: reapertura de una copia de entrega, 110.294 triángulos,
cuatro huesos, un material, ciclo 4 s, apoyo comprobado en 97 cuadros,
deslizamiento cero, cierre cero. Intercambio FBX dentro de 0,000000719 m.
Unity 6000.3.22f1: 32 checks de seguimiento, comprobaciones de material/malla,
ciclo y apoyo, diez estados sintéticos correctos; el Animator avanza.
Estos checks comprueban funcionamiento numérico, no legibilidad visual en el móvil.
Los 1207 archivos inventariados de Assets, Packages, ProjectSettings y scripts
conservan sus hashes tras la reapertura y regresión de partida.

Se intentó una copia temporal de la caché Unity para verificar aisladamente;
la cuota de /tmp impidió completarla. Solo esa copia incompleta de esta sesión
fue retirada. Se ejecutaron los verificadores sobre el proyecto original,
sin alterar sus fuentes ni recompilar la candidata.

## Perfil y cierre

Perfil de partida ejecutado con `scripts/perfil_figura_g20.py`, 310 s solicitados,
después de que el usuario colocó el teléfono y confirmó «listo».
Se completaron pérdidas/recuperación, segundo plano, corrección del defecto de
respiración, repetición física de la candidata final y limpieza, según los registros siguientes.

Fuentes y guía de entrega: `entregas/F7_Nocturno_R08_20261006/`.
Entrega aceptada como demo; se conservan escenas, recursos y APK previos.
Sin commit/push, sin nuevas fases. S23 pendiente y no bloqueante para el G20.

## Corrección observada: respiración R02

El usuario confirmó «recupera bien». CSV físico registra ocultaciones y
recuperaciones; Inicio y retorno mantienen el mismo PID y recuperan figura.
Perfil original: 309,966 s, 28,168 fps; p95 49,990 ms, p99 66,684 ms,
máximo 199,923 ms, 372 intervalos >50 ms y 9 >100 ms. Figura visible en
2530/2530 muestras durante 307,868 s; detector 14,941 Hz, distinto del render.
PSS 438700 → 401881 KiB; batería 36,9 → 37,6 °C; estado térmico 0.
Por minuto: 30,001 / 29,985 / 29,968 / 22,787 / 27,950 fps.
Se conserva carga de otros procesos observada en la ventana temporal del
cuarto minuto; correlación posible, no demostración de causa ni justificación
para excluir cuadros. No se detuvieron apps ajenas ni se cambiaron ajustes.

`refinar_respiracion_nocturno.py` crea una fuente/FBX nuevos desde R08,
sin rehacer geometría ni texturas. Amplifica cambios respecto a la pose inicial:
tórax 2,5× y cabeza 2×; cola y raíz conservadas. Duración 4 s.
Comprobación nueva: movimiento real entre 0,12 y 0,20 m de autoría,
patas fijas en los 97 cuadros y cierre de ciclo. Resultado: 0,149900 m.
El verificador existente conserva el rango original para R08 y comprueba
ese rango específico para la revisión R02; no reduce las garantías de apoyo.

Unity `FigureBreathingRevision.Configure` importa solo la fuente del clip y
asigna un controlador nuevo al Animator existente. La malla R08 y sus mapas
siguen referenciados por el mismo prefab. `FigureNocturno.VerifyViews` toma
el clip realmente asignado al Animator para evitar verificar por error el antiguo.
No cambia runtime, escena, luces, escala, seguimiento, interfaz, paquetes ni
configuración gráfica. Las fuentes originales y la APK medida quedan preservadas.
La candidata corregida y su aceptación física se documentan debajo.

## Candidata corregida

APK `builds/android/F6_figure_20261006_181916.apk` de Unity,
0.2.2 / 202, 55.348.110 bytes. SHA-256:
`7db6358cdb13c37467a3d42f76d163ef8359c0ef25583441065ed5b869863aae`.
Build con cero errores/advertencias; firma, ARM64 y alineación verificadas.
Malla, UV y pesos idénticos por hash entre fuentes Blender; los cuatro mapas
son idénticos byte a byte. Unity empaqueta la malla/material/mapas R08 y el
clip/controlador R02. El prefab solo cambia el GUID del controlador.
Scene, runtime, luces, escala, Packages y ProjectSettings conservan sus hashes.

Se restauró un espacio final de URP y nueve temporales CMake que estaban
limpios al inicio; copias generadas y registro en `serializacion/`.
No se restauran ni descartan cambios previos del usuario.

El usuario confirmó «respiracion bien, listo» tras observar varios ciclos
laterales, sin comunicar saltos ni deslizamiento. Video físico:
`respiracion_r02_g20.mp4`. Perfil final de 310 s realizado después de esa respuesta;
no se atribuye a esta APK el perfil de la candidata inicial.

## Perfil físico de la APK final

310,000 s de presentación, 8845 intervalos únicos; candidato identificado arriba.
Se reutilizó el recopilador y resumidor existentes, sin cambiar frecuencia,
cámara ni calidad. USB y consultas ADB activos; sin grabación de pantalla durante
el perfil. Cámara 320 × 240, orientación 0°, marcador 100 mm, FOV provisional 60°.
Todas las consultas de actividad registran la aplicación en primer plano.

| Medida | Resultado R02 final |
| --- | --- |
| Presentación media | 28,532 fps |
| Media por minuto | 29,976 / 27,667 / 29,176 / 28,284 / 27,724 fps |
| Intervalo mediano / p95 / p99 | 33,324 / 49,985 / 50,051 ms |
| Mayor intervalo | 83,303 ms |
| Intervalos >50 ms / >100 ms | 150 / 0 |
| Figura visible en CSV interior | 2530/2530 muestras, 307,854 s |
| Frecuencia efectiva del detector | 15,007 Hz |
| Detector mediana / p95 / máximo | 21,017 / 27,286 / 47,665 ms |
| Preparación de imagen mediana / p95 / máximo | 6,353 / 17,048 / 26,602 ms |
| Memoria PSS inicio → final | 410773 → 395597 KiB (401,15 → 386,33 MiB) |
| Rango PSS | 395597–410773 KiB |
| Heap nativo asignado inicio → final | 209645 → 199404 KiB |
| Batería inicio → final | 37,9 → 39,4 °C; USB activo |
| SoC / GPU, lecturas actuales HAL | 59,884–65,573 / 59,062–61,366 °C |
| Estado térmico Android | 0 en las doce lecturas |

**No alcanza 30 fps sostenidos.** Se informa como límite de la demo, sin borrar
intervalos ni sustituir fps de presentación por los ~15 Hz del detector.
No se observa crecimiento sostenido de PSS durante este tramo ni paradas >100 ms.
El registro retenido no contiene FATAL EXCEPTION, ANR, OutOfMemory,
NullReferenceException ni AndroidJavaException. Esto no prueba ausencia de
cualquier error o fuga a largo plazo. No se obtuvo tiempo GPU por cuadro.

Las temperaturas HAL se distinguen de la sección de valores en caché del servicio,
que contiene lecturas antiguas. Estado térmico 0 significa ausencia de limitación
reportada por ese servicio, no prueba universal de que nunca intervino un gobernador.
Los dos perfiles tuvieron cargas y temperaturas distintas; la variación de medias
no demuestra mejora de rendimiento por aumentar la respiración.

La APK instalada se comprobó mediante SHA-256 del `base.apk` en el teléfono:
coincide con `7db6358…863aae`. Evidencia `apk_instalada.json`.

## Recuperación, aceptación y limpieza finales

Tras el perfil final, el usuario retiró y volvió a mostrar el marcador.
El CSV registra ocultaciones y recuperaciones; no se atribuye una latencia exacta
porque el instante físico de volver a mostrarlo no está instrumentado.
Se observaron transiciones breves durante la manipulación; el perfil estable
previo conserva sus 2530/2530 muestras visibles. Ante la pregunta por figura
única, escala, respiración recuperada y fluidez —incluyendo el resultado de
28,53 fps— respondió: «si, suficiente como demo».

Se envió Inicio durante tres segundos y se reabrió la actividad. Android registró
el cambio a segundo plano; volvió el mismo PID, detección y figura visibles.
`reanudacion_final.json`, `reanudacion_final.png`, `recuperacion_final.json`,
`final_files/` y `final_logcat.txt` conservan evidencia de la candidata final.
El comportamiento de ocultación inmediata en segundo plano, ID incorrecto y
timeout cuenta además con regresión sintética; no se presenta el ID incorrecto
como una prueba de otro marcador físico.

`adb uninstall com.chupacabras.ar.figure` devolvió Success. Paquete y proceso
ausentes; carpeta externa inexistente. `cleanup.json` confirma la limpieza.
Ese paquete y sus datos no existían al inicio: no se retiró ninguna instalación
ni datos previos. No se cambiaron redes, giro, ahorro de batería u otros ajustes.

## Entrega, reproducción y límites

La entrega contiene la APK final exacta, Blender R08 y su revisión de respiración
R02, FBX/mapas, proyecto Unity con Assets/Packages/ProjectSettings, scripts,
marcador existente, avisos de licencias, guía e inventario con SHA-256.
La candidata inicial se conserva en `evidencias/candidata_original/`; no es la
APK de uso. Las fuentes Unity conservan recursos históricos y sus licencias;
la build vigente excluye los recursos cinematográficos, como comprueba BuildReport.
No se distribuyen Library, Editor, SDK, credenciales ni cachés de compilación.

Solo Unity 6000.3.22f1. Desde Unity:
`CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh`.
Desde Blender:
`CHUPA_ART_REV=r08_respira_r02 blender -b -t 2 --python-exit-code 1 --python scripts/verificar_nocturno.py`.
La compilación y los verificadores existentes se ejecutaron; sintaxis Python y
`git diff --check` correctos. No hay linter general configurado.
Recompilar produce otra APK; su identidad/validación física no se debe heredar
sin verificarla. No se recompiló después del perfil final.

El cierre es de **demo funcional aceptada**, no de cumplimiento de 30 fps
sostenidos ni de acabado comercial. No acredita funcionamiento durante horas,
calibración métrica exacta, ejecución con páginas Android de 16 KB ni S23.
S23 queda pendiente y no bloquea esta entrega G20. Sin commits, push ni fases nuevas.
