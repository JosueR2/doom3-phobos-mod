# Walkthrough - Weapon-Mounted Flashlight Mod for Doom 3: Phobos (`pak004_weapon_flashlight.pk4`)

## 1. Resumen de Cambios Implementados

### 1.1 Diagnóstico y Resolución del Conflicto del Mod Base
- **Causa del Crash Previo:** El mod `zzzz_pak105.pk4` definía a nivel global `boolean on;` en `weapon_base.script`. En Phobos, tres scripts de IA de enemigos (`ai_monster_demon_imp_archspawn.script:158`, `ai_monster_zombie_boney_archspawn.script:167` y `ai_monster_demon_pinky_archspawn.script:149`) utilizan una variable local `float on`. El compilador abortaba el inicio del juego por colisión de tipos.
- **Acción:** El usuario eliminó `zzzz_pak105.pk4` del juego base para evitar conflictos globales.

### 1.2 Paquete Complementario Nativo (`pak004_weapon_flashlight.pk4`)
Para que las armas de Phobos tengan linterna montada funcional respetando la arquitectura de idTech 4, se construyó un paquete complementario dedicado de alta prioridad (`pak004_weapon_flashlight.pk4`, 38.53 KB):
- **Compatibilidad 100% con Phobos:** Se basó en las definiciones y scripts de armas nativas de Phobos (preservando cadencias de tiro, dispersión, retroceso, animaciones de recarga y el arma exclusiva Super Shotgun / Doble Cañón).
- **Proyector Dinámico Oficial:** Cada arma utiliza el shader y textura oficial de linterna de alta resolución de idTech 4 (`lights/flashlight5`), proporcionando iluminación realista con sombras dinámicas sin requerir texturas externas pesadas ni generar advertencias de consola.
- **Persistencia de Estado:** El estado encendido/apagado se mantiene entre cambios de armas mediante la variable global segura `dfm_flashlight_on`. Si el jugador enciende la linterna con la pistola y cambia a la escopeta, la escopeta mantendrá la linterna encendida automáticamente.

### 1.3 Asignación de Tecla
- Se configuró la tecla `F` vinculada a `_button5` en `autoexec.cfg` y `DoomConfig.cfg`:
  ```cfg
  bind "f" "_button5"
  ```
- Al pulsar `F` mientras se sostiene cualquier arma, se alterna de forma instantánea el foco montado en el arma activa con sonido de clic (`player_pistol_empty`), sin guardar el arma ni interrumpir el combate.

---

## 2. Archivos Creados y Modificados

| Archivo | Propósito |
| :--- | :--- |
| `src_flashlight/def/weapon_*.def` (10 archivos) | Parámetros del proyector dinámico (`mtr_flashShader "lights/flashlight5"`, `flashTarget`, `flashAngle 18.0`, `flashRadius 400`, `snd_click`). |
| `src_flashlight/script/weapon_base.script` | Definición de señal `_BUTTON5`, variable de estado global `boolean dfm_flashlight_on;` y método `weapon_base::ToggleOnOff()`. |
| `src_flashlight/script/weapon_*.script` (10 archivos) | Soporte de encendido/apagado en `Idle()`, persistencia de foco en `Raise()` y `Lower()`. |
| `tools/generate_flashlight_mod.py` | Generador automatizado de código de linterna montada. |
| `tools/validate_flashlight_mod.py` | Validador sintáctico para scripts de armas. |
| `tools/build_flashlight_mod.py` | Compilador y sincronizador de `pak004_weapon_flashlight.pk4`. |
| `mod/tfphobos/pak004_weapon_flashlight.pk4` | Paquete compilado de distribución y respaldo (38.53 KB). |
| `F:\...\tfphobos\pak004_weapon_flashlight.pk4` | Paquete instalado en el directorio del juego Steam. |
| `mod/tfphobos/autoexec.cfg` y `DoomConfig.cfg` | Asignación de `bind "f" "_button5"`. |

---

## 3. Pruebas y Verificación

- [x] **Validación Sintáctica:** Todos los 11 scripts de armas pasaron la validación de llaves y comillas (`tools/validate_flashlight_mod.py`).
- [x] **Validación de Defs:** Todos los 10 archivos `.def` validados con balance de llaves y parámetros de proyector.
- [x] **Construcción y Empaquetado:** Paquete `pak004_weapon_flashlight.pk4` (38.53 KB) generado exitosamente e instalado en `tfphobos/` y sincronizado en `mod/tfphobos/`.
- [x] **Configuración de Tecla:** Verificado que `autoexec.cfg` y `DoomConfig.cfg` tienen `bind "f" "_button5"`.
- [x] **Aislamiento Modular:** El paquete `pak004` opera en paralelo con `pak003_skipcinematics.pk4` sin conflictos.
- [x] **Hotfix Sintaxis en `weapon_pistol.script`:** Corregida inserción de comprobación `_BUTTON5` dentro del bucle de `Idle2()` en lugar de fuera de la función, eliminando el error del compilador `"if" is not a type`.
- [x] **Hotfix Declaración `WEAPON_NETFIRING` en `weapon_base.script`:** El parche 1.3 de Doom 3 (`pak006.pk4`) introdujo soporte de red con la bandera `WEAPON_NETFIRING`, referenciada por `weapon_chainsaw.script`. Se agregó `boolean WEAPON_NETFIRING;` a `object weapon_base` en `src_flashlight/script/weapon_base.script`, eliminando el error fatal `Unknown value "WEAPON_NETFIRING"`. Reconstruido `pak004_weapon_flashlight.pk4` (38.53 KB) y sincronizado en Steam y `mod/tfphobos/`.
- [x] **Hotfix Ámbito de Macro `_BUTTON5` en `weapon_shotgun_double.script` (`d3xp_main.script`):** En idTech 4, las macros `#define` son locales a cada archivo de compilación principal (`CompileFile`). El arma doble cañón (`weapon_shotgun_double.script`) se compila dentro de `d3xp_main.script` en una sesión de análisis separada de `doom_main.script`, donde la macro `_BUTTON5` de `weapon_base.script` no existía en el preprocesador. Se implementó una guarda `#ifndef _BUTTON5` en la cabecera de todos los scripts de armas en `src_flashlight/script/`, garantizando que `_BUTTON5` esté disponible en cualquier unidad de compilación. Reconstruido `pak004_weapon_flashlight.pk4` (38.99 KB) y sincronizado.

