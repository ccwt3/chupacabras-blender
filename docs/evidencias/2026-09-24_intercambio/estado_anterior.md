# Estado de continuidad

Actualizado: **23 de septiembre de 2026**, tras el recorrido físico del marcador en el Moto G20. **Pasos 2 y 3 completados. Distancia/escala aproximada aceptada expresamente por el usuario; rendimiento observado aceptado para esta etapa y evaluación adicional aplazada. Paso 4 listo para comenzar, pero NO ejecutarlo hasta nueva indicación. App retirada y limpieza comprobada.**

## Alcance y punto de partida

Se comprobaron documentos, archivos, APK, Git y G20 antes de actuar. Estado anterior conservado en `docs/evidencias/2026-09-23_prueba_marcador/estado_anterior.md`. Unity estaba limpio en `a94ac93`; Blender no tiene repositorio Git utilizable. En esta continuación se retomó únicamente **paso 3**; **4** era el segundo previsto, pero no se inició. No se avanzó a un tercer paso ni se modificaron demos o entregas anteriores.

El usuario confirmó distancia nominal de 30 cm, después aclaró que no puede medir exactamente y sostener el teléfono completamente quieto. Aceptó comprobar aproximadamente 50 cm y pidió continuar/cerrar si funcionaba razonablemente. Se respetó: **no exigir más medidas exactas a mano hoy ni tratar las aproximaciones como calibración**. Completó una última comprobación breve de giro y ocultación; la sesión física terminó y se le indicó que puede desconectar el G20.

## Cierre acordado del paso 3

El usuario indicó explícitamente: «ya marca la distancia como hecha» y «el rendimiento bueno, eso viene despues», y pidió dejar listo el paso 4 **sin ejecutarlo aún**. Se acepta la aproximación física observada alrededor de la referencia de 30 cm (lectura inicial cercana a 27.4 cm y tramo posterior de 34.55 cm), con las limitaciones manuales ya registradas. **Distancia/escala hecha; no volver a pedir esta medición para abrir el paso 4.** Las lecturas originales se conservan; esta aceptación no cambia los datos ni declara una calibración exacta.

Se cierra **paso 3 por aceptación explícita del alcance funcional probado**: detección, cubo/ventana, giro, pérdida/recuperación y rendimiento observado. AprilTag queda aceptado como ruta para continuar. La medición adicional de rendimiento y la comprobación física de la revisión 0.0.5 pasan a la fase posterior de rendimiento/validación móvil, sin bloquear el paso 4. No se declara que 0.0.5 haya sido probada en el G20. Esta decisión sustituye las instrucciones previas de mantener abierto el paso 3.

## Pasos y subpasos

| Paso | Estado comprobado |
| --- | --- |
| 1.1–1.4 | Completados previamente; ficha, referencias y M#[1] conservadas. |
| 2.1–2.4 | Completados: Unity exacto/Linux, proyecto/dependencias/build; G20 real Android 11/API 30/ARM64, carga nativa e instalación comprobadas. |
| 3.1 | Preparadas APK, marcador carta medido y guía. Última APK 0.0.5 compilada, sin instalar. |
| 3.2 | Completado durante esta prueba: G20 y autorizaciones USB/cámara. App retirada al cerrar. |
| 3.3 | Completado con alcance aceptado: cámara 0 real, detección/pose y giros 0→90→0 en 0.0.4; escala aproximada aceptada. FOV 60° conservado, sin atribuir calibración exacta. |
| 3.4 | Completado: impresión medida, cubo/ventana, distancias aproximadas aceptadas, giro y tres ocultaciones confirmados por el usuario. M#[2] cerrada para esta etapa. |
| 3.5 | Completado por aceptación del usuario: ~30 fps con RT en tramos registrados, pérdida/recuperación y pausa comprobadas. Rendimiento adicional y validación móvil ampliada aplazados a etapas posteriores. |
| 4 | Listo para iniciar; expresamente NO ejecutado todavía. Esperar nueva indicación del usuario. |
| 5–24 | Pendientes; no iniciados. |

**Paso 3 cerrado por instrucción y aceptación expresa del usuario; paso 4 habilitado y en espera.** S23 sigue pendiente de prueba propia.

## Decisiones confirmadas

- Blender/animaciones/fuentes: `/home/cacawatin/code/blender/chupacabras`.
- AR Android: `/home/cacawatin/code/unity/chupacabras`.
- **Unity exclusivo 6000.3.22f1**, revisión `1c726e1fb402`, instalado en `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`; desarrollo y compilación desde Linux. Sin otro Editor ni cambios globales.
- Producción definitiva **40 s**, cronología del plan; demo de **35 s** independiente y conservada. Ventana anclada al marcador, escena 3D en tiempo real y cámaras internas.
- Chupacabras original; oveja reutilizada con licencia adecuada.
- **M#[1] resuelta:** arrastre inicial a izquierda y giro a salida derecha; ocultamiento desde aterrizaje hasta 25 s; ambiente/efectos sin música. Salto a 20 s; duración 40 s. No preguntar otra vez.
- AprilTag aceptado como ruta para continuar tras la prueba funcional del paso 3. No añadir ARCore ni cambiar de tecnología. G20 obligatorio; S23 disponible solo en exposición y pendiente.
- tagStandard41h12 ID 0: cuadrado entre esquinas de detección **100 mm**, dibujo completo **180 mm**, cubo **50 mm**. FOV **60° provisional**, sin perfil universal ni calibración G20 confirmada.
- Papel **carta**, Brother DCP-T510W, trabajo **43** al 100 % de sesión anterior; regla **100 mm/10 cm confirmada por el usuario**. A4 anterior preservado. No reimprimir ni volver a preguntar medida de la regla sin causa.
- Notificar acciones manuales y retirar lo instalado para pruebas al terminar. No tocar otras apps ni ajustes del móvil. No trasladar comandos/depuración al usuario.

## Cambios y motivo

- 0.0.4 solicita **320 × 240 @15** frente a 640 × 480, porque la prueba real tenía unos 40–53 ms/frame. Detector sin decimación a resolución pequeña y con decimación 2 si la cámara entrega mayor tamaño. Android confirmó 320 × 240.
- Añadido contador `processed_frames` al CSV y `scripts/summarize_tracking.py` para medir frecuencia real y reproducir estadísticas de intervalos explícitos. No confundir frecuencia del CSV con frecuencia de detección; las poses pueden repetirse.
- 0.0.5 procesa cada imagen fresca de WebCamTexture: eliminada segunda puerta temporal que podía saltarse imágenes nuevas al combinar captura de 15 Hz y pantalla cercana a 30 Hz. **Beneficio pendiente de medida física**; no se reinstaló después de cerrar el recorrido.
- Pruebas ampliadas a reconocimiento, profundidad métrica y blanco sin falsos positivos a 320 × 240; 32 aserciones. Corregidos textos obsoletos de ABI en nuevos informes y límite del verificador estático; informes antiguos intactos.
- Fuentes, escena, paquete y tecnología conservados. Demos Blender, APK previas y marcador no sobrescritos. Cachés propias de build archivadas en `Library/GeneratedCmake_20260923_225651/` y `Library/GeneratedCmake_20260923_230715/`; no se incluyen como fuente en commit.

## Resultados físicos y limitaciones

- G20 `motorola moto g(20)`, Android 11/API 30, ARM64 y páginas de 4096 bytes confirmados previamente. Camera 0 trasera WideAngle. Sin validación de un Android de páginas de 16 KB.
- Usuario: **«Sí, aparecen ambos»** ante cubo y ventana. Capturas reales inspeccionadas; imagen y cubo sobre la impresión, ventana con escena 3D a la derecha. Detector nativo sigue pasando su prueba incluida, que por sí sola no es evidencia de impresión.
- 0.0.4, referencia nominal de 30 cm, intervalo CSV 84.7163–114.8737 s: 246/246 muestras visibles, RT activa; mediana frame suavizado **33.322 ms (~30 fps)**, imagen **4.881 ms**, detector **14.743 ms**, procesamiento **8.99 Hz**. Profundidad mediana **34.55 cm**. La hoja no estaba plenamente paralela; el usuario después explicó el límite manual. La aproximación de escala queda **aceptada por el usuario para cerrar esta etapa**, conservando estas lecturas sin certificar precisión exacta.
- A unos 50 cm aproximados, intervalo 250.0956–264.6908 s: 122/122 muestras visibles, frame **33.322 ms**, profundidad **42.28 cm**, procesamiento **7.81 Hz**. Detección funcional conservada; distancia aproximada no sirve para medir error ni fijar FOV.
- Usuario: **«Sí, gira bien y desaparecen/regresan»**, tras giro vertical/horizontal y tres ocultaciones. CSV registra 0→90→0, pérdidas, reloj detenido y recuperación sin reinicio. Ejemplo: 339.4665–342.1989 s mantiene reloj en 189.0553 s y continúa al recuperar. No se sincronizó individualmente cada ocultación; hubo también pérdidas breves durante manipulación. Otra horizontal, inclinación controlada y segundo plano no se comprobaron en esta tanda; se conservan para validación móvil posterior, sin reabrir el paso 3.
- Los tiempos de frame son medias suavizadas, no medición directa de GPU. No se hizo comparación RT 60 s sí/no, prueba final de cinco minutos ni se demuestra margen con recursos finales. La frecuencia efectiva anterior está por debajo del objetivo diagnóstico ≥10 Hz; 0.0.5 intenta corregirla, pero no está físicamente validada.

## Entregas y evidencias

Raíz Unity:

- [APK físicamente probada 0.0.4](/home/cacawatin/code/unity/chupacabras/builds/android/03_tracking_20260923_225712.apk): **36 273 984 bytes**, SHA-256 `9cca2d400c7ff44e28bb65dde4ce59137f18d6de87ec02bd06f3944274ff81f8`.
- [APK preparada 0.0.5](/home/cacawatin/code/unity/chupacabras/builds/android/03_tracking_20260923_230736.apk): **36 274 616 bytes**, SHA-256 `752eb7cd342644761dfa965701991de57a8cf752d7b54c236db24976af3aa755`. **No instalada/probada físicamente**. Informes, hashes y licencias acompañantes conservados.
- [Recorrido y cambios](/home/cacawatin/code/unity/chupacabras/docs/seguimiento_fisico_g20.md), [guía](/home/cacawatin/code/unity/chupacabras/docs/prueba_g20.md), [marcador carta](/home/cacawatin/code/unity/chupacabras/marker/03_marker_carta.pdf).
- `docs/evidencias/g20_marcador_20260923/`: `ownership.json`, `baseline_640.json`, `30cm_revision.json`, `50cm_aproximados_revision.json`, `transitions.json`, **`cleanup.json`**.
- Recogida final **`g20_collect_20260923_230650/`**: logs propios, captura, memoria y CSV de ambas sesiones. Recogidas intermedias `225015`, `225316`, `230204`, `230431` conservadas.
- Instalaciones `g20_install_20260923_224921/` (0.0.3) y `g20_install_20260923_225942/` (0.0.4). Sesiones app `probe_20260923_224949_071` y `probe_20260923_230009_349`.
- Informes APK `g20_apk_20260923_225712.json`, `g20_apk_20260923_230736.json`; checks `tracking_checks_20260923_225703.json`, `tracking_checks_20260923_230726.json`; logs configure/build de `225651` y `230715`.

Raíz Blender: `docs/evidencias/2026-09-23_prueba_marcador/`, con estado previo, copia del informe de cierre y limpieza. Evidencias anteriores intactas.

## Verificaciones y limpieza

- Ambas builds con **Unity 6000.3.22f1/Linux**, IL2CPP/ARM64, **Succeeded, 0 errores/0 advertencias**: 0.0.4 en 1 min 11.94 s; 0.0.5 en 1 min 05.00 s.
- Ambas pasan firma, zipalign de 16 KB y ocho bibliotecas AArch64; alineación estática no equivale a probar Android de 16 KB. 32 aserciones de Editor pasan en ambas. Sintaxis Bash, Python y `git diff --check` sobre fuentes/documentación correctos; sin linter propio configurado. El chequeo global muestra 305 avisos de espacios/líneas vacías en logs y memoria originales; se conservan sin reformatear.
- **Limpieza comprobada a las 23:07:15 UTC**: desinstalación `Success`; paquete, proceso y carpeta externa ausentes, sin errores de acceso. App no instalada al inicio. No se modificaron otras aplicaciones ni configuraciones globales. **No queda nada por retirar ni hace falta USB hoy.**

## Acciones manuales y preguntas

- **M#[1] resuelta:** decisiones narrativas/audio; no repetir.
- **M#[2] resuelta para el paso 3:** preparación y recorrido físico realizados, distancia aproximada aceptada y rendimiento adicional diferido por instrucción explícita. No repetir medidas ni pedir otra conexión para habilitar el paso 4. Limpieza completa.
- **M#[3] resuelta:** Brother DCP-T510W e impresión carta.
- Sin acciones manuales ni preguntas pendientes para pasar al 4. Aceptación explícita de distancia y aplazamiento de rendimiento registrados; las pruebas futuras del producto se coordinarán cuando correspondan.

## Git

Unity: repositorio existente, limpio inicialmente en `a94ac93`; commit de cambios propios registrado al final de este documento, **sin push**. APK en `builds/` ignorado, hashes y evidencias versionados. Blender: `git rev-parse` confirma que no hay repositorio; no se inicializó.

## Punto exacto de reanudación y próximos dos pasos

**Esperar nueva indicación: el usuario pidió dejar el paso 4 listo y no ejecutarlo aún.** No se crea muestra, exportación, escena ni build adicional en esta actualización documental.

1. **Paso 4:** intercambio Blender–Unity con muestra pequeña de rig, restricción horneada, deformación, cámara y RenderTexture. Verificar metros/ejes, contacto y duración de 40 s; documentar exportación. Dependencia (paso 2) satisfecha; paso 3 ya cerrado. No requiere conectar el G20.
2. **Paso 5:** bloquear los 40 s y encuadres de la ventana, después de cumplir sus dependencias del plan. Solo previsto; no ejecutado ni autorizado en este turno.

Próxima pareja prevista: **4 + 5**, cuando el usuario solicite continuar. El rendimiento adicional se retoma en su fase posterior; no volver a abrir la medida de distancia aceptada para iniciar el 4.

## Actualización documental de aceptación

Cambios de esta actualización: cierre de paso 3/M#[2], aceptación de escala aproximada, rendimiento adicional diferido y punto de reanudación trasladado a 4. Motivo: instrucción explícita del usuario. Actualizados estado, plan, evaluación y documentos Unity; evidencia bruta, APK y código intactos. Verificación: coherencia de estados y diferencias de documentación; no se repiten pruebas de código ni builds al no modificarse implementación. No se ejecutó el paso 4.

Commit principal Unity: **`41dc0bac67ea2b3eb361fe8f850a517bc4416f59`** — validación física y optimización. Commit documental posterior aclara el alcance del control de formato de logs originales. Sin push.
Commit documental de cierre: **`4b4aa022dd92d88b68a91451d803ff9e0168e2a0`**. Unity verificado limpio tras ambos commits; sin push. Blender permanece sin repositorio Git.

Cierre documental por aceptación del usuario: commit Unity **`836adb21ddab0b18650e8533e52d1ca362623770`**, árbol limpio y sin push. Actualización limitada a documentación. Comprobados coherencia del estado y formato del diff; no se ejecutaron builds ni pruebas físicas nuevas. Blender continúa sin repositorio Git. **Paso 4 listo y expresamente sin ejecutar.**
