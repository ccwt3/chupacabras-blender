# Síntesis del proyecto Chupacabras AR

Se creó `output/pdf/chupacabras_ar.pdf`, con fuente editable en
`output/pdf/chupacabras_ar.tex`, para explicar funcionalidades, tecnologías,
librerías, procesos de intercambio y empaquetado, y estado de la entrega 0.2.8.

El historial se limita a las dos fases solicitadas: modelo Nocturno con
respiración sobre el AprilTag, seguido de incorporación de oveja y ataque.
La redacción prioriza prosa, reduce los rótulos y enlaza las dependencias y la
fuente oficial de la oveja al mencionarlas. Incluye referencias en formato APA.

Las versiones y mediciones se contrastaron con documentación local, manifiestos
y fuentes Unity. El PDF tiene tres páginas; se revisaron las páginas renderizadas,
la extracción de texto, los enlaces y la ausencia de advertencias de composición.
La preparación de este documento no modifica modelos, escenas
ni aplicación, ni constituye una nueva prueba móvil.

Para compilar desde la raíz, con XeLaTeX y las fuentes Noto Serif/Noto Sans:

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/chupacabras-ar-pdf output/pdf/chupacabras_ar.tex
```

Crear primero el directorio temporal. Copiar el PDF resultante a `output/pdf/`.
La fuente no necesita imágenes ni otros recursos externos para compilar.
