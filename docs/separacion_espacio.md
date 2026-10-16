# Separación para liberar espacio — 8 de octubre de 2026

Se revisaron de nuevo las dependencias con Unity **6000.3.22f1**, mediante el
verificador existente y `AssetDatabase.GetDependencies`, y se contrastaron con
el informe de recursos empaquetados de la APK final del 6 de octubre. Después
del traslado, las dependencias de la escena son exactamente las mismas.

Se han movido archivos, no eliminado: **el traslado no libera espacio por sí solo**.
Las dos carpetas `historicos/` contienen aproximadamente **2,56 GB** de archivos
agrupados para su eliminación manual. GB en este informe significa 1.000.000.000 bytes.

## Qué permanece activo

- Un personaje, con dos versiones necesarias: **R08 para la malla y R02 para la
  respiración**. Blender conserva dos `.blend`, dos `.fbx`, sus mapas y manifiestos.
  Las copias de `../chupacabras_models/vigentes/` también permanecen intactas.
- `scenes/F2_chupacabras_forma_r04.blend` se conserva por acuerdo del usuario:
  es fuente de generación de Nocturno, aunque no aparece en la app.
- Unity conserva **dos FBX y una escena**, `Assets/Scenes/F4_FiguraAR_r02.unity`.
  El prefab usa la malla R08 y un controlador/clip R02 independiente; el segundo
  FBX es fuente de ese clip. Se conservan ambos conjuntos de autoría/configuración,
  incluido el clip original R08 como soporte del configurador, aunque ese clip
  antiguo no sea el que reproduce la escena final.
- Se conservan código compartido, paquetes, recursos URP, marcador, licencias,
  fixtures y ajustes necesarios. No se clasifica como prescindible una clase C#
  solo por tener un nombre histórico: varias siguen siendo dependencias del código.
- La única APK en `unity/chupacabras/builds/android/` es
  `F6_figure_20261006_181916.apk`, con su informe y los símbolos Burst de Figura AR.

APK final: **55.348.110 bytes**, versión 0.2.2 / 202, SHA-256
`7db6358cdb13c37467a3d42f76d163ef8359c0ef25583441065ed5b869863aae`.

## Histórico separado

| Carpeta | Contenido | Bytes de archivos |
| --- | --- | ---: |
| `blender/chupacabras/historicos/` | 131 modelos ya archivados, más texturas, JSON, previews y recursos de oveja históricos | 1.475.370.357 |
| `unity/chupacabras/historicos/Assets/` y `historicos/builds/` | 44 FBX históricos con materiales/texturas/prefabs y `.meta`, 40 escenas anteriores, 17 APK anteriores y archivos asociados | 1.086.191.805 |
| Total | Histórico agrupado en ambos proyectos | 2.561.562.162 |

Unity deja de importar los recursos que están fuera de `Assets/`. Se conservaron
los `.meta` junto con los archivos archivados para permitir restaurar sus GUID.
El directorio de recursos activos pasa aproximadamente de **416 MiB a 20 MiB**;
el de builds, de **695 MiB a 53 MiB**. Esto reduce el conjunto activo, pero los
archivos aún ocupan disco dentro del histórico.

Los archivos nuevos de `historicos/` se excluyen de Git en ambos proyectos para
evitar añadir otra vez APK, renders y copias que el usuario quiere retirar.
Los archivos previamente versionados aparecerán eliminados de sus rutas originales
en el diff: el inventario registra sus destinos locales. No se hizo commit ni push.

## Compilación y restauración

El valor predeterminado de `build_figure.sh`, `FigureBuild.Stage` y el verificador
de APK pasa de F1 a **F6**. La lista de escenas de `EditorBuildSettings` apunta a
la escena final. Se evita así intentar construir F1 después de archivar sus recursos.
La forma de construir la app final es `bash scripts/build_figure.sh` desde Unity;
el comando explícito `CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh` sigue válido.

Las demos y los generadores de entregas antiguas requieren restaurar sus recursos
desde `historicos/` a las rutas registradas, junto con los `.meta` de Unity y sin
sobrescribir archivos existentes. No se modificaron sus scripts ni sus informes
históricos. Los documentos antiguos pueden mencionar rutas ya archivadas.

Inventarios de movimiento, con tamaño y SHA-256 por archivo:

- [Modelos Blender, primer traslado](archivo_modelos_historicos.json).
- [Recursos Blender, segundo traslado](separacion_espacio_20261008.json).
- [Importaciones y builds Unity](/home/cacawatin/code/unity/chupacabras/docs/separacion_espacio_20261008.json).

## Otros usos de espacio que se conservan

- **Unity `Library/`: aproximadamente 7,3 GiB de caché** (destacan `Bee/`,
  `PackageCache/`, `Artifacts/` y Gradle). Es regenerable y está separada por su
  propia ubicación. Si se retira con Unity cerrado, la siguiente apertura/build
  tendrá que reimportar/recompilar y puede necesitar descargar paquetes. No se
  movió ni borró en esta operación; no confundirla con `Packages/`, que sí es fuente.
- **Entrega F7: unos 1,1 GiB** entre carpeta completa y `.tar.gz`. Son dos formatos
  del respaldo final; contienen también copias históricas. Se conserva su integridad
  en vez de extraer archivos de una entrega con manifiestos y hashes ya publicados.
- Los repositorios `.git` y sus objetos LFS, evidencias y documentación se conservan.
  Borrar el histórico local no purga los objetos guardados en Git/LFS.

## Verificación después de mover

Pasaron los 32 checks de seguimiento, las comprobaciones de figura/malla/materiales/
respiración y los diez estados de reproducción sintética de Unity. La escena y
sus dependencias mantienen sus hashes; solo cambian selección de escena/defaults
y documentación, además de los traslados. La APK final conserva su hash y pasa
verificación de firma, versión, arquitectura y alineación mediante el verificador
existente. R08 y R02 vuelven a pasar `verificar_nocturno.py`; F2 reabre y conserva
su objeto fuente sin bibliotecas ni imágenes externas faltantes.

También se revisaron hashes de todos los archivos trasladados, `bash -n` y
`git diff --check`. No hay linter configurado. Evidencias nuevas en
`unity/chupacabras/docs/evidencias/separacion_20261008/` y
`docs/evidencias/separacion_20261008/` de Blender.

No se generó otra APK ni se repitió una prueba física en teléfono. La APK validada
en G20 permanece intacta; las nuevas comprobaciones de ejecución son del Editor.
