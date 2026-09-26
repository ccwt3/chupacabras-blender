# Estado de continuidad

Actualizado: **23 de septiembre de 2026**, cierre de preparación de seguimiento. Estado comprobado con archivos, hashes, compilación y ejecuciones reales de Editor. **M#[2] pendiente; no hay validación física del G20 ni del S23.**

## Alcance y punto de partida

Aplicadas las instrucciones personales y la continuidad solicitada. No se encontraron `AGENTS.md` adicionales en las raíces/antecesores ni dentro de ambos proyectos. Se leyó el estado anterior y los cuatro documentos solicitados; se comprobó la APK 02 por hash, las 428 entregas/fuentes Blender registradas y la versión real del proyecto Unity.

La información Git del estado anterior había quedado obsoleta: Unity ya contiene un repositorio con commit inicial `ae14afe`, limpio al comenzar esta sesión. Blender no tiene repositorio utilizable; su `.git` no permite operaciones Git. No se inicializó ninguno.

Solo se trabajó en los pasos principales **2 retomado + 3**. Paso 2 continúa pendiente de ABI física; 3.1 preparado y probado de forma sintética. **No se inició el paso 4 ni la producción definitiva.** Estado anterior conservado en `docs/evidencias/2026-09-23_seguimiento/estado_anterior.md`.

## Pasos y subpasos

| Paso | Estado confirmado |
| --- | --- |
| 1.1–1.4 | Completados previamente: referencias, ficha y M#[1] resuelta. Archivos conservados. |
| 2.1–2.3 | Completados previamente: Unity/URP/AprilTag, licencia utilizable, diagnóstico estático y build Linux. |
| 2.4 | Build y binarios comprobados; **ABI real y aceptación física G20 pendientes**. ARM64 provisional. APK 02 intacta. |
| 3.1 | **Preparado:** cámara/permiso/pose, APK 03 compilada y verificada, marcador PDF/PNG/CeTZ y guía de prueba. |
| 3.2 | **Pendiente M#[2]:** acceso USB autorizado al G20. |
| 3.3 | Implementación y diagnóstico por ADB preparados; falta consultar modelo/Android/ABIs, instalar y ejecutar físicamente. |
| 3.4 | **Pendiente M#[2]:** imprimir/medir, conceder cámara y realizar movimientos/oclusiones. |
| 3.5 | Pruebas sintéticas completadas; **aceptación real pendiente** de pose, escala, recuperación y rendimiento. FOV inicial no calibrado. |
| 4–24 | Pendientes; ninguno iniciado en esta sesión. |

## Decisiones confirmadas

- Blender/animaciones/referencias/exportaciones: `/home/cacawatin/code/blender/chupacabras`.
- AR Android: `/home/cacawatin/code/unity/chupacabras`. No proyecto Unity anidado en Blender.
- Editor exclusivo **6000.3.22f1**, revisión `1c726e1fb402`, desde `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`. No instalar, actualizar ni seleccionar otro Editor sin autorización explícita. Linux para desarrollar y compilar; lanzador preexistente intacto.
- Producción definitiva de **40 s** según cronología del plan; demo independiente de **35 s** preservada.
- Ventana anclada al marcador, escena 3D en tiempo real y cámaras internas; chupacabras original y oveja reutilizada con licencia adecuada.
- **M#[1] resuelta:** arrastre inicial a izquierda y giro a salida derecha; ocultamiento desde aterrizaje hasta 25 s; ambiente/efectos sin música. Salto a 20 s y duración de 40 s conservados.
- AprilTag candidato inicial; sin ARCore ni cambio de tecnología antes de resolver la prueba. Moto G20 obligatorio; S23 pendiente hasta prueba física propia.
- Familia provisional `tagStandard41h12`, ID 0, lado de detección 100 mm y cubo 50 mm para esta prueba. No equivale al marcador final del stand ni a calibración confirmada.

## Cambios y motivo

En Unity:

- Añadida escena **03_TrackingProbe**, conservando escena/APK 02. App separada `com.chupacabras.ar.trackingprobe` 0.0.2/2 para no sustituir el diagnóstico anterior.
- `TrackingProbe`, `CameraGeometry` y `TrackingState`: cámara trasera, permiso/reintento, normalización de orientación/reflejo, proporción conservada, proyección común con detector y cubo de 50 mm. Oculta/pausa al perder ID 0 o tras 0.4 s sin frames; libera cámara al pasar a segundo plano y permite continuar. Poses sin suavizado para diagnosticar estabilidad.
- RenderTexture 512 × 288 con cubo giratorio y cámara separada, activable/desactivable para comparar costo mínimo. No integra el corto ni completa el paso 4.
- Registros CSV de estado, parámetros, pose y tiempos; capturas a petición. FOV 60° ajustable **provisional**. Sin intrínsecos físicos ni corrección de distorsión demostrados.
- `TrackingBuild`, `TrackingChecks`, `TrackingPreview`, `MarkerChecks` y scripts de build, marcador, verificación de APK y acceso/recogida G20. El script de instalación exige G20 autorizado, ARM64 y API ≥26 antes de instalar; no desinstala ni borra datos.
- PDF A4 editable CeTZ: original de 9 × 9 celdas verificado, dibujo 180 mm y cuadrado de detección 100 mm, regla y márgenes explícitos. Typst usado desde `/tmp`; sin instalación global.
- Evidencia de Editor redirigida a `docs/evidencias/editor_probe_<UTC>/`; Android guarda sus registros en datos propios de la app. El cambio de ruta posterior al build está bajo `UNITY_EDITOR`, no altera la implementación Android compilada.

En Blender: actualizados estado, plan y evaluación para reflejar preparación real y M#[2]; archivado estado previo y auditada integridad. No se modificaron escenas, animaciones, referencias ni demos.

## Entregas y evidencias

Raíz Unity:

- [APK 03](/home/cacawatin/code/unity/chupacabras/builds/android/03_tracking_20260923_213432.apk), **36 259 124 bytes**, SHA-256 `7b4f3fdd5c50c467fa4b4fc349399971affdb8f30ce21adc4fc3caaa1ac02000`. Informe `.build.txt`, hash y licencias acompañantes. ARM64 provisional; no instalada en teléfono.
- [Marcador A4](/home/cacawatin/code/unity/chupacabras/marker/03_marker_a4.pdf), `03_marker_a4.typ`, `03_marker_a4_preview.png`, original, `matrix_verification.json` y `SHA256SUMS`.
- [Guía de M#[2] y reproducción](/home/cacawatin/code/unity/chupacabras/docs/prueba_g20.md).
- `Assets/Scenes/03_TrackingProbe.unity`, fuentes/automatismos y `.meta`.
- `docs/evidencias/tracking_checks_20260923_213418.json`: 29 aserciones.
- `docs/evidencias/marker_checks_20260923_214021.json`: verificación del PDF rasterizado.
- `docs/evidencias/tracking_apk_verificacion.json`, `tracking_build_20260923_213405.log` y `tracking_configure_20260923_213405.log`.
- Capturas finales: `editor_tracking_20260923_214251_0.png` (visible), `editor_tracking_20260923_214252_1.png` (perdido), `editor_tracking_20260923_214253_2.png` (recuperado). Fuente **sintética en Editor**, no cámara/Android. Log `tracking_preview_local_20260923_2144.log`, CSV `editor_probe_20260923_214248_159/tracking.csv`.
- Primer juego de capturas y sus logs conservados. La escena guardada mantiene `syntheticPreview: 0`; el modo sintético se excluye de Android.

Raíz Blender:

- `docs/evidencias/2026-09-23_seguimiento/`: estado previo, integridad y cierre. Evidencias anteriores `2026-09-23_continuidad/` y `2026-09-23_unity/` conservadas.
- APK 02 intacta: SHA-256 `0a150d6bd72390e8d20d9acb5d33ccb90d85ff826e23cfe7998be0e4646f51f9`.

## Pruebas y limitaciones

- **428 archivos Blender** registrados previamente coinciden por SHA-256. No fue necesario regenerar ni volver a renderizar las demos; auditorías Blender/FFprobe anteriores siguen conservadas.
- C# compilado por Unity; prueba positiva/negativa previa del detector ejecutada nuevamente como parte de las comprobaciones 03. **29 aserciones**: imagen asimétrica en ocho combinaciones giro/reflejo, FOV, proporción, pérdida/recuperación, caducidad y segundo plano; cuatro giros de tag real con escala y orientación sintéticas.
- Matriz CeTZ idéntica al PNG original. PDF A4 de una página, revisado visualmente. Rasterización 849 × 1200 detecta solo ID 0 y pose compatible con los 100 mm previstos. **No es impresión medida.**
- Build Android: **Succeeded, 0 errores, 0 advertencias de BuildReport**, 5 min 05.97 s. Firma v2 válida; `zipalign -c -P 16 4` correcto; ocho bibliotecas AArch64 con LOAD ≥16 KB, incluida AprilTag. Mínimo API 26/objetivo 35; permiso CAMERA presente. La build de desarrollo también contiene INTERNET y permiso de receptor privado; no hay ARCore/AR Foundation añadido.
- Capturas automáticas y reloj: adquisición → pérdida/pausa → recuperación/continuación; salida 0. Capturas inspeccionadas. No hay excepciones de la app en el log; persisten avisos del servicio de login y cierre `build-server` del Editor que no impidieron compilar/capturar.
- Sintaxis Bash y Python verificada; no hay linter ni suite propia adicional configurados. Los tests técnicos se ejecutan mediante los métodos de Editor indicados en la guía.
- **Pendiente físico:** ABI, instalación, carga nativa Android, permisos/cámara, lente correcta, orientación/reflejo reales, intrínsecos/distorsión, escala, estabilidad, recuperación y rendimiento con RT. Los tiempos del Editor no son rendimiento móvil; la carga gráfica mínima no garantiza presupuesto para el corto. Ningún teléfono se declara compatible/validado todavía.

## Acciones manuales y preguntas

**M#[1] — Resuelta.** Guion/audio registrado arriba; no volver a preguntar.

**M#[2] — Pendiente, necesaria para continuar:** imprimir el PDF al 100 %, medir la regla/cuadrado de 100 mm; conectar y desbloquear el Moto G20, habilitar/autorizar depuración USB y conceder cámara; ejecutar el recorrido de orientación, distancias, inclinación, pérdida/recuperación y comparación RT de la guía. El agente consulta ABIs, instala, captura logs y diagnostica; no se trasladan comandos al usuario. APK, marcador e instrucciones ya preparados.

No hay decisiones creativas nuevas pendientes. Calibración/tamaño final/orientación del stand se resolverán con las pruebas correspondientes; no inventar resultados. S23 pendiente hasta estar disponible.

## Git

Unity: repositorio existente `ae14afe` como punto de partida, sin cambios ajenos al inicio. Commit de esta sesión **`897b36b`** (`897b36bb257b0f72e69d30aa88af9937baa0985d`), creado y comprobado; árbol de trabajo limpio, **sin push**. Solo se incluyen fuentes, ajustes locales, documentación, marcador y evidencias pertinentes; APK queda en `builds/` ignorado con hash registrado. Caché `.utmp` versionada previamente: cambios generados por build excluidos y conservados aparte; no se retira del historial.

Blender: no hay repositorio Git utilizable. No se inicializó; sus cambios quedan documentados y auditados por archivos/hashes. El identificador del commit Unity se registra en el cierre de esta sesión.

## Punto exacto para retomar y próximos dos pasos

**Detener aquí hasta respuesta de M#[2].** No se necesita redecidir el guion, recrear proyectos, cambiar Editor ni regenerar demos/APK por defecto.

1. **Retomar paso 2 en 2.4:** con G20 autorizado, consultar modelo/Android/ABIs y registrar evidencia; confirmar ARM64/API antes de instalar. Si no cumple, guardar diagnóstico y resolver esa combinación sin cambiar tecnología por iniciativa propia.
2. **Continuar paso 3 desde 3.2–3.3:** instalar APK 03 verificada, conceder cámara y seguir 3.4; analizar pose/escala, calibrar si procede y medir RT para aceptar o rechazar candidato en 3.5. Todavía no se puede declarar completado.

La próxima pareja sigue siendo **2 retomado + 3** porque la aceptación de 2.4 continúa abierta. El paso 4 queda fuera hasta una sesión posterior que respete dependencias y límite.
