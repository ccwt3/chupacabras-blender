# Ataque AR — entrega del 11 de octubre de 2026

Solicitud: ambos personajes en 3D sobre el marcador; ataque único, oveja recostada
sin movimiento y retorno del chupacabras a respiración. El usuario autoriza
reemplazar la app instalada del Moto G20 tanto en pruebas como en la entrega final.

## Tres etapas

1. **Modelamiento, animación e integración Unity.** Fuente nueva `ataque_ar_r02`:
   superficie Nocturno R08 conservada, rig ampliado de 4 a 16 huesos, oveja CC0
   archivada con un nivel de subdivisión (2.528 triángulos). Ataque de 6 segundos
   seguido de respiración de 4 segundos en bucle. El conjunto suma 112.822 triángulos.
   La escena nueva usa el mismo seguimiento AprilTag, proyección y materiales R08.
2. **Testeo móvil.** Moto G20 probado. Identificada instalación previa:
   `com.chupacabras.ar.figure`, 0.2.4 / 204. Sustituir únicamente este paquete cuando
   esté lista la candidata. Validar ataque, cadáver persistente, pausa/recuperación
   del marcador, segundo plano y nueva sesión desde el menú; medir rendimiento.
3. **Reempaquetamiento.** AAB firmado con la clave existente de la copia
   `/home/cacawatin/code/unity/chupacabras/google_play`; APK universal generado
   por bundletool desde ese AAB. Versión 0.2.5 / 205. Instalar y verificar
   el paquete final en el teléfono. No publicar en Play.

## Cambios y motivo

- `scripts/ataque_ar.py`: amplía el rig conservando geometría, UV y textura;
  sincroniza salto breve, contacto con cuello, caída, retirada y respiración.
  El contacto sigue un vértice real de la oveja; caída con apoyo calculado cada
  cuadro. No hay simulación de física ni nuevas dependencias.
- `scripts/preview_ataque_ar.py`: vistas de momentos clave y contacto lateral.
- `integration/attack/`: fuentes de instalación Unity para la copia Play;
  escena/prefab nuevos y copias de seguridad de las fuentes previas.
- Animator compartido para evitar desincronización entre actores; conservación
  de estado al ocultar el marcador. La secuencia reinicia al abrir una nueva
  sesión desde el menú, no por perder brevemente el marcador.
- Se incorpora crédito/licencia CC0 de Quaternius a los avisos de la aplicación.

## Verificación hasta ahora

Generador Blender: apoyo mínimo oveja −0,000000087 m; error máximo de contacto
0,031 m durante agarre; desplazamiento de oveja en reposo y discontinuidad del
bucle: cero. Estas comprobaciones no sustituyen revisión visual ni prueba móvil.
Vistas Blender revisadas al comienzo, durante contacto y en reposo.
Blender–FBX R02: ocho muestras de ambos personajes, máximo 0,000001257 m de
error. R02 corrige el límite de cuatro influencias tras subdividir la oveja.
Unity: dos actores, 112.822 triángulos, ataque de 6 s, reposo de 4 s; material
Nocturno conservado; 32 aserciones de seguimiento y 14 estados en ejecución
superados, incluida pausa del Animator mientras está oculto. Se corrigió la
conversión de ejes del nodo adicional y el recorte de clips empieza en el
cuadro 1 del FBX (reposo: 145–241). Revisión visual de contacto y estado final
hecha con los materiales Unity. Compilación y prueba física completadas; resultados a continuación.

Se conservan entregas previas y cambios preexistentes del archivo de históricos.
El proyecto Unity padre permanece fuera del cambio; la nueva entrega vive en
su copia independiente `google_play`.

Referencia técnica: Unity Technologies. (s. f.). *Animator.keepAnimatorStateOnDisable*.
https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/animator/keepanimatorstateondisable

## Empaquetado comprobado

Unity 6000.3.22f1 produjo el AAB 0.2.5 / 205, paquete
`com.chupacabras.ar.figure`, en 98 segundos: cero errores y cero advertencias.
El APK universal se generó desde ese AAB con bundletool 1.17.2 y la clave de
subida existente. Validación AAB, firma, versión, ARM64, permisos, ELF y
alineación de 16 KB correctas. Sin permiso INTERNET ni modo de desarrollo.

Entrega: `entregas/Ataque_AR_0.2.5_20261011/`.
AAB: 35.694.912 bytes, SHA-256
`61ebe8963348275d81bd4e2ea2abb76cfec8dc122d271cb2d6c2dfa597f3ee12`.
APK: 35.819.266 bytes, SHA-256
`82bcceecf0138921bb17e1044f84d1df397a0967df800a7752354b2e78bca402`.

El informe de contenido empaquetado incluye el FBX `ataque_ar_r02` y los dos
clips Ataque/Reposo; no incluye modelos de las escenas históricas.
Los textos locales de la ficha y declaraciones se actualizaron: ya no afirman
«sin combate» y describen la muerte de la oveja sin sangre ni heridas explícitas.
No se enviaron formularios ni se publicó en Play.

## Prueba móvil

Moto G20, Android 11/API 30, ARM64, páginas reales de 4096 bytes. Se identificó
0.2.4 / 204, se desinstaló solo `com.chupacabras.ar.figure` y se instaló la APK
nueva. La copia extraída del teléfono coincide por SHA-256 con la entrega.
Bienvenida, solicitud de permiso tras el botón, cámara real y detección física
comprobadas. Registros sin excepciones hasta el inicio del perfil.
La consulta inicial de SurfaceFlinger se corrigió antes de atribuir fps;
`mobile_profile_01` no es una medición válida de cuadros. Perfil corregido completado en
`docs/evidencias/ataque_20261011/mobile_profile_02/`.

El usuario confirmó en el Moto G20: «Sí, se ve toda la secuencia correctamente».

Perfil final: 301,05 s de recolección; 299,69 s de presentaciones medidas,
8.883 cuadros, **29,638 fps**. Mediana 33,323 ms, p95 33,471 ms, máximo 99,267 ms.
Se excluye el historial anterior a la primera muestra de SurfaceFlinger.
PSS 404,98 → 402,08 MiB; batería 39,9 → 41,0 °C con USB conectado.
Mismo proceso y sin excepciones en el registro recogido. La mayor parte del
perfil corresponde al reposo final, con cámara, detección y ambos personajes
visibles; no se afirma visibilidad cuadro por cuadro ni se atribuye una mejora
causal frente a la prueba F7, cuyas condiciones son distintas.

La confirmación visual del usuario cubre aparición, ataque, caída y respiración.
La prueba en Android de páginas de 16 KB y en otros teléfonos sigue sin realizarse;
la alineación binaria de 16 KB sí está verificada.

Recuperación física del marcador confirmada por el usuario: «Sí, se ocultan y
regresan sin reiniciar». Segundo plano y reanudación comprobados por ADB: mismo
proceso, cámara reiniciada, detección recuperada y escena final visible en la
captura `lifecycle/resumed.png`. No hay duplicación observada.

## Entrega y reproducción

La APK final es exactamente la probada, sin recompilar después del perfil.
Se retira la instalación de prueba y se reinstala el archivo de la entrega;
la identidad extraída del teléfono se guarda en `install_final/identity.json`.
Se deja instalada por instrucción expresa del usuario, sustituyendo la regla
histórica de retirar las apps de prueba al terminar.

- Blender: generar con `CHUPA_ATTACK_REV=<revisión nueva> blender -b -t 3
  --python-exit-code 1 --python scripts/ataque_ar.py`; verificar con el mismo
  identificador y `scripts/verificar_ataque_ar.py`. No sobrescribir revisiones.
- Unity actual: `google_play/Assets/Scenes/AtaqueAR_r02.unity`; generador
  `Assets/Editor/AttackBuild.cs`. Modelos, clips y prefab en
  `Assets/FiguraAR/Ataque_r02/`. Las fuentes de integración se conservan también
  en `integration/attack/` del proyecto Blender.
- Recompilar la escena configurada: `bash scripts/build_google_play.sh` desde
  la copia `google_play`, con Unity exacto. La evidencia usa un directorio nuevo.
- Para repetir la experiencia: Inicio → Abrir cámara. Perder el marcador o
  poner la app en segundo plano conserva el estado; una sesión nueva lo reinicia.

No se cambiaron paquetes del motor, ajustes globales ni otras aplicaciones.
El proyecto Unity padre y las entregas previas permanecen conservados. Los
cambios previos de archivo de modelos en el repositorio Blender no se revierten.
Sin commit/push ni publicación de la aplicación.
