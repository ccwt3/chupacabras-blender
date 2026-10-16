# Chupacabras — demo Android AR

Chupacabras sobre el marcador AprilTag existente, con nueva piel, anatomía y
respiración de cuatro segundos. [Revisión del personaje](docs/rediseno_nocturno.md).
**F1–F7 completadas como demo funcional en Moto G20**, con Nocturno R08 y
respiración R02. [Informe final](../Blender/docs/figura_ar_f7.md):
310 s a 28,53 fps, por debajo de 30 fps sostenidos; límite aceptado como demo.
Entrega completa en Blender: `entregas/F7_Nocturno_R08_20261006/` y `.tar.gz`.

- [Estado y siguiente trabajo](docs/estado.md).
- [Pruebas G20 y correcciones](docs/figura_ar_f6.md).
- [Plan canónico](../Blender/docs/plan_secuencia.md).

Usar exclusivamente Unity **6000.3.22f1** instalado en
`/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`.
Escena vigente: `Assets/Scenes/F4_FiguraAR_r02.unity`.
APK final: `builds/android/F6_figure_20261006_181916.apk` (**0.2.2 / 202**).
Construcción: `CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh`.
Sin la variable se conserva F1; F4 y sus APK anteriores también permanecen.

Reutilizar el marcador carta impreso. Se conserva URP/AprilTag, sin ARCore.
La app de esta prueba ya fue retirada del G20. S23 pendiente.
Demos, escenas, fuentes y evidencias históricas se conservan; no son el flujo
vigente ni requieren retomar la ventana cinematográfica o el corto.
