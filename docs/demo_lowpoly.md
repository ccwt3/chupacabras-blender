# Demo visual lowpoly

## Alcance

Borrador estático solicitado para evaluar la idea con poco trabajo: granero de tablas, tierra y hierba geométrica, luna, oveja pastando y chupacabras visible en actitud de acecho. La criatura se muestra más iluminada que en el acecho del guion para poder juzgar su silueta.

El chupacabras se construyó con geometría simple: tórax encorvado, patas angulosas, mandíbula, orejas, cola, espinas y ojos amarillos. Es una primera interpretación de las referencias, sin rig ni acabado final. La oveja es un volumen provisional de composición; no reemplaza la decisión de reutilizar un modelo existente en producción.

Esta demo estática no ejecuta los 24 pasos del plan y no incluye animación, Unity ni AR. Sirve para revisar proporciones, paleta y distribución antes de invertir en la secuencia definitiva. Se creó posteriormente una [versión animada de 35 segundos](demo_animada.md) en otro archivo, conservando esta escena original.

## Archivos

- `scenes/demo_lowpoly.blend`: escena editable, objetos agrupados por función.
- `previews/demo_lowpoly.png`: vista general, 1200 × 900.
- `scripts/demo_lowpoly.py`: generador reproducible, con semilla fija y nombres de salida alternativos si existen entregas previas.

Para regenerar desde la carpeta del proyecto:

```bash
blender -b -t 6 --python-exit-code 1 --python scripts/demo_lowpoly.py
```

El script crea una escena nueva y no modifica escenas existentes. Materiales de colores sólidos, geometría facetada y render Cycles de 32 muestras para mantener bajo el costo del borrador.

## Verificación

Verificado con Blender 5.2.2 LTS: el generador terminó correctamente, guardó el `.blend` y renderizó el PNG. Se reabrió el archivo en un proceso independiente y se comprobaron cámara activa, 328 objetos y resolución 1200 × 900. La inspección visual confirmó que se distinguen granero, oveja, criatura con cresta y ojo luminoso, vegetación y luna.

No hay suite de tests ni linter configurados en este proyecto. Blender emitió avisos de futura retirada de `use_nodes` en Blender 6.0; no impidieron generar ni reabrir la demo.
