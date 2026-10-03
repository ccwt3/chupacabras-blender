# Ficha vigente: figura realista del chupacabras

Actualizada el 2 de octubre de 2026 por el cambio de alcance solicitado.
[Plan y aceptación](plan_secuencia.md) · [Continuidad](estado.md).
La [ficha cinematográfica anterior](ficha_produccion_40s_historica.md) es histórica.

## Experiencia de entrega

Al reconocer el marcador AprilTag existente, mostrar una sola figura 3D del
chupacabras, centrada sobre él. El visitante mueve el teléfono para inspeccionar
la criatura. Figura estática como base, sin ventana, oveja, ataque, arrastre,
escenario ni duración narrativa. No se añaden animaciones o interacción en
esta replanificación. Las demos anteriores permanecen disponibles por separado.

## Dirección visual

Realismo mediante anatomía, pose, superficie e iluminación coherentes, no solo
mayor cantidad de polígonos. Conservar la identidad original demacrada: espalda
arqueada, costillas, extremidades angulosas, cresta, cola y ojos amarillos.
Partir de `scenes/09_chupacabras_demacrado_r02.blend`; el rig de
`scenes/11_rigs_contacto_demacrado_r01.blend` puede servir para autoría de pose.
No adoptar de nuevo la versión fornida ni usar un encuadre para ocultar defectos.

Pose tensa y asimétrica con apoyos creíbles. Revisar rostro, uniones anatómicas,
garras, cola y cresta desde seis vistas y de cerca. Acabado de piel, normales y
rugosidad con materiales compatibles con URP; los colores planos y la noche
índigo del corto dejan de ser restricciones. El detalle y las sombras deben
justificarse en pantalla y medirse en G20. No se promete fotorrealismo antes de
producir y evaluar una candidata.

Las tres imágenes `references/chupacabras1.jpg`, `chupacabras2.jpg` y
`chupacabras3.jpg` siguen orientando identidad y proporciones. Su procedencia
está en [el registro de referencias](evidencias/2026-09-23_continuidad/referencias.json).
Las referencias de oveja/escenario se conservan como historia. No hay licencia
comprobada para distribuir las imágenes de referencia dentro de la aplicación;
registrar autoría/licencia de cualquier textura o recurso nuevo.

## Condiciones técnicas

- Fuente Blender en `/home/cacawatin/code/blender/chupacabras`;
  aplicación en `/home/cacawatin/code/unity/chupacabras`.
- Android desde Linux, exclusivamente Unity **6000.3.22f1** instalado.
- Reutilizar URP, cámara, AprilTag y marcador medido actuales; no añadir ARCore.
- Mostrar con pose válida; ocultar al perderla o detenerse la cámara; recuperar
  sin duplicación. No hay reloj del corto ni seguimiento fuera de vista.
- Moto G20 valida la candidata; S23 sigue pendiente hasta probarlo.
- No modificar ni borrar entregas anteriores; crear fuentes y escenas nuevas.

## Revisión y aceptación

F2 revisa forma y pose antes del detalle; F3–F4 comprueban superficie y aspecto
en Unity; F5–F6 validan calidad visual y rendimiento reales. Una exportación
correcta o un test geométrico no constituyen aprobación estética. Documentar
objeciones del usuario y resolverlas. Las medidas del modelo actual son una
referencia inicial, no un presupuesto móvil aprobado.

El antiguo guion, audio y recorrido resueltos en M#[1] quedan fuera de alcance.
M#[6] no se aprueba: su revisión de figura con panel se sustituye por M#[7],
prueba futura de esta figura en G20. No se solicita una prueba física ahora.
