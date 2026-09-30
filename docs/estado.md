# Estado de continuidad

Actualizado: **30 de septiembre de 2026**, continuación física M#[4].
**Paso 12 cerrado; M#[4] resuelta. 13–24 no iniciados.**
Solo se trabajó el paso 12 retomado y la limpieza solicitada.

## Punto de partida y comprobación

Se retomó la APK 0.0.12 desde Blender `5bd5b38` y Unity `296e1c7`, leyendo estado,
guía de aspecto e informe APK. El hash coincidió antes de instalar. El G20 fue
identificado por ADB: Android 11/API 30, ARM64 y páginas de 4096 bytes. No había
paquetes `com.chupacabras` instalados antes de esta prueba.

Ambas raíces mantienen Git. Los tres ajustes ajenos ya preparados en Unity
(GraphicsSettings, QualitySettings y PackageManagerSettings) se conservan y
quedan excluidos del commit. Las demos y entregas Blender no se modificaron.
Estado anterior: `docs/evidencias/2026-09-30_g20_m4/estado_anterior.md`.

## Pasos, correcciones y motivo

- **1–11 conservados**, sin ampliar su aceptación previa.
- **12.1:** APK inicial instalada y capturada; el marcador físico fue detectado.
  La figura se veía recostada y el panel miraba arriba sobre el papel horizontal.
- **12.2, iteraciones previas:** usuario confirmó ese error. R04/0.0.13 corrigió orientación
  y elevó el panel. La segunda revisión física mejoró, pero el usuario aclaró
  que quería la figura **directamente encima del símbolo**, no hacia el borde
  superior del papel. Esa decisión queda confirmada, sin volver a preguntarla.
- **12.1 revisado:** R05/0.0.14 centra el origen de la figura en el origen del tag,
  de pie sobre su plano. Panel vertical a la derecha. La superposición virtual
  de la figura es intencional; el detector lee la imagen original de cámara.
- **12.2 cerrada / M#[4] resuelta:** 0.0.14 instalada y observada en el G20. El
  usuario confirmó «Sí, ahora está como quería» a ubicación y lectura.
- **12.3 cerrada para aspecto:** capturas/logs reales, correcciones y pruebas
  verificadas. No hubo aviso OpenGL ni excepciones C# en el último registro.
  El aviso aislado de 0.0.13 conserva seguimiento diagnóstico posterior.
- **13–24 no iniciados.** La ventana muestra tres vistas de iluminación de dos
  situaciones (pastoreo/agarre), no la animación definitiva. Se aclaró al usuario.

Fuentes originales y todas las revisiones se conservan. R02/R03/R04 son
iteraciones de diagnóstico; **R05 es la entrega vigente**. La prueba geométrica
ahora usa triángulos proyectados y un cuadrilátero para el margen del panel;
la figura está exenta de esa exclusión por la colocación explícita del usuario.
Se comprueba que su origen esté exactamente centrado en el marcador.

## Entregas y evidencia

Unity: `/home/cacawatin/code/unity/chupacabras`.

- `Assets/Scenes/12_AppearanceAR_r05.unity` y
  `Assets/Appearance12/AppearanceStudy_r05.prefab`.
- `Assets/Editor/AppearanceBuild.cs` y scripts de build/verificación actualizados.
- **APK 0.0.14:** `builds/android/12_appearance_20260930_225854.apk`, 38.676.888 bytes.
  SHA-256: `4c4b33846b193684dd925fe9a162f3d2da8c52fe0aaba32994b0ce028b275551`.
  Sigue siendo una revisión del **paso 12**, no ejecución del paso 14.
- `marker/03_marker_carta.pdf` conservado; se usó el marcador previamente impreso.
- Informe: `docs/prueba_aspecto_g20.md`; guía `docs/paso12_aspecto.md`.
- Evidencia física: `docs/evidencias/g20_aspecto_20260930_224133/`.
  Logs de instalación/arranque 0013/0014 identifican cada revisión.
- R05: `docs/evidencias/appearance_20260930_225754/` y
  `docs/evidencias/apk_12_appearance_20260930_225854/`.
- R04: `appearance_20260930_224859`; R02/R03 y verificaciones fallidas conservadas.

Blender: fuentes y animaciones intactas. Plan y estado actualizados con la
colocación aclarada. Resumen/evidencia en `docs/evidencias/2026-09-30_g20_m4/`.

## Pruebas, resultados y limitaciones

- Unity **6000.3.22f1** desde Linux: APK 0.0.13 y 0.0.14 con **0 errores y
  0 advertencias de BuildReport**. Firma, CAMERA, ARM64 y ocho ELF/ZIP alineados
  a 16 KB verificados. El G20 usa páginas de 4 KB; ejecución física 16 KB pendiente.
- C# compilado, clang-format y sintaxis Bash correctos. **32 aserciones existentes
  de tracking** pasan, más separación de cámaras, colocación y adquisición/
  pérdida/pausa/recuperación sintéticas. Capturas nuevas inspeccionadas.
- 0.0.12 y 0.0.13 detectaron el marcador físico y mostraron la composición.
  R04 acumuló 61,236 s de reloj visible en lo registrado. Su posición fue rechazada
  por el usuario; no constituye aceptación de la colocación final R05.
- R04 registró **un aviso nativo `GL_INVALID_OPERATION`**, sin excepción C# ni
  repetición en ese registro. Causa no resuelta; no se declara corregido. Mediana
  de `frame_ms` suavizado con seguimiento: **42,265 ms**. No son tiempos GPU ni
  prueba de 30 fps sostenidos; rendimiento completo sigue pendiente de 22.
- **0.0.14 aceptada físicamente:** 879 muestras, 628 con seguimiento y 76,3558 s
  de reloj visible; mediana `frame_ms` suavizado 39,407 ms. Sin aviso OpenGL ni
  excepciones C# en ese registro; no se presume que la causa anterior esté reparada.
- **844 archivos históricos Blender intactos** y tres configuraciones ajenas
  Unity intactas. No se modificaron demos ni fuentes.
- FOV/calibración exacta, calidad sostenida, costo del corto completo, cinco
  minutos, APK 0.0.5 física y S23 mantienen sus limitaciones previas.

## Acceso y limpieza del teléfono

Unity reinició ADB y se perdió la autorización. Tras reconectar el cable, se
recuperó el acceso usando la clave existente con `ADB_VENDOR_KEYS` en el proceso
ADB. No se cambiaron claves ni ajustes globales. No volver a pedir reconexión
antes de comprobar el servidor con esa clave existente.

0.0.13 se desinstaló correctamente a las **22:56:08 UTC**, sin paquete, proceso
ni carpeta externa restantes (`cleanup.json`). Después, por la aclaración del
usuario, se instaló 0.0.14 para repetir la prueba. **Limpieza final verificada a
las 23:02:40 UTC** en `cleanup_0014.json`: no quedan paquetes `com.chupacabras`,
proceso de la app ni carpeta de datos externa. Android eliminó los datos internos
al desinstalar; no se inspeccionaron directamente sin root. Instalación por
streaming, sin APK copiada a Descargas. Ambas limpiezas se conservan por separado.

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
  12 realizada en una build nueva; figura de pie centrada directamente sobre el símbolo y panel vertical al lado,
  por aclaración del usuario del 30 de septiembre. Su superposición virtual al
  dibujo es intencional; el detector recibe la imagen real sin superposiciones. Las escenas
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
  terminar. El usuario reiteró expresamente esta limpieza.
- **M#[4] resuelta:** acceso USB, ubicación centrada directamente encima del
  símbolo y lectura de figura/panel confirmados por el usuario en 0.0.14. App
  desinstalada y limpieza comprobada. No hay acciones manuales necesarias pendientes.
- **M#[5] prevista para paso 20**, no solicitada. No sustituirla por pruebas de Editor.
- Sin nuevas decisiones creativas pendientes. La revisión estética adicional es opcional.

## Git y reanudación exacta

Unity: commit `630e033` (composición corregida, prueba física y limpieza).
Este estado y su evidencia quedan en el commit de cierre del repositorio Blender.
Solo se incluyen cambios propios, sin push. Los tres cambios ajenos de Unity
continúan preparados como antes. La caché `.utmp` regenerada quedó restaurada
a sus bytes previos.

**Retomar en 13.1:** producir calma/acecho 0–20 s con rigs 10/11 y triangulación
R03 de oveja. Usar materiales/aspecto y composición centrada R05 de paso 12;
conservar los hitos anteriores. Resolver cámara continua anticipada 18,5–20,5 s,
retirada de cuerpo/ojos a 15 s y entrada lateral/detrás del granero para el salto
a 20 s. La cámara AR permanece independiente. No se necesita conectar el teléfono
para comenzar esa actuación ni volver a solicitar M#[4].

Próximos dos pasos principales previstos:

1. **13:** calma/acecho 0–20 s, anticipación continua de cámara y verificación.
2. **14:** salto/ataque 20–25 s, contacto/ocultamiento y continuidad, tras cerrar 13.

No avanzar a 15 en esa pareja. M#[5] se mantiene prevista para 20. Observar el
aviso OpenGL aislado de 0.0.13 en posteriores pruebas móviles; no se reprodujo
en 0.0.14 y no se extrapola ausencia de errores a pruebas prolongadas.
