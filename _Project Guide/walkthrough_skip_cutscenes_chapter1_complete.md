# Walkthrough: Skip de Cinemáticas Capítulo 1 Completo (e1m1, e1m1_1, e1m3, e1m3 Outro)

## 1. Resumen de Cinemáticas Soportadas

El mod ahora cubre de forma integral **todas las cinemáticas principales del Capítulo 1 / Episodio 1 de Doom 3: Phobos**:

| Mapa | Script | Secuencia | Duración Original | Comportamiento al Saltar con `SPACE` o `X` |
| :--- | :--- | :--- | :--- | :--- |
| **Prólogo / e1m1** | `map_intro.script` / `map_e1m1.script` | Intro inicial, viaje de la caja y pesadilla | ~60 s | Teletransporta a la habitación de Marte, otorga la PDA y deja al jugador listo. |
| **e1m1** | `map_e1m1_scanner.script` | Escáner médico de Dr. Nielsen (`BoardScanner`) | ~30 s | Detiene anillos, luces y sonidos; carga directamente el nivel `e1m1_1`. |
| **e1m1_1** | `map_e1m1_1.script` | Secuencia completa de memoria del Hospital y despertar del escáner | > 5 min | Cancela toda la cadena onírica de memorias (lobby, pasillos, jardín, incinerador de ataúd) y el despertar en la camilla; teletransporta al jugador directamente a la enfermería de Marte (`info_player_teleport_3`), desbloquea la puerta, activa la salida del Dr. Nielsen y restaura el control y velocidad de movimiento normales. |
| **e1m3** | `map_e1m3.script` | Despegue del Hangar FCE & Pre-Outro (`fce_departure`) | ~35 s | Salta las cámaras de despegue y teletransporta directo a la sala final de outro. |
| **e1m3 Outro**| `map_e1m3_outro.script` | Escena de la caja y créditos finales (`PlaceBox`) | > 4 min | Detiene los diálogos/cámaras y dispara la pantalla final de fin de episodio (`$EndEpisodeOne`). |

---

## 2. Unificación Global (`phobos_main.script`)
Cualquiera de estas secuencias se salta exactamente con el mismo botón (**`ESPACIO`** o **`X`**). `phobos_main.script` detecta en qué escena te encuentras y ejecuta el salto seguro correspondiente:

```c
void SkipIntro()
{
	// 1. Prologue / e1m1 Intro
	if (map_intro::introActive == 1)
	{
		map_e1m1::SkipIntroSequence();
		return;
	}

	// 2. e1m1 Medical Scanner
	if (map_e1m1::scannerActive == 1 && map_e1m1::canSkipScanner == 1)
	{
		map_e1m1::SkipScannerSequence();
		return;
	}

	// 3. e1m1_1 Hospital Scene
	if (map_e1m1_1::hospitalActive == 1 && map_e1m1_1::canSkipHospital == 1)
	{
		map_e1m1_1::SkipHospitalSequence();
		return;
	}

	// 4. e1m3 Departure & Pre-Outro Hangar Cutscene
	if (map_e1m3::departureActive == 1 && map_e1m3::canSkipDeparture == 1)
	{
		map_e1m3::SkipDepartureSequence();
		return;
	}

	// 5. e1m3 Outro / Episode 1 Ending & Credits
	if (map_e1m3_outro::outroActive == 1 && map_e1m3_outro::canSkipOutro == 1)
	{
		map_e1m3_outro::SkipOutroSequence();
		return;
	}
}
```

---

## 3. Estado de la Instalación
- Todos los scripts verificados sin errores de llaves ni sintaxis.
- Compilado e instalado en:
  `F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak003_skipcinematics.pk4` (40.76 KB).

