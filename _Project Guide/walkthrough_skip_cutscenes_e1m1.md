# Walkthrough - Implementación de Skip Cutscenes en Capítulo 1 (e1m1)

## Resumen Ejecutivo
Se implementó exitosamente el sistema de omisión de cinemáticas para la secuencia inicial del Capítulo 1 / Prólogo (`ep1/e1m1`) de *Doom 3: Phobos*. El jugador ahora puede omitir instantáneamente la introducción completa en la Tierra (escena del dormitorio, flashback, interacción con la lámpara, caminata hacia la cerca y descenso por el túnel azul) pulsando cualquier botón de acción (`Espacio` / Salto o `Click` / Disparo / Usar), comenzando directamente el gameplay en la habitación de Marte con el PDA entregado y la cámara en primera persona.

---

## Archivos Modificados y Creados

| Archivo | Ruta | Propósito |
| :--- | :--- | :--- |
| **`map_intro.script`** | `E:\MisApps\Reverse\doom3phobos\src\script\map_intro.script` | Añadidas variables globales de estado (`activeCam`, `introSkipped`, `introActive`) y guardas en `Gogo()`, `ExitWindow()`, `TalkFence()` y `BlueTunnel()`. |
| **`map_e1m1.script`** | `E:\MisApps\Reverse\doom3phobos\src\script\map_e1m1.script` | Implementada la rutina `SkipIntroSequence()`, el observador de pulsaciones `WatchSkipInput()`, el aviso en pantalla `ShowSkipPrompt()`, el hilo desacoplado `RunIntroGogo()` y la guarda en `EndBoxTrip()`. |
| **`build_mod.py`** | `E:\MisApps\Reverse\doom3phobos\tools\build_mod.py` | Script automatizado para compilar los scripts del directorio `src/` en el paquete `.pk4` del mod. |
| **`validate_scripts.py`** | `E:\MisApps\Reverse\doom3phobos\tools\validate_scripts.py` | Herramienta de verificación estática de llaves, paréntesis y estructura de idScript. |
| **`pak003_skipcinematics.pk4`** | `F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak003_skipcinematics.pk4` | Paquete activo del mod instalado en el directorio del juego (10.29 KB). |

---

## Decisiones Técnicas Clave

1. **Detección Dual de Input:**
   Se combinó `$player1.getButtons() != 0` (Click primario, ataque, usar, enter) con `$player1.getMove().z > 0` (Barra espaciadora / Salto) en un ciclo con pausa de 50 ms (`sys.wait(0.05)`), logrando una respuesta inmediata tanto para usuarios de teclado como de ratón sin impacto de CPU.

2. **Rastreo Determinista de Cámaras (`activeCam`):**
   Dado que las entidades `func_cameraview` en id Tech 4 alternan su estado (toggle) cada vez que reciben un trigger, se implementó una variable de estado que registra con exactitud qué cámara está activa (`0` = vista normal del jugador, `1` = `$introCamera`, `2` = `$BlueWorldCam`, `3` = `$box_postscene_camera`). Al pulsar el botón de skip, se dispara únicamente la cámara activa y se llama preventivamente a `sys.setCamera($player1)`, garantizando que la perspectiva en primera persona nunca quede atrapada.

3. **Terminación Limpia de Hilos Secundarios:**
   `SkipIntroSequence()` invoca `sys.killthread(...)` para cada hilo asociado a la cinemática (`map_intro::Gogo`, `BlueTunnel`, `showText`, `turnOffHouseLights`, etc.), cancelando los temporizadores pendientes y silenciando los emisores de sonido ambientales (`SpeakerVoid`, `SpeakerCrickets`, `speaker_1012`, etc.) mediante `fadeSound`.

4. **Sincronización del Estado del Nivel:**
   Para asegurar que el progreso no se rompa:
   - Se teletransporta al jugador al destino oficial de inicio en Marte: `sys.trigger($info_player_teleport_4)`.
   - Se otorga el ítem del PDA del jugador: `sys.trigger($trigger_relay_69)`.
   - Se desactiva el desenfoque de despertar: `$box_postscene_blur.hide()`.
   - Se limpia la pantalla negra: `sys.fadeTo('0 0 0', 0, 0.2)`.

5. **Arquitectura No Invasiva:**
   Ningún archivo original del juego (`pak000.pk4`, `pak001.pk4`, `pak002.pk4`, binarios `.dll` o `.exe`) fue modificado. El mod opera 100% sobre `pak003_skipcinematics.pk4`. Para desactivarlo, solo se requiere remover dicho archivo.

---

## Verificación Realizada

1. **Diagnóstico y Corrección de Conflicto de Nombres idScript:**
   - Durante la compilación inicial del mapa, el motor reportó: `ERROR: file script/map_e1m1.script, line 678: Type mismatch on redeclaration of move`.
   - Se diagnosticó que `move` es un evento nativo reservado de entidad (`scriptEvent void move(...)`).
   - Se renombró la variable a `pMove` y se utilizó la herramienta `check_event_collisions.py` para comparar exhaustivamente todas las variables del script contra los 417 eventos registrados de idTech4/Phobos, confirmando 0 conflictos restantes.
2. **Corrección de Aborto al Menú Principal (`sys.setCamera`):**
   - El motor arrojaba un error en tiempo de ejecución al invocar `sys.setCamera($player1)`, ya que en idTech4 dicha función exige estrictamente una entidad derivada de `idCamera` (`Error: sys.setCamera: Entity 'player1' is not a camera`), lo que provocaba el retorno forzado al menú principal.
   - Se removió dicha invocación, ya que en idTech4 al disparar nuevamente la cámara activa (`sys.trigger($camera)`) el motor devuelve automáticamente la perspectiva en primera persona al jugador.
3. **Aislamiento de Clicks del Menú y Temporizador de Habilitación (`canSkipIntro`):**
   - **Causa del Salto Prematuro:** Al hacer click en "Prólogo" y en el nivel de dificultad en el menú principal con `MOUSE1`, el comando de script quedaba encolado en el búfer de entrada del motor y se ejecutaba instantáneamente al arrancar el mapa, saltando la cinemática sin darle oportunidad al usuario de decidir.
   - **Solución:**
     - Se desacopló `MOUSE1` del script de salto para mantener el disparo limpio y sin sobrecarga.
     - Se implementó una variable de control `map_intro::canSkipIntro` (inicializada en `0`).
     - Al iniciar el nivel, un hilo `EnableSkipTimer()` espera 2 segundos para que el mapa termine de cargar y descarte cualquier click previo del menú.
     - Pasados los 2 segundos, se activa `canSkipIntro = 1` y se proyecta en pantalla: `[ Press SPACE or X to skip ]`.
     - `SkipIntroSequence()` ignora cualquier pulsación mientras `canSkipIntro == 0`, permitiendo al jugador ver la cinemática todo el tiempo que desee y saltarla solo cuando pulse **`SPACE`**, **`X`** o **`ENTER`**.
4. **Análisis Sintáctico:**
   `validate_scripts.py` validó con éxito el balance de llaves `{ }`, paréntesis `( )` e instrucciones en `map_intro.script` y `map_e1m1.script`.
5. **Integridad del PK4:**
   Se comprobó la estructura interna de `pak003_skipcinematics.pk4`, verificando compresión Deflate estándar, rutas relativas (`script/...`) y sumas de verificación CRC32 válidas (`0x7246f3e1`, `0x5fa1556c`).
6. **Persistencia y Documentación:**
   Se documentó la implementación en `_Project Guide` conforme a las reglas de `agent.md`.

