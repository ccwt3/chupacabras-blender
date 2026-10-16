# Chupacabras AR 0.2.5 / 205

- `Chupacabras_AR_0.2.5_205.aab`: Android App Bundle firmado con la clave de subida existente.
- `Chupacabras_AR_0.2.5_205_desde_AAB.apk`: APK universal generado con bundletool desde ese AAB y firmado con la misma clave.
- `SHA256SUMS`: comprobación de integridad de ambos paquetes.

Ambos personajes son geometría 3D en tiempo real sobre el AprilTag existente.
Ataque único de seis segundos; oveja recostada inmóvil y chupacabras respirando.
Perder el marcador oculta y pausa la escena; recuperarlo continúa. Para repetir,
volver a Inicio y Abrir cámara de nuevo.

Fuentes Blender: `scenes/ataque_ar_r02.blend`, `exports/ataque_ar_r02.fbx`.
Proyecto Unity: `/home/cacawatin/code/unity/chupacabras/google_play`.
Escena: `Assets/Scenes/AtaqueAR_r02.unity`. Usar Unity 6000.3.22f1.

Build sin errores ni advertencias; firma, versión, ARM64, AAB y alineación de
16 KB comprobadas. Prueba física en Moto G20: secuencia y recuperación del marcador confirmadas;
29,638 fps durante aproximadamente cinco minutos, sin excepciones. Consultar
`docs/ataque_ar.md` del proyecto Blender. Otros móviles y ejecución con páginas
de 16 KB no probados. No se ha publicado en Google Play.
