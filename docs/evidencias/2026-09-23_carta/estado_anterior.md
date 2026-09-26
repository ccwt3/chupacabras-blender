# Estado de continuidad

Actualizado: **23 de septiembre de 2026**, tras primer acceso físico al Moto G20 y limpieza solicitada. **Paso 2 completado; paso 3 parcial. M#[2] pendiente de impresión medida y recorrido físico. La app ya está desinstalada del G20.**

## Alcance y continuidad

Se retomaron únicamente **2 + 3**. Se comprobaron estado, APK, fuentes, instrucciones y repositorio antes de actuar. No se inició 4 ni la producción definitiva. Estado anterior archivado en `docs/evidencias/2026-09-23_g20/estado_anterior.md`; las evidencias de sesiones anteriores se conservan.

El usuario conectó el teléfono, autorizó las pruebas del proyecto y pidió **limpiar lo instalado al terminar**. También pidió notificaciones para acciones manuales. Se notificaron autorización USB y disponibilidad de marcador: aceptó USB y confirmó que **todavía no tiene el marcador impreso**. El cierre de Unity reinició ADB y requirió una segunda autorización, también concedida.

## Pasos y subpasos

| Paso | Estado comprobado |
| --- | --- |
| 1.1–1.4 | Completados previamente; ficha, referencias y M#[1] conservadas. |
| 2.1–2.3 | Completados: Editor, proyecto, dependencias y builds Linux. |
| **2.4** | **Completado para el G20 conectado:** Android/API/ABI reales, instalación, arranque y detector nativo verificados. No equivale a aceptar el seguimiento del paso 3. |
| 3.1 | Preparado: APK corregida 0.0.3/3, marcador A4 y guía. |
| 3.2 | Completado en esta sesión: G20 identificado y USB autorizado. Habrá que reconectar/autorizar si corresponde al retomar. |
| 3.3 | **Parcial:** cámara real 640 × 480 abierta y detector probado con imagen incluida en Android. Orientación óptica completa, calibración/proyección física y escala pendientes. |
| 3.4 | **Pendiente M#[2]:** impresión al 100 %, medida de 100 mm, distancias/inclinaciones, pérdida/recuperación. |
| 3.5 | **Pendiente:** estabilidad/escala físicas y rendimiento con ventana visible. AprilTag aún no se adopta para producción. |
| 4–24 | Pendientes; no iniciados en esta sesión. |

## Decisiones confirmadas

- Blender/animaciones/referencias/exportaciones: `/home/cacawatin/code/blender/chupacabras`.
- AR Android: `/home/cacawatin/code/unity/chupacabras`.
- **Unity exclusivo 6000.3.22f1**, revisión `1c726e1fb402`, instalado en `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`; desarrollo/build Linux. No instalar/actualizar/seleccionar otro Editor sin autorización explícita.
- Producción definitiva **40 s**; demo independiente **35 s**, conservada. Ventana anclada al marcador, escena 3D en tiempo real y cámaras internas.
- Chupacabras original; oveja reutilizada con licencia adecuada.
- **M#[1] resuelta:** arrastre inicial a izquierda y giro a salida derecha; ocultamiento desde aterrizaje hasta 25 s; ambiente/efectos sin música. Salto a 20 s y duración de 40 s conservados. No volver a preguntar.
- AprilTag candidato inicial, sin ARCore ni cambio de tecnología antes de resolver la prueba. G20 obligatorio; S23 pendiente de prueba física propia.
- Prueba provisional: tagStandard41h12, ID 0, lado entre esquinas de detección 100 mm, dibujo completo 180 mm; cubo de 50 mm. FOV 60° **provisional, no calibrado**.
- **Preferencia vigente:** notificar acciones manuales y desinstalar las apps añadidas para la prueba al terminar, recogiendo antes la evidencia. No tocar otras apps ni configuraciones globales.

## Datos físicos confirmados

- `motorola moto g(20)`, Android **11 / API 30**.
- ABIs: `arm64-v8a,armeabi-v7a,armeabi`; ABI 64 bits: `arm64-v8a`. ARM64 ya no se infiere del procesador: lo declaró el sistema real.
- Página de memoria **4096 bytes**. No se validó un Android de páginas de 16 KB.
- Cámara trasera `Camera 0` (WideAngle), imagen real **640 × 480**, configuración de 15 fps. Permiso CAMERA concedido por el usuario. Observados metadatos de giro 90° y 0°, sin reflejo reportado; no se verificó todavía correspondencia óptica completa con patrón.
- La prueba nativa en Android reconoció **un ID 0** en la imagen incluida, pose finita delante de cámara y **cero** detecciones sobre blanco. **No es detección de impresión física.**

## Cambios y motivo

- El primer arranque 0.0.2 mostró dos errores de `MeshCollider` eliminado por stripping. Añadido `Assets/link.xml` para conservar tipos requeridos por `GameObject.CreatePrimitive`; corregido y comprobado en Android, no solo en Editor.
- Ajustado tamaño del panel según ancho **y alto**, porque tapaba casi toda la imagen en horizontal. Captura real de 0.0.3 confirma más área visible y ausencia de la consola de errores.
- Añadida comprobación nativa inicial con `AprilTagFixture`; guarda `detector-device.json` con plataforma/resultados y limitación explícita. Esta prueba permite verificar carga real sin inventar seguimiento físico.
- Versión **0.0.3/código 3**, paquete `com.chupacabras.ar.trackingprobe`; APK anterior y diagnóstico 02 conservados.
- `scripts/g20_probe.sh` abre directamente la actividad con `am start -W`, filtra logs por PID propio, captura pantalla solo si nuestra app está al frente y recoge solo carpetas `probe_*`. Evita recopilar otros procesos o caché IL2CPP innecesaria. La primera apertura con Monkey enumeró tombstones existentes: no se interpretan como caída de esta app.
- Documentación/evidencias actualizadas en ambas raíces; cachés regeneradas `.utmp` conservadas bajo `Library/` y restauradas al estado versionado para no mezclar ruido de build en el commit.
- No se modificaron demos, referencias, escenas Blender, paquetes AprilTag, instalación Unity ni configuración global del teléfono/equipo.

## Entregas y evidencias

En Unity:

- [APK corregida](/home/cacawatin/code/unity/chupacabras/builds/android/03_tracking_20260923_220640.apk), **36 273 532 bytes**, SHA-256 `68fd5ac2136d569286f959aa9db0c40985ab64d0f71b2bb1587348353dbbce42`; `.build.txt`, `.sha256` y `.licenses.txt` acompañantes. Conservada localmente; ya no instalada en el G20.
- [Diagnóstico físico y limpieza](/home/cacawatin/code/unity/chupacabras/docs/diagnostico_g20.md).
- [Marcador A4](/home/cacawatin/code/unity/chupacabras/marker/03_marker_a4.pdf) y [guía M#[2]](/home/cacawatin/code/unity/chupacabras/docs/prueba_g20.md), fuentes CeTZ/PNG y hashes conservados.
- `docs/evidencias/g20_inspect_20260923_220306/`: propiedades y ausencia inicial de las dos apps del proyecto.
- `g20_arranque_20260923_2206/`: fallo inicial, captura, cámara y CSV. `g20_install_20260923_220328/`: instalación inicial.
- `g20_install_20260923_221014/`: instalación/arranque corregidos.
- `g20_collect_20260923_221046/`: log exclusivo de la app, memoria, captura física, datos propios y resumen. `files/probe_20260923_221038_017/detector-device.json` demuestra prueba nativa **Android** positiva/negativa.
- `g20_apk_20260923_220640.json`: firma/ABI/empaquetado.
- **`g20_limpieza_20260923.json`**: desinstalación y ausencia comprobadas.
- `tracking_checks_20260923_220625.json`: 29 aserciones; logs `tracking_configure_20260923_220611.log` y `tracking_build_20260923_220611.log`.

En Blender: `docs/evidencias/2026-09-23_g20/` conserva estado previo, cierre y resumen. Evidencias de continuidad/Unity/seguimiento anteriores intactas.

## Pruebas, resultados y límites

- Build Linux Unity **6000.3.22f1**, IL2CPP/ARM64, **Succeeded, 0 errores/0 advertencias de BuildReport**, 1 min 31.70 s. Firma v2 y zipalign de 16 KB correctos; ocho bibliotecas AArch64, incluida AprilTag.
- **29 aserciones de Editor** repetidas correctamente. Sintaxis Bash y XML de preservación comprobadas. No hay linter ni otra suite propia configurados.
- APK 0.0.3 instalada y abierta en G20; prueba nativa incluida aprobada, cámara visible, errores de MeshCollider ausentes en el log recogido. Captura física inspeccionada.
- En la muestra corregida: 50 muestras con cámara, **cero detecciones de marcador**; medianas de frame suavizado 37.049 ms, conversión 5.950 ms y detección 12.673 ms. Muestra corta que incluye arranque/cambio de orientación: **no permite aceptar rendimiento**, no mide GPU ni RT visible. Al no tener pose, la cámara de RT estaba desactivada.
- **Limpieza completada:** desinstalación devuelve `Success`; después no existen paquete, proceso ni carpeta externa de datos. La app no existía al comenzar. No se desinstaló ninguna app previa ni se borraron otros datos.
- La plantilla del informe `.build.txt` aún dice «ABI PROVISIONAL, G20 pending»; es un rótulo heredado del generador, superado por las evidencias físicas de esta sesión. Se conserva el informe original sin alterarlo retroactivamente.
- Pendientes: marcador impreso/medido, pose y escala, calibración/distorsión, orientación/reflejo completos, pérdida/recuperación real, estabilidad y margen con RT. S23 sin prueba. No se da por terminado el paso 3.

## Acciones manuales

**M#[1] — Resuelta.** Guion/audio registrados; no repetir.

**M#[2] — Parcial:** USB y cámara autorizados; arranque comprobado. El usuario confirmó que **no tiene el marcador impreso**. Falta imprimir PDF A4 al **100 %**, medir la regla/cuadrado de **100 mm** y realizar el recorrido físico. Al retomarlo, reconectar G20 para reinstalación temporal por el agente; limpiar lo añadido al terminar. No pedir nuevas decisiones ya confirmadas ni repetir pruebas de preparación sin causa.

No quedan acciones de limpieza pendientes: el usuario puede desconectar el G20. No hay otra decisión creativa solicitada.

## Git

Unity: repositorio existente, limpio al inicio en `897b36b`. Commit **`c2c8132`** (`c2c813219effddc733873d14855e65372c3485c4`) de corrección, diagnóstico, documentación y evidencias de esta sesión; árbol limpio, **sin push**. APK permanece en `builds/` ignorado, con hash registrado.

Blender: no hay repositorio Git utilizable; no se inicializa. Documentos y evidencias guardados dentro del proyecto.

## Punto exacto de reanudación y próximos dos pasos

**Detener hasta disponer de la impresión y respuesta a M#[2].** Preparación técnica cerrada; no hace falta recrear proyectos ni cambiar Editor/tecnología.

1. **Retomar paso 3 en 3.4**, con impresión medida. Reconectar/autorizar e instalar temporalmente APK 0.0.3 para completar 3.3 (proyección/calibración) y 3.5 (pose/escala, recuperación, estabilidad, RT). Diagnosticar y corregir solo lo que los resultados requieran; desinstalar al terminar.
2. **Paso 4**, en la siguiente sesión que lo permita: intercambio de una muestra de animación Blender–Unity y cámara interna/RenderTexture. Depende de 2, ya cerrado; no se inició ahora ni se avanza durante el bloqueo físico bajo la instrucción de detenerse.

Próxima pareja: **3 retomado + 4**. La sesión cerrada solo trabajó **2 retomado + 3**.
