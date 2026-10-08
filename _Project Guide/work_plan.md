# Work Plan - Doom 3: Phobos Modding

## 1. Ficha Técnica & Metadatos del Proyecto

| Parámetro | Detalle |
| :--- | :--- |
| **Proyecto** | Doom 3: Phobos Modding (Skip Cutscenes Mod) |
| **Motor** | id Tech 4 (Doom 3 modified engine) |
| **Ubicación del Juego** | `F:\SteamLibrary\steamapps\common\Doom 3 Phobos` |
| **Carpeta del Mod Activo** | `tfphobos` |
| **Estado Actual** | Fase 1 - Planificación e Inspección Inicial |
| **Versión del Mod** | `v0.1.0-dev` |
| **Pila Tecnológica** | idScript (.script), idTech4 Defs (.def), idTech4 GUIs (.gui), PK4 packaging |
| **Historial** | `_Project Guide/work_plan_history.md` (no aplica aún) |

---

## 2. Objetivo General & Arquitectura

### Objetivo General
Permitir al jugador saltar ("skip") las cinemáticas y secuencias no interactivas en *Doom 3: Phobos*, comenzando por el Capítulo 1 (Prólogo / e1m1 y mapas subsecuentes), mediante la pulsación de un botón de acción (barra espaciadora, botón de disparo/uso o tecla configurada), restaurando inmediatamente el control y el estado del mapa sin romper el progreso de las misiones ni los triggers del nivel.

### Arquitectura Técnica
- **Sistema de Modding sin alterar archivos originales:** Los scripts modificados se empaquetarán en un archivo `.pk4` de alta prioridad (e.g. `pak003_skipcinematics.pk4` o carpeta `script/` en `tfphobos`), garantizando que la instalación sea 100% limpia y reversible.
- **Detección de Input:** Implementación de un hilo observador en idScript (`thread WatchSkipInput()`) que consulta `$player1.getButtons()` o monitorea el botón de salto durante las secuencias de cámara (`sys.setCamera` / `$camera`).
- **Control de Flujo y Limpieza de Cinemática:** Al recibir la señal de salto:
  1. Detener threads de cinemática (`sys.killthread(...)` o señales de interrupción).
  2. Forzar fade de pantalla a normal (`sys.fadeTo('0 0 0', 0, 0.1)`).
  3. Devolver la cámara al jugador (`sys.setCamera($player1)` o disparar toggle de cámara).
  4. Sincronizar el estado del mundo (teleport a posición post-cinemática, desbloqueo de puertas, triggers de continuación).

### Regla Obligatoria de Sincronización y Respaldo ('mod/')
**La IA DEBE mantener siempre sincronizada la carpeta `mod/` (`mod/tfphobos/`) con copias actualizadas de todos los archivos y carpetas modificados o añadidos:**
- **Contenido obligatorio en `mod/tfphobos/`:**
  1. `pak003_skipcinematics.pk4` (paquete principal compilado del mod).
  2. `autoexec.cfg` (configuraciones de cvars y enlaces de teclas).
  3. `guis/` (todos los archivos y subcarpetas de interfaz modificados).
  4. `script/` (todos los archivos idScript modificados del mod).
  5. `mod/INSTRUCCIONES_INSTALACION.txt` (instrucciones claras de instalación).
- **Protocolo de Sincronización:**
  Cada vez que se realicen cambios, correcciones o adiciones en el código fuente (`src/`, scripts, GUIs o configuraciones), la IA **DEBE ejecutar `tools/build_mod.py`** o copiar inmediatamente los archivos modificados a `mod/tfphobos/`.
  Esto garantiza que la carpeta `mod/` siempre esté lista para ser compartida con otros jugadores y funcione como respaldo ante posibles actualizaciones de Steam.

---

## 3. Resumen de Fases

- [x] **Fase 0: Auditoría de Herramientas, MCPs y Skills** — Conexiones verificadas, skills identificados (`game-modding`, `game-modding-debug`, `game-mod-assets`).
- [x] **Fase 1: Análisis e Implementación de Skip para la Cinemática de Inicio (Capítulo 1 / e1m1)** — Completada e instalada en `pak003_skipcinematics.pk4`.
- [x] **Fase 2: Pruebas en Vivo con el Usuario y Ajustes de Sensibilidad / Tecla** — Completada con éxito (salto con SPACE / X probado y validado por el usuario).
- [x] **Fase 3: Soporte para Secuencias Adicionales del Capítulo 1 (Escáner Médico e1m1 y Hospital e1m1_1)** — Implementada y empaquetada.
- [x] **Fase 4: Expansión a Cinemáticas Finales del Episodio 1 (e1m3 Despegue Hangar y e1m3 Outro / Créditos)** — Implementada y empaquetada en `pak003_skipcinematics.pk4` (40.76 KB).
- [x] **Fase 5: Soporte de Subtítulos en Español y Configuración de Tamaño de Texto** — 1,372 líneas de diálogo traducidas a español, controles de idioma (`g_subLang`) y tamaño (`g_subSize`) en el menú del juego, soporte en 26 scripts de mapa y GUI con escalado adaptativo (290.46 KB).
- [ ] **Fase 6: Expansión de Saltos de Cinemáticas a Capítulos Subsecuentes (Episodio 2 / e1m3_1, e1m4, e1m5)** — Próxima fase disponible.

---

## 4. Fase Activa & Tareas Pendientes

### Fase 5: Soporte de Subtítulos en Español y Configuración de Tamaño (Completada)
- [x] Extraer las 1,372 líneas de diálogo únicas a través de los 26 scripts de mapa del juego.
- [x] Traducir y pulir las 1,372 líneas al español garantizando nombres propios (Samantha Miles, Dr. Nielsen, etc.) y compatibilidad Latin-1 con la fuente del juego.
- [x] Integrar opciones de Idioma (`English` / `Español`) y Tamaño (`Normal` / `Grande` / `Muy Grande`) en `GameButton.pd`.
- [x] Crear `src/guis/subtitles.gui` con `editDef SizeSync` vinculado a `g_subSize` y escalado dinámico en las 4 relaciones de aspecto (4:3, 16:9, 16:10, 21:9).
- [x] Generar `script/phobos_subtitles_es.script` con traducción por mapa y normalización de nombres de hablantes.
- [x] Conectar los 26 scripts de mapas para despachar subtítulos a través de `PhobosShowSubtitle_<map>`.
- [x] Validar sintaxis idScript en todos los 28 scripts y empaquetar `pak003_skipcinematics.pk4` (290.46 KB).
- [x] Crear carpeta de distribución y respaldo `mod/` con estructura `tfphobos/` (PK4, autoexec.cfg, fuentes guis/ y script/) e instrucciones de instalación.




