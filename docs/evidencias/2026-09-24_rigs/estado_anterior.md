# Estado de continuidad

Actualizado: **24 de septiembre de 2026, hora local de México** (logs del 25 UTC).
**Pasos 8 y 9 completados.** Se ejecutaron exactamente dos pasos principales.
**10–24 pendientes; no iniciados.** No quedan acciones manuales necesarias.

## Punto de partida comprobado

Se leyeron estado, plan, evaluación AR y alcance de las dos demos. No se
hallaron AGENTS.md adicionales en las rutas aplicables ni dentro de Unity.
Se siguieron las instrucciones globales del usuario. Estado anterior archivado
como `docs/evidencias/2026-09-24_chupacabras/estado_anterior.md`.

Los hashes registrados de entregas 4–7 coinciden. Se registraron y comprobaron
al cierre **481 archivos anteriores intactos**, incluyendo demos, escenas,
exportaciones, referencias y recursos originales. Las demos, escenario y oveja
se reabrieron con sus verificadores; los FBX/JSON nuevos copiados a Unity son
idénticos a las exportaciones Blender.

Unity comenzó en `0dde327db0619141ea64c4761cd1f280a0dcd803`, con árbol limpio y
`ProjectVersion.txt` fijado a **6000.3.22f1 (1c726e1fb402)**. Blender no tiene
repositorio Git utilizable: el `.git` expuesto está vacío. No se inicializó.

## Pasos y subpasos

| Paso | Estado comprobado |
| --- | --- |
| 1–3 | Cierre funcional previo y límites físicos heredados; ninguna aceptación ampliada. |
| 4–5 | Muestra de intercambio y bloqueo R04 conservados; hashes correctos. |
| 6–7 | Escenario y oveja R04 conservados; regresión Blender/Unity correcta. |
| 8.1 | Completado: anatomía original, mandíbula separada, patas, cola y cresta principal. |
| 8.2 | Completado en forma R03: cuatro vistas, proporciones con oveja real, alcance de contacto y ocultamiento por cámaras internas. |
| 8.3 | Vistas entregadas; revisión de preferencias opcional, sin respuesta indispensable. |
| 8.4 | Hito de forma R03 cerrado; primera forma y R02 conservadas como diagnóstico. |
| 9.1 | Completado: cejas, dientes, garras, espinas finas, mechones, UV y seis materiales. |
| 9.2 | Completado: reapertura, comparación de geometría y capturas de rostro/lomo en Blender y Unity. |
| 9.3 | Imágenes disponibles para revisión opcional; no se inventó aprobación del usuario. |
| 9.4 | Acabado consolidado en un archivo nuevo; forma anterior preservada. |
| 10–24 | Pendientes; no se crearon rigs finales, actuación ni iluminación definitiva. |

No queda subpaso en curso. La muestra contextual es de volumen: usa la malla
real de oveja con giro rígido, no su actuación final. Durante el arrastre la
oveja queda elevada; **contacto entre referencias no equivale a mordida
final ni apoyo en el suelo**. Bajar/cerrar la cabeza, deformar lana y colocar
cuerpo/patas sobre el suelo corresponde a 10–11. No utilizar esta prueba
como sustituto de los pasos de rig y animación.

## Cambios y motivo

- Modelo original interpretado desde las tres referencias: espalda arqueada,
  cintura estrecha, hombros altos, brazos largos, patas traseras digitígradas,
  hocico, mandíbula, orejas y cola curva. Forma: **8.486 triángulos/12 mallas**.
- Acabado: **10.550 triángulos/17 mallas/6 materiales**, ojos amarillos, dientes,
  garras, narinas, cejas y mechones geométricos de cuello/lomo. UV 0–1, sin
  texturas externas ni pelo simulado. Materiales reproducidos en URP.
- El primer contexto falló: cola visible por el granero y oveja visible entre
  las patas. Se crearon revisiones nuevas. Los contextos vigentes llevan
  `_contexto_r02`; corrigen además el giro largo que atravesaba el granero y
  separan al hocico (y=9,3 m desde 14 s) y garras (0,25 m extra en el acecho
  inicial del acabado) de la pared. La orientación oculta gira por la ruta corta a −180°
  entre 15–20 s; la de acecho permanece hasta 14 s. La cámara interna de
  20–25 s se eleva a z=2,4 m para ocultar por geometría real. El resto de tiempos,
  trayectoria y cámaras se heredan; R04 y contexto 06 permanecen intactos.
- Puntos de referencia adaptados al nuevo hocico/cuello. El contexto conserva
  40 s y exportación métrica; las superficies aún necesitan rig/deformación.
- Generadores y verificadores nuevos; escenas/prefabs independientes en Unity.
  La comparación usa vértices transformados, evitando el exceso de tamaño de
  las cajas de renderer cuando un ojo gira. Corregida también la comprobación
  de componente Animator ausente durante la importación.
- Unity normalizó GraphicsSettings/QualitySettings al abrir. Se archivaron
  esos cambios propios en `Library/Session_20260924_creature_side_effects/`
  y se restituyeron al estado inicial. No se modificó configuración global.
- Documentación: `docs/chupacabras_modelo.md`, plan y este estado; en Unity,
  `docs/pasos08_09.md`. Intentos fallidos y sus logs quedan conservados.
- Revisión visual solicitada el 24 de septiembre: el plan ahora especifica
  figura exterior estática junto al panel, ambos anclados al mismo AprilTag
  (previsualización en paso 12, integración en 20), y reemplaza como objetivo
  futuro el corte brusco/entrada desde lente por movimiento anticipado y entrada
  lateral o detrás del granero (13–14). Motivo: reflejar la composición deseada
  tras revisar el video sin atribuirla a escenas o builds aún no implementadas.
  Documentado también en la evaluación G20, el bloqueo de 40 s y la nota Unity.

## Entregas y evidencia

Raíz Blender: `/home/cacawatin/code/blender/chupacabras`.

- **`scenes/08_chupacabras_forma_r03.blend`**: forma vigente.
- **`scenes/09_chupacabras_acabado.blend`**: acabado vigente.
- FBX/JSON homónimos en `exports/`; fuentes/FBX de contexto con `_contexto_r02`.
- Cuatro vistas por hito en `previews/`. Revisión principal de Unity:
  **`previews/09_chupacabras_acabado_unity_model_three_quarter.png`**,
  `09_chupacabras_acabado_unity_face.png` y
  `09_chupacabras_acabado_unity_comparison.png`.
- `scripts/chupacabras.py`, `chupacabras_contexto.py`, `verificar_chupacabras.py`.
- `docs/evidencias/2026-09-24_chupacabras/`: estado anterior, hashes iniciales y
  finales, generación/reapertura, resultados Unity y regresiones.

Raíz Unity: `/home/cacawatin/code/unity/chupacabras`.

- **`Assets/Scenes/08_chupacabras_forma_r03_contexto_r02.unity`** y
  **`Assets/Scenes/09_chupacabras_acabado_contexto_r02.unity`**.
- `Assets/Creature/<hito>/Chupacabras.prefab`, modelos y materiales.
- `Assets/Editor/CreatureBuild.cs`, `scripts/verify_creature.sh`.
- Capturas/JSON finales en `docs/evidencias/2026-09-24_08_chupacabras_forma_r03_contexto_r02/`
  y `docs/evidencias/2026-09-24_09_chupacabras_acabado_contexto_r02/`.
- Regresiones: `environment_20260925_003326/` y `sheep_20260925_003326/` bajo
  `docs/evidencias/`. Logs comprimidos y resumen en
  `docs/evidencias/2026-09-24_chupacabras_cierre/`.
- **Sin APK nueva.** Se conservan APK de bloqueo R04 y seguimiento 0.0.5,
  sin instalar ni probar físicamente en esta sesión.

## Pruebas y resultados

- Todas las mallas nuevas cerradas, sin caras degeneradas, UV finitos 0–1,
  escala métrica, sin rig nuevo ni dependencias externas. Reapertura independiente.
- Unity conserva triángulos, materiales y límites de vértices: error máximo
  del acabado **4,30e-7 m**. Capturas de frente, perfil, espalda, tres cuartos,
  rostro, comparación con oveja, escenas y ventana inspeccionadas.
- Contextos finales: cero solapamientos AABB de criatura/granero en **1.200**
  cuadros, con cajas conservadoras de paredes/tejado. **150/150** cuadros de criatura oculta, **114/114** de
  oveja oculta y **30/30** finales vacíos. Resolución de máscara 320 × 180.
  Acabado: ojo visible en 4 píxeles, oveja antes/después en 266/462 píxeles.
- Contacto de referencias: error máximo **9,91e-7 m** Blender, 565 muestras
  incluyendo cierre; **2,40e-6 m** Unity, 564 cuadros antes de volver al inicio.
- Demos reabiertas y 481 hashes históricos intactos. Regresión existente de
  escenario y cuatro poses de oveja correcta; error máximo de oveja **0,11 mm**.
- **32 aserciones de seguimiento correctas**. C# compilado en Unity fijado;
  todos los Python con sintaxis correcta; Bash de los verificadores correcto;
  clang-format del C# nuevo correcto. No hay otro linter propio configurado.
- `verify_assets.sh` se ejecutó con Bash porque no tiene bit ejecutable; no
  se cambió ese permiso. No se necesitó compilar Android para esta aceptación.

No hay validación física nueva. Conteos geométricos, máscaras y capturas de
Editor no demuestran brillo, GPU/fps móviles ni estabilidad del marcador.
Persisten luz definitiva (12), FOV/calibración, costo real del corto, cinco
minutos sostenidos, APK 0.0.5 física, Android con páginas 16 KB y S23 según sus
etapas. No se extrapolan resultados del Editor al teléfono.

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

Unity: commit de importación **`8aa3c292a3eeda9e73b3cc25553f23fe1194c2fd`**;
commit documental de presentación **`9647ab87150ec1cb43d6ad4bb3c47c4464b21195`**,
sin push. Quedó un archivo local no rastreado,
`ProjectSettings/PackageManagerSettings.asset`, que no pertenece a esta tarea
y se deja intacto. Blender: sin repositorio utilizable; no se inicializó ninguno.

**Retomar en 10.1:** adaptar el rig existente de `07_oveja_r04.blend` y preparar
la compresión de lana validada en la muestra 04. Usar la anatomía acabada 09 y
su contexto de cámara como referencia; no adoptar el giro rígido de muestra
como actuación final. Conservar todos los hitos anteriores.

Próximos dos pasos previstos:

1. **10:** rig/deformaciones de oveja, pastoreo/forcejeo y compresión de cuello,
   con exportación y comparación de poses en Unity.
2. **11:** rig del chupacabras, mandíbula/columna/cola y muestra de agarre
   deformable con apoyo correcto, sin mover la raíz AR. Depende de cerrar 10.

No se avanzó a un tercer paso. No hace falta teléfono para retomar 10.1.
