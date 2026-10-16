# Continuidad de Unity AR

**3 de octubre de 2026: personaje rediseñado con respiración, antes de F7.**
El usuario solicita expresamente mejorar el personaje e implementarlo conservando
el funcionamiento de la aplicación. [Revisión artística](rediseno_nocturno.md). [Estado canónico](../../../blender/chupacabras/docs/estado.md) y
[informe físico](../../../blender/chupacabras/docs/figura_ar_f5_f6.md).

APK final **0.2.2 / 202**, `com.chupacabras.ar.figure`:
`builds/android/F6_figure_20261003_222832.apk`, **55.348.110 bytes**.
SHA-256: `0bf9b53293e4035d2decba069845bace2afc0c8330f8a77ad131b333a47b3e16`.
Escena `Assets/Scenes/F4_FiguraAR_r02.unity`; prefab F4 R02 y personaje Nocturno R08.
Compilar con `CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh`, solo Unity
6000.3.22f1. Sin variable se conserva F1. Fuentes/APKs anteriores preservadas.

Corregidos bucle de cámara denegada, fondo sin imagen y ruta de Captura Android.
32 checks y diez estados sintéticos correctos; regresión F1 y pruebas G20
registradas. Build sin errores/advertencias; firma/ARM64/alineación verificadas.
La APK anterior 0.2.2 fue probada en G20; esta compilación con el personaje nuevo
no se ha instalado ni perfilado físicamente. Perfiles largos de 0.2.0 y 0.2.1,
con límites explícitos en el informe. No se atribuyen a la última APK.

La app de prueba fue retirada: paquete, proceso y datos externos ausentes.
M#[7] atendida; S23 M#[8] pendiente. Sin cambios de paquetes ni ajustes globales
por el agente; cambios ajenos del índice preservados. Sin commit/push.
No se retoma cine/arrastre. F7 continúa pendiente. El alcance de esta sesión
fue únicamente el personaje, con sus recursos y comprobaciones.
