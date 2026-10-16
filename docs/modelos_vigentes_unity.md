# Modelos vigentes de Unity — revisión del 8 de octubre de 2026

La demo final usa la malla **Nocturno R08** y el clip de respiración **R02**.
Se separan sus fuentes en `/home/cacawatin/code/blender/chupacabras_models/vigentes/`
mediante copias, conservando originales, históricos, entregas y rutas de trabajo.
Esta carpeta es una selección verificada a esta fecha; no se sincroniza automáticamente
con los proyectos Blender o Unity ni sustituye el proyecto Unity completo.

**Actualización posterior del 8 de octubre:** por solicitud del usuario se movieron
131 archivos históricos de trabajo a `historicos/`. Se conservó F2 R04 al comprobar
que el generador Nocturno depende de ella y confirmar el usuario su conservación.
Los inventarios y las afirmaciones de preservación de rutas que siguen describen
la revisión inicial, anterior a ese traslado. El estado y las rutas actuales están
en [archivo de históricos](modelos_historicos.md) y su inventario de movimientos.
La [segunda revisión para liberar espacio](separacion_espacio.md) también archiva
importaciones/builds de Unity y cambia su selección predeterminada a F6; prevalece
sobre las observaciones iniciales de configuración que siguen.

## Estado de la aplicación

Proyecto revisado: `/home/cacawatin/code/unity/chupacabras`, Unity 6000.3.22f1,
commit `e7045e3`, limpio al comenzar. Blender: commit `c7e10db`, también limpio.
La documentación registra F1–F7 completadas como demo en Moto G20: 28,532 fps
durante 310 s; no se acreditan 30 fps sostenidos. S23 sigue pendiente.
Son resultados de la prueba del 6 de octubre, no una nueva prueba física.

La APK `builds/android/F6_figure_20261006_181916.apk` existe y su SHA-256 se
recalculó: `7db6358cdb13c37467a3d42f76d163ef8359c0ef25583441065ed5b869863aae`,
idéntico al de la entrega documentada; versión registrada 0.2.2 / 202.

**La configuración general de compilación aún apunta a `03_TrackingProbe.unity`.**
La entrega vigente usa `CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh`:
`FigureBuild.BuildAndroid` pasa explícitamente `F4_FiguraAR_r02.unity` al
compilador. Ejecutar el script sin esa variable selecciona F1. La configuración
se conserva; esta revisión no cambia el comportamiento de la aplicación.

## Qué usa realmente

| Fuente seleccionada, en `.blend` y `.fbx` | Uso comprobado |
| --- | --- |
| `chupacabras_nocturno_r08` | Malla y esqueleto referenciados por el prefab final; material y texturas de `Nocturno_r08`. Su respiración original ya fue sustituida. |
| `chupacabras_nocturno_r08_respira_r02` | Fuente de la respiración vigente. `FigureBreathingRevision.Configure` extrajo el clip a `Respiracion.anim`; el controlador usa ese clip independiente. Este FBX no aparece como dependencia directa de la escena final. |

No hay `.blend` dentro de `Assets`: son fuentes de autoría, no archivos cargados
directamente por la app. Los dos FBX de Blender coinciden byte a byte con sus
copias importadas en Unity.

Referencias comprobadas por GUID en los archivos serializados:

```text
Assets/Scenes/F4_FiguraAR_r02.unity
  → Assets/FiguraAR/F4_r02/Figure.prefab
    → Nocturno_r08/chupacabras_nocturno_r08.fbx
    → Nocturno_r08/Surface.mat → BaseColor, Normal, MetallicSmoothness
    → Nocturno_r08_respira_r02/Respiracion.controller → Respiracion.anim
```

El recorrido encuentra 12 dependencias, incluida la escena. La búsqueda en C#
no encontró carga dinámica de modelos; `Resources` contiene solo la textura
`AprilTagFixture.png`. La procedencia del clip se corroboró en el código de
`FigureBreathingRevision.cs` y en el informe F7. Este análisis de referencias
no reemplaza un nuevo informe de empaquetado de Unity.

## Separación y alcance

En Unity hay **46 FBX**: uno para la malla vigente, otro como fuente del clip
vigente y **44 fuera de la escena F6 actual**. Entre ellos están F3, Nocturno R07,
oveja, escenario, intercambio, rigs y actuaciones. Algunos siguen siendo usados
por demos y escenas históricas; no se consideran archivos eliminables.

En `scenes/`, `exports/` y `assets/` de Blender se inventariaron **136 modelos**:
cuatro archivos seleccionados y 132 históricos o referencias fuera de esta entrega.
No se cuentan como fuentes adicionales las copias de entregas/evidencias,
comprimidos ni respaldos `.blend1`; permanecen intactos.

La nueva carpeta conserva `scenes/` y `exports/`, con ambos pares y los cuatro
mapas PBR de cada revisión. Esto conserva las rutas relativas de las texturas.
También contiene los manifiestos originales, el verificador existente,
resultados de las pruebas y los inventarios:

- `docs/referencias_unity.json`: modelos de Unity y cadenas de dependencias.
- `docs/inventario_blender.json`: clasificación y SHA-256 de las 136 fuentes.
- `docs/enlaces_blender.json`: imágenes y ausencia de bibliotecas externas.
- `SHA256SUMS`: integridad de los archivos de la selección.

## Verificación realizada

Se ejecutó el verificador existente `scripts/verificar_nocturno.py` en las copias
con Blender 5.2.2 LTS, para `r08` y `r08_respira_r02`: ambas pasan. Comprueba
geometría, UV, mapas 2K, pesos, huesos, apoyo, ciclo y correspondencia Blender–FBX.
Ambas tienen 110.294 triángulos, cuatro huesos, un material y ciclo de cuatro
segundos. Deriva de pies y discontinuidad del ciclo: cero. Error máximo
Blender–FBX menor de 0,000001 m.

Se reabrieron ambos `.blend` con scripts desactivados: no tienen bibliotecas
externas y las imágenes usadas están empaquetadas; también se incluyen los mapas
externos. Las copias se cotejan por SHA-256 y se revisa `git diff --check`.
No hay un linter configurado para este cambio documental/de archivos.

No se volvió a compilar Unity ni se repitieron las pruebas de Android: no cambia
ningún recurso de Unity. Para conservar el aspecto final al trabajar en esa app,
deben mantenerse la malla/material R08 y el clip/controlador R02; importar solo
el FBX R08 devolvería la respiración anterior.

Referencias locales: [estado de continuidad](estado.md), [informe F7](figura_ar_f7.md)
y [guía de distribución](distribucion_demo.md).
