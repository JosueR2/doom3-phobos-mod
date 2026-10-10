# -*- coding: utf-8 -*-
import os

autoexec_content = """seta logFileName "qconsole.log"
seta logFile "1"
seta com_allowConsole "1"
// Doom 3: Phobos Config & Keybinds
seta g_subLang "spanish"
seta g_subSize "0.275"

// Controls
bind "f" "_impulse11"
bind "SPACE" "_moveUp"
bind "x" "script SkipIntro()"
bind "ENTER" "_button2"
"""

# 1. Update mod/tfphobos/autoexec.cfg
mod_cfg = r"mod/tfphobos/autoexec.cfg"
with open(mod_cfg, "w", encoding="latin-1") as f:
    f.write(autoexec_content)
print(f"Updated {mod_cfg}")

# 2. Update Steam tfphobos/autoexec.cfg
steam_cfg = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\autoexec.cfg"
if os.path.exists(os.path.dirname(steam_cfg)):
    with open(steam_cfg, "w", encoding="latin-1") as f:
        f.write(autoexec_content)
    print(f"Updated {steam_cfg}")

# 3. Update Steam tfphobos/DoomConfig.cfg
doom_cfg = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\DoomConfig.cfg"
if os.path.exists(doom_cfg):
    with open(doom_cfg, "r", encoding="latin-1") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.strip().startswith('bind "f"'):
            new_lines.append('bind "f" "_impulse11"\n')
        elif line.strip().startswith('bind "ENTER"'):
            new_lines.append('bind "ENTER" "_button2"\n')
        elif line.strip().startswith('bind "SPACE"'):
            new_lines.append('bind "SPACE" "_moveUp"\n')
        elif line.strip().startswith('bind "x"'):
            new_lines.append('bind "x" "script SkipIntro()"\n')
        else:
            new_lines.append(line)
            
    with open(doom_cfg, "w", encoding="latin-1") as f:
        f.writelines(new_lines)
    print(f"Updated {doom_cfg}")

