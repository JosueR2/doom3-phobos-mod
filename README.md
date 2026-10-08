# Doom 3: Phobos Mod - Subtítulos en Español & Salto de Cinemáticas

Mod para el juego standalone **Doom 3: Phobos** que añade localización completa al español para todos los diálogos del juego, opciones de configuración de idioma y tamaño de texto en el menú, y la capacidad de saltar cinemáticas no interactivas.

---

## Características

1. **Subtítulos 100% en Español:**
   - 1,372 líneas de diálogo traducidas y adaptadas al español a lo largo de los 26 mapas y escenas del juego.
   - Nombres de personajes y roles normalizados (`Chica`, `Sujeto`, `Guía Turístico`, `Soldado de la FCE`, `Megafonía`, etc.) conservando nombres propios (`Samantha Miles`, `Dr. Nielsen`, `Calloway`, etc.).
   - Caracteres especiales acentuados (`á`, `é`, `í`, `ó`, `ú`, `ñ`, `¿`, `¡`) formateados para compatibilidad total con la fuente nativa del motor.

2. **Opciones en el Menú (`Options -> Game`):**
   - **Subtitle Language:** Selector para cambiar entre `English` y `Español` al instante (cvar `g_subLang`).
   - **Subtitle Size:** Selector para ajustar el tamaño de texto (`Normal`, `Grande`, `Muy Grande`) (cvar `g_subSize`).

3. **GUI Adaptativa y Escalado Dinámico:**
   - Soporte para todas las relaciones de aspecto del motor: **4:3**, **16:9**, **16:10** y **21:9 Ultra-Wide**.
   - Cajas de texto ampliadas para evitar recortes al usar fuentes grandes.
   - Sincronización en tiempo real sin requerir reinicio del mapa.

4. **Salto de Cinemáticas (Skip Cutscenes):**
   - Salto instantáneo de secuencias no interactivas pulsando la barra espaciadora (`SPACE`) o la tecla `X`.
   - Soporte para el prólogo / introducción de e1m1, escáner médico, secuencia de memoria del hospital e1m1_1, despegue en el hangar de e1m3 y escena de outro/créditos de e1m3.

---

## Instalación

### Método Rápido (Recomendado)
1. Descarga o clona este repositorio.
2. Copia la carpeta `mod/tfphobos` directamente en el directorio principal de tu instalación de **Doom 3: Phobos** (donde se encuentra `Doom3phobos.exe`, usualmente en `SteamLibrary\steamapps\common\Doom 3 Phobos\`).
3. Si el sistema te pregunta si deseas combinar o reemplazar archivos, confirma.
4. Inicia el juego.

### Método Manual (Solo archivos esenciales)
Copia los siguientes dos archivos dentro de la carpeta `tfphobos/` de tu juego:
- `mod/tfphobos/pak003_skipcinematics.pk4`
- `mod/tfphobos/autoexec.cfg`

---

## Estructura del Repositorio

```text
├── mod/
│   ├── INSTRUCCIONES_INSTALACION.txt
│   └── tfphobos/
│       ├── pak003_skipcinematics.pk4     # Paquete maestro del mod compilado
│       ├── autoexec.cfg                  # Configuración de teclas y cvars
│       ├── guis/                         # Archivos de interfaz de usuario modificados
│       └── script/                       # Scripts idScript modificados
├── src/                                  # Código fuente de desarrollo (guis, scripts)
├── tools/                                # Herramientas en Python para extracción, traducción y empaquetado
├── _Project Guide/                       # Documentación técnica, planes de trabajo e historial
├── extracted_subtitles.json              # Subtítulos extraídos del juego original
└── translated_subtitles.json             # Base de datos de traducciones al español
```

---

## Créditos y Licencia
Desarrollado para la comunidad de *Doom 3: Phobos*. Los archivos originales pertenecen al equipo de desarrollo de *Team Future* y *id Software*.
