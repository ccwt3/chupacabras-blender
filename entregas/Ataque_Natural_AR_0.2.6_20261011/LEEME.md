**CANDIDATA SUPERADA:** en la prueba física se observó estiramiento del cuello.
El usuario pidió corregir el agachado y añadir 30 cm de separación inicial.
Esta carpeta conserva la prueba 0.2.6; no es la entrega final de esa corrección.

# Chupacabras AR 0.2.6 / 206 — actuación R05

- `Chupacabras_AR_0.2.6_206.aab`: Android App Bundle firmado.
- `Chupacabras_AR_0.2.6_206_desde_AAB.apk`: APK universal generado de ese AAB y firmado con la misma clave de carga.
- `Vista_animacion_R05.mp4`: revisión de movimiento desde Blender, con materiales neutros. La APK utiliza las texturas de la aplicación.

La oveja pasta; el chupacabras anticipa, salta, muerde y la derriba. Tras el
forcejeo sin sangre, gira y regresa caminando a la posición original. A los
13,5 segundos queda respirando, con la oveja recostada e inmóvil.

Toda la animación ocupa **0,90 × 0,833 × 0,416 m** en Unity, incluida la cola y
el desplazamiento. Escala uniforme para conservar proporciones. No se cambia
el AprilTag: usa el mismo marcador físico y los PDF anteriores.

Pulsa «Abrir cámara», concede permiso y enfoca el marcador. Aléjate lo
necesario para encuadrar toda la escena. Al perder el marcador ambos se
ocultan y la secuencia se pausa; al recuperarlo continúa. Vuelve a Inicio
y abre la cámara de nuevo para repetir el ataque.

Paquete `com.chupacabras.ar.figure`, Android 8 o posterior, ARM64.
La correspondencia exacta de la medida virtual con el entorno depende de la
calibración y del seguimiento de cámara existentes. No se cambió esa calibración.
No se publicó en Google Play.

Fuentes: `../../scenes/ataque_ar_r05.blend`, `../../exports/ataque_ar_r05.fbx`.
Informe y resultados de prueba: `../../docs/ataque_natural_1m.md`.
Proyecto Unity: `/home/cacawatin/code/unity/chupacabras/google_play`.

Para verificar los archivos, ejecuta `sha256sum -c SHA256SUMS` dentro de esta carpeta.
