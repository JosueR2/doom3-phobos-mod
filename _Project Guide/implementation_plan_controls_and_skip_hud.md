# Implementation Plan - Keybinds (Flashlight, Skip, Jump) & Persistent Cutscene Skip HUD

## 1. Objetivo
1. Corregir el enlace de la tecla `F` para que active directamente la linterna (`_impulse11`) y no el cambio de arma por defecto (`_impulse0`).
2. Configurar la tecla de salto de cinemáticas para que **únicamente** se use la tecla `X` (`script SkipIntro()`), retirando la invocación de `SPACE` y `ENTER`.
3. Garantizar que la barra espaciadora (`SPACE`) esté configurada por defecto exclusivamente para Saltar (`_moveUp`).
4. Mostrar un indicador persistente en pantalla con el mensaje `[ X ] Saltar escena` / `[ X ] Skip scene` durante toda la duración de las escenas que admiten salto, ocultándolo inmediatamente al salir de la cinemática o saltarla.
5. Posicionar el mensaje de salto fijado en la **esquina superior derecha** de la pantalla, adaptado a todas las resoluciones y relaciones de aspecto compatibles (4:3, 16:9, 16:10, 21:9).

---

## 2. Estado Actual Relevante
- En `DoomConfig.cfg`, la tecla `F` está configurada como `bind "f" "_impulse0"` (arma 0 / siguiente arma), lo que causa que solo pase a la linterna cuando el resto de armas carecen de munición. La asignación oficial del motor para la linterna es `_impulse11`.
- En `autoexec.cfg`, `SPACE` tiene `_moveUp; script SkipIntro()`, lo que activa el salto de cinemática con la barra espaciadora.
- Los mensajes previos de ayuda de salto se mostraban a través del sistema de subtítulos (`subtitles.gui`), el cual:
  - Solo se redibuja cuando hay un diálogo activo (`subtitlesVisible != 0` en `gamex86.dll`).
  - Desaparecía a los 5 segundos de iniciar la escena.
  - Se colocaba en la parte inferior de la pantalla sobre el texto del diálogo.
- El archivo `textmessagesystem.gui` es cargado por `idPlayer::Spawn` en todos los mapas y el motor lo procesa incondicionalmente en cada frame incluso durante secuencias cinemáticas (`InCinematic() == true`), convirtiéndolo en el contenedor ideal para el HUD persistente de cinemáticas.

---

## 3. Problema que se Pretende Resolver
- El jugador no puede encender la linterna con `F` en situaciones normales.
- El jugador puede saltar accidentalmente cinemáticas al presionar la barra espaciadora o ENTER.
- Durante las cinemáticas, el aviso de cómo saltar la escena desaparece a los 5 segundos, impidiendo que el jugador sepa si la escena sigue siendo saltable más adelante.
- El aviso anterior ocupaba la zona de subtítulos de diálogo en lugar de un indicador limpio en la esquina superior derecha.

---

## 4. Solución Propuesta

### A. Configuración de Teclas (`autoexec.cfg` y `DoomConfig.cfg`)
- `bind "f" "_impulse11"`: Linterna directa.
- `bind "SPACE" "_moveUp"`: Salto de personaje.
- `bind "x" "script SkipIntro()"`: Única tecla para saltar cinemáticas.
- `bind "ENTER" "_button2"`: Uso e interacción sin invocar skip.

### B. Sistema de Estado y Visibilidad en Script (`phobos_subtitles_es.script`)
- Crear función `PhobosSetCanSkip(float enable)`:
  - Si `enable == 1`: activa `g_canSkip "1"` y sincroniza `g_subLangIsES` (`"1"` para español, `"0"` para inglés).
  - Si `enable == 0`: establece `g_canSkip "0"`.
- Inicializar `g_canSkip` a `"0"` en `InitSubtitleCVars()`.

### C. HUD Persistente en `src/guis/textmessagesystem.gui`
- En el `windowDef Desktop` raíz, incorporar dos `editDef` sincronizados con `liveUpdate 1`:
  - `editDef SkipSync` vinculado a `cvar "g_canSkip"` -> actualiza `gui::skip_visible`.
  - `editDef LangSync` vinculado a `cvar "g_subLangIsES"` -> actualiza `gui::is_spanish`.
- En cada uno de los 4 escritorios por relación de aspecto (`Desktop_4_3`, `Desktop_16_9`, `Desktop_16_10`, `Desktop_21_9`):
  - Añadir `windowDef SkipPrompt_<ratio>` en la esquina superior derecha con fondo semitransparente oscuro y borde sutil.
  - Contenido condicional:
    - `windowDef SkipText_ES` (`visible "gui::is_spanish"`): `[ X ] Saltar escena`
    - `windowDef SkipText_EN` (`visible 1 - "gui::is_spanish"`): `[ X ] Skip scene`
  - Coordenadas de esquina superior derecha por relación de aspecto:
    - 4:3 (ancho 640): `rect 468, 12, 160, 24`
    - 16:9 (ancho 853): `rect 677, 12, 160, 24`
    - 16:10 (ancho 768): `rect 592, 12, 160, 24`
    - 21:9 (ancho 1120): `rect 940, 12, 160, 24`

### D. Actualización de los 5 Scripts de Cinemática
- Eliminar las llamadas temporales a `PhobosShowSubtitle_*("", "[ Press SPACE or X to skip ]")`.
- Sustituir por `PhobosSetCanSkip(1)` cuando el temporizador de skip se activa.
- Invocar `PhobosSetCanSkip(0)` cuando:
  1. El jugador presiona `X` (en la rutina de skip).
  2. La cinemática concluye de manera natural.

---

## 5. Archivos Modificados / Creados
1. `src/guis/textmessagesystem.gui` (Modificado - Inyección de variables, editDefs y SkipPrompts en los 4 Desktops).
2. `src/script/phobos_subtitles_es.script` (Modificado - Añadir `PhobosSetCanSkip` e inicialización de cvar).
3. `src/script/map_e1m1.script` (Modificado - Intro Prólogo).
4. `src/script/map_e1m1_scanner.script` (Modificado - Escáner Médico).
5. `src/script/map_e1m1_1.script` (Modificado - Recuerdo del Hospital).
6. `src/script/map_e1m3.script` (Modificado - Despegue Hangar FCE).
7. `src/script/map_e1m3_outro.script` (Modificado - Outro y Créditos Episodio 1).
8. `mod/tfphobos/autoexec.cfg` y `F:\...\tfphobos\autoexec.cfg` (Modificado - Binds de F, SPACE, X).
9. `F:\...\tfphobos\DoomConfig.cfg` (Modificado - Binds sincronizados).

---

## 6. Flujo de Implementación
1. Implementar la sincronización de cvars y elementos visuales en `src/guis/textmessagesystem.gui`.
2. Implementar `PhobosSetCanSkip(float enable)` en `src/script/phobos_subtitles_es.script`.
3. Actualizar la lógica de skip en los 5 scripts cinemáticos.
4. Actualizar `autoexec.cfg` y `DoomConfig.cfg` con las nuevas asignaciones de teclas.
5. Ejecutar `tools/validate_scripts.py` para verificar que la sintaxis de todos los scripts idScript sea válida.
6. Ejecutar `tools/build_mod.py` para empaquetar `pak003_skipcinematics.pk4` y sincronizar la carpeta `mod/tfphobos/`.
7. Registrar walkthrough y actualizar `work_plan.md`.

---

## 7. Estrategia de Verificación
- Verificación sintáctica con `validate_scripts.py`.
- Verificación de empaquetado de `textmessagesystem.gui` y scripts en el PK4.
- Comprobación de que `autoexec.cfg` y `DoomConfig.cfg` contienen los binds exactos (`f` -> `_impulse11`, `SPACE` -> `_moveUp`, `x` -> `script SkipIntro()`).

