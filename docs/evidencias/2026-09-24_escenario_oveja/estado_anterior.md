# Estado de continuidad

Actualizado: **24 de septiembre de 2026**. **Pasos 4 y 5 completados en esta sesión**
con muestra de intercambio y bloqueo R04 de 40 s. Se ejecutaron exactamente dos
pasos principales; **6–24 no iniciados**. No hay acciones manuales pendientes.

## Punto de partida comprobado

Leídos plan, evaluación AR, demos y estado anterior, archivado en
`docs/evidencias/2026-09-24_intercambio/estado_anterior.md`. No se encontraron
AGENTS.md adicionales en las rutas aplicables. Unity estaba limpio en `836adb2`
y fija 6000.3.22f1 (1c726e1fb402). La última APK de seguimiento 0.0.5 conserva
su SHA-256 `752eb7cd342644761dfa965701991de57a8cf752d7b54c236db24976af3aa755`.
Las demos se reabrieron con el verificador existente y sus hashes siguen intactos.
Blender no tiene repositorio Git utilizable; el directorio `.git` expuesto está vacío.

El paso 3 permanece cerrado con la aceptación registrada de escala aproximada y
rendimiento de esta etapa. Su alcance físico no se reinterpreta ni se amplía.
La nueva instrucción de continuar habilitó los pasos 4–5 que estaban en espera.

## Pasos y subpasos

| Paso | Estado |
| --- | --- |
| 1.1–1.4 | Completados previamente; ficha y decisiones conservadas. |
| 2.1–2.4 | Completados previamente con Unity/Linux y G20. |
| 3.1–3.5 | Cerrados por aceptación expresa anterior; no se reabrieron mediciones. |
| 4.1 | Completado: fuente con rig, COPY_LOCATION y shape key; FBX importado. |
| 4.2 | Completado: metros/ejes, normales, curvas, contacto, duración, deformación, cámara y RT. |
| 4.3 | Completado: contrato reproducible y compresión de lana mediante blend shape. |
| 4.4 | Sin intervención manual requerida. |
| 5.1 | Completado: bloqueo 40 s, salto a 20 s, aterrizaje a 21.2 s, salida a 39 s. |
| 5.2 | Decisiones de trayectoria y ocultamiento ya resueltas en M#[1]; no se preguntaron otra vez. |
| 5.3 | Completado: arrastre izquierdo, giro/salida derecha, cámaras y ventana 16:9. |
| 5.4 | Completado: máscaras por fotograma, vistas exteriores y video Unity. |
| 6–24 | Pendientes; no iniciados. |

No hay subpasos en curso. La geometría de bloqueo, su movimiento provisional y
el reproductor Playables no completan los modelos, rigs, actuación ni Timeline
finales de pasos posteriores.

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


Acuerdos técnicos fijados por las pruebas de esta sesión:

- Fuente a 30 fps, curvas 1–1201 y captura 1–1200. El límite 1201 conserva 40 s.
- FBX explícito Generic, metros, sin root motion; Blender (x,y,z) → Unity (x,z,y).
- Compresión de lana mediante blend shape; huesos/constraints se hornean al exportar.
- Ventana provisional 240 × 135 mm, 16:9, ancho 2.4 veces el lado de detección.
  RT de revisión 960 × 540; no constituye presupuesto de rendimiento móvil.
- Caída de la oveja desde 21.2 s y plano abierto a 25 s. Son decisiones de bloqueo
  dentro de la cronología confirmada; el refinamiento sigue en 13–15.

## Cambios y motivo

- Añadidos generadores y verificador de reapertura en `scripts/`, fuentes por
  revisión y exportaciones en `exports/`. No se reutilizaron ni sobrescribieron
  demos. R02/R03 se conservan; R04 añade caída y forcejeo provisional legible.
- Unity incorpora `ExchangeBuild`, `BlockingBuild` y `SequencePreview`, escenas
  independientes, materiales URP y RT. Se resolvió la ausencia de Animator en
  la raíz importada para evaluar todo el clip con un solo reloj.
- Añadidos scripts de verificación y build; el verificador APK admite un paquete
  alternativo para comprobar la APK sin AR sin alterar sus valores por defecto.
- Corregidos resúmenes obsoletos del plan/evaluación; conservados sus registros
  históricos y la aceptación física previa.
- La build regeneró caché `.utmp` previamente versionada y normalizó dos ajustes
  de URP. Se preservó su resultado en `Library/Session_20260924_build_side_effects/`
  y se restituyeron solo esos cambios propios al estado inicial. No se versionan
  cachés nuevas. Logs brutos conservados; copias `.gz` idénticas versionadas.

## Entregas y evidencias

Raíz Blender:

- `scenes/04_intercambio.blend` y `exports/04_intercambio.{fbx,json}`.
- **`scenes/05_blocking_r04.blend`** y `exports/05_blocking_r04.{fbx,json}`.
- **`previews/05_blocking_r04.mp4`**: video final de revisión desde Unity.
- `docs/intercambio_blender_unity.md`, `docs/bloqueo_40s.md`.
- `docs/evidencias/2026-09-24_intercambio/`: estado anterior, hashes de demos y
  entregas, logs Blender, reapertura, comprobaciones, APK y metadatos de video.

Raíz Unity:

- `Assets/Scenes/04_Exchange.unity` y **`Assets/Scenes/05_Blocking_r04.unity`**.
- `Assets/Exchange/`, `Assets/Preview/` y `docs/pasos04_05.md`.
- **APK R04:** `builds/android/05_blocking_20260924_233453.apk`, **36 858 340 bytes**,
  SHA-256 `ba21a91015d6757d5d70a48e90020716cb192ce15dcafa275b5a48e2ff587cb3`.
  Paquete `com.chupacabras.ar.blockingpreview`, versión 0.1.0/code 10.
  Es un visor independiente del bloqueo sin cámara AR. **No instalada ni probada
  físicamente.** La APK R03 y las anteriores de seguimiento están conservadas.
- `docs/evidencias/2026-09-24_intercambio/`, `2026-09-24_blocking/`,
  `2026-09-24_blocking_r03/`, **`2026-09-24_blocking_r04/`**.
  Incluyen checks, máscaras/vistas, logs y verificación APK; fotogramas intermedios
  locales reproducibles, excluidos del commit para evitar duplicar los videos.

## Pruebas ejecutadas y resultados

- Blender 5.2.2 LTS: generación y reapertura independientes. Duración 40 s;
  contacto verificado en 1201 instantes de muestra y 565 del bloqueo desde el
  aterrizaje. Demos existentes verificadas y hashes conservados.
- Intercambio Unity: 41 muestras frente a Blender, cubo 1 m, ejes/normales y
  blend shape. Error máximo de vértice **3.46e-7 m**; contacto de ejecución
  **1.79e-7 m**. Cuatro esquinas UV y proporción 16:9 correctas.
- Bloqueo R04: 564 muestras de contacto; error máximo **2.01e-6 m (0.00201 mm)**.
  Error de cámara frente a Blender <0.000463 m; trayectoria <0.000002 m.
  Clip float 40.0000038 s; reloj reinicia en el límite exacto 40 s.
- Máscaras reales a 320 × 180: **150** fotogramas con criatura/ojos ocultos,
  **114** con oveja oculta y **30** vacíos; todos pasan. Oveja visible antes y
  después, ojo visible durante acecho. No se usaron partículas para tapar errores.
- Tres cámaras exteriores dejan la imagen interna idéntica byte a byte.
  Capturas inspeccionadas. Video H.264, **960 × 540, 12 fps, 480 cuadros, 40 s**.
- 32 aserciones existentes de seguimiento correctas; sintaxis Python/Bash correcta.
  Código C# nuevo formateado con clang-format y compilado por Unity. Sin suite
  propia de linters configurada. Diff de fuentes/documentos correcto; 556 espacios finales propios de YAML
  serializado por Unity preservados y documentados, sin modificar sus recursos.
- APK R04: Unity **6000.3.22f1/Linux**, IL2CPP/ARM64, **Succeeded**, **0 errores y
  0 advertencias**, 1 min 02.46 s. Firma v2, zipalign 16 KB, ocho ELF AArch64
  y ausencia de ARCore verificadas. La APK anterior 0.0.5 vuelve a pasar el
  verificador con sus opciones originales y conserva su hash.

## Límites físicos que continúan pendientes

No se hizo ninguna prueba física nueva. Se conserva el cierre anterior del G20:
Android 11/API 30, ARM64 y páginas de 4096 bytes, Camera 0; escala aproximada
aceptada y giro/pérdida/recuperación observados. El FOV 60° sigue provisional.
La APK de seguimiento 0.0.5 sigue sin prueba física; tampoco se midió la carga
del corto, cinco minutos sostenidos ni Android de páginas de 16 KB. El S23 sigue
pendiente de su propia prueba. La alineación estática y el Editor no cierran
ninguna de estas validaciones. La integración del corto con AprilTag es el paso 20.

## Acciones manuales y preguntas

- **M#[1] resuelta:** narrativa, trayectoria, ocultamiento y audio; conservada.
- **M#[2] resuelta para paso 3:** alcance físico aceptado, rendimiento adicional
  aplazado. No repetir distancia ni pedir USB para habilitar producción.
- **M#[3] resuelta:** impresora Brother y carta; regla de 100 mm confirmada.
- **Sin acciones manuales ni decisiones indispensables pendientes en 4–5.**
  Revisión del video opcional. No se requiere teléfono para el próximo paso.

## Git y punto exacto de reanudación

Unity: commit **`fde1295060e982d9a7783aa2cea31da2d415ce5a`**, fuentes, recursos y evidencias
propias de esta sesión. **Árbol limpio comprobado, sin push.** Se excluyen cachés, builds y fotogramas
intermedios. Blender sigue sin repositorio utilizable; no se inicializó uno.
No quedan cambios ajenos ni archivos fuente pendientes de commit en Unity.

**Retomar en paso 6.1**, usando el bloqueo R04 y su contrato de intercambio:

1. **Paso 6:** construir escenario definitivo de costo contenido, exportarlo y
   comprobar encuadres/recorridos. Depende de 5, ya satisfecho.
2. **Paso 7:** seleccionar/importar la oveja reutilizada, verificar licencia,
   escala y aptitud para la secuencia. Depende de 6; no se buscó ni descargó aquí.

No iniciar otro paso en esta sesión. Se conservarán los 40 s, Unity exacto,
las dos raíces y las limitaciones físicas anteriores.
