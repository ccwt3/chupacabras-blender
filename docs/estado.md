# Estado de continuidad

Actualizado: **3 de octubre de 2026 — F1 y F2 completadas en su alcance técnico**.
[Plan F1–F7](plan_secuencia.md) · [Entrega y reproducción F1–F2](figura_ar_f1_f2.md) ·
[Ficha](ficha_produccion.md) · [Estado anterior](evidencias/2026-10-03_figura/estado_anterior.md).

**Próxima pareja: F3 + F4. No iniciadas en esta sesión.**
La figura estática AR sigue vigente: **M#[9] resuelta** por el usuario, que
aclaró que el bloque del corto de 40 s era una plantilla anterior. No retomar
arrastre, ventana cinematográfica ni prueba física histórica M#[6].

## Punto de partida y alcance comprobados

Dos repositorios existentes, ambos en `main`, al iniciar esta sesión:
Blender `38350be`, Unity `e23cae4`. No se encontraron AGENTS.md locales
aplicables; se siguieron las instrucciones personales proporcionadas.
Blender estaba limpio. Unity tenía preparados tres cambios ajenos:
`ProjectSettings/GraphicsSettings.asset`, `QualitySettings.asset` y
`PackageManagerSettings.asset`; se conservan y excluyen del commit.

Las fuentes demacradas, rigs, actuaciones 13–14 y demos existen. Los hashes
de la APK histórica 0.0.15 y el marcador coinciden con el estado anterior.
El ejecutable Unity exclusivo existe y `ProjectVersion.txt` indica
**6000.3.22f1**. No existía entrega F1/F2 antes de esta sesión.
Inventario/hashes iniciales: [inicial.json](evidencias/2026-10-03_figura/inicial.json).

Acuerdos conservados: Blender como fuente, Unity/AR en la segunda raíz,
Android desde Linux, AprilTag existente sin ARCore, G20 de pruebas, S23
pendiente de acceso y figura original demacrada centrada sobre el tag.
Sin ventana, oveja, escenario, ataque ni requisito de 40 s. Figura estática,
sin idle, autorrotación o efectos añadidos. Demos e hitos anteriores conservados.

## Etapas y subpasos

- **F1 completada técnicamente.** Ruta explícita de figura estática en
  `TrackingProbe`; escena/prefab y materiales propios; UI adaptada; cámara,
  detector y estados compartidos. Tres composiciones, checks históricos,
  ocho estados de runtime, regresión histórica y APK propia comprobados.
  BuildReport revisado: sin assets del corto. No acredita prueba física nueva.
- **F2 completada como revisión de forma/pose.** Nueva fuente **R04**,
  rostro/mandíbula/cresta/garras revisados, pose asimétrica, cuatro apoyos,
  seis vistas equivalentes a la base y giro. Reapertura/topología comprobadas.
  Valoración visual del agente registrada; no equivale a aprobación estética
  del usuario ni acabado realista final. Si llega una objeción, resolverla
  antes de F3. La aceptación visual móvil sigue en F5.
- **F3 pendiente:** malla exportable móvil, UV, acabado de superficie,
  materiales/texturas y licencias. Fuente F2 de 88.952 triángulos sin presupuesto
  móvil aprobado; no transferir ese conteo como objetivo de rendimiento.
- **F4 pendiente:** integrar la malla preparada en el prefab propio y ajustar
  materiales/luz; candidata Android nueva. La APK F1 usa aún la base demacrada R02.
- **F5 pendiente:** revisión física y rendimiento en G20, M#[7].
- **F6 pendiente:** correcciones y regresión sobre esa evidencia.
- **F7 pendiente:** entrega reproducible; posible S23 M#[8] cuando esté disponible.

Se trabajaron exactamente dos etapas principales: **F1 + F2**.

## Entregas y evidencia

En Blender:

- `scenes/F2_chupacabras_forma_r04.blend`: fuente actual de forma.
- `previews/F2_chupacabras_forma_r04/`: seis vistas de base y revisión,
  [comparación](../previews/F2_chupacabras_forma_r04/comparacion.png),
  [resumen visual](../previews/F2_chupacabras_forma_r04/seis_vistas.png),
  [giro MP4](../previews/F2_chupacabras_forma_r04/giro.mp4), métricas y checks.
- `scripts/figura_forma.py`, `verificar_figura_forma.py`, `resumen_figura.py`:
  reproducción sin sobrescribir entregas. R01–R03 y frames se conservan
  localmente; fuente/evidencia final y logs de los intentos quedan versionados.

En `/home/cacawatin/code/unity/chupacabras`:

- `Assets/Scenes/F1_FiguraAR_r01.unity` y `Assets/FiguraAR/F1_r01/Figure.prefab`.
- `Assets/Editor/FigureBuild.cs`, `FigurePreview.cs`, `scripts/build_figure.sh`,
  `verify_figure_apk.py`: construcción y comprobación independientes.
- APK **0.1.0**, `builds/android/F1_figure_20261003_162413.apk`, 38.200.938 bytes.
  SHA-256 `48f1adf50143ed4c9fa83134a68316529752a12b4e93a50f0b801faca25e5cd5`.
  Paquete `com.chupacabras.ar.figure`; conserva el modelo R02, no F2.
- `docs/evidencias/F1_20261003_162304/`: capturas/checks de escena/runtime,
  BuildReport/dependencias, verificación APK y regresión de la escena antigua.
- Marcador sin cambios: `marker/03_marker_carta.pdf`,
  SHA-256 `c670fc855c002dea0ad70c458db525b36dfcfff6e14400347bd0c7d1a47f1a83`.
  Reutilizar la impresión carta ya medida: tagStandard41h12, ID 0,
  100 mm de detección, dibujo 180 mm.

## Cambios, pruebas y límites

[Informe de cambios y reproducción](figura_ar_f1_f2.md). F1 separa presentación
sin duplicar tracking; F2 mejora forma manteniendo identidad y fuentes anteriores.

- Unity **6000.3.22f1**: 32 checks existentes; ocho estados sintéticos correctos,
  misma instancia/escala, sin reloj narrativo ni ruta de cine en la escena nueva.
  Regresión histórica de adquisición/pérdida/reanudación aprobada en Editor.
- APK: BuildReport con cero errores/advertencias, firma y permiso de cámara,
  ARM64 y alineación ELF de ocho bibliotecas comprobados. Sin recursos de
  oveja/escenario/actuación/Timeline en la lista empaquetada. Metadatos de scripts
  históricos siguen en el ensamblado compartido; no se instancian en F1.
- Blender **5.2.2 LTS**: reapertura independiente; 88.952 triángulos, 18 mallas
  cerradas, cuerpo/cráneo continuos, dientes/garras unidos a sus soportes,
  apoyo asimétrico y geometría por encima del plano. Juicio visual separado.
- Seis vistas inspeccionadas y giro H.264 verificado: 720×540, 12 fps,
  72 fotogramas, seis segundos. Workbench sirve para evaluar forma, no materiales.
- Sintaxis Python y shell comprobadas; `git diff --check` de archivos de la
  sesión. No hay linter o suite general Blender configurados.
- **Sin teléfono, instalación ni prueba física**. No hay medición nueva de fps,
  brillo o estabilidad real. UV/materiales finales y malla móvil siguen pendientes.
- Verificación de preservación y alcance:
  [verificacion.json](evidencias/2026-10-03_figura/verificacion.json).

La build regeneró archivos temporales `.utmp` ya versionados; se restauraron
solo los que coincidían con los hashes iniciales/HEAD. Configuración y paquetes
previos conservados; no se incluyeron cambios ajenos. Commit por repositorio,
sin push, conforme a la solicitud de esta sesión.

## Acciones manuales

- **M#[1]–M#[4]:** cierres históricos, con los límites ya registrados.
- **M#[5]:** antigua prueba del corto integrado, sustituida, nunca aprobada.
- **M#[6]:** antigua revisión 0.0.15, sustituida sin validación física.
- **M#[7]:** prueba de nueva figura en G20, futura F5–F7, no solicitada.
- **M#[8]:** posible S23 en exposición, futura y no solicitada.
- **M#[9]: resuelta.** Usuario confirmó continuar figura AR F1–F2; la plantilla
  del corto era anterior. No queda pregunta pendiente ni bloqueo manual actual.

## Punto exacto de retoma

1. **F3:** leer este estado y revisar la fuente **F2 R04** y sus seis vistas;
   resolver cualquier objeción recibida. Crear salidas nuevas para malla móvil,
   UV, superficie/texturas PBR y FBX estático. Conservar R04 como fuente de forma.
   Medir geometría/materiales/memoria sin asumir que 88.952 triángulos sea un
   presupuesto aprobado. Registrar autoría/licencias. No rehacer el motor AR.
2. **F4:** integrar la exportación F3 en una nueva revisión de figura AR,
   manteniendo escena/APK F1 como referencia. Comprobar materiales, luz,
   centrado y seis vistas Blender/Unity, y compilar candidata propia con hash.

Detenerse tras F3 + F4. No iniciar F5 ni pedir teléfono por adelantado.
Preparar APK, marcador, instrucciones y resultados concretos antes de M#[7].
No interpretar silencio como aprobación ni borrar escenas para reducir la build.
Actualizar este estado canónico; Unity conserva su enlace.
