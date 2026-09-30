# Estado de continuidad

Actualizado: **30 de septiembre de 2026, hora local de México**.
**Paso 12 en curso: 12.1 preparado; 12.2 bloqueado por M#[4] física.**
**13–24 no iniciados.** Se trabajó un solo paso principal de la pareja 12–13;
no se avanzó al segundo porque depende de la revisión física del primero.

## Punto de partida comprobado

Se leyeron las instrucciones personales, estado, plan completo, evaluación AR
y documentos de ambas demos. No se encontraron AGENTS.md adicionales aplicables.
Se comprobaron los nueve hashes de entregas de rigs del cierre anterior y se
registraron **844 archivos históricos** de escenas, exportaciones, previews,
referencias y assets. Todos conservan sus bytes. Las demos se reabrieron en
Blender 5.2.2 LTS: 328 objetos en la estática y 35 s/contacto en la animada.

**Ambas raíces tienen ahora Git utilizable**, a diferencia del estado anterior.
Blender comenzó en `4e2d007`; Unity en `0f38435`. En Unity ya estaban preparados
en el índice GraphicsSettings, QualitySettings y PackageManagerSettings. Se
conservan byte por byte y se excluyen de los commits de esta sesión.
Estado anterior: `docs/evidencias/2026-09-30_visual/estado_anterior.md`.

## Pasos y subpasos

- **1–11 conservados** con su alcance y limitaciones anteriores. Contacto vigente:
  R03 de paso 11; ni la muestra de 6 s ni la de oveja de 8 s son el corto final.
- **12.1 preparado:** escena AR nueva, materiales URP, luz nocturna, figura
  exterior estática y panel con tres muestras de luz. APK compilada y verificada.
- **12.2 / M#[4] pendiente:** acceso al G20 y revisión física de brillo, tamaño,
  perspectiva y tag descubierto. No existe aceptación física de esta APK.
- **12.3 pendiente:** recoger evidencia física, contrastarla y corregir lo necesario.
- **12.4 opcional:** preferencias estéticas que surjan de la revisión.
- **13–24 pendientes, sin iniciar.** La cámara continua y actuación 0–20 s
  del paso 13 no se trabajaron; se respetó la dependencia del paso 12.

## Cambios y motivo

Unity contiene `12_AppearanceAR.unity` y `AppearanceStudy.prefab` nuevos.
La figura exterior procede del acabado 09; escenario 06 y rigs 10/11 proporcionan
las muestras interiores. Materiales mate, ojos amarillos, sombras duras de 1024
y rellenos independientes permiten revisar lectura sin añadir postprocesado.
Pipeline y materiales propios conservan los anteriores. La ventana mide
240 × 135 mm y renderiza a 960 × 540; figura a la izquierda, panel a la derecha.

`TrackingProbe` conecta opcionalmente esta muestra a su seguimiento existente,
sin cambiar detector, FOV ni tecnología. Ambos elementos comparten una raíz;
la escena/cámara interna permanecen independientes. Tres poses de luz alternan
cada seis segundos: no son actuación final ni un cambio de los 40 s acordados.
El paquete `com.chupacabras.ar.appearance12` es independiente de la prueba 03.

Se corrigieron pérdida de rotación de ejes FBX en figura estática, exceso de
relleno exterior y encuadres mediante capturas. El primer intento de captura
asíncrona en batch agotó el tiempo; se reemplazó por render explícito de cámara
en Play Mode, ajustando el viewport al tamaño de la evidencia. Iteraciones
conservadas. No se cambiaron fuentes Blender, demos ni configuración global.
Detalles: [materiales_iluminacion.md](materiales_iluminacion.md) y
[guía Unity](/home/cacawatin/code/unity/chupacabras/docs/paso12_aspecto.md).

## Entregas y evidencias

Blender: `/home/cacawatin/code/blender/chupacabras`.

- `docs/materiales_iluminacion.md`, plan y este estado actualizados.
- `docs/evidencias/2026-09-30_visual/`: estado anterior, hashes iniciales,
  verificación de entregas, reapertura de demos, informes Unity/APK y cierre.
- Sin nueva escena Blender: este subpaso reconstruye materiales en Unity.

Unity: `/home/cacawatin/code/unity/chupacabras`.

- `Assets/Scenes/12_AppearanceAR.unity`, `Assets/Appearance12/` (prefab/materiales/URP).
- `AppearanceStudy.cs`, `AppearanceBuild.cs`, `AppearancePreview.cs` y extensión
  opcional de `TrackingProbe.cs`; scripts de build y verificación de APK.
- **APK:** `builds/android/12_appearance_20260930_223107.apk`, **38.676.908 bytes**.
  SHA-256: `5f96b6b3632ab7f07f72d64d5b89e00664509263e54a49d0b0553aa473f7ae07`.
- **Marcador conservado:** `marker/03_marker_carta.pdf`; reutilizar la impresión
  carta previamente medida. No se pidió ni realizó otra impresión.
- **Guía física:** `docs/paso12_aspecto.md`, apartado M#[4].
- **Aspecto/composición vigente:** `docs/evidencias/appearance_20260930_222740/`,
  `cinema_0..2.png`, `composition_front/left/right.png` y `checks.json`.
- **Ejecución sintética vigente:** `docs/evidencias/2026-09-30_visual/runtime03/`.
- Compilación/firma/alineación: `docs/evidencias/2026-09-30_visual/`.
  No usar el `runtime.json` fallido de `appearance_20260930_222740` como cierre;
  runtime03 lo sustituye. runtime02 pasó estados pero su captura tenía proporción
  incorrecta; también queda como diagnóstico.

## Pruebas y límites

- Unity **6000.3.22f1**: C# compilado; APK IL2CPP/ARM64 con **0 errores / 0
  advertencias de BuildReport**. Firma, permiso CAMERA y empaquetado verificados.
  Ocho bibliotecas ELF y ZIP alineados a 16 KB; ejecución física de 16 KB pendiente.
- **32 aserciones de tracking** existentes correctas. La escena original 03
  pasó también adquisición/pérdida/recuperación en Play Mode. Tres vistas internas y
  tres exteriores revisadas. Los límites proyectados de cada mesh exterior dejan
  libre un cuadrado de 220 mm (dibujo 180 + 20 mm de margen por lado) en las tres
  vistas de referencia. No garantiza cualquier ángulo ni sustituye el G20.
- Cámara interna: píxeles idénticos al cambiar pose exterior. Play Mode con
  detector real sobre imagen sintética: adquisición, ocultación conjunta, reloj
  detenido y recuperación correctos. No es seguimiento físico.
- Dos demos reabiertas; sintaxis de los 19 scripts Blender correcta. Scripts
  Bash verificados; clang-format de C# nuevo correcto. Sin otro linter configurado.
- **844 archivos históricos intactos** y tres configuraciones ajenas intactas.
  Fuentes, exports, APK y evidencia anteriores conservados.

**No se conectó, instaló ni retiró ninguna app del teléfono en esta sesión.**
Siguen pendientes la lectura/brillo G20 de este paso, calibración exacta/FOV,
costo del corto completo, cinco minutos sostenidos, APK 0.0.5 física, Android
16 KB en ejecución y S23. Los resultados de Editor no amplían aceptación móvil.

## Decisiones confirmadas y acciones manuales

- Dos raíces separadas: Blender/fuentes/animaciones y Unity/AR Android.
- Exclusivamente **Unity 6000.3.22f1**, instalación existente
  `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`, desde Linux.
- Corto definitivo **40 s**, 30 fps, claves 1–1201, captura 1–1200. Demo de
  35 s independiente, conservada.
- Ventana cinematográfica anclada al marcador: escena 3D en tiempo real,
  cámaras internas, 16:9, dimensión provisional 240 × 135 mm, RT 960 × 540.
- **Composición híbrida solicitada:** sumar al panel lateral una figura 3D
  estática del chupacabras, anclada a la misma pose AprilTag y vista por la
  cámara exterior AR. Mover el teléfono cambia su perspectiva; la animación
  ocurre dentro de la ventana con su cámara interna. Preparación técnica del paso
  12 realizada en una build nueva; escala/separación
  y visibilidad física de esquinas/márgenes pendientes de M#[4]. Las escenas
  08–09 conservan su función de revisión de modelos.
- **Cámara del corto:** rehacer el corte brusco del bloqueo en escenas nuevas
  13–14 con anticipación continua alrededor de 18,5–20,5 s y entrada lateral o
  detrás del granero. Se conserva el salto a 20 s y la cámara AR. R04 sigue como
  hito histórico y no se modifica.
- Chupacabras original; oveja reutilizada Quaternius CC0. Blender fuente,
  FBX métrico Generic, sin root motion; compresión de lana mediante blend shape.
  Para contacto/actuación, conservar triangulación fija de la oveja R03.
- Ruta AprilTag heredada y alcance funcional previo del G20 conservados;
  mediciones reales pendientes sin ampliación de aceptación. Sin ARCore ni
  cambio de tecnología. G20 para pruebas; S23 solo exposición, aún sin probar.
- Marcador tagStandard41h12 ID 0, 100 mm entre esquinas de detección, dibujo
  180 mm; cubo 50 mm y FOV 60° provisional sin calibración exacta.
- **M#[1] resuelta:** arrastre izquierda, giro/salida derecha, salto 20 s,
  aterrizaje 21,2 s, ocultamiento hasta 25 s, campo vacío 39–40 s; efectos y
  ambiente sin música.
- **M#[2] resuelta para paso 3:** alcance físico anterior aceptado y medición
  adicional aplazada. No repetir esa solicitud para continuar producción.
- **M#[3] resuelta:** Brother DCP-T510W, carta/trabajo 43 y regla de 100 mm
  confirmados previamente; no se reimprimió ni se pidió medir/conectar teléfono.
- Mantener aviso de acciones manuales y retirar lo instalado para pruebas al
  terminar. No se instaló nada en el teléfono en esta sesión.
- **M#[4] pendiente y necesaria:** conectar/desbloquear el G20 cuando se retome,
  aceptar USB/cámara si se solicita y revisar las tres muestras conforme a la guía.
  Debe confirmar lectura de ojos/espinas/lana/sombras, tamaño relativo, perspectiva
  exterior y dibujo/márgenes libres. APK, marcador e instrucciones están listos.
  El agente instalará, recogerá logs/capturas y retirará la app propia al terminar.
- **M#[5] prevista para paso 20**, no solicitada. No sustituirla por pruebas de Editor.
- Sin nuevas decisiones creativas pendientes. La revisión estética adicional es opcional.

## Git y reanudación exacta

Unity: commit **`296e1c7a2a27ab1fcb0db5f79767d2175201d0ce`**.
Blender: este estado y su evidencia se incluyen en el commit de cierre de sesión
(ver `git log -1`). Solo cambios propios; sin push. Los tres cambios ajenos
preparados en Unity permanecen excluidos. La caché `.utmp` rastreada que regeneró
el build se restituyó a su estado previo.

**Retomar exactamente en 12.2 / M#[4]** con la APK y guía indicadas. Antes de
instalar, comprobar dispositivo autorizado y modelo/ABI; no recompilar ni pedir
reimprimir por defecto. Obtener la revisión física y completar 12.3; si requiere
ajustes, preparar una nueva APK y repetir solo los casos afectados. No cerrar 12
ni iniciar 13 mientras falte esa evidencia.

Próximos dos pasos principales previstos:

1. **12 retomado:** revisión G20 M#[4], evidencia y ajustes de materiales/composición.
2. **13:** calma y acecho 0–20 s, anticipación continua de cámara; únicamente tras
   cerrar 12. Después detenerse, sin iniciar 14 en esa pareja.
