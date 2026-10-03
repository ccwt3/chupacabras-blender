# Estado de continuidad

Actualizado: **3 de octubre de 2026 — F3 y F4 completadas técnicamente**.
[Plan F1–F7](plan_secuencia.md) · [Entrega F3–F4](figura_ar_f3_f4.md) ·
[Entrega F1–F2](figura_ar_f1_f2.md) · [Estado anterior](evidencias/2026-10-03_figura_f3_f4/estado_anterior.md).

**Próxima pareja: F5 + F6. No iniciadas.**
La figura estática AR sigue vigente: M#[9] resuelta. No retomar el corto,
arrastre, ventana cinematográfica ni la revisión física histórica M#[6].
No quedan contradicciones de alcance ni bloqueos técnicos conocidos para
preparar F5. La calidad visual y el rendimiento reales aún no están aprobados.

## Alcance y preservación

Se ejecutaron las dos etapas autorizadas **F3 y F4**, sin iniciar F5 ni pedir
el teléfono. Blender sigue siendo la fuente y Unity 6000.3.22f1 el Editor
exclusivo. Se conserva URP, AprilTag y la captura existente, sin ARCore ni
cambios de paquetes. Figura original estática, sin idle, autorrotación,
Animator, oveja, escenario, Timeline o duración narrativa.

Inventario inicial y hashes: [inicial.json](evidencias/2026-10-03_figura_f3_f4/inicial.json).
Blender estaba limpio. Unity conservaba tres cambios ajenos preparados:
GraphicsSettings, QualitySettings y PackageManagerSettings. Fuentes, escenas,
APKs y referencias anteriores se conservan; no se hicieron commits ni push.

## Etapas

- **F1 y F2 completadas previamente:** presentación AR propia y fuente de
  forma/pose R04 de 88.952 triángulos. F1 y su APK 0.1.0 siguen disponibles.
- **F3 completada técnicamente:** fuente de superficie **R05**, 34.026
  triángulos, una malla y un material. UV, mapas PBR originales 2K, FBX estático,
  ficha de memoria/licencia, seis vistas y comparación con F2. Reapertura y
  reimportación correctas. Ningún presupuesto móvil se considera aprobado.
- **F4 completada técnicamente:** prefab/escena **R02**, mapas URP y luz propia,
  seis vistas y APK **0.2.0** firmada/verificada. 32 checks y ocho estados de
  ejecución sintéticos correctos. Regresión F1 aprobada en Editor.
- **F5 pendiente:** revisión física y rendimiento en Moto G20, M#[7].
- **F6 pendiente:** correcciones y regresión según esa evidencia.
- **F7 pendiente:** entrega reproducible; S23 M#[8] solo cuando esté disponible.

## Entregas actuales

Blender:

- [Fuente F3 R05](../scenes/F3_chupacabras_superficie_r05.blend) y
  [FBX](../exports/F3_chupacabras_superficie_r05.fbx).
- [Mapas, métricas y licencia](../exports/F3_chupacabras_superficie_r05/manifest.json).
- [Seis vistas](../previews/F3_chupacabras_superficie_r05/seis_vistas.png),
  [comparación F2/F3](../previews/F3_chupacabras_superficie_r05/comparacion_forma.png),
  [comprobación independiente](../previews/F3_chupacabras_superficie_r05/reopen_checks.json).
- `scripts/figura_superficie.py`, `verificar_figura_superficie.py` y el montador
  reutilizable `resumen_figura.py`. Fuentes/intentos R01–R04 conservados localmente;
  logs de errores comprimidos y revisión R05 forman parte de la entrega.

Unity (`/home/cacawatin/code/unity/chupacabras`):

- `Assets/Scenes/F4_FiguraAR_r02.unity`, `Assets/FiguraAR/F4_r02/Figure.prefab`.
- APK: `builds/android/F4_figure_20261003_172936.apk`,
  **42,421,014 bytes**, versión 0.2.0, código 200, paquete `com.chupacabras.ar.figure`.
- SHA-256: `e5acda3e837a7054aff879d64de176599695ffc6c73b315b868c9cb2fd268104`.
- `docs/evidencias/F4_20261003_172800/`: build, dependencias, runtime y APK.
- `docs/evidencias/F4_revision_visual_20261003/`: seis vistas finales con encuadre
  comparable a Blender y dos fondos sintéticos de contraste.
- `docs/evidencias/F4_regresion_F1_20261003/`: regresión de F1.
- Reproducción: `CHUPA_FIGURE_STAGE=F4 bash scripts/build_figure.sh`.
  La ruta por defecto sin variable sigue siendo F1.

Marcador sin cambios: `marker/03_marker_carta.pdf` en Unity,
SHA-256 `c670fc855c002dea0ad70c458db525b36dfcfff6e14400347bd0c7d1a47f1a83`.
Reutilizar la impresión carta medida: tagStandard41h12, ID 0,
100 mm entre esquinas de detección y dibujo de 180 mm. La copia adicional
impresa en sala está documentada en [impresión](impresion_sala.md).

## Errores corregidos y límites

Se corrigieron islas UV sin muestras de horneado, la conversión de coordenadas
del verificador, una captura inicial transitoria de URP y la orientación de la
iluminación. Se documentó un intento de acceso a una propiedad de solo lectura
del Editor; el código final conserva su valor correcto. Diagnósticos y causas
en [el informe](figura_ar_f3_f4.md). No se eliminaron pruebas para aprobarlos.
[Verificación final y hashes](evidencias/2026-10-03_figura_f3_f4/verificacion.json):
sin archivos anteriores ausentes ni cambios inesperados; APK F1 y marcador intactos.

BuildReport final: **cero errores y cero advertencias**. Firma, permiso de cámara,
ARM64 y alineación ZIP/ELF comprobados. No hay recursos cinematográficos
empaquetados por dependencia; clases históricas siguen en el ensamblado compartido.
Una sola instancia en adquisición, pérdida, recuperación, timeout, imagen nueva,
segundo plano y reanudación, con escala estable y reloj narrativo cero.

**Sin teléfono, instalación ni medición física nueva.** La piel tiene acabado
PBR, pero persisten formas estilizadas/angulosas de F2. Las vistas no equivalen
a aprobación estética, fotorrealismo ni brillo real en exposición. Memoria de los
mapas: estimación 7,14 MiB ASTC con mipmaps; no es memoria total de la aplicación.
Fps, temperatura y estabilidad se medirán en F5.

## Acciones manuales y punto de retoma

M#[1]–M#[4] conservan sus cierres históricos; M#[5] y M#[6] quedaron sustituidas,
sin aprobación física nueva. M#[9] (alcance figura AR) y M#[10] (impresión) resueltas.
**M#[7]** sigue futura para G20; **M#[8]** para S23 si hay acceso.

1. **F5:** revisar este estado y la candidata F4 R02, comprobar su hash y preparar
   instrucciones/resultados a observar antes de solicitar M#[7]. Usar la impresión
   existente. Validar varios ángulos, pérdidas/recuperaciones, segundo plano y
   al menos cinco minutos de rendimiento. Registrar la opinión estética del usuario
   y las medidas reales; limpiar únicamente lo instalado para esa prueba.
2. **F6:** corregir defectos concretos surgidos de F5 y comprobar regresión.
   No sustituir la prueba física por las capturas de Editor ni avanzar a F7 sin evidencia.

Como máximo esas dos etapas en la próxima sesión; esta sesión termina tras F3–F4.
Unity enlaza a este estado canónico. No crear `next-job` ni reabrir decisiones resueltas.
