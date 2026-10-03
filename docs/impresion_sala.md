# Reimpresión del marcador en sala — 3 de octubre de 2026

El usuario solicitó otra copia para pruebas posteriores. CUPS identifica
**Brother_DCP-T530DW** con ubicación **sala**; la T510W indica «chuzo».
Se reutilizó el PDF carta existente, sin modificarlo:

`/home/cacawatin/code/unity/chupacabras/marker/03_marker_carta.pdf`

SHA-256: `c670fc855c002dea0ad70c458db525b36dfcfff6e14400347bd0c7d1a47f1a83`.
Una página carta, 612 × 792 puntos; AprilTag tagStandard41h12 ID 0,
100 mm de detección y 180 mm de dibujo. No es un QR convencional.

Se envió **una sola copia**, trabajo **Brother_DCP-T530DW-47**, con Letter,
escala 100, `print-scaling=none`, `fit-to-page=false`, una cara y ColorModel Gray.
No se cambiaron preferencias globales de impresora.

**M#[10] resuelta por confirmación del servidor de impresión.** Primero la
impresora informó falta de papel; se pidió colocar carta. La consulta posterior
registró `completed`, `job-completed-successfully`, **una impresión y una hoja
completadas**. La impresora volvió a disponible, sin alertas. No fue necesario
reenviar ni cancelar el trabajo. No se infiere quién repuso el papel ni se
atribuye una respuesta manual no recibida.

La medida física de esta nueva copia no se ha comprobado; su terminación no
valida seguimiento, escala de la app o rendimiento. M#[7] sigue futura.

Consulta reproducible:

```bash
ipptool -tv ipp://localhost/jobs/47 docs/evidencias/2026-10-03_impresion_sala/consulta.test
lpstat -l -p Brother_DCP-T530DW
```

[Estado inicial](evidencias/2026-10-03_impresion_sala/job47.txt),
[confirmación de terminación](evidencias/2026-10-03_impresion_sala/job47_completado.txt)
y [impresora sin alertas](evidencias/2026-10-03_impresion_sala/impresora_final.txt).
No se modificaron modelo, PDF, escenas, aplicación ni configuración global.
La próxima pareja digital sigue siendo F3–F4, no iniciada aquí.
