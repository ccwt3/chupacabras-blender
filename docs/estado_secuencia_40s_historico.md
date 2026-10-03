> **Archivo histórico del alcance cinematográfico, sustituido el 2 de octubre de 2026.**
> No usar sus próximos pasos o acciones manuales como tareas vigentes. Ver [plan actual](plan_secuencia.md) y [estado](estado.md).

# Estado de continuidad

Actualizado: **2 de octubre de 2026**, actuación 13–14 (logs del 3 de octubre UTC).

**13 y 14 completados técnicamente en R07. 12 físico / M#[6] aplazado por
instrucción expresa del usuario. 15–24 no iniciados.** Solo se ejecutaron
estos dos pasos principales; no se atribuye aceptación física al Editor.

## Punto de partida comprobado

Blender partía de `fb39a6d`, limpio; Unity de `d8a173a`, con tres cambios ajenos
ya preparados: `GraphicsSettings.asset`, `QualitySettings.asset` y
`PackageManagerSettings.asset`. No hay AGENTS.md adicionales en las raíces y
ancestros consultados; se aplicaron las instrucciones de la conversación.

Se leyeron estado, plan, evaluación AR y ambas demos. Se comprobaron las fuentes
reales del rig demacrado 11, escenario 06 y contexto 09; se reabrieron en Blender.
El estado anterior completo queda en
`docs/evidencias/2026-10-02_actuacion/estado_anterior.md`.
La petición actual sustituye el bloqueo previo de 13 por M#[6]; **aplazar no
significa aprobar 12**. Las dos raíces ya existían y se mantuvieron separadas.

## Pasos y subpasos

- **1–11 conservados**, incluida la adaptación demacrada de 11 y la oveja CC0
  triangulada R03. No se amplía el alcance de pruebas físicas históricas.
- **12.1 preparada** en R02/0.0.15. **12.2 aplazada / M#[6]**; **12.3 parcial**:
  pruebas Editor/build anteriores, brillo y legibilidad reales pendientes.
  12.4 revisión estética opcional. **12 no se cierra físicamente.**
- **13.1 completa:** pastoreo con variaciones, acecho, retirada y pasos;
  cuerpo/ojos ocultos desde 15 s. **13.2 completa:** cámara anticipada desde
  18,5 s y exportación de 0–20 s. **13.3 completa:** reapertura, importación,
  máscaras y vídeo. 13.4 revisión de ritmo opcional, no solicitada como bloqueo.
- **14.1 completa:** despegue a 20 s, entrada desde detrás del granero,
  trayectoria sobre/cerca de cámara, aterrizaje a 21,2 s, caída/forcejeo hasta
  25 s. **14.2 completa:** ocultación sin polvo y continuidad verificadas.
  **14.3 completa:** exportación/importación, cámara exterior independiente.
  14.4 revisión estética opcional; no se inventa aceptación del usuario.
- **15–24 pendientes:** arrastre 25–40 s, consolidación, Timeline, efectos,
  audio, conexión final al tracking, stand y pruebas/entrega Android.

## Cambios y motivo

`scripts/actuacion.py` reutiliza el rig demacrado y escenario existentes;
no cambia mallas, pesos ni licencias. Autoría a 30 fps, curvas horneadas y
compensación de apoyo. Genera dos hitos nuevos, con el mismo tramo 0–20 s,
y rechaza sobrescrituras. `scripts/verificar_actuacion.py` reabre las fuentes
y comprueba curvas, vértices, apoyo, edificio, salto y continuidad entre hitos.

La retirada retrocede antes de girar para despejar la cola. La cámara avanza
y eleva la mirada de forma continua para mostrar la entrada del salto; vuelve
al aterrizaje sin corte. La caída compensa su giro para mantener la oveja detrás
del atacante. R01–R06 son diagnósticos locales, conservados pero excluidos de
Git; sus logs/informes/capturas se versionan. R07 es la entrega.

Unity añade `ActingBuild.cs`, `scripts/verify_acting.sh` y recursos de revisión
propios. Reutiliza materiales demacrados y `RigPreview`, sin cambiar paquetes,
versión, seguimiento ni escenas anteriores. La búsqueda `SearchFall` midió 16
variantes sobre máscaras reales; se aplicó el resultado en Blender y se volvió
a exportar. El criterio de ocultación permaneció en **cero píxeles**.
[Detalle y reproducción](actuacion_13_14.md).

## Entregas y evidencia

Blender: `/home/cacawatin/code/blender/chupacabras`:

- **`scenes/13_calma_r07.blend`**, rango activo 1–601, **0–20 s**.
- **`scenes/14_ataque_r07.blend`**, rango 1–751, **0–25 s** con continuidad.
- FBX y JSON homónimos en `exports/`.
- **`previews/13_calma_r07.mp4`** y **`previews/14_ataque_r07.mp4`**.
- `docs/evidencias/2026-10-02_actuacion/`: estado anterior, hashes iniciales y
  finales, logs Blender, informes Unity copiados, vídeo y cierre verificable.

Unity: `/home/cacawatin/code/unity/chupacabras`:

- **`Assets/Scenes/13_calma_r07.unity`** y **`14_ataque_r07.unity`**.
- `Assets/Acting/`: FBX/JSON, RenderTextures y materiales de panel.
- `docs/evidencias/actuacion/13_calma_r07/` y `14_ataque_r07/`: pruebas,
  capturas internas/exteriores y PNG de vídeo regenerables excluidos de Git.
- `docs/pasos13_14_actuacion.md`: apertura, alcance y reproducción.

No se compiló una APK nueva: la aceptación de 13–14 pide previews importados.
La APK de aspecto preparada para M#[6] se conserva sin instalar:
`builds/android/12_appearance_20261003_012410.apk`, **0.0.15**,
SHA-256 `b10e73187f762d6691ecea2319fcb8f1676df37283531bee41d4bafaae5ae4a5`.
Marcador `marker/03_marker_carta.pdf`, SHA-256
`c670fc855c002dea0ad70c458db525b36dfcfff6e14400347bd0c7d1a47f1a83`.
Ambos hashes se comprobaron en esta sesión; guía `docs/pasos11_12_demacrado.md`.

## Pruebas, resultados y límites

- Blender **5.2.2 LTS**: reapertura de 601/751 cuadros, error cero contra las
  referencias, apoyo sin penetración apreciable y ningún vértice dentro del
  volumen conservador de paredes/techo. Coincidencia exacta del tramo común.
- Cámara: desplazamiento máximo 0,25279 m/cuadro y giro máximo 2,924°/cuadro;
  sin corte en 20 s. Despegue/aterrizaje en los límites previstos. La comprobación
  del edificio por vértices/volumen no es un solver exhaustivo de colisiones.
- Unity **6000.3.22f1**: compilación de scripts e importaciones correctas;
  751 muestras/297.396 puntos en ataque. Error máximo de deformación
  **0,05822 mm** y posición de cámara **0,01495 mm**.
- Máscaras **960 × 540**: 150 cuadros de criatura oculta (15–20 s) y 115 de
  oveja oculta (21,2–25 s, límite incluido), **cero píxeles expuestos**.
  Controles positivos: ojos 10 píxeles, oveja pastando 4.380, oveja sin atacante
  23.365. La ocultación usa profundidad real, sin partículas ni desactivaciones
  en las escenas entregadas. Cámara interna idéntica al mover la vista exterior.
- **32 aserciones existentes de tracking** pasan en ambas verificaciones.
  Demos reabiertas: estática correcta; animada conserva **35 s** y contacto.
- Python compila; Bash válido; clang-format y diff de código/documentación
  correctos. No se encontró otra suite/linter Python configurado.
- Vídeos H.264, **960 × 540, 15 fps**, 20 s/300 cuadros y 25 s/375 cuadros;
  FFprobe y capturas inspeccionadas. Son tramos de trabajo, no un corto de 40 s.
- Hitos históricos y tres configuraciones ajenas conservan sus hashes. Los
  avisos de entorno/PlayableGraph no impidieron los resultados finales;
  fallos reales de revisiones previas quedan identificados como diagnóstico.
- **Ninguna prueba física nueva.** No se conectó/instaló nada en el G20.
  Brillo/legibilidad, calibración/FOV, costo de nueva geometría, rendimiento
  sostenido, Android de 16 KB y S23 siguen pendientes de sus pruebas reales.

## Decisiones confirmadas y acciones manuales

- Blender/fuentes/animaciones y Unity/AR Android en las dos raíces indicadas.
  Exclusivamente Editor existente **6000.3.22f1**, desarrollo/compilación Linux.
- Producción definitiva **40 s**, 30 fps; demo **35 s** independiente.
  Los previews actuales de 20/25 s no cambian esos acuerdos.
- Ventana 3D en tiempo real, cámaras internas y raíz AR independiente;
  figura estática centrada sobre el tag y panel lateral 240 × 135 mm.
  El detector recibe cámara sin composición; oclusión virtual de figura intencional.
- Chupacabras original demacrado, oveja Quaternius CC0, fuente Blender/FBX
  métrico Generic, sin root motion y lana por blend shape. Triangulación R03.
- AprilTag se conserva con el alcance físico histórico del G20; no ARCore.
  S23 solo exposición y pendiente hasta probarlo. Tag Standard41h12 ID 0,
  100 mm entre esquinas y dibujo 180 mm; FOV 60° provisional.
- Salto 20 s, aterrizaje 21,2 s y ocultamiento hasta 25 s. Arrastre izquierdo,
  giro/salida derecha y campo vacío 39–40 s pendientes del paso 15.
  Ambiente/efectos sin música; no se implementaron audio ni polvo en esta sesión.
- **M#[1] resuelta:** guion/audio. **M#[2] resuelta** para paso 3; medición
  adicional aplazada. **M#[3] resuelta:** impresión carta/medida física.
- **M#[4] resuelta históricamente:** composición/brillo de R05/0.0.14 en G20;
  su aceptación no valida la malla demacrada ni estas animaciones.
- **M#[5] prevista para paso 20**, no solicitada.
- **M#[6] aplazada por el usuario:** revisar aspecto demacrado de APK 0.0.15
  sobre el marcador existente en G20 (ojos, costillas, espinas, dientes, lana,
  brillo y composición). Permitirá cerrar 12.2–12.3 cuando se retome. APK,
  marcador y guía listos; **no se solicita conexión ahora**. El agente instala,
  diagnostica y retira lo instalado al cerrar, verificando limpieza.
- No hay una nueva decisión creativa indispensable ni preguntas sin responder.
  El aplazamiento no aprueba el resultado físico por silencio.

## Git y punto exacto de reanudación

Ambos repositorios ya existían. Unity: commit **`d74fae0`**, solo cambios propios;
los tres ajustes ajenos siguen preparados y excluidos. Blender: este estado y
las entregas forman el commit de cierre de la sesión. Identificador en el
reporte final/historial. Sin push. Evidencia: `cierre.json` e integridad final.

**Retomar en 15.1**, usando `14_ataque_r07.blend` en el fotograma **751 / 25 s**.
Resolver agarre sobre superficie, apoyo, peso y arrastre, sin reciclar la muestra
11 como actuación final. Conservar la cámara interna y los primeros 25 s
validados. M#[6] continúa aplazada, sin marcar 12 completo.

Próximos **dos pasos principales previstos**, sujetos a la siguiente solicitud:

1. **15:** agarre/arrastre 25–40 s, izquierda, giro/salida derecha y campo vacío.
2. **16:** consolidar/exportar los 40 s, solo después de aceptar técnicamente 15.

Si se reanuda 12 físico antes, ese paso retomado contará como el primero de
esa sesión. No ejecutar un tercero. No repetir decisiones ya confirmadas.
