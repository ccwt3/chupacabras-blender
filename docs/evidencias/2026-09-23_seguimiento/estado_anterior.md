# Estado de continuidad

Actualizado: 23 de septiembre de 2026, tras la respuesta de M#[1] y la preparación Unity/Android. Estado contrastado con archivos, ejecuciones y logs.

## Alcance y punto de partida

Se aplicaron las instrucciones personales suministradas; no se encontraron `AGENTS.md` adicionales en las raíces ni antecesores consultados. Al comenzar no había estado y Unity estaba vacío. La auditoría inicial y sus evidencias se conservan en `docs/evidencias/2026-09-23_continuidad/`.

Se trabajaron únicamente los pasos principales **1 y 2**, contando el retomado como primero. **Paso 1 cerrado. Paso 2 preparado y compilado, con aceptación física de ABI pendiente.** No se inició el paso 3 ni la producción definitiva.

## Pasos y subpasos

| Paso | Estado comprobado |
| --- | --- |
| 1.1 | Completado: cinco referencias copiadas/revisadas y demos comprobadas. |
| 1.2 | Completado: evaluación AprilTag revisada; requisitos y límites registrados. |
| 1.3 | Completado: respuesta explícita M#[1] incorporada a ficha y plan. |
| 1.4 | Completado: ficha, decisiones y continuidad actualizadas. AprilTag sigue siendo candidato hasta prueba real. |
| 2.1 | Completado: proyecto en la raíz Unity solicitada; Editor 6000.3.22f1, URP 17.3.0, revisión AprilTag y herramientas Android comprobadas. |
| 2.2 | No requirió intervención: la licencia existente permitió crear, abrir y compilar. |
| 2.3 | Completado para esta preparación: escena de diagnóstico estático, configuración Android, compilación automatizada y captura de Editor reproducible. |
| 2.4 | Build Linux→Android exitosa, detector Linux y empaquetado verificados. **Pendiente consultar ABIs reales del G20** antes de cerrar arquitectura/aceptación completa; ARM64 provisional. |
| 3 | No iniciado: falta cámara física, marcador imprimible, APK de seguimiento y prueba G20. La APK actual solo prueba una imagen incluida. |
| 4–24 | Pendientes. Las demos independientes no sustituyen estos hitos. |

## Decisiones confirmadas

- Blender, animaciones, referencias y exportaciones: `/home/cacawatin/code/blender/chupacabras`.
- Aplicación AR Android: `/home/cacawatin/code/unity/chupacabras`, ahora con `Assets/`, `Packages/`, `ProjectSettings/`, `scripts/`, `docs/` y `builds/android/`. No hay Unity anidado en Blender.
- Editor exclusivo **6000.3.22f1**, revisión `1c726e1fb402`, invocado desde `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`. Su lanzador Vulkan preexistente y la instalación permanecen intactos; no se instaló/seleccionó otro Editor.
- Linux para desarrollo y compilación; no se modificó swap ni configuración global para resolver el fallo de memoria.
- Producción final de **40 s** según el plan; demo independiente de **35 s** conservada.
- Ventana anclada al marcador, escena 3D en tiempo real y cámaras internas; chupacabras original y oveja reutilizada con licencia adecuada.
- **M#[1] resuelta:** arrastre inicial a la izquierda y giro hacia salida derecha; ocultamiento desde aterrizaje hasta 25 s; ambiente y efectos sin música. Salto a los 20 s y duración de 40 s se conservan.
- AprilTag como candidato inicial, sin ARCore ni cambio de tecnología. Moto G20 obligatorio; S23 pendiente hasta prueba física propia.
- Diseño, cronología y referencias: [ficha de producción](ficha_produccion.md). Orientación final del stand, tamaño físico y calibración aún pendientes de preparación/prueba; no son nuevas decisiones solicitadas ahora.

## Cambios y motivo

- Organizadas cinco referencias y creada ficha/estado para evitar depender del historial. Actualizado el plan con las dos rutas, el máximo de dos pasos y M#[1].
- Añadida auditoría Blender `scripts/verificar_demos.py`, sin guardar escenas ni regenerar entregas.
- Creado proyecto Unity y configurado URP con los paquetes del Editor fijado. AprilTag **1.0.3**, revisión **fd6dd4698c9c6d2dc4a5e676beeab7f620006c78**, embebido sin modificar sus 62 archivos; licencias y procedencia conservadas.
- Preparados `DetectorSmokeTest`, `DiagnosticScreen`, `ProjectBuild` y `DiagnosticPreview`: prueba positiva/negativa de detección, pantalla de diagnóstico, build y evidencia visual. No implementan todavía cámara/seguimiento del paso 3.
- IL2CPP, stripping Low, ARM64 provisional, OpenGLES3, API mínimo 26/objetivo 35 y firma de depuración. JDK 17.0.18, NDK 27.2.12479018 y build-tools 36.0.0 existentes utilizados realmente.
- Primer build falló por OOM del proceso IL2CPP, confirmado por kernel. El script final limita trabajadores administrados mediante `DOTNET_PROCESSOR_COUNT=2` y `-job-worker-count 2`; caché Gradle local en `Library/`. Se usó afinidad temporal durante el diagnóstico, luego retirada; el script final no impone afinidad ni configura el sistema.
- Corregido el automatismo de captura para esperar callbacks de inicio con `EditorApplication.delayCall` antes de entrar en Play Mode; la captura final ya no presenta la excepción del indexador Search de las dos primeras pruebas.

## Entregas y evidencias

En Blender:

- `references/`: cinco imágenes verificadas contra sus originales; [procedencia y hashes](evidencias/2026-09-23_continuidad/referencias.json).
- [Auditoría Blender](evidencias/2026-09-23_continuidad/blender.log), [FFprobe](evidencias/2026-09-23_continuidad/video.json), [hashes previos](evidencias/2026-09-23_continuidad/entregas_previas.sha256) y [cierre de auditoría](evidencias/2026-09-23_continuidad/cierre.json).
- `docs/evidencias/2026-09-23_unity/`: creación del proyecto, inventario de herramientas, diagnóstico OOM, integridad y [verificación de APK](evidencias/2026-09-23_unity/apk_verificacion.json).

En `/home/cacawatin/code/unity/chupacabras`:

- [Preparación y reproducción](/home/cacawatin/code/unity/chupacabras/docs/preparacion_android.md).
- [APK de diagnóstico](/home/cacawatin/code/unity/chupacabras/builds/android/02_detector_20260923_205436.apk), **35 986 932 bytes** (34.3 MiB), con archivos `.build.txt`, `.licenses.txt` y `.sha256` acompañantes.
- SHA-256 APK: `0a150d6bd72390e8d20d9acb5d33ccb90d85ff826e23cfe7998be0e4646f51f9`.
- `Assets/Scenes/02_DetectorSmoke.unity`, fuentes y `.meta`; `Packages/manifest.json`, `packages-lock.json`, paquete embebido y `ProjectSettings/`.
- [Captura final del Editor](/home/cacawatin/code/unity/chupacabras/docs/evidencias/editor_diagnostic_20260923_211159.png), 321 × 531; no es captura del teléfono.
- `docs/evidencias/detector-editor.json`, `detector-playmode.json`, `build_20260923_205406.log`, `preview_inicio_diferido_20260923.log`, registros de intentos previos y `fuentes_sha256.json` con 113 archivos fuente.
- Se conserva el informe del primer intento fallido; no existe APK para ese intento. `BurstDebugInformation_DoNotShip` no es parte de la entrega a instalar.

## Pruebas ejecutadas y límites

- Auditoría inicial con Blender **5.2.2 LTS**: ambas escenas reabiertas; estática 328 objetos/1200 × 900; animada 342 objetos, 1–840 a 24 fps, 35 s y ataque a los 15 s. Contacto correcto en seis puntos (error máximo ≈1.2 × 10⁻⁷ unidades). No es revisión exhaustiva de todos los fotogramas.
- FFprobe: H.264, 640 × 480, 12 fps, 420 fotogramas y 35 s. Secuencia 0001–0420 completa. **428 archivos anteriores de Blender conservados por hash**, nuevamente comprobados en esta continuación.
- C# compilado por Unity. Prueba del detector ejecutada en preparación y Play Mode: **un ID 0, pose finita delante de cámara y cero detecciones sobre blanco**. Biblioteca Linux realmente cargada; las pruebas son sintéticas.
- Compilación Android final: **Succeeded, 0 errores y 0 advertencias de BuildReport**, 13 min 05.7 s. Primer intento OOM conservado y diagnosticado; no se confunde con incompatibilidad AprilTag.
- `apksigner verify`: firma v2 válida. `zipalign -c -P 16 4`: correcto. Ocho bibliotecas ARM64 con segmentos ELF LOAD ≥16 KB; incluye AprilTag, cuyo código `.text` coincide con el original tras eliminación de símbolos por Unity. No demuestra ejecución en Android de 16 KB.
- Manifiesto mínimo 26/objetivo 35, sin permiso CAMERA en esta prueba estática; permiso INTERNET de la build. Sin dependencias ARCore/AR Foundation ni ficheros ARCore encontrados en APK.
- Captura final inspeccionada: patrón y resultado legibles. Automatismo terminó con salida 0; la excepción de indexación no reapareció después del ajuste de inicio. Se conservan los logs anteriores. Avisos de login de servicios y cierre `build-server` no impidieron usar licencia, compilar ni capturar; no se instaló .NET global.
- `bash -n scripts/build_android.sh` correcto; sintaxis de los cuatro Python Blender comprobada en auditoría inicial. No había suite propia ni linter configurados. Las verificaciones del detector son código compartido entre Editor y APK.
- **No hay instalación ni ejecución en Moto G20/S23**, consulta ABI real, prueba de cámara, escala, estabilidad o rendimiento móvil. AprilTag no se adopta aún como viable para producción. No hay marcador físico validado ni corto final integrado.

## Acciones manuales

**M#[1] — Resuelta.** Respuesta explícita del usuario registrada arriba y en ficha/plan. No volver a preguntar.

**No hay solicitud manual activa al cierre.** No se pide conectar el teléfono con esta APK estática. La próxima acción se identificará **M#[2]** cuando el paso 3 tenga APK de cámara/seguimiento, marcador e instrucciones concretas; entonces se solicitarán acceso USB y prueba física. S23 continúa pendiente hasta estar disponible.

## Git

Recomprobado al cierre: ninguna raíz se reconoce como repositorio. `.git` de Blender está vacío y no es utilizable. No se inicializó ni reparó un repositorio; no se hizo commit ni push. Los hashes de fuentes y entregas permiten verificar la integridad del trabajo guardado.

## Punto exacto de reanudación y próximos dos pasos

1. **Retomar paso 2 en la aceptación pendiente de 2.4:** leer los informes existentes y conservar el proyecto/APK. La preparación y compilación ya pasaron; queda confirmar ABI real del G20. No repetir M#[1], recrear el proyecto ni regenerar las demos. No volver a fijar ARM64 como definitivo por conocer solo el procesador.
2. **Paso 3:** preparar captura de cámara, permiso y manejo de error, orientación/reflejo, proyección, cubo de tamaño conocido, marcador imprimible y APK de seguimiento. Con todo listo, abrir M#[2] para conectar/desbloquear el G20 y realizar la prueba. La consulta ABI cerrará la aceptación restante del paso 2 antes de instalar la combinación correspondiente. Medir pose/escala, pérdida/recuperación y margen para RenderTexture; registrar pruebas reales.

Esta dependencia se interpreta por subpasos: la APK mínima del paso 2 permite preparar la prueba del 3; la ABI se consulta al acceder físicamente al G20 como ya prevé 3.3. Ninguno de esos criterios físicos se declara completado ahora. La pareja siguiente es **2 retomado + 3**, sin avanzar al 4.
