# Personaje Nocturno R08

Reemplazo autorizado del personaje, conservando la aplicación funcional.
[Diseño, fuentes, reproducción y validación](../../../blender/chupacabras/docs/rediseno_nocturno.md).

Se modifica únicamente el hijo `StaticFigure` del prefab F4 R02, incorporando
`Assets/FiguraAR/Nocturno_r08/`: FBX, tres mapas PBR 2K, material y respiración
nativa de cuatro segundos. 110.294 triángulos, un material, cuatro huesos.
`Respiracion.anim` conserva las curvas de huesos y excluye las curvas de raíz
que sobrescribían la colocación del personaje. Sin nuevos scripts runtime.

`FigureNocturno` importa y verifica el personaje; `FigureBuild` y `FigurePreview`
comprueban también la malla animada y su transformación. Los tests existentes de
seguimiento se conservan. Las versiones estáticas anteriores y fuentes siguen disponibles.
Los ensayos previos y temporales permanecen locales; los logs se guardan comprimidos.

La escena, luces, escala, seguimiento, UI, paquetes y ProjectSettings no cambian.
`final_v2/scope_audit.json` compara los hashes de los archivos previos y los
componentes de luz. Diez archivos reserializados/de compilación fueron restaurados
con copias locales de sus versiones generadas. No se modificaron archivos del índice.

Entrega: `builds/android/F6_figure_20261003_222832.apk`, 55.348.110 bytes,
0.2.2 / 202, `com.chupacabras.ar.figure`. SHA-256:
`0bf9b53293e4035d2decba069845bace2afc0c8330f8a77ad131b333a47b3e16`.
Compilar: `CHUPA_FIGURE_STAGE=F6 bash scripts/build_figure.sh`.

Evidencia final: `docs/evidencias/2026-10-03_nocturno_r08/final_v2/`.
32 checks, diez estados y respiración real en Editor correctos; build sin errores
ni advertencias; firma, cámara, ARM64 y alineación verificadas. No instalada ni
perfilada en teléfono. Los perfiles anteriores pertenecen al modelo F3.
