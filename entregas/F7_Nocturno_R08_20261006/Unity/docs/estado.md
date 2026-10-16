# Continuidad de Unity AR

**6 de octubre de 2026: F1–F7 completadas como demo funcional en Moto G20.**
[Estado canónico](../../Blender/docs/estado.md) ·
[Informe final y límites](../../Blender/docs/figura_ar_f7.md).

APK medida y entregada: `builds/android/F6_figure_20261006_181916.apk`,
**0.2.2 / 202**, **55.348.110 bytes**, `com.chupacabras.ar.figure`.
SHA-256: `7db6358cdb13c37467a3d42f76d163ef8359c0ef25583441065ed5b869863aae`.
Instalación final cotejada por hash; no recompilada después de la prueba.

Nocturno R08 conserva malla, material y mapas. Se corrigió únicamente la
respiración imperceptible mediante `Assets/FiguraAR/Nocturno_r08_respira_r02/`:
clip y controlador nuevos sobre el mismo personaje. Escena
`Assets/Scenes/F4_FiguraAR_r02.unity` y prefab F4 R02 conservados, salvo la
referencia del controlador. Runtime, luces, escala, seguimiento, interfaz,
paquetes y ProjectSettings intactos.

El usuario aceptó respiración y recuperación finales y consideró suficiente
la demo tras conocer el resultado: 310 s, 28,532 fps; no cumple 30 fps sostenidos.
Métricas, condiciones, fuentes Blender y pruebas completas están en el informe
canónico, sin atribuir perfiles de versiones anteriores a la candidata final.

Build cero errores/advertencias; verificadores de fuente, 32 checks y diez
estados sintéticos correctos. Solo Unity 6000.3.22f1:
`CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh`.

Entrega empaquetada en Blender: `entregas/F7_Nocturno_R08_20261006/` y `.tar.gz`.
Incluye APK, fuentes, recursos/licencias, marcador, guía y hashes.
Instalación de prueba retirada; paquete, proceso y datos externos ausentes.
Previas fuentes/APKs/cambios preservados. Sin commit/push ni nuevas fases.
S23 pendiente y no bloqueante para el cierre G20. Sin garantía de sesiones de
horas ni calibración métrica exacta. No crear `next-job`.
