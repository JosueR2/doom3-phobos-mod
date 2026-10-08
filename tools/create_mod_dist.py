import os
import shutil

def create_mod_folder():
    base_proj = r"E:\MisApps\Reverse\doom3phobos"
    src_dir = os.path.join(base_proj, "src")
    game_tfphobos = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos"
    mod_dir = os.path.join(base_proj, "mod")
    mod_tfphobos = os.path.join(mod_dir, "tfphobos")

    if os.path.exists(mod_dir):
        shutil.rmtree(mod_dir)
    os.makedirs(mod_tfphobos, exist_ok=True)

    # 1. Copy pk4 package
    pk4_src = os.path.join(game_tfphobos, "pak003_skipcinematics.pk4")
    if os.path.exists(pk4_src):
        shutil.copy2(pk4_src, os.path.join(mod_tfphobos, "pak003_skipcinematics.pk4"))
        print(f"Copied {os.path.basename(pk4_src)} to mod/tfphobos/")

    # 2. Copy autoexec.cfg
    cfg_src = os.path.join(game_tfphobos, "autoexec.cfg")
    if os.path.exists(cfg_src):
        shutil.copy2(cfg_src, os.path.join(mod_tfphobos, "autoexec.cfg"))
        print(f"Copied {os.path.basename(cfg_src)} to mod/tfphobos/")

    # 3. Copy unpacked folders guis and script
    shutil.copytree(os.path.join(src_dir, "guis"), os.path.join(mod_tfphobos, "guis"))
    print("Copied guis/ to mod/tfphobos/guis/")

    shutil.copytree(os.path.join(src_dir, "script"), os.path.join(mod_tfphobos, "script"))
    print("Copied script/ to mod/tfphobos/script/")

    # 4. Create README / Instructions in Spanish
    readme_path = os.path.join(mod_dir, "INSTRUCCIONES_INSTALACION.txt")
    readme_content = """================================================================================
  DOOM 3: PHOBOS - MOD DE SUBTITULOS EN ESPAÑOL & SALTO DE CINEMATICAS
================================================================================

Este paquete contiene todas las mejoras y parches desarrollados para Doom 3: Phobos:
1. Subtítulos 100% traducidos al Español (1,372 líneas de diálogo en todos los mapas).
2. Selector de idioma en el menú (Options -> Game -> Subtitle Language: English / Español).
3. Selector de tamaño de subtítulos (Options -> Game -> Subtitle Size: Normal / Grande / Muy Grande).
4. Escalado adaptativo de subtítulos para monitores 4:3, 16:9, 16:10 y 21:9 Ultra-Wide.
5. Salto inmediato de cinemáticas y escenas narrativas pulsando la BARRA ESPACIADORA (SPACE) o la tecla X.

--------------------------------------------------------------------------------
  INSTRUCCIONES DE INSTALACIÓN
--------------------------------------------------------------------------------

MÉTODO RECOMENDADO (Muy fácil):
1. Copia la carpeta 'tfphobos' que está dentro de esta carpeta 'mod'.
2. Pégala en el directorio principal de tu juego Doom 3: Phobos (donde se encuentra 'Doom3phobos.exe', usualmente en:
   SteamLibrary\\steamapps\\common\\Doom 3 Phobos\\)
3. Cuando Windows te pregunte si deseas combinar o reemplazar archivos, acepta.
4. ¡Listo! Inicia el juego.

MÉTODO DIRECTO (Dentro de tfphobos):
Si prefieres copiar solo los archivos esenciales:
1. Copia 'pak003_skipcinematics.pk4' y 'autoexec.cfg' dentro de la carpeta 'tfphobos' de tu juego.
2. ¡Listo! El archivo .pk4 tiene máxima prioridad de carga y contiene todos los scripts y GUIs del mod.

--------------------------------------------------------------------------------
  CÓMO USAR EN EL JUEGO
--------------------------------------------------------------------------------
1. Abre el juego y ve a Options -> Game.
2. En 'Subtitle Language' elige 'Español' para jugar en español (o 'English' para inglés).
3. En 'Subtitle Size' selecciona el tamaño que prefieras (Normal, Grande o Muy Grande).
4. Para saltar cualquier cinemática (como la introducción o escenas de diálogo pasadas), pulsa SPACE o la tecla X.

--------------------------------------------------------------------------------
  COMO RESPALDO CONTRA ACTUALIZACIONES DE STEAM
--------------------------------------------------------------------------------
Si Steam actualiza o verifica los archivos de Doom 3: Phobos en el futuro y se sobrescriben los cambios,
simplemente vuelve a copiar el contenido de esta carpeta 'mod' en el juego para restaurar todo al instante.
================================================================================
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"Created {readme_path}")

if __name__ == "__main__":
    create_mod_folder()
