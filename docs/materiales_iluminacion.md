> **Referencia histórica del alcance anterior.** Sus resultados se conservan;
> sus próximos pasos y requisitos cinematográficos no son tareas vigentes.
> Consultar el [plan de figura AR](plan_secuencia.md) y el [estado](estado.md).

# Materiales, iluminación y composición — paso 12

Trabajo del 30 de septiembre de 2026, limitado al paso **12.1** y sus pruebas
previas a **12.2 / M#[4]**. El paso 13 depende de la revisión física y no se inició.

La fuente permanece en este proyecto Blender. Se reutilizan el escenario 06,
el acabado original 09, el rig de oveja 10 y el contacto 11 R03, con su
triangulación fija. No se guardaron cambios en esas fuentes ni se alteraron
las demos. Los materiales de producción se resuelven en Unity, como indica el
plan; no se requiere un `.blend` nuevo para este trabajo.

En `/home/cacawatin/code/unity/chupacabras` se añade la escena
`Assets/Scenes/12_AppearanceAR.unity`, el prefab `Assets/Appearance12/AppearanceStudy.prefab`,
materiales propios y una copia del pipeline URP. La figura estática se coloca a
la izquierda del marcador y el panel a la derecha. El panel mide 240 × 135 mm
y usa RenderTexture 960 × 540. Las luces de relleno separan figura y corto;
la captura real de cámara no recibe esa iluminación.

La revisión presenta tres poses de luz a partir de los rigs validados, cada
una durante seis segundos. Es una muestra de materiales/composición, sin
actuación final ni cronología narrativa. Se conservan los **40 segundos** de
producción y la demo independiente de **35 segundos**. No cierra el paso 20.

La primera captura detectó pérdida de la rotación de conversión del FBX en la
figura estática. Se corrigió conservando esa rotación y aplicando el giro de
presentación por encima. Se ajustaron el relleno exterior, el plano general y
el encuadre de las espinas mediante capturas nuevas. Los intentos de diagnóstico
se conservan identificados como tales; consultar `docs/estado.md` para la
revisión vigente.

La captura de pantalla de Play Mode no produjo archivo en batch y alcanzó el
límite de tiempo. La verificación ahora renderiza explícitamente la cámara AR
durante Play Mode, después de actualizar la cámara del panel. Así se comprueba
la composición de ejecución sin depender de la captura diferida de Game View.
No se interpreta ese resultado como evidencia física.

Reproducción, guía de M#[4], compilación e implementación:
[paso12_aspecto.md](/home/cacawatin/code/unity/chupacabras/docs/paso12_aspecto.md).
No se modificaron ajustes del Editor instalado ni se cambiaron versiones.
