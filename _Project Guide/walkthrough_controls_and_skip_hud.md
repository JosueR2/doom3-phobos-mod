# Walkthrough - Keybinds (Flashlight, Skip, Jump) & Persistent Cutscene Skip HUD

## 1. Resumen de Cambios Implementados

### 1.1 Corrección de la Linterna (`F`)
- **Problema previo:** La tecla `F` estaba configurada como `_impulse0` (arma 0 / fists / ciclo de armas), lo que impedía sacar la linterna a menos que todas las demás armas se quedasen sin munición.
- **Solución:** Se reconfiguró `F` a `_impulse11` (comando nativo de idTech 4 para equipar/alternar la linterna) tanto en `autoexec.cfg` como en `DoomConfig.cfg`.

### 1.2 Configuración Exclusiva de Salto de Cinemáticas con `X`
- **Problema previo:** La barra espaciadora (`SPACE`) y `ENTER` ejecutaban simultáneamente `script SkipIntro()`, lo que podía saltar escenas accidentalmente al querer saltar o interactuar.
- **Solución:**
  - Se eliminó la llamada a `script SkipIntro()` de `SPACE` y `ENTER`.
  - `SPACE` queda asignado de forma limpia y exclusiva a Jump (`_moveUp`).
  - `ENTER` queda asignado a Use (`_button2`).
  - La tecla `X` es ahora la **única** tecla configurada para saltar cinemáticas (`bind "x" "script SkipIntro()"`).

### 1.3 HUD Persistente en Esquina Superior Derecha durante Cinemáticas
- **Problema previo:** El mensaje de salto anterior se inyectaba en el búfer de subtítulos de diálogo en la parte inferior de la pantalla y desaparecía a los 5 segundos.
- **Solución:**
  - Se integró un indicador visual fijo en `src/guis/textmessagesystem.gui`. Dado que `textmessagesystem.gui` es procesado incondicionalmente en cada fotograma por el motor durante cinemáticas (`InCinematic() == true`), el indicador se mantiene en pantalla mientras la escena sea saltable y se oculta inmediatamente al terminar o saltarla.
  - El indicador está posicionado en la **esquina superior derecha** con marco semitransparente oscuro y soporte nativo para las 4 relaciones de aspecto (4:3, 16:9, 16:10, 21:9).
  - Detección automática de idioma:
    - Español (`g_subLang "spanish"`): `[ X ] Saltar escena`
    - Inglés (`g_subLang "english"`): `[ X ] Skip scene`

### 1.4 Sincronización en los 5 Scripts de Cinemática
- Se implementó la función `PhobosSetCanSkip(float enable)` en `src/script/phobos_subtitles_es.script`.
- Se actualizaron los 5 scripts cinemáticos para activar el indicador (`PhobosSetCanSkip(1)`) y desactivarlo inmediatamente (`PhobosSetCanSkip(0)`) tanto en la secuencia de salto como en la finalización natural de la escena:
  1. `map_e1m1.script` (Intro y viaje a Marte).
  2. `map_e1m1_scanner.script` (Escáner médico).
  3. `map_e1m1_1.script` (Recuerdo del hospital y despertar).
  4. `map_e1m3.script` (Despegue hangar FCE).
  5. `map_e1m3_outro.script` (Outro y créditos Episodio 1).

---

## 2. Archivos Modificados

| Archivo | Tipo de Cambio |
| :--- | :--- |
| `src/guis/textmessagesystem.gui` | Se añadieron `editDef SkipSync`, `editDef LangSync` y `SkipPrompt_*` en `Desktop_4_3`, `Desktop_16_9`, `Desktop_16_10`, `Desktop_21_9`. |
| `src/script/phobos_subtitles_es.script` | Se añadió la función `PhobosSetCanSkip` e inicialización de cvars `g_canSkip` y `g_subLangIsES`. |
| `src/script/map_e1m1.script` | Reemplazo de subtítulo temporal por `PhobosSetCanSkip(1)` y desactivación con `PhobosSetCanSkip(0)`. |
| `src/script/map_e1m1_scanner.script` | Reemplazo de subtítulo temporal por `PhobosSetCanSkip(1)` y desactivación con `PhobosSetCanSkip(0)`. |
| `src/script/map_e1m1_1.script` | Reemplazo de subtítulo temporal por `PhobosSetCanSkip(1)` y desactivación con `PhobosSetCanSkip(0)`. |
| `src/script/map_e1m3.script` | Reemplazo de subtítulo temporal por `PhobosSetCanSkip(1)` y desactivación con `PhobosSetCanSkip(0)`. |
| `src/script/map_e1m3_outro.script` | Reemplazo de subtítulo temporal por `PhobosSetCanSkip(1)` y desactivación con `PhobosSetCanSkip(0)`. |
| `mod/tfphobos/autoexec.cfg` | Binds: `f` -> `_impulse11`, `SPACE` -> `_moveUp`, `x` -> `script SkipIntro()`, `ENTER` -> `_button2`. |
| `F:\...\tfphobos\autoexec.cfg` | Sincronizado idéntico a `mod/tfphobos/autoexec.cfg`. |
| `F:\...\tfphobos\DoomConfig.cfg` | Binds de `f`, `SPACE`, `x` y `ENTER` sincronizados. |
| `pak003_skipcinematics.pk4` | Compilado con 292.66 KB conteniendo todos los GUIs y scripts actualizados. |

---

## 3. Pruebas y Verificación

- [x] **Validación Sintáctica idScript:** `python tools/validate_scripts.py` ejecutado; los 28 scripts pasaron exitosamente sin errores de sintaxis ni comillas.
- [x] **Construcción y Empaquetado:** `python tools/build_mod.py` ejecutado; archivo `pak003_skipcinematics.pk4` generado (292.66 KB) e instalado en el juego, sincronizando toda la estructura a `mod/tfphobos/`.
- [x] **Verificación de Binds:** Verificado con búsqueda regex que `DoomConfig.cfg` y `autoexec.cfg` tienen `f` en `_impulse11`, `SPACE` en `_moveUp`, `x` en `script SkipIntro()` y `ENTER` en `_button2`.
- [x] **Verificación de Variables y HUD:** Elementos `SkipSync`, `LangSync` y `SkipPrompt_*` verificados en el archivo `.gui` para las 4 relaciones de aspecto.
- [x] **Hotfix Colisión de Símbolo idScript (`enable`):** En idTech 4, `enable` es un evento de entidad global (`event void enable()`). Se renombró el parámetro de `PhobosSetCanSkip(float enable)` a `PhobosSetCanSkip(float canSkipState)` en `phobos_subtitles_es.script`, resolviendo el error del compilador `Type mismatch on redeclaration of enable`.

