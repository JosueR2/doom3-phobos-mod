# Walkthrough: Skip de Cinemáticas Capítulo 1 (Escáner Médico & Hospital)

## 1. Resumen de la Implementación

Extendimos el sistema de omisión de cinemáticas para cubrir todas las cinemáticas principales del Capítulo 1 de *Doom 3: Phobos*:
1. **Prólogo / Intro de e1m1** (`map_intro.script` y `map_e1m1.script`).
2. **Escáner Médico en e1m1** (`map_e1m1_scanner.script`).
3. **Flashback del Hospital en e1m1_1** (`map_e1m1_1.script`).

Todo el sistema está unificado bajo la misma función global en `phobos_main.script`:
```c
void SkipIntro()
{
	if (map_intro::introActive == 1)
	{
		map_e1m1::SkipIntroSequence();
		return;
	}

	if (map_e1m1::scannerActive == 1 && map_e1m1::canSkipScanner == 1)
	{
		map_e1m1::SkipScannerSequence();
		return;
	}

	if (map_e1m1_1::hospitalActive == 1 && map_e1m1_1::canSkipHospital == 1)
	{
		map_e1m1_1::SkipHospitalSequence();
		return;
	}
}
```

---

## 2. Detalle de Cinemáticas Añadidas

### A. Escáner Médico de e1m1 (`script/map_e1m1_scanner.script`)
- **Comportamiento original:** El jugador se acuesta en la camilla (`BoardScanner`), la cámara pasa a modo cinemático en primera persona (`$scanner_camera`), los anillos giran, luces y efectos parpadean, y al cabo de ~30 segundos se carga el siguiente nivel (`$target_endlevel_1`).
- **Comportamiento con el Mod:**
  - Al acostarse, se inicia un temporizador de 1.5s (`EnableScannerSkipTimer`).
  - Aparece el mensaje: `[ Press SPACE or X to skip ]`.
  - Al presionar **`ESPACIO`** o **`X`**, se cancelan los hilos activos del escáner, se apaga la cámara y los sonidos, y se dispara de inmediato el teleport y transición al siguiente nivel (`$target_endlevel_1`).

### B. Flashback del Hospital en e1m1_1 (`script/map_e1m1_1.script`)
- **Comportamiento original:** Al comenzar el mapa `e1m1_1`, arranca `StartHospitalScene()` con `$hospitalCamera` activa en el vestíbulo del hospital, esperando diálogos y fades antes de devolver el control y habilitar el timbre de recepción (`$CounterBell`).
- **Comportamiento con el Mod:**
  - A los 1.5s de iniciar la escena aparece: `[ Press SPACE or X to skip ]`.
  - Al presionar **`ESPACIO`** o **`X`**, se desactiva `$hospitalCamera`, se limpian los subtítulos y sonidos de fondo, se reactiva el control en primera persona y se habilita el timbre (`$CounterBell.setKey("item_disabled", "0")`), permitiendo al jugador continuar jugando sin esperar la cinemática.

---

## 3. Archivos Modificados e Instalados
- `src/script/map_e1m1_scanner.script`: Variables `scannerActive`, `canSkipScanner`, función `SkipScannerSequence()`.
- `src/script/map_e1m1_1.script`: Variables `hospitalActive`, `canSkipHospital`, función `SkipHospitalSequence()`.
- `src/script/phobos_main.script`: Función global `void SkipIntro()` que delega según la escena activa.
- `src/script/map_e1m1.script`: Limpieza de declaración local para evitar duplicados con `phobos_main.script`.
- `tfphobos/pak003_skipcinematics.pk4`: Compilado y desplegado (24.18 KB).

