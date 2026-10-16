# Chupacabras AR — 0.2.8 / 208

Escena 3D de chupacabras y oveja: pastoreo, salto A → B, mordida y forcejeo
sin sangre, regreso caminando y reposo sobre el AprilTag. Misma actuación R08
aceptada, ampliada uniformemente ×1,375, incluidos los modelos y el recorrido.

- Envolvente animada: **80,18 × 91,57 × 35,14 cm** (ancho, largo, altura).
- Separación libre inicial: **41,25 cm**; AprilTag sin cambios, 10 cm.
- Al perder el marcador se oculta la escena; al recuperarlo se reinicia desde
  el pastoreo, incluso después del reposo final. Volver de segundo plano o
  de Inicio también reinicia.
- AAB firmado; la APK universal incluida procede de ese AAB mediante bundletool.
- Android mínimo 8.0 / API 26, ARM64, target API 36. No se publicó en Google Play.

Abre la aplicación, pulsa «Abrir cámara», concede el permiso y enfoca el mismo
AprilTag. Aléjate lo necesario para ver toda la escena. Para repetirla, tapa
el marcador hasta que desaparezcan ambos animales y vuelve a mostrarlo.
La instalación limpia requiere conceder de nuevo el permiso de cámara.

El vídeo muestra la misma animación con materiales neutros de Blender; no
sirve como regla de tamaño físico. La aplicación conserva sus materiales PBR.
Fuente: ../../scenes/ataque_ar_r08.blend. La escala ampliada se aplica en Unity,
en Assets/Scenes/AtaqueAR_r09.unity, copia independiente google_play.

Probada y aceptada en Moto G20: «todo bien 10/10». Perfil de 180,70 s a
29,33 fps de media; mediana 33,32 ms y p95 33,61 ms. Cámara recuperada al volver
de segundo plano. Reinstalación final limpia del mismo APK, verificada por hash.

Informe y pruebas: ../../docs/ataque_natural_1m.md.
La equivalencia exacta entre metros virtuales y físicos depende de la
calibración y seguimiento existentes; no se midió con cinta. Moto G20 usa
páginas de 4 KB: no se acredita ejecución en un dispositivo de 16 KB.
