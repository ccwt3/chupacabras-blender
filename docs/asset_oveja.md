> **Referencia histórica del alcance anterior.** Sus resultados se conservan;
> sus próximos pasos y requisitos cinematográficos no son tareas vigentes.
> Consultar el [plan de figura AR](plan_secuencia.md) y el [estado](estado.md).

# Oveja reutilizada — paso 7

Se seleccionó **Sheep, de Farm Animals Pack, por Quaternius (2018)**. La página
del autor y la publicación en OpenGameArt declaran CC0; el ZIP incluye su propio
`License.txt`, que confirma CC0 1.0 y atribución opcional. Permite adaptar y
distribuir el modelo dentro de la aplicación. Se conserva crédito voluntario:
«Oveja adaptada de Farm Animals Pack, creado por Quaternius, CC0 1.0».

## Selección breve

| Candidato | Evidencia pública | Decisión |
| --- | --- | --- |
| Quaternius, Farm Animals Pack | CC0; Blender/FBX/OBJ; animales animados; fuente editable descargable sin cuenta. | Elegido. Inspección real: 307 vértices, 612 triángulos, 24 huesos, 2 materiales, 6 acciones. |
| pracalic, Sheep (2014) | CC0; Blender, huesos y movimiento sencillo declarados en OpenGameArt. | Alternativa documental; no se descargó ni se atribuye un conteo verificado. El elegido ya aporta formatos y acciones aprovechables. |

La ficha Sheep de Quaternius en Poly Pizza también se consultó, pero **no es la
fuente descargada**. No se mezclan su fecha/conteos con el ZIP de 2018. No hubo
compras, cuentas personales ni recursos privados.

## Fuentes y archivos conservados

- ZIP intacto: `assets/oveja/Farm_Animals_Quaternius_original.zip`.
- Solo se extrajeron Sheep.blend, Sheep.fbx, Sheep.obj, Sheep.mtl y License.txt
  en `assets/oveja/original/Farm Animals by @Quaternius/`.
- `assets/oveja/procedencia.json`: URL, fecha UTC de descarga, tamaños y SHA-256.
- `assets/oveja/procedencia/{quaternius,opengameart}.html`: páginas de licencia
  descargadas. El texto íntegro de CC0 se consultó en Creative Commons; su
  descarga directa devolvió HTTP 403. Se conserva la licencia incluida por el
  autor y el enlace oficial, sin fabricar una copia atribuida al servidor.
- Fuente vigente: **`scenes/07_oveja_r04.blend`**. Revisiones anteriores conservadas.
- `exports/07_oveja_r04.fbx`: malla y esqueleto en pose neutral.
- `exports/07_oveja_r04_poses.fbx`: muestra de aptitud de 6 s; **no es el corto**.
- `exports/07_oveja_r04.json`: escala, biblioteca original, conteos y vértices
  evaluados para contrastar cuatro poses con Unity.
- Unity: `Assets/Sheep/`, prefab `Sheep_Quaternius_r04.prefab` y escena
  **`Assets/Scenes/07_Sheep_r04.unity`**, con la oveja quieta dentro del escenario.

## Adaptación y alcance

Se conserva la topología, el rig existente y sus acciones **Death, Idle, Jump,
Run, Walk y WalkSlow**. No se reconstruye la oveja. Se ajustan lana marfil,
cabeza/patas oscuras, sombreado facetado y escala uniforme **0.2703578356** bajo
`SheepAssetRoot`. La altura neutral es **1.18 m**, ancho **0.602 m** y longitud
**1.600 m**; patas en Z=0, frente −Y en Blender/−Z en Unity.

Para que Blender y el skin móvil usen los mismos pesos, se conservan las cuatro
influencias mayores y se normalizan. **35 de 307 vértices** tenían más de cuatro;
la primera importación truncada discrepaba hasta 3.24 cm. No se añaden huesos ni
controles. Los cuatro IK originales permanecen en la fuente, y sus resultados
se hornean en la prueba exportada. La muestra de caída toma la acción original
y corrige únicamente su altura de apoyo; no pretende cerrar el forcejeo final.

Se reconstruyen nodos de color sólido y se retira de la copia de trabajo una
referencia heredada a `Texture.png` en el equipo del autor. No era parte de los
materiales de color usados. La fuente original y el ZIP siguen intactos.

La muestra comprueba pose neutral, cabeza/cuello inclinados, caída original y
retorno neutral. No hay shape keys todavía. **Paso 10 pendiente:** compresión
de lana, adaptación final de controles/pesos, pastoreo con contacto con hierba
y forcejeo extremo; el agarre con el chupacabras corresponde al paso 11.
La oveja reutilizada todavía no sustituye los proxies del bloqueo animado.

## Verificación y reproducción

Blender 5.2.2 LTS reabre el modelo sin dependencia de texturas externas y mantiene
24 huesos y seis acciones. Unity 6000.3.22f1 importa 612 triángulos y dos submallas;
las cuatro muestras pasan con error máximo **0.00011044 m** y apoyo mínimo
**−0.00008874 m** (tolerancia 1 mm). Altura importada: **1.17999947 m**.

`SheepBuild.Verify` evalúa el clip mediante Playables. Usa `BakeMesh(..., true)`
para compensar la escala del skin y recalcula matrices por render al capturar
varias poses en una misma actualización del Editor; de otro modo la captura
conservaba matrices de la pose previa. Este ajuste pertenece al verificador.
Las imágenes finales muestran las poses importadas, sin sustituirlas por un
render de Blender. Evidencia vigente: `docs/evidencias/2026-09-24_oveja_r04/`
en Unity. La escena `07_Sheep.unity` y capturas previas son intentos superados.

```bash
CHUPA_SUFFIX=_r05 blender -b --disable-autoexec -t 4 --python-exit-code 1 --python scripts/oveja.py
blender -b --disable-autoexec -t 4 --python-exit-code 1 --python scripts/verificar_oveja.py
```

Las salidas existentes se rechazan. `scripts/verify_assets.sh` en Unity repite
comprobaciones y capturas vigentes en carpetas nuevas. Ni las poses ni el Editor
constituyen una prueba física del G20/S23. No se generó otra APK porque estos
pasos requieren importación y aptitud de recursos, sin intervención del teléfono.

## Referencias

Quaternius. (2018, junio). *Farm Animal Pack* [Modelos 3D]. https://quaternius.com/packs/farmanimal.html

Quaternius. (2018, 8 de junio). *LowPoly Animated Farm Animal Pack* [Modelos 3D]. OpenGameArt. https://opengameart.org/content/lowpoly-animated-farm-animal-pack

pracalic. (2014, 1 de febrero). *Sheep* [Modelo 3D]. OpenGameArt. https://opengameart.org/content/sheep

Creative Commons. (s. f.). *CC0 1.0 Universal: Legal code*. https://creativecommons.org/publicdomain/zero/1.0/legalcode.en

Unity Technologies. (s. f.). *SkinnedMeshRenderer.BakeMesh*. Unity 6.3. https://docs.unity3d.com/6000.3/Documentation/ScriptReference/SkinnedMeshRenderer.BakeMesh.html
