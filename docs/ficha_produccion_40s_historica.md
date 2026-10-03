> **Archivo histórico del alcance cinematográfico, sustituido el 2 de octubre de 2026.**
> No usar sus próximos pasos o acciones manuales como tareas vigentes. Ver [plan actual](plan_secuencia.md) y [estado](estado.md).

# Ficha de producción — paso 1

Fecha: 23 de septiembre de 2026. Fuente: instrucciones de esta sesión, plan vigente y archivos inspeccionados. Esta ficha no certifica Unity, Android ni seguimiento físico.

## Acuerdos confirmados

- Fuente Blender, animaciones, referencias y exportaciones: `/home/cacawatin/code/blender/chupacabras`.
- Aplicación AR Android: `/home/cacawatin/code/unity/chupacabras`. Proyecto creado allí durante la continuación del paso 2; ver estado para resultados.
- Desarrollo y compilación desde Linux; exclusivamente `/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity`. No cambiar el Editor ni instalaciones globales.
- Corto definitivo de 40 s, con cámaras internas y escena 3D en tiempo real sobre una ventana anclada al marcador. La demo de 35 s conserva su alcance independiente.
- Cronología: pastoreo/acecho 0–15 s; criatura y ojos ocultos 15–20 s; salto iniciado a los 20 s y ataque hasta 25 s; arrastre/salida 25–39 s; campo vacío 39–40 s como margen provisional del plan; reinicio instantáneo a los 40 s.
- Chupacabras original prioritario, cuadrúpedo fibroso, espalda arqueada, hombros marcados, garras, mandíbula articulable, orejas, cola y cresta. Ojos amarillos; mechones geométricos, sin pelo simulado.
- Oveja reutilizada con licencia para modificación y distribución Android, pendiente de selección en el paso 7. La oveja de las demos es un proxy, y la referencia JPG no es un modelo ni una licencia de distribución.
- Paleta nocturna índigo, sombras marcadas, luna geométrica, tierra seca, granero pequeño y una oveja. Violencia mediante actuación y polvo, sin requerir sangre.
- AprilTag es candidato inicial. No añadir ARCore ni sustituir tecnología antes de resolver su prueba. Ocultar y pausar al perder pose; continuar al recuperar. No hay seguimiento persistente fuera de vista.
- Moto G20 para pruebas; posible S23 solo en exposición, pendiente de prueba física propia.

## Referencias organizadas y revisadas

Las cinco copias de `references/` coinciden byte por byte con sus originales en `/home/cacawatin/Pictures/chupacabras/`. Procedencia, tamaño y SHA-256 en [referencias.json](evidencias/2026-09-23_continuidad/referencias.json).

| Archivo | Aplicación al diseño |
| --- | --- |
| `chupacabras1.jpg` | Postura baja, garras largas, hocico agresivo y cresta alta. |
| `chupacabras2.jpg` | Orejas puntiagudas, cara oscura, ojos grandes y hombros fuertes; conservar amarillo acordado. |
| `chupacabras3.jpg` | Espalda arqueada, anatomía fibrosa, cola, cresta y tratamiento gráfico de sombras. |
| `ejemplo_de_oveja.jpg` | Lana clara facetada, cabeza y patas oscuras; orientar búsqueda de un recurso existente. |
| `ejemplo_de_escenario.jpg` | Noche azul, luna, refugio rural y bosque en silueta; adaptar a tierra seca y una oveja. |

Se conservan como referencias visuales. No se ha comprobado una licencia para redistribuir estas imágenes dentro de la APK; no confundirlas con los recursos de producción autorizados.

## Decisiones confirmadas — M#[1] resuelta

El usuario respondió explícitamente: «Izquierda y giro a la derecha; ocultamiento hasta 25 s; ambiente y efectos sin música». Subpaso 1.3 completado; cierre 1.4 registrado.

| Decisión | Acuerdo |
| --- | --- |
| Trayectoria | Arrastre inicial a la izquierda, giro amplio y salida por la derecha; el paso 5 fijará coordenadas y encuadres. |
| Ocultamiento | Desde el aterrizaje hasta los 25 s, conservando salto a los 20 s y duración total de 40 s. |
| Audio | Ambiente y efectos de pastoreo, balidos, impacto, pasos y arrastre; sin música. |

Orientación de pantalla, dimensiones físicas del marcador y parámetros de cámara siguen pendientes para la preparación técnica y validación del stand; no se solicitan ahora. No hay nueva pregunta sobre dispositivo, presentación o versión de Unity.

## Requisitos técnicos por comprobar

Se revisó [evaluacion_ar_moto_g20.md](evaluacion_ar_moto_g20.md); su evaluación documental previa no acredita ejecución real. Antes de adoptar AprilTag:

1. Abrir/crear el proyecto con 6000.3.22f1, fijar URP y revisión del candidato, comprobar manifest/bloqueo y carga nativa Linux.
2. Verificar SDK/NDK/JDK y compilar APK mínima desde Linux con el detector. Su ubicación física se observó, pero su funcionamiento no se ha probado.
3. Preparar APK, marcador con familia/ID/medidas e instrucciones antes de pedir el teléfono. Consultar las ABIs reales por ADB antes de cerrar arquitectura.
4. Probar cámara trasera, orientación/reflejo, proyección/intrínsecos, pose y escala con la impresión medida; pérdida/recuperación y costo de RenderTexture en el G20.
5. Registrar resultados físicos y decidir viabilidad. Mantener S23 pendiente hasta disponer de él.

Continuación: dependencias revisadas e integradas en el paso 2. La carga Linux, detección sintética y compilación Android pasaron; la aceptación física y ABI siguen pendientes en `estado.md`.
