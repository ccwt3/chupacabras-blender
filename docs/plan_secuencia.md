# Plan de producción: Chupacabras en AR para Android

## Objetivo y alcance

Crear una secuencia 3D estilizada de **40 segundos**, producida en Blender e integrada como modelos y animaciones en **Unity 6.3 LTS, versión exacta 6000.3.22f1**, para una aplicación Android de realidad aumentada desarrollada desde Linux. Al reconocer un AprilTag impreso en un stand, la aplicación muestra una figura estática del chupacabras junto a la secuencia cinematográfica y la repite. El salto del campo vacío a la oveja reapareciendo es deliberado.

La entrega principal pasa a ser **el proyecto Unity, sus recursos editables y una APK instalable**. Un MP4 puede servir como evidencia, pero no sustituye la escena animada ejecutándose en Unity.

El chupacabras es el protagonista visual: tendrá un modelo original basado en las tres referencias recibidas. La oveja procederá de un modelo low-mid poly existente, adaptado para Blender y Unity.

El trabajo se divide en **24 pasos**, cada uno con subpasos asignados a Astra o al usuario y una entrega verificable. Se han creado demos Blender aparte. Los pasos 1–3 están cerrados con el alcance aceptado y documentado; la ABI, instalación, cámara y seguimiento físico se comprobaron en el G20. Los pasos 4–9 están completados con evidencia de intercambio, bloqueo, escenario, oveja y modelado/acabado del chupacabras; consultar `docs/estado.md`. Los pasos 10–11 también están completados con rigs y contacto R03 validados. El paso 12 está cerrado tras la revisión física de R05/0.0.14 en el G20 y aceptación del usuario; M#[4] resuelta. La solicitud del 2 de octubre de 2026 reabre 8–9 para un chupacabras demacrado; se revisan en esta sesión. La nueva malla requiere propagar y revalidar 11–12 antes de iniciar 13–14. El cierre físico de 12/M#[4] se conserva para el modelo anterior. Véase [revisión demacrada](chupacabras_demacrado.md). **Continuación vigente:** 11 adaptado y verificado con la nueva malla; 12.1 preparado en R02/0.0.15, pendiente de revisión física **M#[6]** antes de cerrar 12.2–12.3. 13–24 no iniciados. Véase [rig/aspecto demacrado](rigs_demacrado.md).

## Dispositivos confirmados: G20 para pruebas, posible S23 para exposición

**El Moto G20 es obligatorio para todo el desarrollo y las pruebas previas.** El Samsung Galaxy S23 probablemente se usará en la exposición, pero no estará disponible antes. Esta decisión ya está resuelta; no volver a pedir otro teléfono para poder desarrollar.

El G20 no figura en la lista oficial de ARCore; el S23 sí. La ruta se diseña para el G20 y se mantendrá la misma implementación en ambos teléfonos. El posible S23 no justifica probar una tecnología diferente en cada equipo. [Google, s. f.-a](https://developers.google.com/ar/devices).

La validación de entrega se hará en el G20. El S23 quedará expresamente pendiente de prueba física hasta que esté disponible; preparar una comprobación de cámara, escala y reproducción para el día de exposición. No prometer compatibilidad del segundo teléfono solo por haber probado el primero.

## Tecnología candidata y alcance Linux

**Editor fijado por el usuario: Unity 6000.3.22f1.** Usar la instalación existente en `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity` y sus herramientas Android. Crear, abrir y compilar este proyecto con esa versión; no instalar otro Editor, actualizarlo ni seleccionar otra versión ya instalada sin autorización explícita. Invocar la ruta exacta para evitar que un lanzador genérico seleccione otra versión. Al crear el proyecto, comprobar que `ProjectSettings/ProjectVersion.txt` registra `6000.3.22f1`. Si una dependencia resulta incompatible, documentar el problema y buscar una versión compatible sin cambiar el Editor acordado.

**Primer candidato para comprobar:** Unity 6.3 LTS + URP + captura de cámara + seguimiento AprilTag mediante `jp.keijiro.apriltag`. El wrapper declara Linux x86-64 y Android ARM64; su manifest referencia Unity 2021.3. Es evidencia para una prueba de viabilidad, no certificación de Unity 6.3 ni del G20. [Takahashi, s. f.](https://github.com/keijiro/jp.keijiro.apriltag).

La evaluación, alternativas, limitaciones y prueba mínima están en [evaluacion_ar_moto_g20.md](evaluacion_ar_moto_g20.md). AprilTag fue el candidato inicial y es **la ruta aceptada tras la prueba funcional física en el G20**, con escala aproximada aceptada y medición adicional de rendimiento aplazada. Si falla, evaluar una alternativa concreta manteniendo Linux y el G20; no trasladar la prueba al S23 ni ampliar a un motor de visión propio sin acordarlo.

El requisito Linux sigue siendo edición y compilación Android desde Linux; Unity 6.3 documenta Ubuntu 22.04 y 24.04 como plataformas del Editor. Comprobar además que el plugin nativo del candidato carga en el equipo real. [Unity Technologies, s. f.-b](https://docs.unity.com/en-us/engine/6000.3/manual/get-started/install-and-upgrade/getting-started-installing-unity/system-requirements).

La nueva ruta no depende de ARCore, AR Foundation, XR Origin ni Google Play Services for AR. No añadir esos componentes por inercia del plan anterior. El proyecto gestiona cámara, proyección, pose del marcador y estado de seguimiento. Astra verificará arquitectura Android, carga de bibliotecas, orientación de imagen y proyección en los pasos 2–3.

## Marcador del stand y diferencia respecto a un QR

La prueba candidata usa **un AprilTag impreso en blanco y negro**, con familia, ID, tamaño y márgenes definidos. Puede integrarse en un cartel decorado sin alterar el símbolo. La ilustración del cartel aporta diseño; el tag aporta seguimiento. No se pretende reconocer cualquier imagen o la geometría del stand.

El marcador no es un QR con un enlace. Un QR lateral puede servir para distribución o información, pero no forma parte del detector AprilTag. La selección final de marcador queda ligada al candidato que pase la prueba.

**Comportamiento base:** con pose válida, mostrar el personaje AR estático y la ventana; al perder el marcador, ocultar ambos y pausar el corto; al recuperarlo, mantener la pose anclada y continuar. No se incluye seguimiento persistente de la habitación cuando el tag sale de vista. AprilTag es el marcador de seguimiento, aunque en la vista del Editor pueda parecer un QR; no se añade un lector QR para reemplazarlo.

## Presentación confirmada: figura 3D y ventana de cine ancladas en AR

La composición tiene dos elementos AR junto al mismo marcador: (1) un modelo estático del chupacabras, de pie y centrado directamente encima del tag a escala de maqueta; y (2) una ventana lateral que muestra la secuencia 3D en tiempo real mediante la cámara cinematográfica interna. El chupacabras de la maqueta permanece quieto; el de la ventana actúa la historia. El tamaño y la separación exactos se fijan al revisar una previsualización en el paso 12. Aclaración del usuario del 30 de septiembre: la figura debe estar directamente encima del símbolo, no desplazada hacia el borde superior del papel. Su oclusión virtual del dibujo es intencional; el detector recibe la imagen de cámara sin superposiciones. Mantener el patrón físico sin obstrucciones y el panel fuera del dibujo.

La cámara exterior AR sigue al teléfono y presenta directamente la figura 3D. La ventana muestra una RenderTexture de la escena, vista desde su cámara de cine. Mover el teléfono cambia la perspectiva de la figura exterior y el conjunto; no mueve la cámara cinematográfica ni altera el encuadre interno del corto. No se construye un portal volumétrico ni se añade seguimiento persistente de la habitación.

La figura se renderiza con la cámara exterior AR; el contenido y luces del corto se renderizan en la cámara interna. La captura real del teléfono sustituye el plano/patrón de AprilTag de referencia de las escenas de revisión del Editor. Ese patrón simula la composición en Editor y no es un QR funcional de la aplicación.

Con pose válida, ambos elementos siguen una sola raíz de marcador y no se duplican por detecciones repetidas. Al perder tracking, ocultarlos y pausar; al recuperarlo, continuar sin desplazar la figura respecto al tag. Se conservan la producción de 40 s, las cámaras internas y el fondo real del teléfono.

El cielo índigo, la luna y la iluminación nocturna pertenecen a la escena interna. La figura exterior recibe iluminación AR contenida que la mantiene legible sobre la cámara real. El salto y las sacudidas afectan solo a la cámara del corto, no a la cámara AR, el tracking ni la figura estática. La salida se evalúa dentro del panel interno.

**Revisión de cámara tras comentario del usuario, 24 de septiembre de 2026:** el corte del bloqueo a los 20 s y el inicio del salto detrás de la cámara son provisionales. En los pasos 13–14 se preparará un movimiento continuo y anticipado de la cámara interna alrededor de 18,5–20,5 s, sin un cambio abrupto en el fotograma del salto. El chupacabras entrará desde el lateral o detrás del granero y cruzará hacia la oveja; no empezará en el centro del lente. Conservar el inicio del salto en el segundo 20, la trayectoria cercana/por encima de la cámara interna y la independencia de la cámara AR. R04 permanece como referencia histórica; aplicar ajustes a nuevas escenas de animación.

## Referencias y dirección visual

Origen: `/home/cacawatin/Pictures/chupacabras/`. Las cinco imágenes se revisaron y copiaron a `references/` el 23 de septiembre de 2026; se verificó igualdad de contenido con los originales. Véanse [ficha de producción](ficha_produccion.md) y [registro de copias](evidencias/2026-09-23_continuidad/referencias.json). Los nombres antiguos `image_0.png`–`image_4.png` quedan sustituidos por estos archivos.

| Archivo | Función |
| --- | --- |
| `chupacabras1.jpg` | Postura baja de acecho, extremidades largas, garras, hocico agresivo y cresta alta. |
| `chupacabras2.jpg` | Rostro oscuro, orejas puntiagudas, ojos grandes y hombros fuertes. Mantener ojos amarillos luminosos según el encargo. |
| `chupacabras3.jpg` | Espalda arqueada, cuerpo fibroso, cola larga, cresta y contraste gráfico de trazos en las sombras. |
| `ejemplo_de_oveja.jpg` | Seleccionar una oveja existente con cuerpo claro y facetado, cabeza y patas oscuras. La imagen no contiene un modelo importable. |
| `ejemplo_de_escenario.jpg` | Noche azul, luna, refugio rural y bosque en silueta. Mantener tierra seca, un granero pequeño y una sola oveja. |

Chupacabras: cuadrúpedo demacrado y esquelético, abdomen hundido, costillas y articulaciones marcadas, hombros huesudos, espalda encorvada, extremidades angulosas, garras, mandíbula articulable, orejas puntiagudas, cola y cresta reconocibles. Integrar las referencias en una anatomía coherente low-mid poly. Resolver el aspecto desgreñado con mechones geométricos concentrados en cuello y lomo.

Acabado: colores sólidos, sombras profundas y definidas, cielo índigo y luna geométrica. La trama pintada o cruzada debe funcionar como material de Unity; no depender del compositor de Blender. Sin texturas detalladas ni pelo simulado. La violencia se comunica mediante actuación, mordida en el cuello lanudo, forcejeo y polvo; no se requieren sangre ni heridas abiertas.

## Cronología y decisiones narrativas

| Tiempo | Acción |
| --- | --- |
| 0–15 s | Oveja pastando; chupacabras apenas perceptible al fondo, con ojos visibles. |
| 15–20 s | Criatura completamente oculta, incluidos los ojos; continúa el pastoreo. |
| 20–25 s | Salto iniciado a los 20 s, aterrizaje y ataque. En modalidad ventana, la oveja queda oculta tras el atacante desde el aterrizaje hasta los 25 s. |
| 25–39 s | Ambos modelos visibles: agarre, forcejeo, arrastre pesado y salida. Margen de salida provisional. |
| 39–40 s | Campo vacío, según el margen propuesto. |
| 40 s | Reinicio completo al estado inicial y comienzo de otro ciclo. |

Decisiones confirmadas en M#[1]:

- **Trayectoria:** arrastre inicial hacia la izquierda y giro amplio hacia la salida derecha; fijar coordenadas y encuadres en el paso 5.
- **Ocultamiento:** desde el aterrizaje hasta los 25 s. Se conserva el salto iniciado a los 20 s y el corto de 40 s.
- **Audio:** incluir ambiente y efectos de pastoreo, balidos suaves, impacto, pisadas y arrastre; sin música.

Prototipo: autorrotación vertical/horizontal y marcador con 100 mm entre esquinas de detección; diseño final del stand pendiente en el paso 21. Moto G20 de pruebas y posible S23 solo en exposición ya confirmados; conectar el G20 cuando la prueba esté preparada.

Autoría propuesta a 30 fps: en Blender, `t = (fotograma - 1) / 30`; 0 s corresponde al 1, 15 s al 451, 20 s al 601, 25 s al 751 y el límite 40 s al 1201. El rango visible de una captura de 40 s sería 1–1200. Para exportar curvas puede ser necesario conservar una clave de límite en el 1201; verificar la duración importada y no perder 1/30 s al recortar clips.

Unity gobierna el ciclo por **tiempo**, con una duración de 40 s, independientemente de los fps efectivos del teléfono. El objetivo inicial de rendimiento es 30 fps sostenidos en el dispositivo acordado. No acumular fotogramas para medir la duración ni interpolar suavemente entre el campo vacío y el reinicio.

## Contrato de intercambio Blender–Unity

Estas son decisiones de implementación propuestas y se validan con una muestra pequeña en el paso 4.

- Conservar `.blend` como fuente y exportar explícitamente FBX con mallas, huesos y animación horneada. Importar los FBX en Unity; evitar depender de la conversión automática de archivos Blender.
- Usar escala coherente en metros, probar ejes y orientación con un objeto de tamaño conocido. Aplicar la escala AR uniformemente en una raíz de presentación, sin reescalar rigs de forma independiente.
- Usar rigs de tipo Generic para cuadrúpedos. Hornear el resultado de IK, constraints y contacto a huesos y transformaciones exportables; los controles de Blender no son el sistema de ejecución de Unity.
- Probar shape keys como blend shapes antes de depender de ellas. Si fallan en el recorrido de exportación elegido, resolver la compresión de lana con huesos simples.
- Mantener recorridos relativos a una raíz común de secuencia. Evitar que root motion y curvas de posición desplacen dos veces al personaje o muevan la raíz de seguimiento AR.
- Reconstruir materiales, luces y efectos en URP. Los nodos, sombras, mundo y partículas de Blender no constituyen una transferencia visual automática.
- Exportar movimientos de cámara para la cámara cinematográfica interna; ajustar y verificar su lente y encuadres en Unity.
- Dirigir ambos personajes, cámara interna, audio y efectos desde una única Timeline de 40 s. No ejecutar loops independientes que se desincronicen.
- Reutilizar la oveja bajo una licencia que permita modificaciones y distribución dentro de una app Android; registrar autor, enlace y atribución. Preferir recurso gratuito, sin asumir que cualquier descarga pública es reutilizable.
- Empezar con materiales compartidos, mallas sencillas, pocas luces y partículas limitadas. Establecer presupuestos de geometría, sombras, texturas y render según mediciones móviles; dar prioridad al chupacabras.

## Organización y continuidad entre sesiones

```text
/home/cacawatin/code/blender/chupacabras/
  docs/                 # Plan, estado, decisiones, pruebas y procedencia.
  references/           # Las cinco imágenes recibidas.
  assets/               # Oveja original y licencia.
  scenes/               # Fuentes Blender por hito.
  exports/              # FBX y recursos exportados.
  previews/             # Evidencias visuales; MP4 opcional.
  scripts/              # Automatización puntual de Blender, si hace falta.

/home/cacawatin/code/unity/chupacabras/
  Assets/               # Escenas, scripts y recursos importados de AR.
  Packages/             # Manifest y bloqueo de dependencias.
  ProjectSettings/      # Unity 6000.3.22f1 y configuración local.
  docs/                 # Configuración y pruebas de la aplicación.
  marker/               # Imagen de seguimiento, medidas y versión imprimible.
  builds/android/       # APK de pruebas y entrega; AAB solo si se acuerda.
```

Rutas separadas confirmadas por el usuario el 23 de septiembre de 2026: Blender y animaciones en la primera; aplicación AR real en la segunda. No crear el antiguo proyecto anidado `unity/ChupacabrasAR/`. El árbol expresa la organización prevista; consultar [estado.md](estado.md) para saber qué existe realmente. El estado general permanece en `docs/estado.md` del proyecto Blender. Las entregas `marker/` y `builds/android/` de los pasos posteriores pertenecen al proyecto Unity.

Ejecutar como máximo los siguientes dos pasos principales pendientes por sesión, contando el retomado como primero, y conservar el último hito validado. Respetar dependencias; ante una decisión indispensable sin respuesta, guardar estado y detenerse. Actualizar `docs/estado.md` al terminar: qué cambió y por qué, entradas, salidas, pruebas realizadas, decisiones pendientes y siguiente paso. Para Unity, conservar `.meta`, `Packages/manifest.json`, `Packages/packages-lock.json` y `ProjectSettings/`; no tratar `Library/` como fuente.

Usar nombres de hitos relacionados con el paso, como `08_chupacabras_forma.blend`. No duplicar todo el proyecto Unity por paso; registrar sus cambios en el control de versiones disponible. No alterar otras instalaciones o proyectos del equipo para resolver problemas locales.

Ejecutar tests y linters existentes al modificar código. Las pruebas nuevas deben cubrir riesgos reales, principalmente duración/reset y transiciones del seguimiento. Para cambios visuales, generar evidencia reproducible. Si una prueba necesita un dispositivo no disponible, documentarla como pendiente y continuar únicamente trabajo independiente.

## Pasos de ejecución

### Cómo leer los subpasos y repartir las sesiones

- **Astra — ejecución:** investigar, programar, modelar, animar, configurar el proyecto, ejecutar comandos, compilar, instalar por ADB cuando esté autorizado el dispositivo, capturar evidencias accesibles y documentar resultados.
- **Astra — verificación:** hacer pruebas automatizables y revisión técnica/visual. No trasladar al usuario la depuración de errores, la lectura de logs ni la ejecución de comandos que Astra pueda realizar.
- **Tú — necesario:** decisiones creativas sin resolver, acceso privado o interacción física que Astra no puede hacer: conectar/desbloquear el teléfono, aceptar autorización USB, sostenerlo, moverlo e imprimir el marcador. Cuando se requiera intervención, Astra entrega primero la APK, imagen o lista concreta de acciones que se va a probar.
- **Tú — revisión opcional:** observar una imagen o clip y dar preferencias. Astra puede continuar conforme a las referencias acordadas si no hay una decisión indispensable pendiente. No se exige aprobación de cada cambio técnico.
- **Tú — sin intervención:** el paso se desarrolla autónomamente y termina con una entrega verificable.

Los subpasos **no son conversaciones nuevas por defecto**. Se ejecutan juntos dentro de la sesión del paso; las acciones manuales pueden ocupar solo unos minutos en medio de ella. Se mantienen 24 sesiones base como organización, con correcciones y evaluación de la ruta Moto G20 por estimar. El reparto expresa responsabilidad, no una medición exacta del 90 % del tiempo.

### Momentos en los que necesitarás participar

| Momento | Lo que prepara Astra antes | Tu intervención |
| --- | --- | --- |
| Arranque, paso 1 | Referencias recibidas, evaluación técnica y opciones de guion/audio. | Resolver únicamente guion/audio pendiente; G20 de pruebas y posible S23 de exposición ya confirmados. |
| Primer acceso, pasos 2–3 | Proyecto, herramientas de diagnóstico, APK mínima y marcador provisional. | Iniciar sesión en Unity solo si hace falta; conectar y desbloquear el Moto G20, habilitar depuración USB y aceptar este equipo; apuntar al marcador. |
| Diseño, pasos 5 y 8–9 | Clips y vistas del modelo con propuestas concretas. | Cerrar trayectoria/ocultamiento y dar ajustes de apariencia si los quieres. |
| Aspecto móvil, paso 12 | Build con las luces y materiales del corto. | Observar brillo, escala y legibilidad en la pantalla; conectar el teléfono cuando se solicite. |
| Integración final, pasos 20–23 | APK, marcador final y recorrido breve de pruebas. | Imprimir/montar/medir, mover el teléfono, tapar/destapar la imagen y probar fondo/reanudación y luz real. |
| Entrega, paso 24 | APK final e instrucciones. | Facilitar la última instalación y hacer una reproducción con el marcador físico. |

No necesitas programar, crear rigs, reparar exportaciones, configurar materiales ni aprender a interpretar el Profiler para completar tus intervenciones. Si una operación en el equipo queda bloqueada por acceso o permisos, Astra explica exactamente qué acción puntual falta y por qué.

### 1. Cerrar la ficha de producción y organizar referencias

**Trabajo:** crear `docs/estado.md`, copiar las cinco referencias y registrar diseño, ventana cinematográfica ya confirmada, Linux disponible, teléfono objetivo y decisiones narrativas. Mantener la prioridad del chupacabras original y la oveja reutilizada.

**Subpasos y responsables:**

- **1.1 · Astra — ejecución:** Revisar las cinco referencias y las demos ya disponibles; preparar una ficha con lo confirmado y propuestas para trayectoria, ocultamiento y audio.
- **1.2 · Astra — verificación:** Revisar evaluacion_ar_moto_g20.md y registrar requisitos de la prueba AprilTag/Linux/Unity. El G20 es el dispositivo de desarrollo; el posible S23 se probará solo cuando esté disponible.
- **1.3 · Tú — necesario:** Responder solo las decisiones pendientes de guion/audio en un bloque. No volver a confirmar dispositivo, referencias ni ventana cinematográfica.
- **1.4 · Astra — cierre:** Registrar los acuerdos en docs/estado.md, el candidato AprilTag y sus verificaciones pendientes. Aprobar la ruta para producción solo después de la prueba real de los pasos 2–3.

**Entrega:** ficha de producción y estado inicial.

**Aceptación:** referencias localizables y decisiones pendientes separadas de las confirmadas. El requisito Linux significa desarrollo y compilación Android; si se solicita además AR real en Linux, debe replantearse la arquitectura.

**Depende de:** ningún paso.

### 2. Preparar Unity 6000.3.22f1 y el proyecto Android en Linux

**Trabajo:** comprobar Editor y módulo Android Build Support con SDK, NDK y JDK correspondientes. Crear proyecto URP e integrar el candidato AprilTag para prueba; revisar dependencias, captura de cámara y carga de plugins nativos Linux/Android. Resolver la validación de proyecto para Android y fijar versiones estables compatibles. Mantener ajustes dentro del proyecto.

**Subpasos y responsables:**

- **2.1 · Astra — ejecución:** Verificar la instalación existente de Unity 6000.3.22f1 y preparar el proyecto con ese Editor, sus módulos Android y las dependencias de la ruta resuelta en el paso 1. No instalar ni seleccionar otro Editor.
- **2.2 · Tú — solo si hace falta:** Completar personalmente el inicio de sesión o activación de Unity y cualquier aprobación del sistema que requiera tu identidad. No compartir contraseñas con Astra.
- **2.3 · Astra — ejecución:** Crear escenas/configuración y scripts de compilación pertinentes; resolver errores dentro del proyecto.
- **2.4 · Astra — verificación:** Compilar la app mínima, revisar logs y fijar versiones. Si la ruta técnica sigue pendiente, limitar este paso a Unity/Android y URP, sin dar por validado un proveedor AR.

**Entrega:** proyecto mínimo y registro de versiones y configuración.

**Aceptación:** abre y compila desde Linux sin errores. El build Android contiene el detector candidato y no requiere servicios ARCore. Comprobar las ABIs reales del G20 antes de fijar arquitectura, y validar binarios nativos y requisitos Android de la combinación instalada.

**Depende de:** paso 1.

### 3. Probar seguimiento del marcador en el Moto G20

**Trabajo:** integrar captura de cámara trasera, detección AprilTag y estimación de pose/proyección. Preparar un marcador provisional y mostrar un cubo de tamaño conocido. Compilar desde Linux, instalar en el G20 y comprobar pose estable. Adaptar/corregir los parámetros de cámara: detectar solo el ID no basta.

**Subpasos y responsables:**

- **3.1 · Astra — ejecución:** Preparar una APK mínima de detección, imagen provisional imprimible, dimensiones y un recorrido de prueba breve para el dispositivo/proveedor resuelto.
- **3.2 · Tú — necesario:** Conectar el teléfono con un cable de datos, desbloquearlo, habilitar opciones de desarrollador/depuración USB y aceptar la autorización del equipo en pantalla. Astra dará instrucciones concretas cuando llegue el momento.
- **3.3 · Astra — ejecución:** Identificar G20, Android y ABIs con ADB; instalar/abrir APK y recoger logs. Verificar carga del detector, cámara trasera, orientación, reflejo y proyección. Preparar ajuste/calibración si la escala o pose lo requiere.
- **3.4 · Tú — necesario:** Imprimir y medir el marcador/patrón preparado, conceder cámara y apuntar con el G20: acercar/alejar, inclinar y ocultar/mostrar. Si hace falta calibración, realizar las capturas físicas guiadas por Astra.
- **3.5 · Astra — verificación:** Analizar detección, escala y recuperación con logs y capturas accesibles; corregir y pedir solo la repetición concreta que haga falta. No marcar el paso completado sin evidencia del teléfono.

**Entrega:** APK mínima, imagen provisional con medidas y evidencia de detección.

**Aceptación:** compilación Linux, carga nativa, cámara y pose del cubo funcionan en el G20. Escala/orientación estables y pérdida/recuperación comprobadas; rendimiento con margen para una ventana renderizada. Esta prueba decide si adoptar el candidato antes del modelado detallado.

**Cierre aceptado — 23 de septiembre de 2026:** el usuario da por hecha la distancia/escala aproximada observada en el G20 y acepta el rendimiento de esta etapa; la medición adicional de rendimiento se aplaza. **Paso 3 completado con este alcance, M#[2] resuelta.** Conservar lecturas reales y limitaciones; no declarar calibración exacta ni prueba física de APK 0.0.5. Paso 4 listo, **sin ejecutarlo hasta nueva indicación**. Esta aceptación expresa sustituye los bloqueos cuantitativos anteriores para iniciar 4.

**Depende de:** paso 2 y acceso físico al Moto G20. Una prueba con imagen estática o en otro teléfono no cierra este paso. No esperar al S23.

### 4. Probar el intercambio de animación Blender–Unity

**Trabajo:** exportar una malla pequeña con esqueleto, desplazamiento, una restricción horneada y una deformación de prueba. Importar en Unity y verificar metros, ejes, orientación, normales, duración y deformación. Probar cámara interna y RenderTexture sobre una superficie virtual, con las capas separadas del fondo AR.

**Subpasos y responsables:**

- **4.1 · Astra — ejecución:** Crear la muestra pequeña de huesos, restricción y deformación; exportar FBX e importar en Unity.
- **4.2 · Astra — verificación:** Comparar dimensiones, ejes, curvas, contacto y duración; comprobar cámara interna y RenderTexture.
- **4.3 · Astra — cierre:** Resolver diferencias y guardar los ajustes reproducibles de exportación.
- **4.4 · Tú — sin intervención:** No necesitas hacer exportaciones ni tocar importadores. Este paso puede avanzar mientras coordinamos el teléfono.

**Entrega:** muestra Blender, FBX, escena Unity de prueba y ajustes de exportación documentados.

**Aceptación:** movimiento y contacto sobreviven al intercambio; queda fijado el método de compresión de lana. Una prueba de duración confirma cómo conservar el límite de 40 s sin alargar el loop.

**Cierre técnico — 24 de septiembre de 2026:** muestra, FBX, escena Unity, metros/ejes, normales, contacto, blend shape, límite de 40 s y cámara/RenderTexture comprobados. Compresión de lana mediante blend shape; véase [contrato verificado](intercambio_blender_unity.md).

**Depende de:** paso 2. Puede avanzarse mientras se coordina la prueba física del paso 3.

### 5. Bloquear los 40 s y los encuadres de la ventana

**Trabajo:** construir la secuencia con formas simples para la ventana cinematográfica confirmada. Resolver recorrido, salto, ocultamiento y salida. Probar el conjunto importado en Unity, los encuadres internos, la relación de aspecto de la ventana y su tamaño relativo al marcador.

**Subpasos y responsables:**

- **5.1 · Astra — ejecución:** Preparar el bloqueo de los 40 s y una previsualización con trayectoria, salto, ocultamiento y salida claramente visibles.
- **5.2 · Tú — necesario si sigue pendiente:** Elegir entre las rutas de arrastre propuestas y confirmar la interpretación del ocultamiento. No volver a elegir ventana frente a maqueta.
- **5.3 · Astra — ejecución:** Aplicar la decisión al bloqueo y ajustar encuadres internos, superficie de la ventana y escala.
- **5.4 · Astra — verificación:** Comprobar la cronología y que cambiar la vista exterior no revele lo que la cámara interna oculta; dejar una evidencia corta para revisión opcional.

**Entrega:** `scenes/05_blocking.blend`, bloqueo Unity y previsualización de 40 s.

**Aceptación:** historia y tiempos se entienden; las cámaras internas reproducen los planos del guion. Mover el teléfono cambia la vista de la ventana, pero no descubre a la oveja tapada dentro del corto. La superficie no muestra imágenes invertidas ni estiradas.

**Cierre del bloqueo — 24 de septiembre de 2026:** revisión R04 con formas provisionales, cámara interna, caída y arrastre; máscara por fotograma verifica ocultamientos, salida y separación de vistas exteriores. Previsualización de 40 s y [detalle de entrega](bloqueo_40s.md). No se declara acabado de recursos, actuación final ni nueva validación física.

**Depende de:** pasos 3 y 4. No detallar geometría antes de cerrar esta revisión.

### 6. Construir el escenario para uso móvil

**Trabajo:** modelar granero envejecido, tierra seca, hierba y escondites. Crear luna y decorado nocturno para el corto dentro de la ventana. Mantener libres recorridos y zonas de salida.

**Subpasos y responsables:**

- **6.1 · Astra — ejecución:** Modelar el escenario final de costo contenido, aprovechando elementos útiles de la demo.
- **6.2 · Astra — ejecución:** Preparar materiales básicos, exportar la geometría estática y organizarla en Unity.
- **6.3 · Astra — verificación:** Revisar encuadres, recorridos, escala y costo preliminar; corregir intersecciones.
- **6.4 · Tú — revisión opcional:** Ver una imagen general y señalar si deseas cambiar distribución o apariencia. No se requiere que modeles objetos.

**Entrega:** `scenes/06_escenario.blend` y primera importación de geometría estática en Unity.

**Aceptación:** el escenario encaja en los encuadres, resulta legible en la ventana vista desde el móvil y usa geometría/materiales contenidos. La retirada deja el campo vacío dentro del corto.

**Cierre técnico — 24 de septiembre de 2026:** escenario de 2915 triángulos/10 materiales; distribución corregida sin cambiar R04, importación Unity y máscaras de ocultación/salida verificadas. [Detalle](escenario_movil.md). Legibilidad inspeccionada en capturas de ventana; brillo/rendimiento físicos pendientes de sus etapas.

**Depende de:** paso 5.

### 7. Seleccionar e integrar una oveja existente

**Trabajo:** buscar una selección breve de recursos low-mid poly cercanos a la referencia. Revisar licencia, geometría y rig; descargar e importar el elegido. Ajustar escala, orientación y colores. Preferir un rig aprovechable.

**Subpasos y responsables:**

- **7.1 · Astra — ejecución:** Buscar pocos candidatos adecuados y revisar licencia, formato, geometría y rig.
- **7.2 · Astra — ejecución:** Elegir una opción gratuita compatible con lo acordado, descargarla, adaptarla e importarla en Unity.
- **7.3 · Astra — verificación:** Comprobar poses posibles, dependencias y atribución; guardar fuente y licencia.
- **7.4 · Tú — solo si hace falta:** Intervenir si un recurso imprescindible requiere acceso privado o compra. Astra intentará primero una alternativa pública adecuada; no se presupone autorización para pagar.

**Entrega:** `scenes/07_oveja.blend`, recurso original, licencia y `docs/asset_oveja.md` con procedencia y atribución.

**Aceptación:** compatible con Blender y Unity, adaptable a las poses y autorizado para distribuir dentro de la app. No reconstruir la oveja desde cero; descartar candidatos que exijan demasiado retrabajo.

**Cierre técnico — 24 de septiembre de 2026:** Sheep de Quaternius, CC0, fuente/licencia conservadas, 612 triángulos, 24 huesos y cuatro poses comparadas en Unity. [Procedencia y adaptación](asset_oveja.md). No completa el rig final del paso 10.

**Depende de:** paso 6.

### 8. Modelar anatomía y silueta del chupacabras

**Trabajo:** crear el modelo original con cuerpo fibroso, cabeza, mandíbula, extremidades, cola y volúmenes principales de cresta. Evaluar con materiales neutros, junto a la oveja importada.

**Subpasos y responsables:**

- **8.1 · Astra — ejecución:** Crear anatomía y silueta original del chupacabras, con especial atención a espalda, hocico y extremidades.
- **8.2 · Astra — verificación:** Comparar proporciones con las tres referencias, probar encuadres y comprobar que el volumen permite el agarre y ocultamiento.
- **8.3 · Tú — revisión de diseño:** Mirar vistas de frente, perfil y espalda y comunicar los cambios que te importen. Este es el momento recomendado para corregir identidad antes del detalle; una preferencia opcional no bloquea por sí sola.
- **8.4 · Astra — cierre:** Aplicar los ajustes recibidos y guardar el hito de forma; si surge una decisión de diseño incompatible con el guion, plantear esa elección concreta.

**Entrega:** `scenes/08_chupacabras_forma.blend`, vistas frontal, lateral, posterior y tres cuartos comparadas con las referencias.

**Aceptación:** identidad clara, anatomía coherente y proporciones aptas para salto, agarre y arrastre. Revisar desde las cámaras internas y validar el ocultamiento de la oveja.

**Cierre técnico — 24 de septiembre de 2026:** forma R03 original de 8.486 triángulos,
cuatro vistas, comparación con oveja y contexto Unity. Se corrigen orientación
de ocultamiento y cámara interna en entregas nuevas; 150/114 cuadros ocultos y
30 finales vacíos. La muestra es de volumen, sin rig ni apoyo de arrastre final.
Véase [modelo y límites de aceptación](chupacabras_modelo.md).

**Depende de:** paso 7.

### 9. Terminar espinas, rostro y pelaje estilizado

**Trabajo:** refinar espinas, garras, dientes visibles y mechones; preparar UV y asignaciones de material exportables. Dar atención al rostro y a la espalda, protagonistas de la secuencia.

**Subpasos y responsables:**

- **9.1 · Astra — ejecución:** Añadir espinas, garras, dientes y mechones geométricos; preparar UV y materiales exportables.
- **9.2 · Astra — verificación:** Comprobar silueta y legibilidad del rostro/lomo en Blender y Unity.
- **9.3 · Tú — revisión opcional:** Revisar imágenes cercanas del protagonista y señalar ajustes de ferocidad, espinas o proporciones.
- **9.4 · Astra — cierre:** Consolidar el aspecto antes de cerrar los rigs; conservar la versión previa.

**Entrega:** `scenes/09_chupacabras_acabado.blend` y previsualización del modelo importado en Unity.

**Aceptación:** mantiene los rasgos de las tres referencias y concentra el detalle donde es visible. Sin pelo simulado ni dependencia de materiales exclusivos de Blender.

**Cierre técnico — 24 de septiembre de 2026:** acabado original de 10.550 triángulos,
17 mallas y seis materiales; cejas, ojos amarillos, dientes, garras, espinas y
mechones geométricos. UV y reapertura Blender/Unity verificados, rostro y lomo
inspeccionados. [Entregas y evidencia](chupacabras_modelo.md). La luz definitiva,
los rigs y las mediciones físicas conservan sus dependencias posteriores.

**Depende de:** paso 8.

### 10. Adaptar rig y deformaciones de la oveja

**Trabajo:** aprovechar el rig existente o crear uno sencillo si falta. Preparar cabeza, cuello, patas y compresión de lana con el método validado en el paso 4.

**Subpasos y responsables:**

- **10.1 · Astra — ejecución:** Inspeccionar y adaptar el rig de la oveja; añadir únicamente los controles o pesos faltantes.
- **10.2 · Astra — ejecución:** Preparar compresión de cuello/lana y poses extremas de pastoreo y forcejeo.
- **10.3 · Astra — verificación:** Exportar una prueba y corregir deformaciones o pérdidas de datos en Unity.
- **10.4 · Tú — sin intervención:** No necesitas crear huesos, pintar pesos ni reparar el modelo.

**Entrega:** `scenes/10_rig_oveja.blend` y prueba de poses exportada a Unity.

**Aceptación:** pastoreo y forcejeo no rompen la malla; cuello y lana admiten la mordida. La deformación también funciona en Unity.

**Cierre técnico — 24 de septiembre de 2026:** rig reutilizado, compresión de
66 vértices de lana y 241 cuadros de poses exportados; error máximo Unity
0,04261 mm. [Fuentes y evidencia](rigs_contacto.md). No sustituye actuación final.

**Depende de:** paso 9.

### 11. Crear el rig del chupacabras y resolver el agarre

**Trabajo:** preparar locomoción, columna, cola, cabeza y mandíbula. Definir contacto con la oveja y hornear una muestra de agarre y desplazamiento de ambos.

**Subpasos y responsables:**

- **11.1 · Astra — ejecución:** Crear controles de locomoción, columna, cola y mandíbula del chupacabras.
- **11.2 · Astra — ejecución:** Preparar el contacto con el cuello y una muestra horneada de desplazamiento conjunto.
- **11.3 · Astra — verificación:** Comprobar el agarre en Blender y Unity, corregir saltos y evitar que la animación mueva la raíz AR.
- **11.4 · Tú — sin intervención:** La preparación y depuración de rigs queda a cargo de Astra.

**Entrega:** `scenes/11_rigs_contacto.blend` y muestra conjunta reproducible en Unity.

**Aceptación:** mandíbula y cuello mantienen contacto sin saltos; no hay dependencias circulares. La raíz AR permanece independiente de las trayectorias animadas.

**Cierre técnico — 24 de septiembre de 2026:** rig original de 23 huesos y
muestras de controles/contacto de seis segundos. R03 conserva triangulación;
181 cuadros comparados, error de superficie en Unity 0,001408 mm, raíz exterior
independiente. [Detalle](rigs_contacto.md). Pisadas y actuación definitivas son 13–15.

**Depende de:** paso 10.

### 12. Resolver materiales e iluminación definitiva en Unity

**Trabajo:** reconstruir el aspecto nocturno en URP, ojos amarillos, contornos y sombras; implementar una trama sencilla si aporta al estilo y al rendimiento. Crear una previsualización de la nueva composición con el chupacabras estático en 3D sobre o junto al marcador y el panel cinematográfico a su lado. Ajustar tamaño y separación: figura de pie centrada sobre el símbolo y panel frontal a su lado, según la aclaración del usuario del 30 de septiembre. El panel no cubre el dibujo; la figura puede superponerse virtualmente. Revisar en el teléfono.

**Subpasos y responsables:**

- **12.1 · Astra — ejecución:** Reconstruir la iluminación y materiales en URP, preparar la ventana y una build visual de prueba.
- **12.2 · Tú — necesario, M#[4]:** cuando estén preparados la build, el marcador y las instrucciones, comprobar en el G20 la maqueta desde varios ángulos, su tamaño junto al panel y su posición directamente sobre el tag; comprobar que el panel quede al lado. Revisar también la lectura de ojos, espinas, oveja y sombras.
- **12.3 · Astra — verificación:** Recoger capturas/logs disponibles, contrastar con las referencias y corregir brillo, sombras o materiales.
- **12.4 · Tú — revisión opcional:** Dar preferencia estética entre ajustes concretos. No necesitas configurar luces ni shaders.

**Entrega:** materiales, iluminación y prefab visual del escenario, la figura AR estática y la ventana de Unity; capturas de los tres momentos y de la composición completa.

**Aceptación:** aspecto fiel a la dirección visual y lectura suficiente en pantalla móvil. Se ven simultáneamente la figura 3D en perspectiva y la secuencia en el panel lateral. Cambiar el punto de vista altera la perspectiva exterior, sin mover la cámara del corto. La figura puede cubrir virtualmente parte del símbolo por la colocación confirmada; el panel deja libre el dibujo y la cámara física debe seguir viendo el patrón completo. El cielo o iluminación ficticios no alteran accidentalmente el fondo AR real. Unity es la referencia visual de producción.

**Depende de:** paso 11.

### 13. Animar calma y acecho: 0–20 s

**Trabajo:** refinar pastoreo con variaciones, acecho lento y retirada completa a los 15 s. Preparar la cámara interna para el ataque con anticipación gradual, sin fijarla bruscamente al terminar el acecho.

**Subpasos y responsables:**

- **13.1 · Astra — ejecución:** Animar el pastoreo y acecho, con retirada completa del chupacabras y sus ojos a los 15 s del corto definitivo.
- **13.2 · Astra — ejecución:** Preparar el movimiento anticipado y continuo de la cámara interna que conduce al ataque, y exportar el tramo.
- **13.3 · Astra — verificación:** Comprobar continuidad, ausencia de ojos desde los 15 s y lectura del movimiento; producir un clip corto.
- **13.4 · Tú — revisión opcional:** Indicar si el ritmo parece demasiado lento o mecánico después de ver el clip.

**Entrega:** `scenes/13_calma.blend` y preview importado en Unity.

**Aceptación:** la oveja pasta todo el intervalo; cuerpo y ojos de la criatura quedan ocultos desde los 15 s. No aparecen saltos al evaluar el tramo exportado.

**Depende de:** paso 12.

### 14. Animar salto y ataque: 20–25 s

**Trabajo:** irrupción exacta a los 20 s, salto, aterrizaje y forcejeo con peso. Hacer que la criatura entre desde un lateral o detrás del granero, con una aproximación y aceleración legibles hacia la oveja; suavizar el movimiento de cámara interna antes, durante y después del salto. Reservar efectos para el paso 18.

**Subpasos y responsables:**

- **14.1 · Astra — ejecución:** Animar el salto a los 20 s, el aterrizaje y el forcejeo hasta los 25 s.
- **14.2 · Astra — verificación:** Comprobar la ocultación sin polvo fotograma a fotograma; corregir cámara/poses y revisar que la cámara no salta en el segundo 20 ni la criatura nace del eje del lente.
- **14.3 · Astra — cierre:** Exportar a Unity y comparar el resultado, conservando la cámara AR independiente.
- **14.4 · Tú — revisión opcional:** Valorar fuerza y claridad del ataque en una previsualización; no ajustar keyframes manualmente.

**Entrega:** `scenes/14_ataque.blend` y preview Unity del tramo.

**Aceptación:** el cuerpo tapa completamente a la oveja desde el aterrizaje hasta los 25 s aun sin polvo. La cámara y la criatura se aproximan con continuidad; el salto empieza a los 20 s y cruza cerca/por encima de la cámara interna después de entrar desde fuera del eje del lente. No animar la cámara AR.

**Depende de:** paso 13.

### 15. Animar agarre, arrastre y retirada: 25–40 s

**Trabajo:** sostener mordida, forcejeo, pasos y peso de ambos animales. Ejecutar la trayectoria acordada y completar la retirada para dejar el escenario vacío.

**Subpasos y responsables:**

- **15.1 · Astra — ejecución:** Animar mandíbula, fuerza de arrastre, apoyo de patas y oposición de la oveja.
- **15.2 · Astra — ejecución:** Ejecutar el recorrido acordado, la apertura de cámara y la salida antes del tramo vacío.
- **15.3 · Astra — verificación:** Comprobar contacto, penetraciones, deslizamientos y duración en Blender/Unity.
- **15.4 · Tú — revisión opcional:** Ver el tramo y comentar si transmite el peso y ritmo deseados.

**Entrega:** `scenes/15_arrastre.blend` y preview Unity del tramo.

**Aceptación:** contacto estable y patas sin deslizamientos accidentales. Salida fuera del encuadre y último tramo vacío. La apertura del plano se aplica solo a la cámara interna de la ventana.

**Depende de:** paso 14.

### 16. Consolidar y exportar la secuencia completa

**Trabajo:** limpiar recursos de exportación, hornear curvas finales, exportar FBX y configurar clips Generic y deformaciones. Comprobar transiciones de 15, 20 y 25 s y final de 40 s contra Blender.

**Subpasos y responsables:**

- **16.1 · Astra — ejecución:** Consolidar fuentes, hornear animaciones y exportar mallas, huesos y curvas definitivas.
- **16.2 · Astra — verificación:** Comparar transiciones y duración; revisar materiales, escala y root motion en Unity.
- **16.3 · Astra — cierre:** Corregir diferencias, guardar ajustes y empaquetar los recursos importados.
- **16.4 · Tú — sin intervención:** No necesitas exportar archivos ni resolver errores de importación.

**Entrega:** fuente Blender final, FBX y recursos importados con ajustes documentados.

**Aceptación:** ambos personajes conservan sincronización y recorrido; no hay pérdida de duración, transformaciones duplicadas ni materiales ausentes. Las restricciones de autoría no se requieren en ejecución.

**Depende de:** paso 15.

### 17. Montar Timeline y reinicio completo de 40 s

**Trabajo:** reunir animaciones y cámara interna en una Timeline dirigida por un único reloj. Implementar reinicio explícito de poses, posiciones, visibilidad y estados. Preparar puntos de integración de efectos y audio.

**Subpasos y responsables:**

- **17.1 · Astra — ejecución:** Montar Timeline y un controlador de reproducción/reset de 40 s.
- **17.2 · Astra — verificación:** Ejecutar pruebas de duración, sincronización y restauración de estados, incluidos varios ciclos y fps variables.
- **17.3 · Astra — cierre:** Corregir deriva, flashes o restos del ciclo anterior y guardar el prefab reproducible.
- **17.4 · Tú — revisión opcional:** Observar dos vueltas completas si quieres revisar el salto deliberado entre final e inicio.

**Entrega:** prefab de secuencia reproducible en Unity sin necesidad de detección AR y prueba de varios loops.

**Aceptación:** cada vuelta dura 40 s de tiempo de reproducción; el reset es instantáneo e intencional. No hay deriva entre personajes ni fotograma negro. Añadir pruebas pertinentes de duración y reset; comprobar también con fps variables.

**Depende de:** paso 16.

### 18. Integrar polvo y movimientos secundarios en Unity

**Trabajo:** crear partículas de impacto y arrastre de costo acotado. Integrarlas al reloj común y añadir asentamiento corporal o sacudida de cámara interna según corresponda.

**Subpasos y responsables:**

- **18.1 · Astra — ejecución:** Crear polvo de impacto/arrastre y movimientos secundarios de costo limitado.
- **18.2 · Astra — verificación:** Probar sincronización y limpieza al reiniciar; medir partículas en una build Android disponible.
- **18.3 · Tú — solo para medición física:** Conectar el dispositivo y mantener el marcador visible si esa medición necesita AR. Astra ejecuta el registro y analiza los resultados.
- **18.4 · Astra — cierre:** Ajustar efectos para conservar la actuación visible y el presupuesto móvil.

**Entrega:** efectos Unity y preview de dos vueltas.

**Aceptación:** no ocultan la actuación del arrastre ni dejan residuos al reiniciar. La sacudida no mueve el seguimiento del teléfono. El pico de partículas se mide en Android.

**Depende de:** paso 17.

### 19. Integrar audio, si se incluye

**Trabajo:** preparar recursos permitidos, registrar procedencia y sincronizar ambiente y acciones. Ajustar la mezcla del corto y decidir su atenuación con la distancia a la ventana.

**Subpasos y responsables:**

- **19.1 · Astra — ejecución:** Si se acordó audio, seleccionar/preparar recursos permitidos y sincronizarlos con Timeline; si no, registrar «no aplica».
- **19.2 · Astra — verificación:** Revisar mezcla, saturación, pausa, recuperación y reinicio; preparar un clip con sonido.
- **19.3 · Tú — revisión manual si hay audio:** Escuchar en el teléfono o auriculares y comentar volumen, carácter y sonidos molestos. La medición técnica no sustituye tu preferencia auditiva.
- **19.4 · Astra — cierre:** Aplicar ajustes y registrar procedencia y atribuciones.

**Entrega:** audio integrado a Timeline y registro de recursos, o estado «no aplica» si se acordó una pieza muda.

**Aceptación:** sin saturación, clics de reset ni sonidos duplicados al recuperar el seguimiento; pausa y reinicio sincronizados con la animación.

**Depende de:** paso 18 y decisión de audio.

### 20. Conectar la experiencia con el seguimiento AR

**Trabajo:** reemplazar los elementos de prueba por la composición híbrida: una figura estática 3D y una ventana cinematográfica lateral, ambas ancladas a una sola pose AprilTag. Crear una instancia de cada elemento, mostrar estado de búsqueda y comenzar el corto en 0 s al adquirir seguimiento válido. Gestionar pérdida/recuperación, pausa de aplicación y botón de reinicio.

**Subpasos y responsables:**

- **20.1 · Astra — ejecución:** Conectar la ventana al seguimiento y programar búsqueda, instancia única, reproducción, pausa/recuperación y reinicio.
- **20.2 · Astra — verificación:** Probar las transiciones automatizables y preparar una APK con un recorrido de prueba física.
- **20.3 · Tú — necesario, M#[5]:** comprobar en el G20 que figura y ventana aparecen juntas, mover el teléfono para revisar su perspectiva y la ventana, apartar/tapar el tag y recuperarlo, pulsar reinicio y enviar la app a segundo plano según instrucciones preparadas.
- **20.4 · Astra — cierre:** Capturar y analizar estados/logs, corregir duplicación o desincronización y repetir solo los casos afectados.

**Entrega:** experiencia integrada y pruebas de sus transiciones.

**Aceptación:** figura y ventana comparten la pose anclada, sin duplicación por detecciones repetidas. La figura conserva su postura estática; la ventana reproduce la secuencia. Ocultar ambos y pausar al perder pose válida; al recuperarlo, continuar en su posición respecto al tag. Probar perspectiva, visibilidad de tag/márgenes, estados buscando/visible/perdido, detecciones intermitentes, segundo plano y sincronización. No dejar los elementos flotando con la última pose cuando el marcador sale de vista.

**Depende de:** pasos 3, 17, 18 y 19.

### 21. Preparar y validar el marcador final del stand

**Trabajo:** preparar el marcador de la familia validada, registrar ID, tamaño medido, márgenes y orientación. Integrarlo en el diseño del stand sin alterar su patrón. Preparar PNG y PDF imprimible a escala. Añadir QR lateral solo si se necesita un enlace.

**Subpasos y responsables:**

- **21.1 · Astra — ejecución:** Preparar diseño final y tag validado, PNG/PDF a escala y configuración de familia/ID/tamaño; indicar márgenes y orientación.
- **21.2 · Tú — necesario:** Imprimir sin ajuste automático de escala, medir el ancho real con una regla, montar la imagen plana en el stand y comunicar las medidas. Astra proporciona las indicaciones de impresión.
- **21.3 · Astra — ejecución:** Actualizar dimensiones físicas del tag y su configuración y generar la build final del marcador.
- **21.4 · Tú — necesario:** Apuntar desde las distancias y ángulos indicados y probar luz/oclusión parcial.
- **21.5 · Astra — verificación:** Analizar estabilidad, escala y detección; corregir imagen o parámetros y registrar qué versión física se validó.

**Entrega:** archivos en `marker/`, medidas e instrucciones de uso.

**Aceptación:** detección y escala correctas con la impresión real; probar distancia, ángulo, luz y oclusión parcial. La escena se orienta correctamente si el cartel es vertical o está sobre una mesa. Cambiar patrón, ID o tamaño exige actualizar y verificar su configuración. No recortar márgenes ni deformar el tag.

**Depende de:** paso 20.

### 22. Medir y optimizar en Android

**Trabajo:** medir CPU, GPU, memoria, número de dibujos, partículas y temperatura durante varios ciclos. Ajustar sombras, materiales, texturas y geometría según los cuellos de botella; medir también resolución y costo de RenderTexture junto con la composición AR.

**Subpasos y responsables:**

- **22.1 · Astra — ejecución:** Preparar build de medición, conectar Profiler u obtener métricas disponibles y definir un recorrido reproducible.
- **22.2 · Tú — necesario:** Mantener el teléfono y marcador en condiciones representativas durante al menos cinco minutos, mover la cámara cuando se indique y comentar calentamiento perceptible.
- **22.3 · Astra — verificación:** Medir CPU/GPU cuando estén disponibles, memoria, fps, partículas y costo de RenderTexture; identificar el cuello de botella.
- **22.4 · Astra — cierre:** Optimizar y comparar antes/después. No pedirte interpretar el Profiler; si alguna métrica no está disponible, documentar la limitación y usar las medidas accesibles.

**Entrega:** perfil antes/después y configuración de calidad para el teléfono objetivo.

**Aceptación:** objetivo inicial de 30 fps sostenidos durante al menos cinco minutos, incluyendo seguimiento y ataque. Sin crecimiento continuo de memoria ni degradación que vuelva ilegible la acción. Reducir costo conservando prioridad visual del chupacabras.

**Depende de:** paso 21.

### 23. Verificar la experiencia completa

**Trabajo:** revisar guion y estilo; probar primera ejecución, cámara denegada/aceptada, error de carga del detector, marcador ausente/incorrecto, pérdida/recuperación, segundo plano y loops repetidos en el G20. Verificar ejecución sin red con los recursos empaquetados; no depender de Google Play Services for AR.

**Subpasos y responsables:**

- **23.1 · Astra — ejecución:** Preparar la lista final de pruebas y ejecutar tests/linters configurados y comprobaciones automatizables.
- **23.2 · Tú — necesario:** Seguir una lista breve: cámara denegada/aceptada, marcador fuera/dentro, app en segundo plano, reproducción sin red con la APK instalada y varios ciclos.
- **23.3 · Astra — verificación:** Relacionar evidencia física con logs, revisar guion y resolver errores. Si no hay un dispositivo incompatible disponible, declarar simulada la comprobación correspondiente.
- **23.4 · Astra — cierre:** Registrar resultado y cobertura real; pedir repetición únicamente de casos fallidos o afectados por una corrección.

**Entrega:** `docs/verificacion_android.md`, evidencia y problemas corregidos o pendientes.

**Aceptación:** ninguna prueba crítica pendiente en el Moto G20; cronología, reset, estabilidad y comportamiento AR comprobados. Ejecutar tests/linters configurados y confirmar independencia de servicios ARCore. S23 se declara pendiente por falta de acceso, sin bloquear la entrega verificada en G20.

**Depende de:** paso 22.

### 24. Empaquetar la entrega Android reproducible

**Trabajo:** compilar desde Linux la APK de entrega e instalar/probar en el G20. Reunir fuentes, proyecto, marcador, licencias e instrucciones. Preparar la misma APK para el posible S23, con selección de cámara trasera y comprobación/ajuste de proyección por dispositivo; no fijar los parámetros del G20 como universales. Adjuntar un procedimiento breve de instalación y prueba del S23 el día de exposición. AAB/publicación solo si se acuerda.

**Subpasos y responsables:**

- **24.1 · Astra — ejecución:** Crear APK final desde Linux y reunir proyecto, fuentes, marcador, licencias y guía reproducible.
- **24.2 · Tú — necesario:** Facilitar el G20 para la última instalación y reproducción con la impresión validada. Cuando esté disponible el S23, instalar esa misma APK, conceder cámara y seguir la comprobación de orientación/escala y un ciclo completo preparada por Astra.
- **24.3 · Astra — verificación:** Comprobar build e instalación finales y que la entrega contiene los recursos/versiones correctos; cerrar documentación.
- **24.4 · Tú — solo si se amplía a publicación:** Gestionar identidad, cuentas y decisiones de firma/distribución. Publicar en una tienda no forma parte de esta entrega.

**Entrega:** proyecto Unity editable, APK instalable, recursos fuente y `docs/entrega.md`. Captura MP4 opcional como demostración.

**Aceptación:** el proyecto reabre/compila; la APK reconoce el marcador y reproduce en bucle en el G20. Documentar «S23 pendiente de prueba física» hasta comprobarlo; no exigir acceso previo ni afirmar compatibilidad probada. Adjuntar guía de comprobación y mantener disponible la APK validada del G20 como respaldo. No incluir credenciales de firma; publicación fuera de alcance.

**Depende de:** paso 23.

## Revisiones que evitan rehacer trabajo

- **Paso 3:** demostrar compilación Linux y seguimiento AprilTag en el Moto G20 antes de adoptar el candidato e invertir en producción detallada.
- **Pasos 4–5:** cerrar intercambio de animación, RenderTexture y encuadres antes de construir el escenario final.
- **Pasos 8–9:** revisar diseño del chupacabras frente a las referencias antes de cerrar rig.
- **Paso 12:** validar el aspecto en Unity y móvil antes de pulir las actuaciones.
- **Paso 17:** comprobar sincronización y reset antes de conectar todo al seguimiento.
- **Pasos 22–24:** medir, validar y entregar la APK real; un preview del Editor no demuestra la experiencia final.

## Instrucción reutilizable para continuar

> Trabaja en `/home/cacawatin/code/blender/chupacabras`. Lee las instrucciones locales, `docs/plan_secuencia.md` y `docs/estado.md` si existe. Ejecuta el siguiente paso pendiente con sus subpasos y responsables; solicita solo la intervención manual que haga falta y prepara antes una entrega concreta para probar. Conserva los hitos, documenta qué cambió y por qué y verifica la aceptación. Usa exclusivamente Unity 6000.3.22f1 ya instalado en `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`; no instales, actualices ni selecciones otro Editor sin autorización explícita. Mantén desarrollo Linux, oveja reutilizada y chupacabras original. El Moto G20 es obligatorio para pruebas y el posible S23 no estará disponible hasta la exposición. Consulta evaluacion_ar_moto_g20.md: AprilTag es la ruta aceptada para continuar; no añadir ARCore ni exigir otro teléfono. Usar una sola implementación y declarar el S23 pendiente hasta probarlo. La presentación confirmada combina la figura estática 3D anclada al AprilTag con la ventana cinematográfica lateral en tiempo real; conservar cámaras internas. Si una prueba requiere un teléfono no disponible, regístrala pendiente y avanza solo en trabajo independiente. Actualiza el estado y el siguiente paso al terminar.

## Referencias técnicas

Las referencias ARCore/AR Foundation se conservan como antecedentes de la evaluación; no son dependencias de la nueva ruta. Las fuentes vigentes de seguimiento están también en [evaluacion_ar_moto_g20.md](evaluacion_ar_moto_g20.md).

Takahashi, K. (s. f.). *jp.keijiro.apriltag* [Repositorio de código]. GitHub. https://github.com/keijiro/jp.keijiro.apriltag

Documentación consultada el 21 de septiembre de 2026. Volver a comprobar requisitos y compatibilidad de dependencias al preparar el proyecto, conservando el Editor 6000.3.22f1 fijado por el usuario.

Google. (s. f.-a). *ARCore supported devices*. Google for Developers. https://developers.google.com/ar/devices

Google. (s. f.-b). *Add dimension to images*. Google for Developers. https://developers.google.com/ar/develop/augmented-images

Unity Technologies. (s. f.-a). *AR Foundation samples* [Repositorio de código]. GitHub. https://github.com/Unity-Technologies/arfoundation-samples

Unity Technologies. (s. f.-b). *System requirements for Unity 6.3*. Unity Documentation. https://docs.unity.com/en-us/engine/6000.3/manual/get-started/install-and-upgrade/getting-started-installing-unity/system-requirements

Unity Technologies. (s. f.-c). *Changelog: Google ARCore XR Plugin 6.3*. Unity Documentation. https://docs.unity3d.com/Packages/com.unity.xr.arcore@6.3/changelog/CHANGELOG.html

Unity Technologies. (s. f.-d). *XR Simulation: AR Foundation 6.3*. Unity Documentation. https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@6.3/manual/xr-simulation/simulation.html

Unity Technologies. (s. f.-e). *Changelog: AR Foundation 6.3*. Unity Documentation. https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@6.3/changelog/CHANGELOG.html

Unity Technologies. (s. f.-f). *Google ARCore XR Plug-in 6.3*. Unity Documentation. https://docs.unity3d.com/Packages/com.unity.xr.arcore@6.3/manual/index.html

## Registro de cambios y estado

- Plan inicial: secuencia renderizada en Blender en 16 pasos.
- Revisión de personajes: cinco referencias revisadas, oveja reutilizada y modelado original del chupacabras dividido en anatomía/acabado; 17 pasos.
- Revisión AR: entrega trasladada a Unity 6.3 LTS y APK Android, con desarrollo desde Linux mediante AR Foundation/ARCore. Se añaden pruebas tempranas, exportación, Timeline, seguimiento, optimización y validación móvil; 24 pasos.
- Presentación original: ventana cinematográfica anclada en AR, con escena 3D en tiempo real y cámaras internas. **Actualización del usuario, 24 de septiembre de 2026:** sumar una figura estática exterior anclada a la misma pose AprilTag y mantener el panel cinematográfico al lado; ver presentación y criterios de los pasos 12 y 20. La figura aún no está implementada en la aplicación. También solicita suavizar la transición de cámara en escenas 13–14 y que la criatura no entre desde el centro del lente; el bloqueo R04 queda histórico.
- Revisión de responsabilidades: añadidos subpasos de ejecución/verificación de Astra e intervenciones manuales necesarias u opcionales en las 24 etapas. El usuario declara un Moto G20; su ausencia en la lista oficial de ARCore obliga a resolver dispositivo o proveedor antes de validar AR.
- Ejecución de producción: no iniciada. Se crearon aparte una [demo estática](demo_lowpoly.md) y una [versión animada económica de 35 s](demo_animada.md), con ataque a los 15 s, a petición del usuario. No validan ni sustituyen los hitos de Unity/AR del plan; la duración del corto definitivo sigue siendo 40 s.
- Dispositivos confirmados: Moto G20 para todas las pruebas previas; Samsung S23 posible únicamente en la exposición. Evaluación documental completada; candidato inicial AprilTag, con prueba de viabilidad pendiente. Actualizados marcador, cámara, calibración, pruebas y entrega; se conservan 24 etapas y el reparto de responsabilidades.
- 23 de septiembre de 2026: el usuario fija **Unity 6000.3.22f1** para aprovechar su instalación existente y evitar instalar o seleccionar otro Editor. Se incorpora la restricción al alcance, al paso 2 y a la instrucción de continuidad. Se comprobó que el ejecutable existe; la compilación y AprilTag siguen pendientes de validación.
- 23 de septiembre de 2026, continuidad: referencias copiadas y demos reabiertas/verificadas; creados ficha y estado. Incorporadas las dos rutas y el límite de dos pasos por sesión. El paso 1 permanece abierto en **1.3 / M#[1]** (guion/audio); no se inició el paso 2, dependiente del primero. Detalle y evidencias en [estado.md](estado.md).
- Continuación: **M#[1] resuelta**, acuerdos incorporados a ficha y guion; paso 1 cerrado. Proyecto Unity 6000.3.22f1/URP/AprilTag creado en la segunda raíz, detector Linux probado y APK estática compilada. Aceptación completa de 2 pendiente de ABI real G20; 3 no iniciado. Próxima pareja: 2 retomado + 3; véase [estado.md](estado.md).

- Continuación del 23 de septiembre de 2026, pasos **2 retomado + 3**: preparada escena de cámara/pose, APK 03 y marcador A4 de ID 0; pruebas sintéticas y build correctas. **M#[2] pendiente**: USB G20, impresión medida y recorrido físico. No se cierra 2.4 ni 3.5, no se adopta AprilTag como validado y no se inicia 4. Véase [estado.md](estado.md).

- Primer acceso físico G20, 23 de septiembre de 2026: **paso 2 cerrado** (Android 11/API 30/ARM64, instalación y detector nativo). Paso 3 parcial: cámara real 640 × 480, impresión y seguimiento físico pendientes **M#[2]**. Corregidos stripping MeshCollider y panel horizontal en APK 0.0.3; desinstalada al terminar por petición del usuario. Próxima pareja **3 retomado + 4**; no se inició 4. Estado y evidencias en [estado.md](estado.md).

- Adaptación a hojas **carta** solicitada por el usuario: PDF y generador actualizados conservando el tag de 100 mm y la entrega A4 anterior. **M#[3] resuelta** (Brother DCP-T510W); una copia, trabajo 43 completado por CUPS. **M#[2] pendiente de medida física** y recorrido G20. No cambia APK ni completa el paso 3.

- Recorrido físico posterior del 23 de septiembre de 2026: impresión carta ya medida; detección real de cubo y ventana, giro y ocultación/recuperación confirmados por el usuario en G20. Revisión 0.0.4 logra ~30 fps en tramos con RT, pero escala cuantitativa y frecuencia/margen siguen pendientes; 0.0.5 preparada sin prueba física. Se respeta la limitación del usuario para medidas exactas a mano. App retirada y ausencia verificada. **Paso 3 parcial, 4 no iniciado**; próximos **3 retomado + 4**. Véase estado y evidencias, sin repetir impresión ni decisiones resueltas.

- Cierre explícito posterior del usuario: distancia/escala aproximada aceptada como hecha, rendimiento adicional para después. **Paso 3 completado y M#[2] resuelta; paso 4 listo, NO ejecutar aún.** Próxima pareja prevista al recibir nueva instrucción: **4 + 5**. Se conservan resultados físicos originales y límites de cada APK; no se realizaron nuevas pruebas ni cambios de implementación.

- Continuación del 24 de septiembre de 2026: **pasos 6–7 cerrados**, escenario y oveja reutilizada importados y comprobados. Se preservan demos, R04 y validaciones físicas previas. No se genera nueva APK ni se conecta el móvil. Próximos **8 + 9**, sin iniciar en esta sesión.

- Revisión visual del 24 de septiembre de 2026: figura AR estática del chupacabras junto a la ventana lateral, ambas ancladas al AprilTag, con escala/separación a revisar en paso 12 e integración/prueba en 20. La cámara de la animación final anticipa suavemente el salto de 20 s y la criatura entra desde el lateral/detrás del granero; escenas 13–14. M#[4] y M#[5] requieren build, marcador e instrucciones preparados antes de pedir intervención física. Se mantiene intacto R04 y no se inicia ningún paso principal nuevo.

- Continuación del 24 de septiembre de 2026: **10–11 cerrados**, rigs y contacto R03 comparados en Blender/Unity. Fuentes, demos y configuraciones ajenas preservadas; sin APK ni prueba física nueva. Próximos **12 + 13**, sin iniciar. Véase [estado](estado.md).

- 30 de septiembre de 2026: **12.1 preparado** en una escena nueva AR de aspecto, con APK 0.0.12, materiales URP, figura estática y tres muestras de luz en panel. Capturas y pruebas sintéticas verificadas; **12.2 / M#[4] pendiente de G20**. 13 no iniciado por dependencia. Fuentes Blender, demos y configuraciones ajenas conservadas. Véase [estado](estado.md).

- 30 de septiembre, prueba G20: usuario aclara figura **centrada directamente encima del símbolo**, de pie, y panel vertical frontal al lado. Esta colocación sustituye el requisito de que la figura no se superponga visualmente al dibujo; el detector conserva la imagen real sin composición. La muestra del paso 12 son vistas de iluminación de pastoreo/agarre, no la animación definitiva de 40 s.

- Cierre físico del 30 de septiembre: **12 completado, M#[4] resuelta**. Figura centrada directamente encima del tag y panel vertical frontal, R05/0.0.14 aceptada por el usuario en G20. Capturas/logs guardados y app desinstalada con limpieza verificada. No hubo nuevos avisos OpenGL en la última muestra; rendimiento sostenido y causa del aviso aislado anterior siguen sin validación final. Próximos **13–14**, no iniciados.

- 2 de octubre de 2026: revisión solicitada de **8–9**, únicas etapas trabajadas esta sesión. Nueva forma R01/acabado demacrado R02 y contextos R03; 30.880 triángulos, sin sustituir entregas previas. Importación y ocultamiento comprobados en Unity 6000.3.22f1, sin teléfono. **Próximos 11 (adaptar rig) y 12 (propagar aspecto)**; 13–14 esperan esas dependencias. M#[4] conserva su cierre histórico. [Cambios, evidencia y reproducción](chupacabras_demacrado.md).

- Continuación del 2 de octubre de 2026: **11 retomado cerrado técnicamente**, rig demacrado de 23 huesos y contacto/poses de seis segundos comparados en Blender y Unity; oveja R03 conservada. **12.1 preparado** en escena AR demacrada R02 y APK 0.0.15, build y pruebas sintéticas correctos. **12.2–12.3 pendientes M#[6]** para legibilidad/brillo real del nuevo modelo. M#[4] conserva su cierre histórico y M#[5] queda para 20. No se inició 13; próxima pareja **12 retomado + 13**, condicionada a cerrar M#[6]. [Evidencia y reproducción](rigs_demacrado.md).
