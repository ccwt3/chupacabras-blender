**Revisión 0.2.8 / 208:** ampliación uniforme ×1,375 de modelos y recorrido;
reinicio completo al recuperar el marcador. AprilTag sin cambios.
[Detalle y verificaciones](ataque_natural_1m.md). Instalada limpiamente en Moto G20; pruebas Unity y empaquetado correctos.
Escala, recorrido y reinicio aceptados en Moto G20 («todo bien 10/10»).
29,33 fps durante tres minutos; segundo plano correcto y reinstalación final
limpia del mismo APK derivado del AAB.
El usuario aceptó el movimiento de 0.2.7; versiones anteriores preservadas.

**11 de octubre: ataque AR integrado y probado; entrega 0.2.5 / 205.**
[Modelamiento, animación, integración, prueba móvil y AAB](ataque_ar.md).
Fuente nueva `ataque_ar_r02`; Unity en la copia independiente `google_play`.
Blender/FBX y pruebas de Editor correctos. Secuencia y recuperación física
confirmadas en Moto G20; perfil de cinco minutos: 29,638 fps. AAB firmado y
APK universal derivado en `entregas/Ataque_AR_0.2.5_20261011/`.
El cierre F7 siguiente corresponde a la figura anterior y se conserva como historia.

# Estado de continuidad

**10 de octubre: revisión de interfaz 0.2.3 / 203**, con bienvenida y cámara
bajo demanda, sin modo de desarrollo. [Cambios y validación](../../../unity/chupacabras/docs/interfaz_inicio.md).
El cierre F7 y las medidas físicas siguientes corresponden a la APK 0.2.2 conservada.

Actualizado: **6 de octubre de 2026 — F7 completada como demo funcional en Moto G20**.
[Informe final y límites](figura_ar_f7.md) · [Plan](plan_secuencia.md) · [Rediseño original](rediseno_nocturno.md).

## Entrega final

`entregas/F7_Nocturno_R08_20261006/` y su archivo hermano `.tar.gz` en Blender.
Incluye APK, fuentes Blender/Unity, FBX/texturas, recursos/licencias, marcador,
guía `LEEME.md`, inventario `manifest.json` y hashes `SHA256SUMS`.

APK medida y entregada en Unity: `builds/android/F6_figure_20261006_181916.apk`.
Versión **0.2.2 / código 202**, paquete `com.chupacabras.ar.figure`, **55.348.110 bytes**.
SHA-256: `7db6358cdb13c37467a3d42f76d163ef8359c0ef25583441065ed5b869863aae`.
Hash del paquete instalado comprobado contra esta misma candidata; no se recompiló después.

Fuente vigente: `scenes/chupacabras_nocturno_r08_respira_r02.blend`.
Conserva geometría, UV, pesos, material y mapas R08; 110.294 triángulos,
un material PBR 2K y cuatro huesos. Solo amplía respiración, manteniendo cuatro
segundos y patas fijas. El usuario informó que R08 parecía estático y aceptó
R02: «respiracion bien, listo». Malla/luces/escala/escena/runtime/seguimiento/
interfaz/paquetes/ProjectSettings de Unity preservados; cambia el controlador
del Animator. Prefab y escena conservan sus ubicaciones F4 R02.

## Comprobación y criterio de cierre

- Revisión física desde distintos ángulos, texturas, escala, apoyo y respiración;
  defecto observado corregido y revisado de nuevo en G20.
- APK final: 310 s a **28,532 fps**; mediana/p95/p99 de cuadro
  **33,324 / 49,985 / 50,051 ms**, máximo 83,303 ms, ninguno >100 ms.
  Figura visible en 2530/2530 muestras; detector **15,007 Hz**, distinto del render.
- PSS **401,15 → 386,33 MiB**, sin crecimiento sostenido en ese tramo;
  batería **37,9 → 39,4 °C** con carga USB. Estado térmico reportado 0.
- Pérdida/recuperación y segundo plano/reanudación físicos en la APK final,
  misma instancia visible sin duplicación observada y mismo proceso al reanudar.
- Blender/FBX, 32 checks y diez estados sintéticos Unity correctos;
  build cero errores/advertencias, firma/ABI/alineación correctas.

**No se alcanzaron 30 fps sostenidos.** Informado el resultado, el usuario
respondió «si, suficiente como demo». F7 se cierra bajo ese criterio, conservando
los intervalos y limitaciones reales. No se atribuyen a R08 los perfiles F3.
El primer perfil R08 (APK del 3 de octubre) quedó en 28,168 fps; ambos perfiles
se preservan, sin afirmar mejora causal por el cambio de animación.

## Preservación, limpieza y límites

R08 original, F3, F1–F6, escenas, fuentes, APK y entregas anteriores preservadas.
No había instalación previa del paquete de prueba. Se desinstaló solo ese paquete;
proceso y datos externos ausentes, comprobados en `evidencias/2026-10-06_f7/cleanup.json`.
El teléfono se puede desconectar. No se modificaron ajustes globales ni otras apps.
Cierre físico original sin commit/push; solicitud posterior de commits locales
atendida en la sesión de documentación de distribución. Sin push, fases nuevas
ni pulido comercial. [Uso, distribución y requisitos](distribucion_demo.md).

Unity exclusivamente **6000.3.22f1**. Construcción desde Unity:
`CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh`.
Marcador existente `marker/03_marker_carta.pdf`, tagStandard41h12 ID 0,
100 mm de detección, dibujo 180 mm. No se cambió ni reimprimió.
FOV provisional 60°, sin calibración métrica exacta. No se acreditan sesiones
de horas ni ejecución Android con páginas de 16 KB. **S23/M#[8] pendiente,
no bloqueante**; no se extrapola la aceptación del G20.

F1–F7 cerradas para esta demo. No hay siguiente fase automática ni `next-job`.
