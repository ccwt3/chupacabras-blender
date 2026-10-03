# Ruta AR vigente y evaluación histórica

**2 de octubre de 2026:** reutilizar cámara, AprilTag y anclaje existentes para
una sola figura realista; retirar del nuevo flujo la ventana cinematográfica.
Ver [plan F1–F7](plan_secuencia.md) y [estado comprobado](estado.md).
La infraestructura no se reinicia; su aceptación histórica limitada tampoco
valida la futura geometría/materiales ni su carga de rendimiento.

F1 separará la presentación estática de `AppearanceStudy` y del fallback de
ventana de `TrackingProbe`. F5–F6 medirán figura y detector juntos en G20,
con candidata preparada antes de solicitar M#[7]. M#[6] queda sustituida sin
aprobar su antigua prueba física. S23 conserva su validación independiente.
Se mantienen Unity 6000.3.22f1, Linux/Android y el marcador medido existente.

**A continuación se conserva íntegro el informe histórico.** Sus referencias
a ventana, corto, pasos antiguos y solicitudes manuales describen aquel alcance;
no deben usarse como lista actual de tareas ni como validación de la figura nueva.

---

# Evaluación AR: Moto G20 de pruebas y posible Galaxy S23 de exposición

**Estado vigente tras aceptación del usuario (23 de septiembre de 2026): paso 3 completado.** Distancia/escala aproximada aceptada como hecha y rendimiento adicional aplazado; AprilTag es la ruta aceptada para continuar. **Pasos 4–5 ejecutados el 24 de septiembre de 2026; ver estado y evidencia de intercambio/bloqueo.** M#[2] cerrada para esta etapa. Los apartados siguientes conservan la evaluación y pruebas en su orden histórico; sus bloqueos anteriores quedan superados por esta decisión. Las lecturas originales y la ausencia de prueba física de 0.0.5 no cambian. S23 sigue pendiente.


## Requisitos confirmados

- Todas las pruebas previas se harán con el Moto G20. No se contará con el S23 antes de la exposición.
- Desarrollo en Linux, **Unity 6.3 LTS, versión exacta 6000.3.22f1**, y APK Android. Usar el Editor existente en `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`; no instalar, actualizar ni seleccionar otro Editor sin autorización explícita del usuario.
- Una figura estática del chupacabras y una ventana cinematográfica lateral, ambas ancladas a la misma pose del marcador; la ventana renderiza el corto 3D en tiempo real.
- Mantener una sola implementación de seguimiento para probar en el G20 y llevar al S23; no añadir un segundo flujo ARCore exclusivo para la exposición.

## Resultado de la evaluación documental

**Primer candidato para la prueba técnica: AprilTag con `jp.keijiro.apriltag`.** Su repositorio declara Linux x86-64 y Android ARM64, y el paquete indica licencia BSD-2-Clause y Unity 2021.3. Esto justifica probarlo, pero no demuestra funcionamiento en Unity 6.3 LTS ni en el G20 concreto. El ejemplo devuelve posición y rotación de un marcador; la integración de cámara, ventana, pausas y reproducción será trabajo del proyecto. [Takahashi, s. f.-a](https://github.com/keijiro/jp.keijiro.apriltag); [Takahashi, s. f.-b](https://raw.githubusercontent.com/keijiro/jp.keijiro.apriltag/main/Packages/jp.keijiro.apriltag/package.json).

| Candidato | Evidencia y limitación | Decisión para este proyecto |
| --- | --- | --- |
| AprilTag para Unity | Plataformas Linux y Android declaradas; integración pequeña centrada en marcadores. Unity 6.3 y el teléfono están por probar. | Probar primero; no adoptar como validado todavía. |
| OpenCV for Unity + ArUco | El proveedor ofrece Editor, Linux y Android y ejemplos de visión; la prueba gratuita no permite builds Android. | Alternativa si falla AprilTag. Requiere evaluar versión completa y autorización de compra si no se dispone de licencia. |
| artoolkitX / arunityx | SDK Unity de marcadores, con licencia LGPL-3.0 y permisos adicionales. El README del wrapper no incluye Linux entre los destinos de su script de plugins. | Menor prioridad: no asumir que el soporte Linux del núcleo demuestra el del wrapper Unity actual. |
| EasyAR | Seguimiento de imágenes con cámara, pero su tabla de plataformas de escritorio enumera Windows/macOS y no Linux. | No seleccionarlo mientras no exista evidencia suficiente del flujo de desarrollo Linux requerido. |

Fuentes para la comparación: [Enox Software](https://enoxsoftware.com/opencvforunity/), [artoolkitX](https://raw.githubusercontent.com/artoolkitx/arunityx/master/README.md), [EasyAR](https://www.easyar.com/doc/en/develop/image-tracking/devices.html).

## Qué cambia para el usuario

La primera prueba usará un **marcador AprilTag en blanco y negro** sobre el stand. No es un QR con una URL ni una ilustración reconocida libremente. La propuesta permite rodearlo de decoración sin modificar el símbolo ni sus márgenes. El wrapper consultado usa la familia `tagStandard41h12`; fijar familia, ID y tamaño al preparar el recurso. [Takahashi, s. f.-a](https://github.com/keijiro/jp.keijiro.apriltag).

Mientras el marcador sea visible y se obtenga una pose válida, se mostrarán la figura estática a escala de maqueta y la ventana lateral. Al perderlo, ocultar ambos y pausar el corto; recuperarlo permite continuar con la figura en el mismo lugar relativo. Esta ruta no incorpora seguimiento espacial persistente fuera de vista. La misma condición se aplicará en el S23.

La prueba física anterior de cubo estático junto a una ventana móvil sirve como referencia directa para esta composición. La figura virtual se colocará en otro punto de la raíz anclada, dejando libres el dibujo AprilTag y sus márgenes. El ajuste de tamaño y separación se verifica en el paso 12; no cambia el detector ni añade ARCore.

## Prueba de viabilidad antes de producir recursos finales

1. **Astra:** comprobar instalación Unity/Linux, revisar dependencias y plugins del candidato y fijar una revisión. Preparar una escena que detecte un tag desde una imagen de prueba y luego desde cámara. Verificar que las bibliotecas Linux se cargan.
2. **Astra:** construir una APK mínima con vista de cámara trasera, detección y cubo/ventana sin el corto. Comprobar compatibilidad de binarios Android con la versión de Unity y arquitectura real del dispositivo; no suponer que el sistema admite ARM64 solo por el procesador.
3. **Tú:** conectar/desbloquear el G20 y aceptar USB/cámara. Astra identifica modelo, Android y ABIs mediante ADB, instala y recoge logs.
4. **Astra:** resolver orientación, reflejo, proporción de imagen y correspondencia entre cámara y proyección 3D. Medir o ajustar intrínsecos/FOV y registrar resolución y cámara usadas. No basta reconocer el ID: deben ser estables la posición y la escala.
5. **Tú:** imprimir y medir el tag indicado; sostener el teléfono y realizar acercamiento, inclinación y pérdida/recuperación. Si hace falta calibración, Astra prepara el patrón y explica las capturas físicas necesarias.
6. **Astra:** medir tiempo de detección, estabilidad y rendimiento, ajustar solo lo necesario y documentar resultados. Probar la carga gráfica de una RenderTexture antes de dar por viable el corto.

Para aprobar: build desde Linux, bibliotecas cargadas, cámara y marcador funcionando en el G20, pose útil y repetible, pérdida/recuperación correctas y margen gráfico para el corto. No dar por aprobado con una imagen estática o un render del Editor.

Si el wrapper exige una migración extensa o el seguimiento no resulta estable, detener esa integración y comparar una alternativa concreta. No crear un motor de visión propio ni comprar un paquete sin autorización.

## Entrega para el S23

El Galaxy S23 figura en la lista ARCore, pero eso no valida esta integración AprilTag. Mantener la misma APK y el mismo marcador, con calidad conservadora validada en el G20. [Google, s. f.](https://developers.google.com/ar/devices).

La APK deberá seleccionar la cámara trasera normal y permitir comprobar o ajustar la proyección si sus parámetros difieren. La calibración del G20 no se copiará como constante universal al S23. Preparar instrucciones para instalar, conceder cámara, detectar el tag y reproducir un ciclo cuando el S23 esté disponible; verificar su orientación, escala y cámara ese día.

La entrega se rotulará **«verificada en Moto G20; S23 pendiente de prueba física»** mientras no se haya ensayado realmente allí. La falta de acceso previo al S23 no impide cerrar la entrega validada en el G20. Llevar también el G20 con la APK validada como respaldo para la demostración, si está disponible.

## Estado

Evaluación documental realizada el 21 de septiembre de 2026. Se revisaron documentación, manifest y ejemplo de código del candidato. No se han instalado paquetes, creado proyecto Unity, compilado APK ni probado ninguno de los teléfonos en esta evaluación. El próximo hito técnico es la prueba mínima de los pasos 2–3 del plan.

Actualización del 23 de septiembre de 2026: el usuario fija Unity 6000.3.22f1 para utilizar su instalación existente y evitar instalar otro Editor. La prueba de viabilidad debe realizarse con esa versión exacta; esta decisión no constituye validación del candidato.

## Continuación comprobada del paso 2 — 23 de septiembre de 2026

Proyecto creado en `/home/cacawatin/code/unity/chupacabras` con Unity 6000.3.22f1 y URP 17.3.0. AprilTag 1.0.3 embebido en revisión `fd6dd4698c9c6d2dc4a5e676beeab7f620006c78`, con sus archivos originales y licencias. La carga Linux y la detección de ID 0 sobre una imagen sintética pasaron; el blanco no produjo detecciones.

Se compiló desde Linux una APK IL2CPP/ARM64 de diagnóstico estático. Firma y empaquetado verificados; bibliotecas alineadas a 16 KB. El primer intento sufrió OOM de IL2CPP y se resolvió limitando trabajadores en el script del proyecto, sin cambiar configuración global. La implementación de esta revisión calcula FOV **vertical en radianes** en `PoseEstimationJob.cs`, a diferencia de la descripción del README; conservar este dato al preparar proyección real.

**No se ha instalado ni probado en G20 ni S23.** ARM64 es provisional hasta consultar las ABIs del G20; cámara, marcador físico, pose, escala, recuperación y rendimiento siguen pendientes. La compilación no adopta al candidato como validado. Paso 3 no iniciado en esta sesión. Detalles y evidencia en [estado.md](estado.md) y en `docs/preparacion_android.md` del proyecto Unity.

## Referencias

Enox Software. (s. f.). *OpenCV for Unity*. https://enoxsoftware.com/opencvforunity/

Google. (s. f.). *ARCore supported devices*. https://developers.google.com/ar/devices

Takahashi, K. (s. f.-a). *jp.keijiro.apriltag* [Repositorio de código]. GitHub. https://github.com/keijiro/jp.keijiro.apriltag

Takahashi, K. (s. f.-b). *package.json: jp.keijiro.apriltag* [Archivo de código]. GitHub. https://raw.githubusercontent.com/keijiro/jp.keijiro.apriltag/main/Packages/jp.keijiro.apriltag/package.json

artoolkitX. (s. f.). *arunityx* [Repositorio de código]. GitHub. https://github.com/artoolkitx/arunityx

EasyAR. (s. f.). *Device and platform support*. https://www.easyar.com/doc/en/develop/image-tracking/devices.html


## Continuación del paso 3 — preparación física

Se preparó `Assets/Scenes/03_TrackingProbe.unity` en la raíz Unity: permiso/cámara trasera, normalización de giro/reflejo, proyección con proporción conservada, cubo de 50 mm, pérdida/recuperación y carga mínima RenderTexture 512 × 288. APK `03_tracking_20260923_213432.apk`, build Unity 6000.3.22f1 desde Linux con 0 errores/0 advertencias de BuildReport. No es el corto final.

Marcador provisional A4 en `marker/03_marker_a4.pdf`, editable CeTZ: familia tagStandard41h12, ID 0, **100 mm entre esquinas de detección**, dibujo completo 180 mm. El original y el patrón del PDF coinciden; se detecta desde rasterización del PDF. Esto no comprueba impresión ni escala física.

Las 29 comprobaciones sintéticas y las capturas de adquisición/pérdida/recuperación pasaron en Editor. Firma v2, empaquetado y ocho bibliotecas ARM64 alineadas a 16 KB comprobadas. **No se ha conectado ni ensayado el G20/S23 en esta sesión**. FOV 60° provisional, sin calibración; las mediciones de CPU del Editor no son rendimiento móvil. La proyección real, distorsión, escala, estabilidad y margen de render siguen por medir.

**M#[2] pendiente:** acceso USB, impresión medida y recorrido de cámara/pose. Guía preparada en [prueba_g20.md](/home/cacawatin/code/unity/chupacabras/docs/prueba_g20.md). Consultar ABIs reales antes de instalar; si no hay ARM64 o el candidato falla, guardar diagnóstico y detener esta combinación. No cambiar tecnología ni añadir ARCore automáticamente.


## Primer acceso físico al G20 — 23 de septiembre de 2026

Confirmados Android 11/API 30 y `arm64-v8a` por ADB. APK 0.0.3 compilada con Unity 6000.3.22f1, instalada y abierta en el teléfono; biblioteca AprilTag ejecutada con prueba positiva ID 0/pose finita y negativa sobre blanco. La prueba usa imagen incluida: **no valida impresión, seguimiento ni calibración**. Cámara trasera Camera 0 abierta a 640 × 480. Corregido stripping de MeshCollider observado únicamente en Android y panel horizontal demasiado grande.

Se cierra preparación del **paso 2**. **Paso 3 pendiente M#[2]**: el usuario aún no dispone del marcador impreso. Falta escala, orientación óptica, pose estable, recuperación y costo con RT visible. AprilTag continúa candidato, no adoptado para producción; S23 pendiente. La app se desinstaló y se verificó ausencia de paquete/proceso/datos externos por instrucción del usuario. Detalle: [diagnóstico físico](/home/cacawatin/code/unity/chupacabras/docs/diagnostico_g20.md).

## Evidencia física de marcador — continuación del 23 de septiembre de 2026

El G20 detectó la impresión carta medida; usuario confirmó cubo y ventana, giro vertical/horizontal y desaparición/recuperación. Captura 320 × 240 en 0.0.4 reduce conversión de imagen y mantiene ~30 fps con RT en tramos registrados. No demuestra calibración ni margen final: referencias manuales aproximadas, detector efectivo 7.8–9 Hz y comparación RT sí/no todavía pendiente. 0.0.5 elimina una puerta temporal redundante y queda compilada sin instalar; su beneficio no está validado físicamente. Se conserva AprilTag como candidato, sin ARCore ni extrapolación al S23. Teléfono limpio tras retirar la app propia. Detalles y punto de reanudación en `docs/estado.md`; informe técnico en la raíz Unity, `docs/seguimiento_fisico_g20.md`.

## Continuación de intercambio y bloqueo — 24 de septiembre de 2026

Se conserva la ruta AprilTag aceptada y el alcance físico del cierre anterior.
Los pasos 4–5 añaden FBX, escena de intercambio y bloqueo de 40 s con cámara
interna/RenderTexture. Son comprobaciones de Blender y Unity, sin nueva prueba
física ni modificación del seguimiento. La APK de bloqueo usa una escena
independiente sin captura de cámara; no sustituye la APK de seguimiento 0.0.5.
No se ha probado la nueva revisión en el G20 ni en el S23. El costo móvil,
calibración pendiente y validaciones posteriores conservan sus limitaciones.

Detalles: [intercambio](intercambio_blender_unity.md), [bloqueo](bloqueo_40s.md)
y [estado vigente](estado.md).
