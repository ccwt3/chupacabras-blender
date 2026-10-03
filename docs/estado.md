# Estado de continuidad

Actualizado: **3 de octubre de 2026 — F5 y F6 cerradas como demo AR funcional**.
[Informe y evidencia](figura_ar_f5_f6.md) · [Plan F1–F7](plan_secuencia.md) ·
[Estado anterior](evidencias/2026-10-03_figura_f5_f6/estado_anterior.md).

**Siguiente etapa: F7, entrega sencilla. No iniciada.**
El usuario prioriza que funcione el AR y aclara que no es una app comercial.
No abrir más pulido ni repetir perfiles por detalles menores. Se conserva el
alcance de figura estática sobre AprilTag; no retomar corto, arrastre, oveja,
ventana cinematográfica ni M#[6].

## Resultado

- G20: figura visible desde distintos ángulos, pérdidas/recuperaciones,
  segundo plano, giro real de pantalla y funcionamiento sin red comprobados.
  Usuario: «Se ve bien y recupera correctamente» y «Todo listo y si todo se ve bien».
- F4 0.2.0: 309,98 s a 30,005 fps; 2499/2499 muestras visibles en 303,885 s.
- F6 corrigió un bucle real al denegar cámara: la reanudación ya no vuelve a
  solicitar el permiso. Denegación, Reintentar y recuperación comprobados en G20.
  También se ocultó el fondo sin imagen y se corrigió la ruta Android de Captura.
- F6 0.2.1: 310 s, 29,607 fps brutos con una interrupción de foco de 4,132 s;
  305,867 s activos a 30,003 fps. Datos brutos y causa correlacionada conservados.
  Sin limitación térmica reportada; la memoria se estabiliza tras la subida inicial.
- F6 0.2.2 final: instalación, arranque frío, detección, figura y captura real
  correctos. No se le atribuye el perfil de 0.2.1 ni se repite otro largo,
  conforme a la prioridad de demo funcional indicada por el usuario.
- 32 checks, diez estados sintéticos y regresión F1 correctos. ID incorrecto y
  timeout son pruebas sintéticas; permiso, cámara, reanudación y giro tienen
  evidencia física. Build final sin errores ni advertencias.

## Entregas vigentes

Blender mantiene `scenes/F3_chupacabras_superficie_r05.blend` y su FBX/mapas:
34.026 triángulos, una malla/material. [Entrega F3–F4](figura_ar_f3_f4.md).
No se modificó forma, materiales, luz, escala ni detector en F6.

Unity: `/home/cacawatin/code/unity/chupacabras`, exclusivamente **6000.3.22f1**.
Escena `Assets/Scenes/F4_FiguraAR_r02.unity`, prefab `Assets/FiguraAR/F4_r02/Figure.prefab`.
APK final **0.2.2**, código **202**, paquete `com.chupacabras.ar.figure`:
`builds/android/F6_figure_20261003_213520.apk`, **41.621.707 bytes**.
SHA-256: `d8448556ee2529bd8ee130c75d26e424b1ec98106f04f196cdf65574e4cfabbd`.
Reproducción: `CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh` desde Unity.
F1 sigue siendo el valor por defecto; las APK anteriores permanecen.

Marcador existente sin cambios: `marker/03_marker_carta.pdf` en Unity,
tagStandard41h12 ID 0, detección 100 mm, dibujo 180 mm. Reutilizar la impresión.
No se necesita nueva impresión ni cambio de FOV provisional 60°.

## Cierre físico y preservación

La app de prueba fue desinstalada; paquete, proceso y datos externos ausentes.
El móvil se puede desconectar. M#[7] atendida para F5/F6; M#[8] S23 pendiente.
Fuentes/escenas/APKs y cambios previos preservados. Sin cambios de paquetes o
ajustes globales por el agente; ajustes ajenos del índice intactos. Sin commit/push.
Evidencias y fuentes de cada corrección en `docs/evidencias/2026-10-03_figura_f5_f6/`.

F7 preparará únicamente la entrega reproducible y guía breve de esta demo.
No ampliar a producto comercial ni tomar estas pruebas como validación en S23,
calibración exacta o garantía de funcionamiento durante horas. No crear `next-job`.
