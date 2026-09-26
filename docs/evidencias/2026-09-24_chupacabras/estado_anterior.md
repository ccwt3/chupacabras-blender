# Estado de continuidad

Actualizado: **24 de septiembre de 2026, hora local de México** (los últimos
logs tienen fecha 25 en UTC). **Pasos 6 y 7 completados**. Se ejecutaron exactamente
dos pasos principales. **8–24 pendientes; no iniciados en esta sesión.**
No hay acciones manuales necesarias pendientes.

## Punto de partida comprobado

Se leyeron plan, evaluación AR, alcance de ambas demos y estado anterior,
archivado en `docs/evidencias/2026-09-24_escenario_oveja/estado_anterior.md`.
No se encontraron AGENTS.md adicionales en las rutas aplicables; se siguieron
las instrucciones globales proporcionadas por el usuario.

Se comprobaron los hashes de las once entregas registradas de 4–5 y las cinco
entregas de demos; coinciden. Las demos se reabrieron con el verificador existente.
Unity comenzó en **`fde1295060e982d9a7783aa2cea31da2d415ce5a`**, con árbol limpio y
versión **6000.3.22f1 (1c726e1fb402)**. Blender no tiene repositorio Git utilizable:
el `.git` expuesto está vacío. No se inicializó ninguno.

Los pasos 1–5 conservan su cierre anterior y sus límites físicos. No se
reinterpretó la aceptación del G20 ni se convirtió una prueba de Editor en física.

## Pasos y subpasos

| Paso | Estado comprobado |
| --- | --- |
| 1–3 | Cerrados previamente con el alcance documentado; evidencia y límites conservados. |
| 4.1–4.4 | Muestra de intercambio conservada, hashes correctos. |
| 5.1–5.4 | Bloqueo R04 de 40 s conservado, hashes correctos. |
| 6.1 | Completado: granero, suelo seco, hierba, piedras, bosque y luna geométrica. |
| 6.2 | Completado: fuente estática y FBX; diez materiales de color reconstruidos en URP. |
| 6.3 | Completado: intersecciones de granero corregidas en un nuevo contexto; cámaras/ocultaciones/salida verificadas en Unity. |
| 6.4 | Revisión opcional disponible en imagen; no exige respuesta para continuar. |
| 7.1 | Completado: selección breve documentada; elegida oveja Quaternius CC0. |
| 7.2 | Completado: ZIP/fuentes/licencia conservados; escala, colores y pesos compatibles; escena/prefab Unity. |
| 7.3 | Completado: fuente reabierta, dependencias revisadas y cuatro poses comparadas con Unity. |
| 7.4 | Sin intervención: descarga pública gratuita, sin compra ni cuenta. |
| 8–24 | Pendientes. No se inició modelado del chupacabras ni rig final de oveja. |

No queda subpaso en curso. Las poses de aptitud de la oveja no son su actuación
final ni completan el paso 10. La oveja reutilizada aún no sustituye a los proxies
en el corto animado: se entrega por separado en el escenario para trabajar en 8.

## Decisiones confirmadas y límites heredados

- Blender, fuentes y animaciones: `/home/cacawatin/code/blender/chupacabras`.
- Unity, AR Android: `/home/cacawatin/code/unity/chupacabras`.
- **Usar exclusivamente Unity 6000.3.22f1**, instalado en
  `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`, desde Linux.
  No se instaló ni seleccionó otro Editor; no se modificaron ajustes globales.
- Producción definitiva **40 s**, 30 fps, claves 1–1201 y captura 1–1200.
  Demo animada de **35 s** independiente y conservada.
- Ventana anclada al marcador con escena 3D en tiempo real, cámara interna,
  16:9 y tamaño provisional 240 × 135 mm. RT de revisión 960 × 540.
- Chupacabras original basado en las tres referencias; oveja reutilizada con
  licencia adecuada, ahora seleccionada de Quaternius bajo CC0 1.0.
- **M#[1] resuelta:** arrastre a izquierda y giro/salida derecha; salto a 20 s,
  aterrizaje a 21.2 s, ocultamiento hasta 25 s, salida antes del campo vacío
  39–40 s. Ambiente y efectos sin música.
- AprilTag conserva la ruta heredada de la prueba funcional/aceptación anterior;
  esta sesión no añade validación física ni amplía esa aceptación. Se mantienen
  pendientes las mediciones reales documentadas. No se añadió ARCore ni se
  cambió tecnología.
- Moto G20 para pruebas; posible S23 solo en exposición y **pendiente de prueba**.
- tagStandard41h12 ID 0: 100 mm entre esquinas de detección, dibujo completo
  180 mm, cubo 50 mm. FOV 60° provisional, sin calibración exacta confirmada.
- Carta/Brother DCP-T510W/trabajo 43 y regla de 100 mm confirmados previamente.
  No se reimprimió ni se pidió medir o conectar el teléfono.
- Notificar acciones manuales y retirar lo instalado para pruebas al terminar.
  No se instaló nada en el teléfono en esta sesión.
- FBX Generic, metros, Blender (x,y,z) → Unity (x,z,y), sin root motion.
  Compresión de lana mediante blend shape, todavía por preparar en esta oveja.

## Cambios y motivo

- **Escenario:** 2915 triángulos, diez mallas/materiales compartidos. Se agrupa
  la geometría por material para contener el costo; sin texturas ni simulaciones.
- La inspección detectó que el giro del bloqueo intersectaba el granero. Se creó
  `06_escenario_contexto`, desplazando granero y acecho anterior a 20 s **3.2 m
  hacia el fondo** y reduciendo profundidad del edificio. Se conservan curvas
  de cámara, salto, contacto, arrastre y salida. R04 permanece intacto.
- **Oveja:** 307 vértices/612 triángulos, 24 huesos, dos materiales. Fuente y
  seis acciones originales conservadas. Altura neutral 1.18 m; frente −Y.
  Se limitan y normalizan las influencias de 35 vértices para usar un máximo
  de cuatro, evitando discrepancias de hasta 3.24 cm del importador inicial.
- Materiales de color sólido; retirada de una referencia de textura heredada
  del equipo del autor en la copia de trabajo. Original y ZIP intactos.
- La muestra de caída corrige unos 5 cm de penetración del suelo de la animación
  original. No se creó rig nuevo, compresión de lana ni actuación definitiva.
- Scripts nuevos de generación/reapertura y verificación Unity. Corregida la
  medición de escala con `BakeMesh(..., true)` y la actualización de matrices
  del skin en capturas de varias poses por actualización del Editor.
- Documentados los cambios en `docs/escenario_movil.md`, `docs/asset_oveja.md`,
  plan y `docs/pasos06_07.md` de Unity. Intentos anteriores conservados.
- Unity normalizó dos ajustes URP al abrir. Su resultado se conserva en
  `Library/Session_20260924_assets_side_effects/`; se restituyeron únicamente estos
  cambios propios al estado inicial. No se incluyen cambios ajenos en Git.

## Entregas y evidencias

En Blender:

- **`scenes/06_escenario.blend`**, FBX y JSON homónimos en `exports/`.
- `scenes/06_escenario_contexto.blend` y FBX homónimo: proxies animados de contexto.
- **`scenes/07_oveja_r04.blend`**, `exports/07_oveja_r04.fbx`,
  `exports/07_oveja_r04_poses.fbx` y JSON de referencia.
- `assets/oveja/`: ZIP original, fuentes extraídas, licencia, páginas y hashes.
- **`previews/06_escenario.png`**, **`previews/07_oveja.png`**,
  `previews/07_oveja_pastoreo.png` y `previews/07_oveja_caida.png`, desde Unity.
- `docs/evidencias/2026-09-24_escenario_oveja/`: archivo de estado anterior,
  logs de generación/reapertura, resultados Unity y auditoría de integridad.

En Unity:

- **`Assets/Scenes/06_Environment.unity`** y **`07_Sheep_r04.unity`**.
- `Assets/Environment/` y `Assets/Sheep/`; prefab **`Sheep_Quaternius_r04.prefab`**.
- `Assets/Editor/EnvironmentBuild.cs`, `SheepBuild.cs`, `scripts/verify_assets.sh`.
- Evidencia final: `docs/evidencias/2026-09-24_escenario/` y
  **`docs/evidencias/2026-09-24_oveja_r04/`**. Capturas y logs de intentos previos
  permanecen como diagnóstico; `07_Sheep.unity` está superada por R04.
- **Sin APK nueva.** Se mantienen APK R04 de bloqueo y 0.0.5 de seguimiento,
  sin instalar/probar físicamente ninguna de ellas en esta sesión.

## Pruebas y resultados

- Demos reabiertas con el verificador existente; cinco hashes de demos y once
  de entregas 4–5 correctos al inicio y al cierre.
- Escenario Blender: cero intersecciones entre cajas de piezas del granero y
  personajes en **1200 fotogramas**. Hierba/piedras excluidas del recorrido con
  márgenes; muestreo de colocación 10 Hz. No equivale a una prueba de colisión
  de los futuros modelos definitivos.
- Reapertura escenario/contexto: 2915 triángulos/diez mallas; 40 s; contacto
  correcto en **565 muestras**, error máximo **9.83e-7 m**.
- Unity escenario: **150** cuadros con criatura oculta, **114** con oveja oculta,
  **30** de campo vacío; todos correctos. Ojo de acecho visible (4 píxeles a
  320 × 180), oveja visible antes/después (460/653 píxeles).
- Oveja reabierta: 24 huesos, seis acciones, ninguna textura externa requerida.
  Original/licencia/ZIP verificables por SHA-256.
- Unity oveja: cuatro poses evaluadas con Playables; error máximo de vértice
  **0.00011044 m (0.11 mm)**, altura **1.17999947 m**, apoyo mínimo **−0.089 mm**,
  dentro de tolerancia 1 mm. Capturas finales inspeccionadas.
- **32 aserciones existentes de seguimiento correctas**. Scripts Python/Bash
  con sintaxis correcta; C# compilado y clang-format correcto. No hay linter
  propio configurado. Diff de texto revisado; YAML generado mantiene su formato.
- No se ejecutó build Android nueva: aceptación de 6–7 es importación/aptitud,
  sin necesidad de prueba manual. Compilación C# de Editor correcta.

La iluminación es básica; el acabado y brillo móvil se resuelven en paso 12.
Los conteos de geometría no son mediciones de draw calls, GPU o fps del teléfono.
Persisten FOV/calibración, costo real del corto, cinco minutos sostenidos,
0.0.5 física, dispositivo Android de páginas 16 KB y S23 pendientes según las
etapas posteriores. No se declara ninguna validación física nueva.

## Acciones manuales y preguntas

- **M#[1] resuelta:** narrativa, trayectoria, ocultamiento y audio.
- **M#[2] resuelta para paso 3:** alcance físico anterior aceptado; medición
  adicional aplazada. No repetir esa solicitud para iniciar producción.
- **M#[3] resuelta:** impresora/carta/regla medida.
- **Sin decisiones ni acciones manuales indispensables pendientes.**
  Revisión de las imágenes opcional. El siguiente paso no requiere teléfono.

## Git y reanudación exacta

Unity: commit **`0dde327db0619141ea64c4761cd1f280a0dcd803`**, 98 archivos propios añadidos.
Árbol limpio comprobado después del commit; no se hizo push.
Blender: sin repositorio utilizable; no se inicializó Git. Sin push.

**Retomar en paso 8.1**, usando el escenario 06, la oveja R04 y las tres
referencias originales del chupacabras. Conservar el contexto 06 para encuadres
sin cambiar el bloqueo R04 histórico.

Próximos dos pasos previstos:

1. **8:** anatomía/silueta original del chupacabras, proporciones junto a la oveja,
   vistas frontal/lateral/trasera/tres cuartos y aptitud para agarre/ocultamiento.
2. **9:** cresta, rostro, garras y mechones geométricos; UV/materiales exportables
   y legibilidad en Unity. Depende de cerrar 8.

No se avanzó a un tercer paso. Rig final, actuación, Timeline y conexión real
con AprilTag conservan sus dependencias posteriores.
