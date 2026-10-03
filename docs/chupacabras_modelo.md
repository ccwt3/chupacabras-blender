# Chupacabras original: pasos 8 y 9

**Revisión vigente de modelado — 2 de octubre de 2026:** [chupacabras demacrado](chupacabras_demacrado.md), forma R01/acabado R02. El resto de este documento conserva el hito anterior y sus comprobaciones; rig/aspecto de producción aún usan ese modelo.

24 de septiembre de 2026, México. Modelado original generado en Blender
5.2.2 LTS e importado con Unity **6000.3.22f1**. Se completan solamente
anatomía/silueta y acabado geométrico. Rig, actuación e iluminación definitiva
conservan sus pasos posteriores.

## Entregas vigentes

- Forma: `scenes/08_chupacabras_forma_r03.blend`, FBX/JSON homónimos en `exports/`.
- Acabado: **`scenes/09_chupacabras_acabado.blend`**, FBX/JSON homónimos.
- Contextos de volumen: sufijo `_contexto_r02.blend` / `_contexto_r02.fbx` de ambos hitos.
- Cuatro vistas Blender por hito en `previews/`: frente, perfil, espalda y tres
  cuartos. Copias de tres cuartos, rostro y comparación con oveja desde Unity
  llevan `_unity_` en el nombre.
- Unity: escenas `Assets/Scenes/08_chupacabras_forma_r03_contexto_r02.unity` y
  `09_chupacabras_acabado_contexto_r02.unity`; modelos, materiales y prefab `Chupacabras.prefab`
  dentro de `Assets/Creature/<nombre del hito>/`.
- Evidencia detallada de importación/cámaras en Unity:
  `docs/evidencias/2026-09-24_08_chupacabras_forma_r03_contexto_r02/` y
  `docs/evidencias/2026-09-24_09_chupacabras_acabado_contexto_r02/`.

La primera forma y R02, con sus contextos, capturas y fallos de aceptación,
se conservan como diagnóstico. **R03 es el cierre del paso 8.** La anatomía es
idéntica entre las tres formas; cambió la colocación/orientación de revisión
y la medición de límites, no el bloqueo histórico R04. Los contextos vigentes
son **`_contexto_r02`**: una última comprobación de recorrido detectó cruce de
la cola al interpolar un giro de 270° y cercanía del hocico a la pared; se
conservaron los contextos anteriores y se corrigió la ruta corta.

## Decisiones de forma y detalle

Las tres referencias originales se inspeccionaron directamente en `references/`:

| Referencia | Rasgos trasladados al modelo original |
| --- | --- |
| `chupacabras1.jpg` | Postura baja, brazos largos, manos abiertas, hocico y cresta alta. |
| `chupacabras2.jpg` | Orejas puntiagudas, ojos amarillos grandes, hombros y rostro oscuro. |
| `chupacabras3.jpg` | Espalda arqueada, cintura estrecha, patas traseras digitígradas, cola curva y mechones de lomo. |

No se calcaron ni se usaron las imágenes como texturas. El volumen principal
fusiona masas anatómicas con remallado y reducción; cabeza y mandíbula quedan
separadas para la articulación posterior. Las manos tienen tres dedos largos
y garras. Las espinas centrales establecen la silueta; una segunda hilera más
fina y mechones limitados a cuello/lomo añaden detalle sin pelo simulado.

La forma usa gris neutro y ojos amarillos. El acabado añade cejas inclinadas,
narinas, dientes, garras marfil, piel gris verdosa y placas más claras. Son
seis colores sólidos reproducidos con URP Lit y Unlit para los ojos. Los UV
están desplegados en 0–1; no hay texturas externas, compositor ni shader exclusivo
de Blender. El ojo Unlit es visible sin luz; halo/bloom e iluminación nocturna
final no se implementan en este paso.

**Costo de geometría:** forma 8.486 triángulos/12 mallas; acabado 10.550
triángulos/17 mallas/6 materiales. Esto no mide draw calls, fps ni costo real
del teléfono. La agrupación del skin y los huesos corresponderá al paso 11.

## Contexto y correcciones verificadas

La prueba sustituye las mallas provisionales por este modelo y una copia
evaluada de la oveja Quaternius R04, de altura neutral 1,18 m. Conserva cámaras,
40 s y recorrido del contexto 06 salvo estos ajustes en **archivos nuevos**:

1. Entre 15 y 20 s el chupacabras gira hacia el frente del granero y deja la
   cola hacia el fondo, usando −180° para recorrer el giro corto desde −90°.
   Se desplaza el acecho final a y=9,3 m desde 14 s para que el hocico no toque
   la pared. En el acabado, las garras requieren además 0,25 m hacia el fondo
   antes de 14 s. La cola original sobresalía por un lateral. Se fija
   además la orientación de acecho hasta 14 s para no interpolar ese giro desde
   el inicio y perder la aparición de los ojos.
2. En 20–25 s se eleva la cámara interna de z=1,1 m a **z=2,4 m**, mirando a
   `(0,0,0.95)`. El antiguo bloque de hombros tapaba hasta el suelo; la anatomía
   tiene espacio entre las patas. El nuevo punto de vista logra el ocultamiento
   por profundidad real, sin desactivar la oveja, añadir pantallas ni polvo.
3. El punto de boca pasa a `(0,1.30,1.01)` y la referencia local de cuello a
   `(0,-0.55,0.87)`. La traslación de la oveja mantiene coincidentes ambos puntos.
   Los ejes son Blender `(x,y,z)` → Unity `(x,z,y)`; el chupacabras mira a +Y.

**Alcance de esta muestra:** la oveja conserva un giro rígido del bloqueo.
En el arrastre queda elevada con respecto al suelo; todavía no está actuando
ni deformándose. La coincidencia de puntos demuestra alcance geométrico y
continuidad de la referencia de contacto, **no una mordida final ni apoyo físico**.
Los pasos 10–11 deberán bajar/cerrar la cabeza, deformar lana y disponer cuerpo
y patas de la oveja sobre el suelo. No reutilizar esta muestra como actuación
definitiva ni interpretar `passed` como aprobación de rigs o arrastre final.

No se sustituyó la escena AR ni el corto histórico. Las escenas nuevas usan la
ventana/RenderTexture de revisión, sin conexión nueva al detector ni APK nueva.

## Verificación y límites

Reapertura independiente en Blender: todas las mallas cerradas, sin caras de
área nula, UV finitos dentro de 0–1, escala métrica, sin rig nuevo ni texturas
externas. Las demos, escenario y oveja se reabrieron con sus verificadores.

Unity abre de nuevo la escena guardada y compara triángulos, materiales, UV y
límites obtenidos de los **vértices transformados**. No se usa `Renderer.bounds`
para comparar con Blender: la caja local de un ojo girado sobreestima el límite
mundial hasta 3,2 cm. La comparación correcta arroja errores menores de
**0,00000043 m**; no era una deformación del FBX.

Resultados del acabado, a 320 × 180 para las máscaras de profundidad:

- Cero solapamientos AABB entre las piezas del chupacabras y dos cajas
  conservadoras del granero, paredes y tejado, en 1.200 cuadros a 30 Hz.
- 150/150 fotogramas de criatura oculta (15–20 s).
- 114/114 fotogramas de oveja oculta (21,2–25 s).
- 30/30 fotogramas finales vacíos (39–40 s).
- Ojo de acecho: 4 píxeles; oveja antes/después: 266/462 píxeles.
- Contacto de referencias: error máximo **0,00000240 m** en Unity, 564 cuadros
  de reproducción. Blender comprueba 565 incluyendo la clave de cierre; el
  reproductor vuelve al inicio al llegar exactamente a 40 s.
- 32 aserciones existentes de seguimiento correctas. C# compilado en el Editor
  fijado; Python/Bash y formato C# comprobados.

Se inspeccionaron vistas, rostro, comparación con oveja, aterrizaje, salto y
ventana. La máscara de visibilidad es una comprobación de Editor. La escena
requiere todavía rig, actuación, luz definitiva y medición móvil; no hay nueva
validación física en G20 ni S23.

## Reproducción sin sobrescribir

Desde Blender, elegir un sufijo nuevo. Los generadores rechazan entregas ya
existentes; ajustar `CHUPA_MODEL` y `CHUPA_FORM` a la revisión deseada.

```bash
CHUPA_SUFFIX=_revision blender -b -t 4 --python-exit-code 1 --python scripts/chupacabras.py -- 8
CHUPA_MODEL=08_chupacabras_forma_revision blender -b -t 4 --python-exit-code 1 --python scripts/chupacabras_contexto.py
CHUPA_MODEL=08_chupacabras_forma_revision blender -b -t 4 --python-exit-code 1 --python scripts/verificar_chupacabras.py
CHUPA_FORM=08_chupacabras_forma_r03 CHUPA_SUFFIX=_revision blender -b -t 4 --python-exit-code 1 --python scripts/chupacabras.py -- 9
```

En Unity, `bash scripts/verify_creature.sh` reabre las dos entregas vigentes y
genera evidencia en una carpeta nueva. Para una importación nueva, copiar el
FBX estático, JSON y FBX de contexto `_contexto_r02` a `Assets/Creature/<CHUPA_MODEL>/` y ejecutar
`CreatureBuild.Configure` con el Editor exacto. No ejecutar Configure sobre una
escena existente: el script lo rechaza. Para revisar visualmente el modelo en
Blender pueden usarse las vistas guardadas o el modo Material/Solid del visor.

## Referencias

Referencias visuales aportadas por el usuario. (s. f.). *Chupacabras 1–3*
[Imágenes de referencia; autoría y publicación no identificadas]. Archivo local
`references/`. No se atribuye una licencia desconocida ni se redistribuyen como
texturas del modelo.

Quaternius. (s. f.). *Farm animals* [Modelos 3D, CC0 1.0].
https://quaternius.com/packs/farmanimals.html
Véase la licencia conservada y [procedencia de la oveja](asset_oveja.md).
