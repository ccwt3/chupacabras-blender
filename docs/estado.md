# Estado de continuidad

Actualizado: **24 de septiembre de 2026, hora local de México** (25 UTC).
**Pasos 10 y 11 completados.** Se ejecutaron exactamente dos pasos principales.
**12–24 pendientes, no iniciados.** Sin intervención manual necesaria en esta sesión.

## Punto de partida comprobado

Se leyeron estado, plan, evaluación AR y alcance de las dos demos. No se
hallaron AGENTS.md adicionales en los directorios aplicables. Se comprobaron
55 hashes del cierre anterior y se registraron **533 archivos históricos**
de escenas, exportaciones, previews, referencias y assets: todos intactos al
cierre. Estado anterior archivado en `docs/evidencias/2026-09-24_rigs/estado_anterior.md`.

Unity comenzó en `9647ab87150ec1cb43d6ad4bb3c47c4464b21195`, versión
**6000.3.22f1 (1c726e1fb402)**. Ya había cambios ajenos en GraphicsSettings y
QualitySettings, más PackageManagerSettings sin rastrear. Los tres conservan
exactamente sus bytes iniciales y se excluyen del commit. Blender no tiene
repositorio Git utilizable; `.git` expuesto vacío, no se inicializó.

## Pasos y subpasos

| Paso | Estado comprobado |
| --- | --- |
| 1–9 | Conservados, sin ampliar las aceptaciones físicas previas. |
| 10.1 | Rig de oveja reutilizado: 24 huesos, cuatro IK, pesos hasta cuatro influencias. |
| 10.2 | Lana comprimible (66 vértices), pastoreo a 18,5 mm del suelo, forcejeo y poses de costado. |
| 10.3 | FBX/shape/poses comparados en 241 cuadros Blender–Unity; capturas corregidas y revisadas. |
| 10.4 | Sin intervención necesaria. Paso 10 cerrado. |
| 11.1 | Rig original de 23 huesos FK; patas, pelvis, columna, cuello, cabeza, mandíbula y cinco segmentos de cola. |
| 11.2 | Agarre establecido y desplazamiento conjunto horneados; oveja deformable apoyada en suelo. |
| 11.3 | R03 conserva triangulación y contacto sobre superficies; 181 cuadros comparados, raíz exterior independiente. |
| 11.4 | Sin intervención necesaria. Paso 11 cerrado. |
| 12–24 | Pendientes. No se inició iluminación definitiva, composición AR ni actuación final. |

No queda un subpaso incompleto de 10–11. Las muestras duran 8 s y 6 s y
**no reemplazan el corto de 40 s**. La muestra conjunta empieza con el agarre
establecido y traslada ambos personajes lateralmente; todavía no sincroniza
pisadas con el desplazamiento ni actúa el ataque/cierre inicial de mordida.
Esos movimientos se producirán en 13–15, junto con la cámara continua acordada.

## Cambios y motivo

- Fuente nueva `10_rig_oveja`: compresión localizada y poses extremas sobre el
  recurso CC0 existente; las IK se hornean en FBX. Apoyo corregido cada cuadro.
- Fuentes nuevas de paso 11: rig del modelo acabado 09 y dos pruebas distintas,
  controles FK y contacto. Dientes superiores/inferiores se resuelven contra
  lana deformada y se hornean; sin solver móvil ni dependencias circulares.
- La primera comprobación de vértices era correcta pero no garantizaba contacto
  de superficies: Unity mostró separación de 5,31 mm por diagonales distintas.
  R02 resolvió contacto pero la triangulación en modo edición descartó una cara.
  **R03 fija los 612 triángulos originales por índices de loop**, conservando
  vértices, pesos, UV, materiales y shape. La oveja trae un solapamiento de
  caras heredado: no se declara manifold; R03 no tiene bordes abiertos ni
  vértices sueltos. Primer intento y R02 conservados como diagnóstico.
- Generadores/verificadores nuevos, escenas y prefabs Unity independientes,
  `RigPreview` para muestras de duración propia y `RigBuild` para comparación.
  Se conserva `SequencePreview` de 40 s y todo el seguimiento AprilTag existente.
- Corregidas comprobación de Animator ausente y capturas con matrices de skin
  desactualizadas. Piso y luz de revisión ayudan a inspeccionar, sin cerrar 12.
- Documentación de implementación y reproducción: `docs/rigs_contacto.md`;
  en Unity, `docs/pasos10_11.md`. Logs de intentos fallidos conservados.

## Entregas y evidencias

Blender: `/home/cacawatin/code/blender/chupacabras`.

- **`scenes/10_rig_oveja.blend`** y FBX/JSON homónimos en `exports/`.
- **`scenes/11_rig_chupacabras_poses.blend`**, FBX/JSON: aptitud de controles.
- **`scenes/11_rigs_contacto_r03.blend`**, FBX/JSON y `_surface.json`: contacto vigente.
- **`previews/11_rigs_contacto_r03.mp4`**: seis segundos, 960 × 540, 15 fps,
  90 cuadros. Workbench de revisión; no es captura móvil ni el corto definitivo.
- PNG de oveja y agarre en `previews/`; frames del clip conservados.
- `scripts/rig_oveja.py`, `rig_contacto.py`, `rig_chupacabras_poses.py`,
  `verificar_rigs.py`, `preview_rigs.py`.
- `docs/evidencias/2026-09-24_rigs/`: hashes, reaperturas, regresiones,
  pruebas de superficie, resultados Unity y metadatos del video.

Unity: `/home/cacawatin/code/unity/chupacabras`.

- `Assets/Scenes/10_rig_oveja.unity`, `11_rig_chupacabras_poses.unity` y
  **`11_rigs_contacto_r03.unity`**; recursos/prefabs en `Assets/Rigs/`.
- `Assets/Editor/RigBuild.cs`, `Assets/Scripts/RigPreview.cs`,
  `scripts/verify_rigs.sh` (invocar con Bash).
- Evidencia vigente bajo `docs/evidencias/2026-09-24_rigs/`:
  `10_rig_oveja_final/`, `11_rig_chupacabras_poses/`, `11_rigs_contacto_r03/`.
- Regresiones `environment_20260925_015050/` y `sheep_20260925_015050/`.
- Sin APK nueva ni instalación en teléfono. Las APK anteriores se conservan.

## Pruebas ejecutadas y límites

- Reapertura independiente Blender: duración, vértices, shape, áreas finitas,
  apoyo, contacto y topología. 241 cuadros de oveja y 181 por muestra de criatura.
  Contacto R03 sobre superficie: máximo **0,00111 mm**, desplazamiento entre
  muestras máximo 19,94 mm a 30 fps, sin salto discontinuo detectado.
- Unity 6000.3.22f1: oveja, **73.987 vértices comparados**, error máximo
  **0,04261 mm**; controles, **205.435**, error **0,00300 mm**; contacto,
  **242.359**, error **0,02770 mm**. Shape conservado y duración dentro de 1 μs.
- R03: **11.162 triángulos** conjuntos (10.550 criatura + 612 oveja).
  Distancia real diente–triángulos de lana máxima **0,001408 mm** en Unity.
  Apoyo mínimo importado −0,02516 mm, dentro de tolerancia numérica de 1 mm.
  Raíz AR de referencia estable con pose identidad y pose/escala exteriores.
- Capturas Blender/Unity de pastoreo, caída, forcejeo, zancadas, mandíbula y
  contacto revisadas. FFprobe confirma el clip final de seis segundos.
- Demos históricas y acabado 09 reabiertos; oveja 07 regresada. Verificadores
  Unity existentes de escenario y oveja correctos; **32 aserciones de tracking**
  correctas. Escenario conserva 150/114 cuadros ocultos y 30 finales vacíos.
- Python: sintaxis comprobada en todos los scripts. Bash del nuevo verificador
  correcto; C# compilado y clang-format correcto. No hay otro linter configurado.
- **533 archivos históricos intactos**; FBX/JSON Blender y copias Unity idénticos.
  Configuraciones ajenas conservadas byte por byte.

No hay nueva aceptación física. Siguen pendientes brillo/legibilidad en G20,
composición figura/panel, calibración/FOV, costo del corto, cinco minutos
sostenidos, APK 0.0.5 física, páginas Android de 16 KB y S23 según sus etapas.
Los resultados del Editor no equivalen a medición del teléfono.

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
  ocurre dentro de la ventana con su cámara interna. Comprobar escala/separación
  y dejar visibles las esquinas y márgenes del tag en el paso 12. Las escenas
  08–09 son revisiones de modelos: aún no integran la composición a una build AR.
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
- No se necesita acción manual ahora. **M#[4]** queda prevista para que el
  usuario revise en el G20 la figura 3D y el panel cuando estén preparados
  build, marcador e instrucciones; **M#[5]** para comprobar perspectiva,
  seguimiento, pérdida/recuperación y reinicio al integrar AR en el paso 20.
  No pedirlas antes de preparar sus entregas. La revisión estética de vistas
  08–09 sigue siendo opcional; no se presume aprobación nueva.


## Git y reanudación exacta

Unity: commit **`0f38435aae8975d82e35da959c6d17cef367ac26`**; sin push. Se incluyen
solo nuevos recursos, verificadores, documentación y evidencia propios.
GraphicsSettings, QualitySettings y PackageManagerSettings permanecen ajenos.
Blender: sin repositorio Git utilizable, no se inicializó.

**Retomar en 12.1:** usar el acabado 09 como figura exterior estática y los rigs
validados (contacto R03 con triangulación fija) para revisar materiales/luz.
Preparar escena AR con figura junto al panel y tag descubierto; mantener las
cámaras interior/exterior independientes. Crear APK, marcador e instrucciones
antes de solicitar M#[4]. No solicitar teléfono durante preparación innecesariamente.

Próximos dos pasos previstos:

1. **12:** materiales, iluminación y composición figura estática/panel; preparar
   build y después realizar la revisión física M#[4]. Detenerse si esa acción
   indispensable queda sin respuesta, guardando estado.
2. **13:** calma y acecho 0–20 s con cámara anticipada continua; depende de cerrar 12.

No se inició un tercer paso. M#[4]/M#[5] siguen previstas, todavía no solicitadas;
no hay acción manual necesaria pendiente de respuesta en este cierre.
