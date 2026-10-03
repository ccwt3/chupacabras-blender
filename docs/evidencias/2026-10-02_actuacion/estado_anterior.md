# Estado de continuidad

Actualizado: **2 de octubre de 2026**, continuación de rig/aspecto demacrado
(logs también fechados 3 de octubre UTC).

**11 adaptado y verificado. 12.1 preparada; 12.2–12.3 pendientes de M#[6].**
Solo se ejecutaron **11 retomado + 12 retomado**. 13–24 no iniciados.

## Punto de partida comprobado

Blender partía de `eae3f25`, limpio; Unity de `b25a97a`, con tres cambios
ajenos preparados: `GraphicsSettings.asset`, `QualitySettings.asset` y
`PackageManagerSettings.asset`. Se leyeron estado, plan, evaluación AR,
demos y documentos técnicos; no se encontraron AGENTS.md adicionales en las
raíces/ancestros consultados. Se aplicaron las instrucciones de la conversación.

Las fuentes demacradas 08 R01/09 R02 y sus contextos R03 existían. El rig
anterior y APK 0.0.14 todavía usaban el modelo fornido. Se retomó exactamente
11.1, sin atribuir a M#[4] una prueba de la nueva malla. Estado anterior íntegro:
`docs/evidencias/2026-10-02_rigs_demacrado/estado_anterior.md`.

## Pasos y subpasos

- **1–10:** conservados, incluidos 8–9 revisados y oveja reutilizada/rig 10.
  No se amplía la aceptación física ni se inventa aprobación estética posterior.
- **11.1 completo:** pesos nuevos por posición, articulaciones adaptadas,
  23 huesos, mandíbula/cabeza/cuencas y dos influencias máximas por vértice.
- **11.2 completo:** contacto horneado y desplazamiento conjunto de seis
  segundos, con oveja R03 y sus diagonales conservadas. No es arrastre final.
- **11.3 completo:** reapertura Blender, importación Unity, deformaciones,
  contacto contra triángulos, apoyo y raíz AR independiente. 11.4 sin intervención.
- **12.1 completa:** escena demacrada R02, materiales/pipeline propios,
  tres estudios de luz, figura sobre el símbolo, panel lateral y APK 0.0.15.
- **12.2 pendiente M#[6]; 12.3 parcial:** verificaciones Editor/build completas;
  legibilidad y brillo reales por comprobar y corregir si procede. **12 no cerrado.**
  12.4 revisión estética opcional, sin decisiones creativas nuevas indispensables.
- **13–24 pendientes:** no se animaron calma/acecho, cámara continua ni salto final.

## Cambios y motivo

Fuentes nuevas de contacto y controles parten del acabado demacrado R02.
No se copian pesos/índices antiguos: contacto superior **174**, inferior **35**,
cuello **174**, seleccionados sobre la geometría correspondiente. Se ajustan
hombros, pelvis y nacimiento de cola al cuerpo nuevo. Las 18 mallas en reposo
coinciden exactamente con la fuente; oveja, triángulos y shape keys coinciden
con R03. Se conservan 30.880 + 612 triángulos y los 23 huesos del chupacabras.

Unity reemplaza la criatura en figura exterior, pastoreo y muestra de contacto,
conservando posición/rotación/escala de R05. Materiales propios mantienen piel
seca y cuencas oscuras. La primera revisión falló `Exterior layer`: el prefab
heredó la capa de cine. La sustitución ahora conserva también la capa del
objeto reemplazado; R02 pasó. R01 se conserva como diagnóstico, no entrega aceptada.

Generadores/verificadores existentes admiten fuentes nuevas y recuento de
triángulos por entrega; mantienen expectativas y destinos históricos por
defecto. No se cambiaron tolerancias para aceptar la nueva malla. Selección
opcional de escena/carpeta/versión en build de aspecto; sin cambios al runtime
AR, paquetes ni Editor. [Detalle y reproducción](rigs_demacrado.md).

## Entregas y evidencias

Blender: `/home/cacawatin/code/blender/chupacabras`:

- **`scenes/11_rigs_contacto_demacrado_r01.blend`** y
  **`scenes/11_rig_chupacabras_poses_demacrado_r01.blend`**.
- FBX/JSON homónimos en `exports/`; contacto adicional `_surface.json`.
- **`previews/11_rigs_contacto_demacrado_r01.mp4`**, 6 s, 960 × 540, 15 fps.
- Cuatro PNG de contacto; 90 PNG de vídeo regenerables excluidos de Git.
- `docs/evidencias/2026-10-02_rigs_demacrado/`: logs, referencias, informes Unity,
  hashes, comprobación reproducible de fuentes, FFprobe y estado anterior.
  El respaldo local `respaldo_unity/` queda fuera de Git.

Unity: `/home/cacawatin/code/unity/chupacabras`:

- `Assets/Rigs/11_*demacrado_r01.*` y escenas homónimas en `Assets/Scenes/`.
- **`Assets/Scenes/12_AppearanceAR_demacrado_r02.unity`**.
- **`Assets/Appearance12DemacradoR02/AppearanceStudy.prefab`**, materiales y URP.
- `docs/evidencias/2026-10-02_rigs_demacrado/`: capturas y pruebas de rigs.
- `docs/evidencias/2026-10-02_aspecto_demacrado_r02/`: tres planos internos,
  tres vistas exteriores, comparación de cámara y ejecución sintética.
- `docs/evidencias/2026-10-02_aspecto_demacrado_apk/`: firma, alineación, APK.
- `docs/evidencias/rigs_20261003_012606/`: regresiones existentes.
- **Guía M#[6]:** `docs/pasos11_12_demacrado.md`.

**APK nueva preparada, sin instalar:**
`builds/android/12_appearance_20261003_012410.apk`, **0.0.15**, 41.400.738 bytes,
SHA-256 `b10e73187f762d6691ecea2319fcb8f1676df37283531bee41d4bafaae5ae4a5`.
Paquete `com.chupacabras.ar.appearance12`, ARM64/IL2CPP.
La APK contiene estudios de iluminación, **no el corto definitivo**.

APK histórica 0.0.14 conservada: `builds/android/12_appearance_20260930_225854.apk`,
SHA-256 `4c4b33846b193684dd925fe9a162f3d2da8c52fe0aaba32994b0ce028b275551`.
Marcador conservado `marker/03_marker_carta.pdf`, SHA-256
`c670fc855c002dea0ad70c458db525b36dfcfff6e14400347bd0c7d1a47f1a83`.

## Pruebas, resultados y limitaciones

- Blender **5.2.2 LTS**: 181 cuadros por muestra nueva; duración seis segundos,
  pesos normalizados, sin áreas triangulares nulas, apoyo y coincidencia de
  superficies. Error contra referencias guardadas cero. Contacto máximo
  0,001016 mm; salto entre cuadros 19,74 mm, bajo umbral existente de 30 mm.
- Unity **6000.3.22f1**: contacto 259.735 puntos comparados, error de vértice
  máximo 0,02780 mm, contacto sobre lana máximo **0,001396 mm**. Controles:
  222.811 puntos, error máximo 0,009343 mm. Raíz AR independiente.
- Regresiones Blender: demos, rig oveja, controles antiguos y contacto R03
  correctos. Demo animada conserva 35 s y contacto. Regresiones Unity mediante
  `scripts/verify_rigs.sh`: las tres muestras anteriores pasan.
- Aspecto: geometría/capas/centrado correctos, tres planos y tres perspectivas;
  panel fuera del dibujo, píxeles internos idénticos al cambiar pose AR.
  Inspección visual de boca, poses, composición y los tres estudios realizada.
- Play Mode sintético: adquisición, pérdida, reloj detenido y recuperación
  correctos. 32 aserciones existentes de tracking pasan en rigs/aspecto.
- APK: BuildReport **0 errores / 0 advertencias**; firma, CAMERA, ARM64 y ocho
  bibliotecas ELF/empaquetado a 16 KB comprobados. Sin ejecución física nueva.
- FFprobe: H.264, 90 cuadros, 6 s. Python compila, Bash válido, clang-format
  y diff de código/documentación correctos. No hay suite/linter Python configurado.
- Los hitos/entregas históricos y tres configuraciones ajenas conservan sus
  hashes. El verificador antiguo reserializó escena 10: diff diagnóstico guardado
  y bytes originales restituidos. Cachés rastreadas `.utmp` también restituidas.
- Avisos de entorno GTK/Vulkan, SDL y cierre de PlayableGraph no impidieron los
  resultados finales. El fallo R01 de capa sí fue real y queda separado.
- **Sin prueba física de 0.0.15.** Costo de geometría nueva, brillo/legibilidad,
  calibración/FOV exactos, rendimiento sostenido, prueba física Android 16 KB y
  S23 pendientes. El aviso OpenGL aislado histórico no se considera resuelto
  por pruebas de escritorio. No se conectó ni instaló nada en el G20.

## Decisiones confirmadas y acciones manuales

- Dos raíces separadas: Blender/fuentes/animaciones y Unity/AR Android.
- Exclusivamente **Unity 6000.3.22f1** existente en
  `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`, desde Linux.
- Corto definitivo **40 s**, 30 fps, claves 1–1201 y captura 1–1200. Demo de
  **35 s** independiente. Efectos y ambiente sin música.
- Ventana 3D en tiempo real con cámaras internas: panel 16:9, 240 × 135 mm,
  RT 960 × 540, lateral vertical; figura estática de pie centrada sobre el tag.
  Su oclusión virtual del dibujo es intencional; detector usa cámara sin composición.
- Cámara del corto: continuidad anticipada 18,5–20,5 s, entrada lateral/detrás
  del granero, salto 20 s, aterrizaje 21,2 s, ocultamiento hasta 25 s y campo
  vacío 39–40 s. Arrastre izquierda y giro/salida derecha. Cámara AR independiente.
  Estos trabajos de actuación siguen pendientes; R04 histórico se conserva.
- Chupacabras original demacrado/esquelético/tenebroso preservando forma general;
  mayor geometría autorizada. Oveja Quaternius CC0, sin reconstruirla. Blender
  fuente, FBX métrico Generic, sin root motion, compresión de lana por blend shape.
  Conservar triangulación fija R03 para actuación/contacto.
- AprilTag se mantiene conforme a la prueba funcional y aceptación histórica
  documentada del G20; no ampliar ese alcance ni añadir ARCore/cambiar tecnología.
  G20 de pruebas; S23 solo exposición y pendiente hasta probarlo.
- Marcador tagStandard41h12 ID 0; 100 mm entre esquinas de detección y dibujo
  180 mm. FOV 60° provisional, sin calibración exacta.
- **M#[1] resuelta:** guion/audio. **M#[2] resuelta** para paso 3, medición
  adicional aplazada. **M#[3] resuelta:** Brother DCP-T510W/carta, trabajo 43 y
  medida física confirmados; no repetir impresión/medida sin necesidad.
- **M#[4] resuelta históricamente:** composición centrada/brillo de R05/0.0.14
  confirmados en G20; app retirada y limpieza verificada entonces.
- **M#[5] prevista para paso 20**, no solicitada.
- **M#[6] necesaria y pendiente:** conectar/desbloquear el G20 y observar esta
  APK 0.0.15 con la impresión existente durante tres estudios (18 s), moviendo
  suavemente la vista. Comprobar lectura de ojos, costillas, espinas, dientes,
  lana y brillo; figura centrada/panel lateral conservados. APK, marcador y
  guía listos. El agente instala, diagnostica, captura y retira la app al cerrar.
  No atribuir aceptación física al silencio ni a las capturas del Editor.
- Retirar lo instalado para pruebas y comprobar limpieza al terminar sigue
  siendo una instrucción expresa. No se necesita una decisión creativa nueva.

## Git y reanudación exacta

Unity: commit **`d8a173a`**, únicamente cambios propios; los tres ajustes ajenos
siguen preparados y excluidos. Blender: este estado y las entregas forman el
commit de cierre de la sesión. No se inicializan repositorios ni se hace push.

**Retomar exactamente en 12.2 / M#[6]** con APK 0.0.15 y escena demacrada R02.
Primero recibir acceso físico del G20, identificarlo e instalar la APK ya
verificada. Registrar legibilidad real, corregir únicamente fallos observados,
completar 12.3 y retirar la app con limpieza comprobada. No repetir decisiones
cerradas de posición, duración, tecnología ni impresión. No iniciar 13 antes
de resolver esta dependencia.

Próximos **dos pasos principales previstos**:

1. **12 retomado:** cerrar M#[6]/12.2–12.3 sobre la malla demacrada.
2. **13:** calma/acecho 0–20 s y anticipación continua de cámara, solo después
   del cierre físico de 12. No incluir 14 en esa misma sesión de dos pasos.

Esta sesión se detiene en la intervención física pendiente; no se ejecuta un
tercer paso. Para actuar después, usar `11_rigs_contacto_demacrado_r01.blend`,
el acabado `09_chupacabras_demacrado_r02.blend` y las diagonales R03 de la oveja.
