# Estado de continuidad

Actualizado: **2 de octubre de 2026 — cambio autorizado a figura AR realista**.
[Plan vigente F1–F7](plan_secuencia.md) · [Ficha](ficha_produccion.md) ·
[Estado cinematográfico archivado](estado_secuencia_40s_historico.md).

**Replanificación documental completada. F1–F7 pendientes; ninguna etapa nueva
implementada en esta sesión. Próxima sesión: F1 y F2, como máximo.**
El usuario sustituyó el corto de 40 s por una figura del chupacabras sobre el
marcador. No retomar el arrastre ni cerrar físicamente la antigua ventana.

## Punto de partida comprobado

Repositorios existentes en `main`: Blender `95b88d9`, Unity `d74fae0` al inicio.
Blender limpio. Unity tenía tres cambios ajenos preparados en el índice:
`ProjectSettings/GraphicsSettings.asset`, `ProjectSettings/QualitySettings.asset`
y `ProjectSettings/PackageManagerSettings.asset`. Se preservan y excluyen del
commit de documentación. No se encontraron AGENTS.md adicionales aplicables.

La cámara, AprilTag, proyección/anclaje y compilación Android existen. El
tracking aún llama a `AppearanceStudy`, que crea panel/RenderTexture/Playables;
su alternativa nula también crea una ventana de diagnóstico. La figura aislada
requiere desacoplar esa presentación en F1. No basta con ocultar un objeto.

Fuentes y resultados existentes comprobados:

- `scenes/09_chupacabras_demacrado_r02.blend`: base de aspecto demacrado;
  30.880 triángulos, 18 mallas y 6 materiales documentados en la entrega previa.
- `scenes/11_rigs_contacto_demacrado_r01.blend`: rig conservado para autoría.
- `scenes/13_calma_r07.blend`, `scenes/14_ataque_r07.blend`, FBX/JSON en
  `exports/` y MP4 en `previews/`: hitos técnicos anteriores, no la nueva entrega.
  La revisión del usuario indicó que la actuación no le convence.
- Unity: `Assets/Scenes/12_AppearanceAR_demacrado_r02.unity`, prefab
  `Assets/Appearance12DemacradoR02/AppearanceStudy.prefab` y escenas 13/14 R07.
- APK histórica **0.0.15**, `builds/android/12_appearance_20261003_012410.apk`,
  SHA-256 `b10e73187f762d6691ecea2319fcb8f1676df37283531bee41d4bafaae5ae4a5`.
  Conserva figura y panel; no representa el nuevo alcance ni fue validada físicamente.
- Marcador Unity `marker/03_marker_carta.pdf`, SHA-256
  `c670fc855c002dea0ad70c458db525b36dfcfff6e14400347bd0c7d1a47f1a83`.
  Impresión medida histórica: familia tagStandard41h12, ID 0, 100 mm de
  detección, dibujo 180 mm. Reutilizarla; no pedir otra sin necesidad.

## Etapas y subpasos

- **Replanificación completada:** evaluación de reutilización y acoplamiento,
  alcance/aceptación nuevos, correspondencia con los 24 pasos antiguos,
  archivo de plan/ficha/estado anteriores y entradas de continuidad.
- **F1 pendiente:** presentación estática propia, escena/build nuevos, UI,
  dependencia de recursos y pruebas de estados. No existe aún esa nueva escena.
- **F2 pendiente:** anatomía y pose; nueva fuente, seis vistas y comparación.
- **F3 pendiente:** malla móvil, UV/materiales, exportación y licencias.
- **F4 pendiente:** integración y luz; candidata Android propia.
- **F5 pendiente:** evidencia física y rendimiento en G20, M#[7].
- **F6 pendiente:** correcciones y regresión sobre esa evidencia.
- **F7 pendiente:** entrega reproducible y preparación de exposición; M#[8]
  solo cuando esté disponible el S23.

Los pasos antiguos 1–11 y resultados técnicos 13–14 se conservan como historia;
12 físico estaba aplazado y no se aprueba. 15–24 dejan de ser tareas activas.
Los subpasos y métricas anteriores están en el estado archivado; no se atribuyen
al nuevo modelo o aplicación. La demo de 35 s sigue siendo independiente.

## Cambios y motivo

El usuario prefiere concentrar el trabajo en la criatura. Se sustituyeron plan,
ficha y continuidad; los originales se archivaron sin alterar su cuerpo. Se
señalaron como históricos los documentos con instrucciones de continuación del
corto. La evaluación AR conserva evidencias y ahora distingue el alcance nuevo.
Unity enlaza al estado y plan canónicos; los README permiten encontrarlos.

No se encontró «next-job»; el usuario aclaró que confundió proyectos y pidió
un punto equivalente de continuidad. Este archivo cumple esa función, con un
enlace en `docs/estado.md` de Unity. No se crea otra lista duplicada de tareas.
No se modificaron modelos, scripts, escenas, paquetes, configuración ni APKs.

## Verificaciones de esta sesión y límites

La evidencia inicial de ambos repositorios está en
[evidencias/2026-10-02_cambio_figura/inicial.json](evidencias/2026-10-02_cambio_figura/inicial.json).
El [cierre verificable](evidencias/2026-10-02_cambio_figura/verificacion.json)
registra comprobación de enlaces nuevos, preservación por hashes de los archivos
ajenos a documentación, equivalencia de archivos históricos con el commit base,
hashes de APK/marcador y `git diff --check` de documentación en ambos repositorios.
El chequeo global del índice de Unity señala cuatro espacios finales en el
`PackageManagerSettings.asset` ajeno ya preparado; no se modificó para corregirlos.

No se repitieron Blender, Unity, tests de ejecución ni compilación Android:
solo cambia documentación. No se generó nueva evidencia visual ni se realizó
una prueba física; todo ello corresponde a F1–F7. Las pruebas y renders anteriores
conservan únicamente el alcance documentado en sus entregas.

## Decisiones y acciones manuales

Confirmados: dos raíces, Blender como fuente, Unity **6000.3.22f1** exclusivo,
Android desde Linux, AprilTag existente, G20 de pruebas, S23 pendiente, figura
original demacrada sobre el marcador y conservación de todas las demos/hitos.
Sin ventana ni oveja/escenario/ataque; 40 s ya no es requisito de la nueva entrega.
Figura estática como base, sin añadir idle/rotación/efectos por defecto.

- **M#[1]**: guion/audio resuelto histórico, fuera de alcance.
- **M#[2]**: aceptación histórica limitada de la ruta; no valida nueva carga.
- **M#[3]**: impresión/medida resuelta histórica.
- **M#[4]**: aceptación histórica del aspecto anterior, no del modelo futuro.
- **M#[5]**: prueba prevista del corto integrado, sustituida, nunca aprobada.
- **M#[6]**: revisión de 0.0.15 aplazada antes; ahora sustituida por cambio
  de alcance, **sin cierre físico ni aprobación**.
- **M#[7]**: figura nueva en G20, prevista para F5–F7, **no solicitada**.
- **M#[8]**: posible S23, prevista para exposición, **no solicitada**.

No hay decisiones ni acciones físicas indispensables pendientes de respuesta
para empezar F1–F2. Antes de M#[7], preparar APK, marcador, instrucciones y
resultados concretos; el agente realiza compilación, instalación y diagnóstico.
No volver a pedir decisiones confirmadas ni interpretar silencio como aprobación.

## Punto exacto de retoma

1. **F1:** comprobar este estado y los archivos reales en ambas raíces. Leer
   `TrackingProbe`, `AppearanceStudy`, `CameraGeometry`, `TrackingChecks` y
   builders completos. Crear una ruta estática mínima con escena y build propias
   que reutilice tracking sin ejecutar ninguna ruta de cine. Conservar las
   escenas históricas. Validar estados, dependencias, capturas y APK con el
   Editor exacto; no solicitar teléfono todavía.
2. **F2:** sobre la base demacrada R02, crear fuente nueva y refinar anatomía/pose
   con revisión desde seis vistas y comparación reproducible. Registrar la
   valoración visual separada de los checks numéricos.

Detenerse tras esas dos etapas, o antes ante bloqueo real. No iniciar F3 en la
misma sesión. Actualizar aquí subpasos, evidencias, límites y próxima pareja;
Unity mantiene el enlace. Commit/push según autorización de la sesión, sin
incluir cambios ajenos ni borrar entregas anteriores.
