# Chupacabras AR 0.2.7 / 207 — actuación corregida R08

- `Chupacabras_AR_0.2.7_207.aab`: Android App Bundle firmado.
- `Chupacabras_AR_0.2.7_207_desde_AAB.apk`: APK universal generado de ese AAB, firmado con la misma clave de carga.
- `Vista_animacion_R08.mp4`: revisión de movimiento desde Blender con materiales neutros. La APK utiliza las texturas de la aplicación.

La oveja pasta con **30 cm de espacio libre** respecto al chupacabras. Este
anticipa y salta unos **36 cm** hasta ella; baja el cuerpo flexionando las
patas para morder, sin estirar el cuello. Tras el forcejeo sin sangre, gira
y regresa caminando. A los **13,5 s** queda respirando **sobre el AprilTag**, con
la oveja recostada e inmóvil. El punto inicial del chupacabras está fuera del
marcador; el final es distinto.

Toda la actuación ocupa **0,583 × 0,666 × 0,256 m** en coordenadas de Unity,
incluida la cola durante el giro. Ambos animales comparten una escala uniforme,
conservando proporciones. No se cambia el AprilTag: usa el mismo impreso y
los PDF anteriores, con 10 cm de tamaño de detección.

Pulsa «Abrir cámara», permite su uso y enfoca el marcador. Al perderlo, ambos
se ocultan y la secuencia se pausa; al recuperarlo continúa. Vuelve a Inicio
y abre la cámara de nuevo para repetir el ataque.

Paquete `com.chupacabras.ar.figure`, Android 8 o posterior, ARM64.
La precisión de las medidas en el entorno depende de la calibración y del
seguimiento de cámara existentes. No se publicó en Google Play.

Fuentes: `../../scenes/ataque_ar_r08.blend` y `../../exports/ataque_ar_r08.fbx`.
Informe y resultados: `../../docs/ataque_natural_1m.md`.
Proyecto Unity: `/home/cacawatin/code/unity/chupacabras/google_play`.
Las candidatas anteriores se conservan, incluida la 0.2.6 con los defectos reportados.

Para comprobar los archivos, ejecuta `sha256sum -c SHA256SUMS` dentro de esta carpeta.
