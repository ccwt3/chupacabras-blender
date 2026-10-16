# Archivo de modelos históricos — 8 de octubre de 2026

Actualización posterior: se agruparon también texturas, datos y previews históricos,
y se separaron importaciones/builds en Unity. El [informe de espacio](separacion_espacio.md)
describe el estado actual; las limitaciones de rutas y el proyecto Unity intacto
mencionados debajo corresponden al primer traslado de modelos.

Se trasladaron **131 archivos** de modelos de trabajo a `../historicos/`:
**66 `.blend` y 65 `.fbx`**, 277.948.719 bytes en total. Son archivos, no 131
personajes distintos: incluyen revisiones, escenas, fuentes y exportaciones.
El traslado fue solicitado para que el usuario pueda eliminarlos manualmente.
No se ha eliminado ningún archivo.

## Vigentes y fuente necesaria

La aplicación final usa dos versiones del mismo personaje: la malla Nocturno R08
y la respiración R02. Se mantienen sus **cuatro archivos**, dos `.blend` y dos
`.fbx`, en `scenes/` y `exports/`, además de las copias ya verificadas en
`../../chupacabras_models/vigentes/`.

Se conserva también `scenes/F2_chupacabras_forma_r04.blend`, por decisión expresa
del usuario. Aunque no aparece en la app, `scripts/chupacabras_nocturno.py`, función
`geometry`, la abre para generar Nocturno R08. Por eso se reclasificó como fuente
necesaria: el recuento inicial de 132 archivos fuera de la app se divide en
**131 archivados y una fuente de generación conservada**.

Después del traslado quedan cinco archivos de modelos en las carpetas de trabajo:
tres `.blend` y dos `.fbx`. Texturas, scripts, manifiestos, previews y licencias
conservan sus ubicaciones.

## Rutas y efectos

Se mantiene la estructura de origen dentro del archivo:

```text
historicos/scenes/...
historicos/exports/...
historicos/assets/oveja/original/Farm Animals by @Quaternius/...
```

El [inventario de movimientos](archivo_modelos_historicos.json) registra origen,
destino, tamaño y SHA-256 de cada archivo. Queda fuera de `historicos/` para que
la lista sobreviva si el usuario elimina esa carpeta. Para deshacer un movimiento,
devolver el archivo desde `destino` a `origen`, sin sobrescribir archivos existentes.

Los scripts, documentos y demos históricos conservan referencias a las rutas
antiguas. Para utilizarlos habrá que restaurar los modelos correspondientes.
Al mover solo modelos, algunas rutas relativas de texturas de esos `.blend`
históricos también pueden dejar de resolver; no se presenta esta carpeta como
un paquete de escenas históricas listo para abrir. Borrarla elimina esas fuentes
de trabajo históricas; no afecta a las referencias de la aplicación vigente.

El proyecto `/home/cacawatin/code/unity/chupacabras` conserva sus recursos:
46 FBX, dos vinculados a la entrega vigente y 44 fuera de esa escena. No se movió
ningún recurso de Unity ni se cambiaron GUID, materiales o controladores.

La entrega `entregas/F7_Nocturno_R08_20261006/` conserva sus 51 archivos `.blend`
y `.fbx`, incluidas 45 copias históricas y seis copias de archivos vigentes entre
sus fuentes Blender y Unity. Se preservan el paquete completo, su inventario y
el comprimido. No se han extraído ni modificado modelos dentro de entregas.
Por tanto, `historicos/` reúne los modelos históricos de trabajo, no todas las
copias históricas existentes en respaldos o en el proyecto Unity.

## Comprobaciones

Cada archivo se cotejó contra el inventario anterior antes de moverlo y contra
su SHA-256 después. Se comprobó que los 131 destinos existen y que sus rutas de
origen quedaron vacías. Los cuatro archivos vigentes y la fuente F2 permanecen
en sus rutas, con el mismo contenido. El inventario permite comprobar también
que los 136 archivos originales están presentes en su ubicación correspondiente.

Se repitió el verificador existente `scripts/verificar_nocturno.py` para R08 y
R02 tras el traslado, usando directorios temporales para no sobrescribir las
evidencias anteriores. Ambas revisiones pasan las comprobaciones de malla,
texturas, rig, respiración y correspondencia FBX. `git diff --check` correcto.
No hay linter configurado para este traslado; no se recompiló Unity ni se repitió
la prueba física. Las demos históricas no se ejecutaron porque sus fuentes se
archivaron expresamente.
