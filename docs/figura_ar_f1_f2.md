# Figura AR: F1 y forma F2

3 de octubre de 2026. Se ejecutaron únicamente **F1 y F2**. La aclaración
**M#[9]** confirmó figura estática AR: el bloque del corto de 40 segundos en
la solicitud era una plantilla anterior. No se restaura ese alcance.

## F1: presentación independiente

En la raíz Unity se creó `Assets/Scenes/F1_FiguraAR_r01.unity` con el prefab
`Assets/FiguraAR/F1_r01/Figure.prefab`. Conserva geometría, centrado y escala
de la figura demacrada R02: **30.880 triángulos**, 18 mallas, seis materiales.
La APK todavía contiene esa base; **no contiene la forma F2**.

`TrackingProbe` recibe una referencia explícita `staticFigure`, comparte
cámara, detector y estados existentes, y evita tanto `AppearanceStudy.Attach`
como el fallback cinematográfico. El reloj narrativo permanece en cero;
la interfaz de figura no ofrece RT ni estudios de iluminación. Se oculta
inmediatamente al suspender/cerrar cámara. Se conserva la configuración
provisional de FOV y los controles de cámara para el diagnóstico físico futuro.
Las escenas antiguas siguen usando su ruta previa.

Entrega Unity:

- Escena/prefab anteriores y `Assets/Editor/FigureBuild.cs`, `FigurePreview.cs`.
- Reproducción: `bash scripts/build_figure.sh` desde la raíz Unity. Usa solo
  Unity **6000.3.22f1**, rutas de evidencia/APK nuevas y restaura ajustes de build.
- APK **0.1.0**, paquete `com.chupacabras.ar.figure`:
  `builds/android/F1_figure_20261003_162413.apk`, **38.200.938 bytes**.
- SHA-256: `48f1adf50143ed4c9fa83134a68316529752a12b4e93a50f0b801faca25e5cd5`.
- [Evidencia F1](../../../unity/chupacabras/docs/evidencias/F1_20261003_162304/):
  tres composiciones, ocho capturas de estados, logs, firma y dependencia real
  de assets según BuildReport (`packed_assets.txt`).

Compilación Android: **0 errores / 0 advertencias de BuildReport**. Firma,
permiso de cámara, ARM64 y ocho bibliotecas ELF con alineación de 16 KB
comprobados. Esto no acredita ejecución en un Android con páginas de 16 KB.
El tamaño total de BuildReport incluye salidas adicionales y no es el tamaño
comprimido de la APK indicado arriba.

Pasaron los **32 checks existentes** de geometría/detector/seguimiento y la
prueba de ejecución de ocho estados: inicio oculto, adquisición, pérdida,
recuperación, timeout, nueva imagen, segundo plano y reanudación. Se conserva
una instancia, escala estable y cero reloj narrativo. En esa ejecución solo
hay cámaras AR/fondo, sin Animator, AppearanceStudy, PlayableDirector ni
materiales con RenderTexture cinematográfica. Las texturas temporales del
capturador de evidencia no son parte de la aplicación.

La lista empaquetada no contiene escena/mallas/materiales de cine, oveja,
escenario, animaciones ni assets Timeline. Unity conserva metadatos de clases
históricas dentro del ensamblado compartido; no se afirma que esos nombres de
scripts hayan desaparecido del BuildReport. No se ejecutan en la escena F1.
La regresión `AppearancePreview.Capture` sobre la escena demacrada histórica
pasó adquisición, pérdida, pausa del reloj y recuperación.

Una primera compilación del verificador falló al usar una API de recuento de
grafos no disponible; se corrigió para comprobar componentes presentes con
las APIs del Editor instalado. El intento fallido se conserva en
`docs/evidencias/F1_20261003_162222/` de Unity.

## F2: anatomía y pose

Fuente nueva: [F2_chupacabras_forma_r04.blend](../scenes/F2_chupacabras_forma_r04.blend),
derivada de `09_chupacabras_demacrado_r02.blend`. Cambios y motivo:

- Unión de cráneo, cejas y mejillas para reducir piezas visualmente superpuestas.
- Mandíbula suavizada conservando el apoyo de los dientes inferiores.
- Cresta y garras con curvas y raíces más continuas.
- Cabeza girada 12 grados, manos y patas escalonadas, variación de cola;
  la misma deformación afecta piel y detalles para conservar sus uniones.
- Apoyos de los cuatro miembros revisados y puntas de garras sobre el plano.

La fuente de forma tiene **88.952 triángulos y 18 mallas cerradas**. Este aumento
corresponde al trabajo de forma del rostro/mandíbula, **no a un presupuesto
móvil aprobado**. No se exportó un FBX F2 ni se inició retopología, UV finales,
texturizado o integración nueva: esas tareas corresponden a F3–F4.

Evidencia:

- [Comparación base / F2](../previews/F2_chupacabras_forma_r04/comparacion.png).
- [Seis vistas](../previews/F2_chupacabras_forma_r04/seis_vistas.png): frente,
  perfil, espalda, tres cuartos, inferior y rostro. Cada original está en la
  misma carpeta con prefijos `base_` y `forma_`, a 1100 × 850.
- [Giro de inspección](../previews/F2_chupacabras_forma_r04/giro.mp4): 72 frames,
  H.264, 720 × 540, 12 fps, seis segundos. No se ejecuta en la app.
- `geometry.json`, `reopen_checks.json` en esa carpeta; logs en
  `docs/evidencias/2026-10-03_figura/`.

**Valoración visual del agente:** se conserva espalda arqueada, cintura
estrecha, costillas, ojos amarillos y cresta. La asimetría es visible de frente
y perfil; el rostro tiene transiciones más continuas y las garras menos
angulosas. La revisión de las seis vistas no mostró detalles flotantes ni
intersecciones evidentes adicionales. Sigue siendo una forma con sombreado
simple, con rasgos todavía estilizados; no se presenta como el acabado
realista final ni como aceptación estética del usuario. Piel, rugosidad y
lectura de ojos/materiales quedan para F3–F4; aceptación visual móvil, F5.

La reapertura independiente comprueba coordenadas finitas, mallas cerradas,
caras no degeneradas, cuerpo/cráneo continuos, ausencia de rig/animación,
asimetría y apoyo. Los mínimos de las cuatro patas están entre 0 y 0,000375 m
en coordenadas de autoría. Todos los componentes de dientes/garras/penachos
comprobados alcanzan el interior de su soporte según normales de proximidad;
esta comprobación local no es una prueba exhaustiva de autointersecciones.
Ninguna geometría queda por debajo del plano de apoyo.

R01 mostró dientes mal apoyados tras subdividir mandíbula; R02 conservó mejor
su volumen, pero algunas garras cruzaban el plano. R03 corrigió altura; la
revisión adicional de raíces y apoyo llevó a R04. Se conservan las versiones
intermedias localmente, excluidas del commit como los ensayos anteriores del
proyecto; se versionan fuente final, evidencia final y logs de iteración comprimidos
sin pérdida (`.log.gz`); los originales permanecen locales.

## Reproducción y límites

Desde Blender, elegir una revisión nueva para no sobrescribir entregas:

```bash
CHUPA_F2_REV=r05 blender -b -t 4 --python-exit-code 1 --python scripts/figura_forma.py
CHUPA_F2_REV=r05 blender -b -t 4 --python-exit-code 1 --python scripts/verificar_figura_forma.py
CHUPA_F2_REV=r05 python scripts/resumen_figura.py
ffmpeg -n -framerate 12 -i previews/F2_chupacabras_forma_r05/giro_frames/%04d.png -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart previews/F2_chupacabras_forma_r05/giro.mp4
```

Blender **5.2.2 LTS**. Base y revisión se renderizan con las mismas cámaras,
escalas, luz Workbench y colores. El resumen usa FFmpeg ya instalado, sin
paquetes nuevos. Los archivos nuevos serializados por Unity se normalizaron únicamente para
quitar espacios finales; el informe de dependencias bruto se conserva también
en `packed_assets.txt.gz`. Los scripts se comprobaron por compilación Python; shell con
`bash -n`; los cambios textuales, con `git diff --check`. No hay linter o suite
general configurados en Blender; se ejecutó el verificador específico de F2.

No se conectó ningún teléfono, no se instaló la APK y no se mide rendimiento
físico. **M#[7]** y **M#[8]** siguen futuras. Unity conserva sus tres cambios
ajenos del índice, sus paquetes y configuración. La build regeneró temporales
`.utmp` ya versionados: se restauraron solo los que coincidían con el estado
inicial/HEAD, conservando copia temporal de los generados. No se borraron demos,
hitos, ni se modificó configuración global.

Próxima pareja: **F3 + F4**, según [estado](estado.md). Sin push.
