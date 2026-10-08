# Plan de Implementación: Skip de Cinemáticas Capítulo 1 (Escáner Médico & Hospital)

## 1. Contexto & Diagnóstico
En la fase anterior logramos con éxito que la cinemática inicial del Prólogo (`map_intro.script` y `map_e1m1.script`) pueda saltarse limpiamente presionando `SPACE` o `X` tras un temporizador de protección de 2 segundos.

En el resto del Capítulo 1 existen dos cinemáticas obligatorias adicionales que bloquean al jugador:
1. **Escáner Médico de e1m1 (`script/map_e1m1_scanner.script`):**
   - Inicia cuando el jugador se acuesta en la camilla (`BoardScanner()`).
   - Activa `$scanner_camera`, mueve la camilla, enciende luces, gira los anillos (`StartScannerRings()`), reproduce sonidos prolongados y al finalizar activa `$target_endlevel_1` que carga el siguiente mapa (`e1m1_1`). Dura más de 25 segundos.
2. **Escena del Hospital en e1m1_1 (`script/map_e1m1_1.script`):**
   - Inicia al comenzar el mapa `e1m1_1` en `main()` -> `StartHospitalScene()`.
   - Activa `$hospitalCamera`, reproduce voces del flashback del hospital y luego devuelve la cámara a primera persona activando el timbre (`$CounterBell.setKey("item_disabled", "0")`).

Además, en `e1m1_1` se encuentra la salida del escáner (`ScannerSceneEnd()`), la cual se puede omitir o acelerar si el jugador lo desea.

---

## 2. Estrategia de Implementación Unificada

Para que las teclas `SPACE` y `X` sigan funcionando en cualquier mapa sin necesidad de cambiar los binds en `autoexec.cfg`, la función global `void SkipIntro()` delegará de manera segura según la cinemática que esté activa en ese momento:

```c
void SkipIntro()
{
    // Si estamos en e1m1 y el intro está activo:
    if (map_intro::introActive == 1) {
        map_e1m1::SkipIntroSequence();
        return;
    }
    // Si estamos en e1m1 y el escáner médico está activo:
    if (map_e1m1::scannerActive == 1 && map_e1m1::canSkipScanner == 1) {
        map_e1m1::SkipScannerSequence();
        return;
    }
    // Si estamos en e1m1_1 y la escena del hospital está activa:
    if (map_e1m1_1::hospitalActive == 1 && map_e1m1_1::canSkipHospital == 1) {
        map_e1m1_1::SkipHospitalSequence();
        return;
    }
}
```

---

## 3. Puntos Críticos y Sincronización del Estado del Nivel

### A. Escáner Médico (`map_e1m1_scanner.script` / `map_e1m1.script`)
- **Estado durante la cinemática:**
  - `scannerActive = 1`, `canSkipScanner = 0` (pasa a 1 tras 1.5s con mensaje `[ Press SPACE or X to skip ]`).
- **Al presionar Skip:**
  - Cancelar threads activos: `WarmupLights`, `ShutdownLights`, `StartScannerRings`, `AdjustScreenAlpha`, `MoveIntoScanner`, `RotateScannerBed`, `StartScanner`.
  - Apagar sonidos del escáner y ocultar subtítulos.
  - Si `$scanner_camera` está activa, desactivarla: `sys.trigger($scanner_camera)`.
  - Teletransportar al jugador al punto final: `sys.trigger($info_player_teleport_2)`.
  - Disparar transición de nivel: `sys.trigger($target_endlevel_1)`.

### B. Escena del Hospital (`map_e1m1_1.script`)
- **Estado durante la cinemática:**
  - `hospitalActive = 1`, `canSkipHospital = 0` (pasa a 1 tras 1.5s con mensaje `[ Press SPACE or X to skip ]`).
- **Al presionar Skip:**
  - Cancelar thread de la escena: `StartHospitalScene`.
  - Desactivar cámara si está activa: `sys.trigger($hospitalCamera)`.
  - Restaurar fade a pantalla normal: `sys.fadeTo('0 0 0', 0, 0.2)`.
  - Disparar triggers de estado del mapa:
    - `sys.trigger($m1_hospital_lobby);`
    - `sys.trigger($setinfluence_hospital);`
    - `$CounterBell.setKey("item_disabled", "0");` (habilita interactuar con el timbre para continuar la misión).
  - Ocultar subtítulos y detener sonidos residuales.

---

## 4. Verificación y Testing
1. Comprobación estática de sintaxis con `tools\validate_scripts.py`.
2. Empaquetado limpio en `pak003_skipcinematics.pk4` con `tools\build_mod.py`.
3. Prueba en el juego:
   - Jugar hasta el escáner médico de e1m1 y saltarlo con `SPACE` o `X`.
   - Iniciar `e1m1_1` (Hospital) y saltar la cinemática del vestíbulo con `SPACE` o `X`.

