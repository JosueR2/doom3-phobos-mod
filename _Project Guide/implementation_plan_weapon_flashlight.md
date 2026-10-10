# Implementation Plan - Weapon-Mounted Flashlight Mod for Doom 3: Phobos (`pak004_weapon_flashlight.pk4`)

## 1. Objetivo
Implementar un paquete complementario modular (`pak004_weapon_flashlight.pk4`) para *Doom 3: Phobos* que proporcione linterna montada funcional en todas las armas del juego (Pistola, Escopeta, Super Escopeta / Doble Cañón, Ametralladora, Cañón de Cadena, Pistola de Plasma, Lanzacohetes, BFG, Granadas y Puños), conmutable mediante la tecla `F` (`_button5`), preservando al 100% el balance de armas, cadencias de tiro, animaciones y compatibilidad con los scripts de Phobos sin generar colisiones ni crasheos.

---

## 2. Estado Actual Relevante
- El mod externo de Doom 3 base (`zzzz_pak105.pk4`) causaba un crash fatal al inicio del motor en Phobos (`Type mismatch on redeclaration of on` en `ai_monster_demon_imp_archspawn.script:158`) debido a una variable global `boolean on` mal estructurada.
- El usuario eliminó `zzzz_pak105.pk4` del juego base para evitar conflictos globales.
- Las armas nativas de Phobos residen en `tfphobos/pak000.pk4`, `pak001.pk4` y `pak002.pk4`, por lo que requieren definiciones actualizadas en la jerarquía de paquetes de Phobos para recibir los parámetros del proyector dinámico (`mtr_flashShader`, `flashTarget`, `flashAngle`, etc.).

---

## 3. Problema que se Pretende Resolver
- El jugador no puede iluminar el entorno mientras empuña sus armas de fuego en *Doom 3: Phobos*, viéndose forzado a alternar continuamente entre el arma y la linterna de mano en escenarios oscuros.
- La solución debe funcionar de forma nativa en Phobos sin interferir con los scripts de campaña ni con el paquete `pak003_skipcinematics.pk4`.

---

## 4. Solución Propuesta

### A. Paquete Modular Independiente (`pak004_weapon_flashlight.pk4`)
- Crear la estructura fuente en `src_flashlight/`:
  - `def/` con las definiciones de armas actualizadas.
  - `script/` con los scripts de armas modificados para responder a `_BUTTON5`.
- Compilar automáticamente en `tfphobos/pak004_weapon_flashlight.pk4` y sincronizar en `mod/tfphobos/`.

### B. Lógica del Sistema de Linterna (`script/weapon_base.script`)
- Declarar la variable global segura:
  ```c
  #define _BUTTON5 ( getOwner() ).getButtons() & 32
  boolean dfm_flashlight_on;
  ```
- Añadir el método base de alternancia:
  ```c
  void weapon_base::ToggleOnOff() {
      dfm_flashlight_on = !dfm_flashlight_on;
      startSound( "snd_click", SND_CHANNEL_ITEM, true );
      flashlight( dfm_flashlight_on );
      wait( 0.2 );
      weaponState( "Idle", 3 );
  }
  ```
- En cada script de arma (`weapon_pistol.script`, `weapon_shotgun.script`, `weapon_shotgun_double.script`, `weapon_machinegun.script`, `weapon_chaingun.script`, `weapon_plasmagun.script`, `weapon_rocketlauncher.script`, `weapon_bfg.script`, `weapon_handgrenade.script`, `weapon_fists.script`):
  - En `Raise()`: `flashlight( dfm_flashlight_on );`
  - En `Lower()`: `flashlight( dfm_flashlight_on );`
  - En el bucle de `Idle()`:
    ```c
    if ( _BUTTON5 ) {
        weaponState( "ToggleOnOff", 3 );
    }
    ```

### C. Parámetros del Foco de Luz en `.def`
- En cada `entityDef weapon_*`, configurar el foco dinámico con el shader oficial de alta calidad de idTech 4 (`lights/flashlight5`):
  ```
  "mtr_flashShader"   "lights/flashlight5"
  "flashColor"        "1 1 1"
  "flashRadius"       "400"
  "flashAngle"        "18.0"
  "flashTarget"       "1380 0 0"
  "flashUp"           "0 480 0"
  "flashRight"        "0 0 -480"
  "flashPointLight"   "0"
  "snd_click"         "player_pistol_empty"
  ```

### D. Configuración de Entrada (`autoexec.cfg` y `DoomConfig.cfg`)
- Asignar `bind "f" "_button5"` para que al pulsar `F` mientras se sostiene cualquier arma, se active instantáneamente la señal de alternancia de linterna montada.

---

## 5. Archivos Modificados / Creados
1. `src_flashlight/def/weapon_*.def` (Pistol, Shotgun, Double Shotgun, Machinegun, Chaingun, Plasmagun, Rocketlauncher, BFG, Fists, Grenade).
2. `src_flashlight/script/weapon_base.script` y `src_flashlight/script/weapon_*.script`.
3. `tools/build_flashlight_mod.py` (Script de empaquetado y sincronización de `pak004`).
4. `mod/tfphobos/autoexec.cfg`, `F:\...\tfphobos\autoexec.cfg` y `DoomConfig.cfg` (`bind "f" "_button5"`).
5. `pak004_weapon_flashlight.pk4` generado en Steam y respaldado en `mod/tfphobos/`.

---

## 6. Flujo de Implementación
1. Crear el árbol de trabajo `src_flashlight/` con base en los archivos extraídos de Phobos.
2. Inyectar los parámetros de foco en los 10 archivos `.def` de armas.
3. Inyectar `ToggleOnOff`, `_BUTTON5` y la persistencia de linterna en los 11 archivos `.script` de armas.
4. Actualizar `bind "f" "_button5"` en los archivos de configuración.
5. Crear el script de build `tools/build_flashlight_mod.py`.
6. Compilar `pak004_weapon_flashlight.pk4`, verificar integridad y sincronizar con `mod/tfphobos/`.
7. Actualizar `work_plan.md` y documentar en `walkthrough_weapon_flashlight.md`.

---

## 7. Estrategia de Verificación
- Verificación sintáctica con `validate_scripts.py`.
- Inspección de archivo `.pk4` para asegurar que contenga todos los defs y scripts.
- Verificación de asignación de tecla `F` a `_button5`.

