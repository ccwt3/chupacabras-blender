# Estado de continuidad

Actualizado: **3 de octubre de 2026 — revisión física del personaje incluida en F7**.
[Rediseño y respiración](rediseno_nocturno.md) · [Prueba anterior F5/F6](figura_ar_f5_f6.md).

**F7 continúa pendiente.** El usuario amplió expresamente el alcance: mejorar
apariencia y animación, tomando principalmente su segunda referencia, e implementar
el reemplazo del personaje en la aplicación sin cambiar su funcionamiento.
La nueva fuente es `scenes/chupacabras_nocturno_r08.blend`: 110.294 triángulos,
un material PBR 2K y respiración de cuatro segundos. El prefab conserva su ubicación
`Assets/FiguraAR/F4_r02/Figure.prefab`. Detalles y validaciones en el informe enlazado.
APK del personaje nuevo: `builds/android/F6_figure_20261003_222832.apk` en Unity,
55.348.110 bytes; verificación de Editor y paquete correcta.
La validación física anterior corresponde a F3; el rendimiento del nuevo personaje
todavía no se ha medido en un dispositivo. No se retoma el corto ni la oveja.

## Punto exacto de retoma

**Acuerdo posterior al rediseño:** la revisión visual y de rendimiento del nuevo
personaje forma parte del inicio de **F7**, seguida de la entrega y cierre.
No se abre otra etapa ni se reinician F5/F6. [Alcance de F7](plan_secuencia.md#f7-revisión-final-entrega-y-cierre).

1. Verificar la candidata Nocturno R08 identificada arriba e instalarla en el
   Moto G20 para la prueba. Reutilizar el marcador impreso existente.
2. Revisar apariencia desde varios ángulos, texturas, escala, respiración sin
   saltos y patas apoyadas. Medir unos cinco minutos con cámara, detector y
   personaje activos: fps/tiempos de cuadro, memoria y temperatura disponibles.
   Objetivo de referencia: 30 fps sostenidos; registrar resultados reales y límites.
3. Comprobar pérdida/recuperación del marcador y segundo plano/reanudación.
   Corregir solo defectos observados del personaje; conservar el funcionamiento
   de la app y repetir únicamente las verificaciones afectadas. Si cambia la
   candidata, la medición que acredita la entrega debe corresponder a la final.
4. Si cumple como demo funcional, completar F7: APK identificada por versión/hash,
   fuentes y recursos necesarios, marcador, guía breve e inventario de entrega;
   actualizar continuidad con el cierre y retirar solo lo instalado para pruebas,
   respetando cualquier instalación o datos previos.

Esta anotación no ejecuta ni aprueba la prueba pendiente. Si falta el G20,
preparar lo independiente y solicitar únicamente la intervención física necesaria;
no marcar F7 completo sin la prueba real. S23 queda pendiente si no está disponible
y no bloquea el cierre de la demo validada en G20. No ampliar el acabado por gusto,
añadir funcionalidades, retomar el corto ni crear una fase nueva.

## Resultado previo F5/F6, con el personaje F3

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

## Entrega anterior preservada

Blender conserva `scenes/F3_chupacabras_superficie_r05.blend` y su FBX/mapas:
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

F7 incluirá la revisión física de Nocturno R08 y la entrega reproducible con guía breve.
No ampliar a producto comercial ni tomar estas pruebas como validación en S23,
calibración exacta o garantía de funcionamiento durante horas. No crear `next-job`.
