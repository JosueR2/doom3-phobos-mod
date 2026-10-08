# Walkthrough - Soporte de Subtítulos en Español y Configuración de Tamaño de Texto

## 1. Resumen de la Implementación
Se ha implementado el soporte completo de localización al español para todos los diálogos de *Doom 3: Phobos*, junto con la capacidad de ajustar el tamaño de fuente de los subtítulos desde el menú de opciones del juego.

---

## 2. Componentes Implementados

### 2.1 Menú de Opciones (`GameButton.pd`)
- **Ruta:** `guis/mainmenu/Options/GameButton.pd`
- **Controles agregados:**
  - **Subtitle Language (`g_subLang`):** Opciones `English` y `Español`.
  - **Subtitle Size (`g_subSize`):** Opciones `Normal` (`0.275`), `Grande` (`0.35`) y `Muy Grande` (`0.43`).
- **Codificación:** Latin-1 con byte `0xF1` (`ñ`) para renderizado nativo correcto.

### 2.2 GUI Adaptativa de Subtítulos (`subtitles.gui`)
- **Ruta:** `guis/subtitles.gui`
- **Sincronización en tiempo real:** Dispone de un `editDef SizeSync` vinculado a la cvar `g_subSize` con `liveUpdate 1`, actualizando la variable `gui::sub_scale`.
- **Compatibilidad de Pantallas:** Soporte para todas las relaciones de aspecto soportadas por el motor:
  - 4:3 (`Subtitles_4_3`)
  - 16:9 (`Subtitles_16_9`)
  - 16:10 (`Subtitles_16_10`)
  - 21:9 (`Subtitles_21_9`)
- **Cajas de texto ampliadas:** Altura de caja aumentada de 80 a 95 píxeles para acomodar textos en fuentes grandes (`0.43`) sin desbordamientos.

### 2.3 Sistema de Localización (`phobos_subtitles_es.script`)
- **Ruta:** `script/phobos_subtitles_es.script`
- **Traducción integral:** 1,372 líneas de diálogo traducidas y optimizadas, 100% compatibles con Latin-1 y los glifos de la fuente del juego (`á`, `é`, `í`, `ó`, `ú`, `ñ`, `¿`, `¡`).
- **Nombres de personajes traducidos:** Normalización de los 25 hablantes del juego (e.g., `Tour Guide` -> `Guía Turístico`, `Girl` -> `Chica`, `Guy` -> `Sujeto`, `FCE Soldier` -> `Soldado de la FCE`, `Captain Rigel` -> `Capitán Rigel`, `PA` -> `Megafonía`).
- **Despacho por mapa:** 21 funciones modulares `LocalizeSubtitle_<map>` y `PhobosShowSubtitle_<map>` para garantizar compilación instantánea y cero impacto en el rendimiento.

### 2.4 Integración en Mapas
- Los 26 scripts de mapa del juego se han actualizado para canalizar los subtítulos a través de `PhobosShowSubtitle_<map>`.
- Preserva al 100% el soporte para saltar cinemáticas con la barra espaciadora (`SPACE`) y la tecla `X`.

---

## 3. Verificación y Empaquetado
- **Validación de scripts:** 28 scripts analizados con balance estricto de llaves (`{}`), paréntesis (`()`) y comillas (`""`).
- **Paquete compilado:** `F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak003_skipcinematics.pk4` (290.46 KB, 30 archivos).

