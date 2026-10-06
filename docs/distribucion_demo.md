# Distribución y uso de la demo F7

6 de octubre de 2026. F7 cerrada como demo funcional en G20. No requiere una
nueva fase: el siguiente paso práctico es instalar la candidata final en el
teléfono de exposición y usar el marcador existente. S23 sigue sin prueba física.

## Archivos y tamaños

- APK de uso, en Unity: `builds/android/F6_figure_20261006_181916.apk`.
  55.348.110 bytes = 55,35 MB decimales (52,78 MiB), versión 0.2.2 / 202.
  SHA-256: `7db6358cdb13c37467a3d42f76d163ef8359c0ef25583441065ed5b869863aae`.
- Marcador: `marker/03_marker_carta.pdf` de Unity. Reutilizar la impresión.
- Respaldo/entrega técnica: `entregas/F7_Nocturno_R08_20261006.tar.gz` de Blender.
  425.689.553 bytes = 425,69 MB (405,97 MiB). Incluye fuentes, recursos,
  licencias, evidencias y guía. No hace falta enviarlo al público para usar la app.
- Visualización sin instalar: `previews/chupacabras_nocturno_r08_respira_r02/respiracion.mp4`.
  Es un video de estudio de cuatro segundos, no AR interactiva.
- Fuente editable: `scenes/chupacabras_nocturno_r08_respira_r02.blend`.
  Verificada con Blender 5.2.2 LTS. Proyecto AR: Unity 6000.3.22f1,
  escena `Assets/Scenes/F4_FiguraAR_r02.unity`.

MB usa 1.000.000 bytes; MiB usa 1.048.576. El tamaño de descarga no es el espacio
instalado. El espacio total tras instalar no se midió; reservar 500 MB libres
es un margen práctico, no un mínimo demostrado. La entrega técnica contiene
aproximadamente 727 MB de archivos sin comprimir, más sobrecarga del sistema
de archivos; las cachés de Unity se generan aparte y ocupan varios GB.

## Distribuir e instalar

Para una demostración, compartir la APK final, el PDF del marcador y sus avisos
AprilTag (`docs/licenses/` en Unity) mediante USB o enlace de descarga.
No se ha publicado ni subido ningún archivo a un servicio externo.

1. Copiar/descargar la APK en el Android de destino y abrirla desde Archivos.
2. Si Android lo solicita, autorizar a ese gestor o navegador a instalar apps
   desconocidas; seguir los requisitos que muestre ese dispositivo.
3. Instalar, abrir Chupacabras — Figura AR y conceder permiso de cámara.
4. Enfocar el AprilTag impreso, con sus esquinas visibles e iluminación suficiente.
   Mover el teléfono para observar la figura; el tórax respira en ciclos de 4 s.
5. Al retirar el marcador, la figura se oculta. Al recuperarlo o reanudar la app,
   vuelve a aparecer. No hay anclaje persistente sin marcador.

Si se necesita imprimir otra copia: carta al 100 %, sin ajustar a página;
comprobar la regla de 100 mm. Dibujo total de 180 mm, tagStandard41h12 ID 0.
No es un QR para abrir la app. Un QR de un enlace de descarga sería independiente.

Android documenta la distribución directa por enlace y la autorización de
instalación por origen. Los requisitos adicionales dependen del dispositivo y
de las políticas de verificación que le apliquen (Android Developers, 2026;
Google, s. f.). La APK actual es una build de desarrollo aceptada para la demo;
no se preparó una publicación de tienda ni una distribución comercial.

## Requisitos y límites comprobados

La APK declara Android **8.0 / API 26 o superior**, ABI **arm64-v8a** y
**OpenGL ES 3.0**. El teléfono debe ejecutar apps ARM64, tener cámara trasera
funcional y permitir su uso. Son requisitos técnicos del paquete, no una
certificación de todos los dispositivos que los cumplan.

Prueba física: Moto G20, Android 11/API 30. ARCore no se utiliza; el seguimiento
usa AprilTag y cámara. Los modelos y texturas están incluidos en la APK.
No hay entrega iOS o de navegador.

No se estableció un mínimo de RAM total ni de CPU/GPU por modelo. El proceso
consumió aproximadamente **386–401 MiB de PSS** en el perfil final, además de
la memoria que necesitan Android y las demás aplicaciones. Ese consumo no
equivale a un requisito de teléfono con 400 MB de RAM.

Resultado final: **28,53 fps durante 310 s**, p95 de cuadro 49,98 ms,
máximo 83,30 ms; figura visible en 2530/2530 muestras. El detector trabajó
a 15,01 Hz, que no son los fps visuales. El usuario aceptó el resultado como
demo; **no alcanza 30 fps sostenidos**. No acredita uso durante horas,
calibración métrica exacta, ejecución con páginas de 16 KB ni funcionamiento
en S23. La app de pruebas fue retirada del G20 al cerrar la sesión.

## Registro en Git

Por solicitud posterior al cierre se preparan commits locales en Blender y
Unity, incorporando Nocturno R08, respiración R02, pruebas y documentación.
Los archivos de entrega y copias duplicadas de datos del teléfono/compilación
se conservan en disco y se excluyen de Git para evitar versionar otros 1,6 GB
de copias. Fuentes, recursos, perfiles, capturas y resultados se conservan en
el repositorio. Se mantienen los filtros Git LFS ya existentes de Blender;
un clon de ese repositorio necesita descargar también sus objetos LFS.

La entrega comprimida previamente verificada y su APK permanecen intactas;
esta guía y la anotación de los commits son documentación posterior al paquete.
No se recompila la aplicación ni se repite el perfil por un cambio documental.
Los informes de F7 que dicen «sin commit/push» describen aquella sesión anterior.
No se solicita ni ejecuta push en esta sesión.

## Referencias

Android Developers. (2026, 26 de febrero). *Alternative distribution options*.
https://developer.android.com/distribute/marketing-tools/alternative-distribution

Google. (s. f.). *Allow app installs from unverified developers*. Android Help.
https://support.google.com/android/answer/17588095
