# -*- coding: utf-8 -*-
import zipfile
import os
import sys
import shutil

def build():
    base_proj = r"E:\MisApps\Reverse\doom3phobos"
    src_dir = os.path.join(base_proj, "src_flashlight")
    game_tfphobos_dir = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos"
    output_pk4 = os.path.join(game_tfphobos_dir, "pak004_weapon_flashlight.pk4")
    
    if not os.path.exists(game_tfphobos_dir):
        print(f"Error: Target directory does not exist: {game_tfphobos_dir}")
        sys.exit(1)
        
    print(f"Building weapon flashlight mod package: {output_pk4}")
    
    with zipfile.ZipFile(output_pk4, 'w', compression=zipfile.ZIP_DEFLATED) as pk4:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, src_dir).replace("\\", "/")
                pk4.write(full_path, arcname=rel_path)
                print(f"  Added: {rel_path}")
                
    file_size = os.path.getsize(output_pk4)
    print(f"Flashlight mod successfully built! File size: {file_size} bytes ({file_size / 1024:.2f} KB)")
    
    # Synchronization to mod/ distribution folder
    mod_tfphobos = os.path.join(base_proj, "mod", "tfphobos")
    os.makedirs(mod_tfphobos, exist_ok=True)
    shutil.copy2(output_pk4, os.path.join(mod_tfphobos, "pak004_weapon_flashlight.pk4"))
    print(f"Synchronized pak004_weapon_flashlight.pk4 to {mod_tfphobos}")

    # Update autoexec.cfg and DoomConfig.cfg to bind 'f' to '_button5'
    autoexec_content = """seta logFileName "qconsole.log"
seta logFile "1"
seta com_allowConsole "1"
// Doom 3: Phobos Config & Keybinds
seta g_subLang "spanish"
seta g_subSize "0.275"

// Controls
bind "f" "_button5"
bind "SPACE" "_moveUp"
bind "x" "script SkipIntro()"
bind "ENTER" "_button2"
"""

    with open(os.path.join(mod_tfphobos, "autoexec.cfg"), "w", encoding="latin-1") as f:
        f.write(autoexec_content)
    with open(os.path.join(game_tfphobos_dir, "autoexec.cfg"), "w", encoding="latin-1") as f:
        f.write(autoexec_content)

    doom_cfg = os.path.join(game_tfphobos_dir, "DoomConfig.cfg")
    if os.path.exists(doom_cfg):
        with open(doom_cfg, "r", encoding="latin-1") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if line.strip().startswith('bind "f"'):
                new_lines.append('bind "f" "_button5"\n')
            else:
                new_lines.append(line)
        with open(doom_cfg, "w", encoding="latin-1") as f:
            f.writelines(new_lines)
        print("Updated DoomConfig.cfg with bind 'f' '_button5'")

    print("All configurations updated successfully!")

if __name__ == "__main__":
    build()

