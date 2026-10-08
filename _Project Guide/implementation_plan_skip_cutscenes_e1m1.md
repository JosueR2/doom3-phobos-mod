# Implementation Plan - Skip Cutscenes en Doom 3: Phobos (Capítulo 1 / e1m1)

## 1. Objetivo
Implementar un mecanismo que permita al jugador saltar ("skip") la cinemática/secuencia introductoria del Capítulo 1 (Prólogo / `ep1/e1m1`) en *Doom 3: Phobos*, pulsando un botón (barra espaciadora, botón de disparo/acción o tecla asignada), pasando inmediatamente al inicio de la jugabilidad en Marte.

---

## 2. Estado Actual Relevante
- En `Doom 3: Phobos`, al iniciar el juego en el Capítulo 1 / Prólogo (`ep1/e1m1`), la función `map_e1m1::main()` llama a `StartIntro()`.
- `StartIntro()` dispara `map_intro::Gogo()`, una secuencia cinemática e interactiva que dura varios minutos (escena en la Tierra, habitación, diálogo con Lee, descenso por el túnel azul).
- Al concluir la cinemática, la función `map_e1m1::EndBoxTrip()` prepara la habitación de Marte, teletransporta al jugador a `info_player_teleport_4`, desactiva la cámara cinemática (`box_postscene_camera`) y entrega el control normal al jugador en primera persona.
- Actualmente no existe ningún mecanismo para omitir esta escena, obligando a esperar o jugar toda la secuencia cada vez que se inicia partida o se quiere probar el nivel.

---

## 3. Problema que se Pretende Resolver
Evitar la pérdida de tiempo y la rigidez de tener que visualizar secuencias cinemáticas largas cuando el jugador ya las conoce o desea iniciar directamente la acción.

---

## 4. Solución Propuesta

### 4.1. Detección de Entrada del Jugador (Botón de Skip)
- En id Tech 4 script, `$player1.getButtons()` devuelve una máscara de bits correspondiente a los botones presionados en el comando de usuario actual (`_attack`, `_moveUp` [salto], `_button2` [usar], etc.).
- Iniciar un hilo en segundo plano (`thread WatchSkipIntro()`) al arrancar la cinemática.
- Si `$player1.getButtons() != 0` (el jugador presiona cualquier botón de acción como Espacio o Click):
  1. Se marca la bandera global `skipIntroDone = 1`.
  2. Se cancela el hilo de la cinemática (`sys.killthread("phobos_intro_thread")`).
  3. Se ejecuta `SkipIntroNow()`.

### 4.2. Función `SkipIntroNow()`
Para asegurar que el estado del mundo y del jugador quede 100% consistente y listo para jugar sin bugs:
1. Limpiar subtítulos en pantalla: `sys.hideSubtitles()`.
2. Restaurar la visibilidad y quitar cualquier pantalla negra: `sys.fadeTo('0 0 0', 0, 0.2)`.
3. Detener sonidos y música de la cinemática inicial si estuvieran sonando.
4. Teletransportar al jugador a su destino inicial en Marte: `sys.trigger($info_player_teleport_4)`.
5. Devolver la vista al jugador: desactivar la cámara (`sys.trigger($box_postscene_camera)` o `sys.setCamera($player1)`).
6. Disparar el PDA inicial: `sys.trigger($trigger_relay_69)`.
7. Ajustar la alarma/iluminación post-llegada como lo hace normalmente `EndBoxTrip()`.

### 4.3. Empaquetado Limpio y Reversible (Arquitectura PK4)
- Los archivos modificados (`script/map_e1m1.script`, etc.) se compilan dentro de un archivo `.pk4` titulado:
  `F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak003_skipcinematics.pk4`
- id Tech 4 carga los archivos `.pk4` alfabéticamente. Dado que el último archivo oficial es `pak002.pk4`, `pak003_skipcinematics.pk4` tendrá la máxima prioridad de carga.
- Los archivos originales del juego (`pak000.pk4`, `pak001.pk4`, `pak002.pk4`) permanecen intactos. Si se desea desinstalar el mod en cualquier momento, basta con borrar o renombrar `pak003_skipcinematics.pk4`.

---

## 5. Archivos Modificados / Creados

| Archivo | Ubicación | Tipo de Cambio |
| :--- | :--- | :--- |
| `script/map_e1m1.script` | Empaquetado en `pak003_skipcinematics.pk4` | Modificado: Incorpora `WatchSkipIntro()`, `SkipIntroNow()` y lanzamiento en hilo separado de `Gogo()` |
| `pak003_skipcinematics.pk4` | `F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\` | Creado: Paquete del mod |
| `_Project Guide/work_plan.md` | `E:\MisApps\Reverse\doom3phobos\_Project Guide/` | Actualizado: Registro del estado y avance del proyecto |

---

## 6. Dependencias
- Motor `id Tech 4` de Doom 3 Phobos.
- Herramienta Python nativa para compilar archivos ZIP/PK4 sin requerir software externo.

---

## 7. Flujo de Implementación
1. Extraer la versión base de `script/map_e1m1.script` desde `pak002.pk4`.
2. Agregar la lógica de detección de salto `WatchSkipIntro()`, etiquetado de hilo `sys.threadname("phobos_intro_thread")` y la rutina de salto seguro `SkipIntroNow()`.
3. Empaquetar el script en `pak003_skipcinematics.pk4` en `tfphobos`.
4. Verificar sintaxis del script.
5. Invitar al usuario a iniciar una nueva partida en el Capítulo 1 y probar la pulsación de la tecla de acción.

---

## 8. Consideraciones de Seguridad y Rendimiento
- **Rendimiento:** El hilo observador `WatchSkipIntro()` duerme `0.05` segundos entre lecturas (`sys.wait(0.05)`), consumiendo 0% de CPU. Una vez finalizada o saltada la cinemática, el hilo finaliza inmediatamente.
- **Seguridad e Integridad:** Los archivos originales del juego nunca se sobreescriben ni alteran.

---

## 9. Estrategia de Pruebas y Verificación
1. Validar la estructura del `.pk4` generado mediante script de inspección.
2. Iniciar el juego en Capítulo 1 / Prólogo.
3. Al comenzar la cinemática de introducción, presionar la barra espaciadora o botón de disparo.
4. Comprobar que:
   - La pantalla se desvanece de inmediato hacia la habitación de Marte.
   - El jugador aparece en la posición correcta frente a la cama/mesa.
   - La cámara vuelve al control en primera persona.
   - Las interacciones y el PDA funcionan normalmente.

---

## 10. Posibles Riesgos y Mitigaciones
- **Riesgo:** Si un trigger dependiente no se dispara, el nivel podría quedar bloqueado.
- **Mitigación:** `SkipIntroNow()` replica exactamente las acciones finales de `EndBoxTrip()` y dispara `trigger_relay_69` y los activadores correspondientes, asegurando la continuidad de la trama.

