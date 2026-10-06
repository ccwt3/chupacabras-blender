# Revisión artística del chupacabras — 3 de octubre de 2026

El usuario solicita priorizar apariencia y respiración antes de F7 y reemplazar
únicamente el personaje de la aplicación. Esta petición sustituye el alcance
anterior de figura estática; F7 continúa pendiente. La referencia principal es
la segunda imagen facilitada en la conversación. Las imágenes no se incorporan
a los recursos distribuidos.

## Diseño y fuentes

Fuente: `scenes/chupacabras_nocturno_r08.blend`; intercambio:
`exports/chupacabras_nocturno_r08.fbx`. Se preservan las fuentes F2/F3 y los
ensayos intermedios. No se modifica la escena histórica de ataque ni la oveja.

- Cráneo alargado reconstruido, órbitas excavadas, ojos pálidos retraídos,
  hocico estrecho y dentadura de tamaños irregulares. Se retiran las cejas
  gruesas del modelo anterior y se rehacen las orejas con interior diferenciado.
- Piel oscura mate, pigmentación irregular, poros y pliegues; queratina oscura
  y marfil envejecido. Texturas procedurales originales horneadas, sin fotos
  ajenas ni iluminación pintada en BaseColor.
- Cresta de agujas curvadas, con separación, inclinación y longitud variables,
  más cerdas cortas en los hombros. Se preserva la anatomía demacrada y el apoyo.
- 110.294 triángulos frente a los 34.026 de F3, una malla y un material.
  El detalle fino queda en Normal; no requiere subdivisión en tiempo de ejecución.
- Atlas 2048 × 2048: BaseColor sRGB, Normal tangente +Y, Roughness lineal
  para Blender, MetallicSmoothness lineal (R=0, alfa=1−rugosidad) para Unity.
  Los tres mapas usados en Android conservan ASTC 6×6 y mipmaps.

La malla se refina desde F2, no desde el FBX reducido de F3. Se corrigen pequeñas
aristas abiertas de la operación de órbitas mediante remallado local antes de
reducir el cráneo. El verificador exige una malla cerrada antes de hornear.
Las islas de las espinas no se amplían artificialmente hasta desplazar del atlas
la resolución destinada a piel y rostro.

## Respiración

Clip `Respiracion_4s`, cuatro segundos a 24 fps, cuatro huesos. El tórax se
expande y asciende levemente; cabeza y cola acompañan con movimientos pequeños.
Las patas conservan peso en la raíz y no deslizan. Los extremos coinciden y la
raíz no se desplaza. No se añade una animación de caminar ni una secuencia narrativa.

En Unity se usa un Animator Controller nativo de un solo estado en el personaje.
El prefab de presentación sigue siendo `Assets/FiguraAR/F4_r02/Figure.prefab`;
solo se sustituye su hijo `StaticFigure`, manteniendo nombre, transformación,
luces y referencias de la escena. El nombre histórico del hijo se conserva para
no alterar la aplicación. No se añade código runtime ni se cambia seguimiento,
permisos, interfaz, marcador, paquetes o configuración gráfica.

El FBX también hornea curvas constantes sobre su raíz. Se genera el recurso
nativo `Respiracion.anim` con las curvas de huesos, retirando únicamente las curvas
con ruta vacía: estas sobrescribían la escala y la rotación de presentación al
reproducir el clip. La inspección visual detectó el problema; las pruebas ahora
comprueban dimensiones, apoyo y transformación local del personaje durante el ciclo.
Se conservan las capturas diagnósticas y la validación corregida en `final_v2/`.

`FigureNocturno.cs` importa el recurso y verifica su deformación. Los verificadores
existentes `FigureBuild` y `FigurePreview` reconocen ahora el personaje animado;
F1 y las figuras estáticas conservan su comprobación anterior. Las comprobaciones
de ciclo narrativo cero y ausencia de recursos cinematográficos siguen activas.

## Reproducción

Para producir otra revisión sin sobrescribir entregas:

```bash
CHUPA_ART_REV=r09 blender -b -t 4 --python-exit-code 1 --python scripts/chupacabras_nocturno.py
CHUPA_ART_REV=r09 blender -b -t 2 --python-exit-code 1 --python scripts/verificar_nocturno.py
CHUPA_ART_REV=r09 blender -b -t 4 --python-exit-code 1 --python scripts/preview_nocturno.py
ffmpeg -n -framerate 12 -i previews/chupacabras_nocturno_r09/respiracion_frames/%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart previews/chupacabras_nocturno_r09/respiracion.mp4
```

La fuente Blender incluye el ciclo; el video de revisión mantiene la cámara fija
para que el movimiento pueda distinguirse. La exportación FBX se vuelve a importar
con `anim_offset=0`, evitando el cuadro de desplazamiento que añade por defecto
el importador Blender. La duración del clip no se modifica para compensarlo.

Para compilar el proyecto Unity una vez importado el recurso:

```bash
CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh
```

Se mantiene la versión funcional 0.2.2 / código 202 y el paquete existente, ya que
esta sesión cambia el recurso visual. La APK tiene nombre de archivo y hash nuevos;
no debe confundirse con la APK F6 anterior. La medición previa de 30 fps corresponde
al personaje anterior y no se atribuye al nuevo.

## Validación y límites

La validación de la fuente comprueba presupuesto, cierre de malla, UV, mapas,
pesos, los 97 cuadros de apoyo y coordenadas finitas, cierre del ciclo e intercambio
FBX en cinco fases. Unity comprueba material, clip, deformación, patas y reproducción
real de la respiración, además de los estados de seguimiento existentes.

Esta revisión no incluye mediciones físicas de rendimiento ni aceptación estética
en un teléfono. Las capturas de estudio y de Unity son evidencia de revisión, no
fotografías del resultado AR en un dispositivo. El presupuesto de 110 mil triángulos
se mantiene moderado para una sola figura, pero no acredita por sí solo 30 fps.

## Entrega comprobada

- APK: `builds/android/F6_figure_20261003_222832.apk` en Unity, **55.348.110 bytes**,
  versión **0.2.2 / 202**, `com.chupacabras.ar.figure`.
- SHA-256: `0bf9b53293e4035d2decba069845bace2afc0c8330f8a77ad131b333a47b3e16`.
- Build: **cero errores y cero advertencias**. El tamaño anterior es el archivo APK;
  `BuildReport.totalSize` también contabiliza productos de compilación y no es ese tamaño.
- Fuente Blender: malla cerrada, 110.294 triángulos, pesos normalizados, mapas/UV
  válidos, apoyo en los 97 cuadros, deslizamiento de patas cero, cierre de ciclo cero.
  La ida/vuelta FBX difiere como máximo 0,000000719 m en las cinco fases comparadas.
- Unity: 72.963 vértices importados, un material, cuatro huesos; ciclo de cuatro
  segundos, desplazamiento de patas cero y diferencia del cierre menor que
  0,000000267 m. Se verifica también el tamaño real y la orientación de la figura.
- Las 32 comprobaciones de seguimiento y los diez estados sintéticos pasan;
  el Animator avanza durante la prueba y el personaje mantiene su transformación.
  APK firmada, ARM64, permiso de cámara y alineación ZIP/ELF verificados.
- Auditoría de alcance: escena, luces, escala del personaje, scripts runtime,
  paquetes y ProjectSettings conservan su contenido previo. Los diez archivos
  regenerados de compilación/espacios serializados se restauran contra sus hashes
  iniciales; copias de los generados se conservan localmente. Sin commit ni push.

Evidencias Unity: `docs/evidencias/2026-10-03_nocturno_r08/final_v2/`.
Evidencias de modelado: `docs/evidencias/2026-10-03_rediseno/` y
`previews/chupacabras_nocturno_r08/checks.json`. El video
`previews/chupacabras_nocturno_r08/respiracion.mp4` tiene 48 cuadros,
640 × 480, H.264 y cuatro segundos. Las vistas estáticas de Blender son 1200 × 900;
`unity_tres_cuartos.png` y `unity_rostro.png` muestran el material con las luces
reales de la aplicación. No se instaló esta APK en un móvil.
