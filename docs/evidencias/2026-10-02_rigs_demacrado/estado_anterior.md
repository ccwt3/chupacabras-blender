# Estado de continuidad

Actualizado: **2 de octubre de 2026**, revisión demacrada solicitada.
**8–9 revisados; modelo nuevo listo para adaptar rig y aspecto (11–12).**
Se trabajaron únicamente los dos pasos reabiertos por la corrección estética;
13–24 no iniciados. No se trabajó un tercer paso principal.

## Punto de partida comprobado

Blender partía de `6750d68`, limpio; Unity de `630e033`, con tres cambios ajenos
preparados en ProjectSettings. Se leyeron estado, plan, evaluación AR, demos,
modelo y rigs; se inspeccionaron las tres referencias originales y el modelo.
No se encontraron AGENTS.md adicionales en las raíces/ancestros consultados.

El paso 12/M#[4] anterior estaba cerrado sobre 0.0.14 y modelo fornido.
El usuario solicita conservar la forma general, volver al aspecto demacrado,
esquelético y tenebroso de las referencias, permitiendo más polígonos. Esta
corrección reabre 8–9 antes de avanzar con la actuación. No implica rechazo de
la colocación AR centrada ni cambio de tecnología, duración o plataforma.
Estado previo íntegro en `docs/evidencias/2026-10-02_demacrado/estado_anterior.md`.

## Pasos y subpasos

- **1–7 y 10:** conservados; no se amplía su aceptación.
- **8.1/8.2/8.4 revisados:** anatomía demacrada R01, vistas, referencia,
  importación y ocultamiento comprobados. 8.3: ajuste recibido aplicado;
  no se inventa una aprobación visual posterior del usuario.
- **9.1/9.2/9.4 revisados:** acabado R02, rostro/cuencas, piel, espinas y
  detalle; 9.3 revisión opcional disponible mediante PNG y giro.
- **11 anterior conservado; adaptación nueva pendiente:** la topología nueva
  requiere reasignar/verificar pesos, mandíbula y contacto antes de actuar.
  No usar índices de los vértices del modelo anterior sobre el nuevo.
- **12 anterior cerrado/M#[4] resuelta; propagación nueva pendiente:** rig,
  materiales y figura/panel de producción aún contienen el modelo anterior.
  La aceptación física previa no certifica la nueva malla ni su legibilidad.
- **13–24:** no iniciados. No se ejecutó calma/acecho ni salto definitivo.

## Cambios y motivo

Tórax/hombros/muslos más secos, abdomen hundido, costillas fusionadas con piel,
caderas/articulaciones marcadas, cola delgada, rostro estrecho y cuencas oscuras.
Se mantienen postura, cresta, garras, mandíbula y seis materiales sólidos.
Volumen de `Chupa_Body` reducido **55,23 %**; acabado **30.880 triángulos**,
18 mallas. Mayor geometría autorizada, costo móvil aún no medido.

La cámara antigua dejó ver oveja en el cuerpo estrecho: fallo guardado, sin
relajar aceptación. Contextos nuevos R03 acercan la cámara interna a
`(0.3,-4,2.8)` en Blender y ocultan por profundidad real, sin desactivar oveja,
polvo ni pantallas. Son muestras de volumen del bloqueo, no actuación final:
conservan cortes y oveja rígida; la cámara continua corresponde a 13–14.

Se reutilizan generadores/verificadores existentes. Nuevos scripts de modelado,
giro y comprobación Unity; presupuesto de geometría explícito por entrega y
posición de cámara opcional, sin cambiar los valores históricos por defecto.
Los PNG intermedios del giro son regenerables, quedan en disco y se excluyen de
Git. [Detalles y comandos](chupacabras_demacrado.md).

## Entregas y evidencias

Blender, raíz `/home/cacawatin/code/blender/chupacabras`:

- `scenes/08_chupacabras_demacrado_r01.blend`.
- **`scenes/09_chupacabras_demacrado_r02.blend`**, acabado vigente.
- FBX/JSON homónimos en `exports/`; contextos vigentes **`_contexto_r03`**.
- Cuatro vistas Blender por fuente y capturas `*_unity_*.png` en `previews/`.
- `previews/09_chupacabras_demacrado_r02_giro.mp4`: 10 s, 960×720, 12 fps.
- `docs/evidencias/2026-10-02_demacrado/`: logs, informes, hashes, estado anterior.

Unity, raíz `/home/cacawatin/code/unity/chupacabras`:

- `Assets/Creature/08_chupacabras_demacrado_r01/` y
  `Assets/Creature/09_chupacabras_demacrado_r02/`: modelos/materiales/prefabs.
- Escenas homónimas **`_contexto_r03.unity`**, independientes de AR R05.
- `Assets/Editor/LeanCameraCheck.cs`, `docs/pasos08_09_demacrado.md`.
- `docs/evidencias/2026-10-02_demacrado_{forma_r03,acabado,fullres}/`.
- R01 de acabado, R02 de contexto y búsquedas se conservan como diagnóstico.

**APK vigente histórica sin cambios:**
`builds/android/12_appearance_20260930_225854.apk`, 38.676.888 bytes,
SHA-256 `4c4b33846b193684dd925fe9a162f3d2da8c52fe0aaba32994b0ce028b275551`.
No contiene la revisión demacrada. No se construyó otra APK ni se solicitó teléfono.
Marcador `marker/03_marker_carta.pdf` y demos conservados.

## Pruebas y limitaciones

- Blender 5.2.2 LTS: reaperturas de revisiones nuevas e históricas, mallas
  cerradas, caras válidas, UV y unidades correctos. Demos verificadas, incluida
  duración 35 s y contacto. Producción sigue fijada a 40 s.
- Contextos nuevos: 1.200 cuadros sin cruce AABB del granero, 565 muestras
  de referencias de contacto con error máximo 0,0000009903 m (no mordida final).
- Unity **6000.3.22f1**: compilación C#, importación y reapertura de escenas,
  clip 40 s, escala/ejes/materiales y 32 aserciones de tracking correctas.
- Ambas fuentes: 150/150 cuadros de criatura oculta, 114/114 de oveja oculta,
  30/30 de campo vacío. Acabado repetido a **960×540**, 264 cuadros y cero
  píxeles visibles de los objetivos ocultos; control positivo 12.809 píxeles.
- Error máximo de límites importados 0,0000004299 m; referencias de contacto
  0,0000023961 m. Es prueba de volumen, no validación de rig nuevo.
- Python compila; clang-format y diff de código/documentación correctos.
  `git diff --check` general de Unity señala espacios finales del YAML generado
  automáticamente (.meta/escenas/prefabs); se conserva el formato del Editor.
  No hay suite/linter Python configurado.
- Giro verificado por FFprobe: H.264, 120 cuadros, 10 s. Vistas y capturas
  inspeccionadas. **844 archivos históricos y tres configuraciones ajenas intactos.**
- La primera cámara falló de verdad; se conservan su log e informe separado.
  Avisos de cierre PlayableGraph/SDL/Vulkan y SDK .NET no impidieron las
  verificaciones finales. No se cambiaron ajustes globales para silenciarlos.
- Sin prueba física nueva, sin APK nueva. Ojos del acabado: un píxel en el
  plano lejano de revisión; legibilidad/luz móviles por revalidar en 12.
  Rendimiento sostenido, calibración, prueba física 16 KB y S23 pendientes.
  Se conserva el seguimiento del aviso OpenGL aislado de 0.0.13; no se presume
  corregido por las pruebas de escritorio. Limpieza del G20 permanece como fue
  comprobada al cerrar la sesión física anterior, sin nuevo acceso ahora.

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


Actualización de esta sesión:

- **Confirmado:** reducir musculatura y añadir anatomía esquelética/tenebrosa,
  preservando forma general; se permiten más polígonos. No volver a preguntar.
- M#[1]–M#[4] conservan sus cierres históricos. **Ninguna acción manual necesaria
  pendiente.** M#[5] sigue prevista para 20, no solicitada.
- Preparar rig/aspecto y APK antes de pedir una eventual revisión física de la
  nueva malla. No atribuir a M#[4] la aceptación de un modelo que no se instaló.
- Revisión estética de las nuevas vistas opcional; no bloquea el trabajo técnico.

## Git y reanudación exacta

Unity: commit `b25a97a`, solo archivos propios. Los tres cambios ajenos
siguen preparados y excluidos. Blender: este estado y las entregas forman el
commit de cierre de esta sesión. Sin push ni repositorios nuevos.

**Retomar en 11.1 con la nueva malla:** partir de
`scenes/09_chupacabras_demacrado_r02.blend`; conservar el hito
`11_rigs_contacto_r03.blend`, la oveja R03 y sus diagonales. Adaptar pesos y
resolución de contacto a la topología nueva, guardar fuentes/exportaciones con
nombres nuevos, comprobar deformaciones en Blender y Unity. No copiar índices
viejos de dientes/cuello sin comprobarlos sobre la revisión correspondiente.

Próximos dos pasos principales previstos:

1. **11 retomado:** adaptar/verificar rig y contacto de la anatomía demacrada.
2. **12 retomado:** propagarla al aspecto/composición R05, mantener figura de pie
   centrada encima del símbolo y panel lateral; revisar legibilidad, preparar
   APK/evidencias antes de cualquier intervención física indispensable.

No ejecutar un tercer paso. **13–14 son la pareja posterior**, una vez cerradas
esas dependencias: pastoreo/retirada de ojos a 15 s, cámara continua anticipada
18,5–20,5 s, entrada lateral/detrás del granero, salto a 20 s y aterrizaje 21,2 s.
La cámara AR permanece independiente y el hito R04 no se sobrescribe.
