# Plan vigente: chupacabras realista como figura AR

**Cambio de alcance autorizado el 2 de octubre de 2026.** Se conserva este
nombre de archivo como entrada de continuidad. El plan de 24 pasos y corto de
40 s queda [archivado](plan_secuencia_40s_historico.md), no vigente.
[Estado comprobado](estado.md) · [Próximo trabajo](estado.md#punto-exacto-de-retoma) ·
[Ficha visual y funcional](ficha_produccion.md).

## Objetivo y alcance

Una aplicación Android, desarrollada y compilada desde Linux con **Unity
6000.3.22f1**, reconoce el **AprilTag existente** y muestra **un chupacabras
original, estático, centrado directamente sobre el símbolo**, con anatomía,
pose y materiales de mayor realismo. El usuario mueve el teléfono para
observarlo desde distintos ángulos. Blender sigue siendo la fuente editable.

La escena de entrega no incluye ventana cinematográfica, RenderTexture de
cine, cámaras internas, oveja, escenario, ataque, arrastre, polvo, audio
narrativo ni Timeline. **La duración de 40 s deja de ser requisito vigente.**
Tampoco se añade por defecto respiración, idle, autorrotación, interacción,
seguimiento persistente de la habitación o plataforma decorativa. Una figura
estática es el alcance base; ampliar eso requiere una petición nueva.

Se conservan físicamente todas las demos, escenas, exportaciones, scripts,
APKs y evidencias anteriores. Excluirlos del nuevo flujo y build no significa
borrarlos. No limpiar `scenes/` ni dependencias históricas en esta migración.

## Evaluación del cambio

La infraestructura existe: Unity exacto, compilación Android ARM64/IL2CPP,
captura de cámara, normalización de imagen, AprilTag, proyección, anclaje y
manejo de pérdida/recuperación. Hay aceptación física histórica en G20 con
alcance limitado y un modelo demacrado exportable. No se reinicia el motor AR.

La simplificación elimina dos personajes actuando, contacto/arrastre,
sincronización, cámara cinematográfica y efectos. La aplicación vigente aún
los referencia: `TrackingProbe.appearance` llama a `AppearanceStudy.Attach`
y `Present`, que crean RenderTexture/Playables. Si `appearance` es nulo,
`TrackingProbe` crea el cubo y ventana de diagnóstico. **Desactivar el panel o
poner `appearance = null` no implementa la figura aislada.** F1 debe dar al
tracking una presentación estática propia y evitar ambas rutas antiguas.

El costo de render de cine puede retirarse; no se promete una ganancia concreta
ni que toda esa capacidad admita más polígonos. Cámara/detector, texturas,
sombras, overdraw y geometría seguirán contando. El salto artístico es trabajo
real: ocultar la ventana no vuelve realista la malla. La aceptación numérica de
13–14 tampoco equivale a aprobación estética; el usuario indicó que esa
actuación no le convence.

## Acuerdos que se mantienen

- Blender/modelos y fuentes: `/home/cacawatin/code/blender/chupacabras`.
- Unity/AR Android: `/home/cacawatin/code/unity/chupacabras`.
- Invocar solo `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`.
  No instalar, actualizar o seleccionar otro Editor; no cambiar configuración
  global ni otros proyectos. `ProjectVersion.txt` ya registra esa versión.
- URP, captura y AprilTag existentes; no ARCore, AR Foundation ni otro detector.
  Conservar paquetes/bloqueos salvo necesidad demostrada y documentada.
- Moto G20 para pruebas; posible S23 solo en exposición y pendiente hasta probarlo.
- Marcador `tagStandard41h12`, ID 0, 100 mm entre esquinas de detección,
  dibujo 180 mm; reutilizar impresión carta medida y sus márgenes. No es un
  lector de QR convencional. No pedir nueva impresión sin necesidad.
- Figura centrada sobre el tag; su superposición virtual es intencional. El
  detector debe usar cámara real sin composición y ver el patrón físico.
- Proyección/FOV 60° provisional; no declarar calibración exacta. No copiar una
  supuesta calibración universal del G20 al S23.
- Chupacabras original demacrado, identidad de las tres referencias: espalda
  arqueada, costillas, extremidades angulosas, cola, cresta y ojos amarillos.
- Retirar únicamente lo instalado para pruebas y verificar limpieza al cerrar
  cada sesión física. No retirar otras aplicaciones ni datos del usuario.

## Comportamiento de la figura

1. Sin pose válida: cámara real y estado de búsqueda; figura oculta.
2. Pose válida del ID correcto: una sola figura anclada, con escala estable.
3. Pérdida, timeout de cámara o segundo plano: ocultar la figura; no dejarla
   flotando en la última pose. Liberar/suspender recursos según el flujo probado.
4. Recuperación/reanudación: volver a detectar y mostrar la misma instancia
   anclada, sin duplicación ni salto de escala. No hay reloj narrativo que continuar.
5. Permiso denegado o detector/cámara fallidos: estado comprensible y recuperación
   controlada; no prometer figura visible si no hay seguimiento.

Conservar los tests históricos y adaptar únicamente los afectados por F1;
no borrar aserciones de pérdida/timeout para hacer pasar el nuevo flujo.

## Etapas nuevas y aceptación

Los identificadores **F1–F7** evitan confundir este plan con los hitos 1–24.
**Todas están pendientes de ejecución. Esta sesión solo cambia documentación.**
Máximo dos etapas principales por sesión, contando una retomada como primera.

### F1. Aislar la figura AR existente

**Depende de:** infraestructura actual comprobada; no de cerrar el viejo paso 12.

- Crear una escena/prefab propios, por ejemplo `Assets/Scenes/F1_FiguraAR_r01.unity`
  y `Assets/FiguraAR/`, reutilizando `StaticFigure` de la escena demacrada R02.
  Conservar transformaciones, conversión de ejes y centrado sobre el tag.
- Leer completo `TrackingProbe`, `AppearanceStudy`, `CameraGeometry`, tests y
  build existentes. Añadir la ruta mínima de figura estática compartiendo cámara,
  detector y estado; no duplicar el sistema de seguimiento ni añadir frameworks.
- Evitar crear/activar panel, cámara interna, RenderTexture de cine, oveja,
  escenario y Playables en la escena nueva. Mantener operativas escenas históricas.
  No eliminar recursos de captura/proyección que sí utiliza la cámara AR.
- Preparar build Android y verificador propios con destinos nuevos. Mantener
  identidad/versionado de prueba documentados y restaurar ajustes temporales.
  Corregir etiquetas/botones de reloj, tres estudios y RT que no aplican.

**Entrega:** escena editable nueva, capturas en tres ángulos, APK base de figura
con nombre/hash nuevos y comprobación de dependencias de la build.
**Aceptación:** abre/compila con el Editor exacto; figura única y centrada;
adquisición/pérdida/timeout/recuperación/segundo plano sintéticos correctos;
ninguna ruta cinematográfica creada ni incluida por dependencia accidental.
Revisar BuildReport/dependencias incluidas, no solo objetos desactivados.
La comprobación sintética no acredita nueva ejecución física.
**Usuario:** sin intervención; no pedir el teléfono solo para empezar F1.

### F2. Refinar anatomía y pose para inspección cercana

**Depende de:** F1, para revisar en la composición real; fuente 09 demacrada R02.

- Trabajar en un `.blend` nuevo (por ejemplo `F2_chupacabras_forma_r01.blend`).
  Reutilizar la base y el rig como herramienta de pose si conviene; no continuar
  la actuación 14 ni adoptar su encuadre para ocultar defectos.
- Refinar uniones anatómicas, rostro, manos/pies, costillas, cola y cresta.
  Dar una pose estática asimétrica, tensa y con apoyo creíble, sin convertirlo
  en otra criatura ni volver al volumen fornido ya descartado.
- Revisar frente, perfil, espalda, tres cuartos, zonas inferiores accesibles
  y primer plano. Preparar giro de inspección, no animación de ejecución.

**Entrega:** fuente versionada, al menos seis vistas y comparación con la base
bajo cámara/luz equivalentes. Propuesta visible antes de dedicar detalle fino.
**Aceptación:** silueta reconocible y anatomía coherente; sin piezas flotantes,
intersecciones evidentes ni defectos escondidos por un único encuadre. Registrar
el juicio visual y sus límites además de verificadores geométricos. La revisión
estética es opcional; cualquier objeción recibida debe resolverse, no ignorarse
porque un test pasó. Aceptación visual final pendiente del modelo en G20/F5.

### F3. Preparar la malla móvil y el acabado de superficie

**Depende de:** F2 con silueta/pose resueltas y sin objeciones abiertas.

- Mantener fuente de detalle separada de la malla exportable si se esculpe alta
  resolución. Usar retopología/bake solo donde aporten a la silueta o superficie.
- UV, normales y materiales PBR compatibles con URP: variación de piel seca,
  rugosidad, ojos, dientes y garras. Registrar autoría/licencia de cualquier
  recurso nuevo; no empaquetar imágenes de referencia sin licencia.
- Partir de los **30.880 triángulos / 18 mallas / 6 materiales** documentados
  del acabado actual como comparación, no como presupuesto final aprobado.
  Reducir materiales cuando sea útil; texturas iniciales de hasta 2K como
  hipótesis de trabajo, no requisito ni autorización para agotar la memoria.
- Para la figura estática, hornear la pose exportable sin necesidad de ejecutar
  Animator/rig. Conservar controles y fuente de alta resolución en Blender.

**Entrega:** `.blend` de detalle/exportación, FBX estático, texturas y ficha de
triángulos, materiales, memoria estimada, mapas y licencias.
**Aceptación:** reapertura e importación métricas correctas, sin costuras/normales
rotas ni materiales ausentes; detalle legible desde cerca y a tamaño de uso;
comparación documentada con F2. Rendimiento todavía por medir en F5.

### F4. Integrar materiales e iluminación de la figura

**Depende de:** F1 y F3.

- Integrar la nueva malla en el prefab AR propio; mantener una sola instancia.
  Reconstruir y comprobar mapas/materiales en Unity, referencia de producción.
- Ajustar luz, reflejos y ojos para lectura sobre fondos reales, sin reintroducir
  cielo, granero, suelo ficticio ni cámara de cine. Sombras/contacto solo si
  aportan y su costo se justifica; no añadir detección de planos por inercia.
- Conservar centrado y escala de partida; afinar presentación en la nueva figura
  si la silueta lo exige, sin inventar mediciones físicas.

**Entrega:** prefab/escena de figura detallada, capturas desde seis vistas y
APK candidata con versión/hash. Registro de materiales y configuración local.
**Aceptación:** comparaciones Blender/Unity, lectura de rostro y silueta, malla
sin defectos visibles desde atrás/lados y ausencia de contenido cinematográfico.
Sin afirmar brillo real o calidad final móvil a partir del Editor.

### F5. Validar figura, seguimiento y costo en Moto G20

**Depende de:** F4; preparar todo antes de solicitar **M#[7]**.

- Preparar APK firmada/verificada, marcador existente, guía corta y resultados
  a observar. El agente identifica ABI/dispositivo, instala, registra y depura.
- Usuario: conectar/desbloquear, permisos, mirar desde varios ángulos/distancias,
  ocultar/recuperar tag y probar segundo plano; observar la figura de cerca.
  Registrar defectos concretos de forma/material/luz y sensación de estabilidad.
- Medir al menos cinco minutos con captura+detector+figura activos: fps/frame
  time, CPU/GPU cuando estén disponibles, memoria, picos y degradación térmica.
  Comparar con la base F1 con condiciones equivalentes si se necesita diagnóstico.
- Conservar objetivo inicial de **30 fps sostenidos**; reportar distribución,
  caídas y condiciones. No confundir frecuencia del detector con fps de render.
  No tratar una captura aislada ni cinco minutos de Editor como prueba móvil.

**Entrega:** evidencia real, lectura visual del usuario registrada, métricas,
fallos priorizados y limpieza del teléfono comprobada.
**Aceptación:** visibilidad/pose/escala útiles, figura única, pérdida/recuperación
y reanudación correctas; sin fallos visuales críticos. Si desempeño o apariencia
fallan, registrar el pendiente y pasar a F6 para corregir, sin declarar F5 aprobado.

### F6. Corregir y verificar la candidata final

**Depende de:** evidencia de F5, aunque haya resultado fallido; no de una
aprobación ficticia. Cierre solo después de resolver sus fallos.

- Corregir primero problemas observados; medir antes/después al cambiar malla,
  texturas, sombras, resolución o frecuencia del detector. No hacer degradaciones
  generales sin identificar el costo; no prometer «máxima calidad» sin números.
- Probar permiso denegado/aceptado, marcador ausente/incorrecto, cámara detenida,
  recuperación, rotación de pantalla, segundo plano, varios ciclos de detección
  y funcionamiento sin red con recursos empaquetados.
- Repetir M#[7] únicamente en casos afectados y el perfil sostenido de la
  configuración final. Revisar firma, ABI, permisos, ELF/empaquetado y build.
  Distinguir comprobación de alineación 16 KB de prueba en un Android de 16 KB.

**Entrega:** APK candidata final, informe de regresiones y perfil comparado.
**Aceptación:** sin fallos críticos pendientes en G20; pruebas visuales y de
rendimiento de la misma configuración que se entregará, no de una anterior.
Sin crecimiento continuo de memoria o degradación que impida la exposición.

### F7. Entregar y preparar la exposición

**Depende de:** F6 aprobado en G20.

- Reabrir/compilar desde Linux; empaquetar fuentes Blender, proyecto Unity,
  recursos/licencias, APK versionada con hash, marcador y guía de uso breve.
- Verificar instalación de esa APK final en G20 dentro de M#[7], y retirar lo
  instalado para pruebas al cerrar conforme a la instrucción vigente.
- Preparar **M#[8]** para el posible S23 cuando esté disponible: misma APK,
  cámara trasera, permiso, orientación, pose, escala y observación de la figura.
  Comprobar proyección en ese equipo; no extrapolar aceptación del G20.

**Entrega:** APK y documentación reproducibles, inventario de entregas vigentes
y comprobación de fuentes. Rótulo «verificado en G20; S23 pendiente» hasta
obtener evidencia real. No publicar en tienda ni añadir AAB/cuentas de firma
sin una ampliación explícita del encargo. Git commit/push según la solicitud.

## Correspondencia con el plan anterior

| Trabajo anterior | Nuevo tratamiento |
| --- | --- |
| 1: guion y ficha | Sustituido por este alcance y ficha de figura. |
| 2–3: Unity/Android/cámara/AprilTag | Se reutilizan; F1/F5 verifican las partes afectadas, sin rehacer el motor. |
| 4: intercambio | Se conserva conocimiento de escala/ejes; figura exportada estática en F3. |
| 5–7: bloqueo, escenario, oveja | Históricos, fuera de la nueva aplicación. Fuente/licencia conservadas. |
| 8–9: chupacabras | Base para F2–F4; no declarado acabado realista por existir ya. |
| 10–11: rigs/contacto | Conservados para autoría/historia; locomoción y contacto no son tareas activas. |
| 12: aspecto con figura/panel | Sustituido por F1/F4–F5; no cerrar la antigua M#[6] como aprobada. |
| 13–19: actuación, 40 s, Timeline, polvo/audio | Retirados del plan activo; demos y resultados permanecen archivados. |
| 20: integración de ventana/corto | Reemplazada por presentación de una figura en F1/F5. |
| 21: marcador | Reutilizar impresión medida; solo revisar cambios reales del stand. |
| 22–24: perfil, verificación y entrega | Conservan su propósito en F5–F7, aplicado a la figura. |

## Acciones manuales y continuidad

- **M#[1]**: guion/audio histórico resuelto, fuera del alcance actual.
- **M#[2] y M#[3]**: cierre histórico de ruta/impresión; no repetir sin motivo.
- **M#[4]**: aceptación histórica del modelo/composición anterior, no de F1–F7.
- **M#[5]**: antigua prueba prevista de integración figura+ventana; sustituida,
  fuera de alcance, nunca ejecutada ni aprobada como prueba nueva.
- **M#[6]**: revisión 0.0.15 anteriormente aplazada; sustituida por cambio de
  alcance, **sin validación física**. No pedir el G20 para cerrar aquella ventana.
- **M#[7]**: nueva figura en G20, prevista para F5–F7; no solicitada todavía.
- **M#[8]**: S23 en exposición, prevista solo si llega a estar disponible.

No hay intervención física indispensable para esta replanificación ni para
empezar F1–F2. No pedir decisiones ya confirmadas. Si aparece una nueva decisión
creativa indispensable, preparar vistas concretas antes de solicitarla y guardar
el punto de interrupción; el silencio no cuenta como aprobación.

Actualizar `docs/estado.md` de Blender tras cada sesión. `docs/estado.md` de
Unity enlaza a esa continuidad, sin duplicar tareas ni resultados. El usuario
aclaró que «next-job» pertenecía a otro proyecto; no se crea ese archivo. El plan
canónico vive en Blender.
Al continuar, comprobar archivos/resultados y ejecutar como máximo las próximas
dos etapas pendientes; conservar fuentes anteriores y documentar límites reales.
**Próxima pareja: F1 + F2. No retomar 15/arrastre ni 16/consolidación del corto.**
