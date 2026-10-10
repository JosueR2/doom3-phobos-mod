import glob
import os

game_dir = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos"
for root, dirs, files in os.walk(game_dir):
    for f in files:
        if f.endswith('.cfg') or f.endswith('.default'):
            full_path = os.path.join(root, f)
            with open(full_path, 'r', encoding='latin-1', errors='ignore') as fp:
                for line in fp:
                    l = line.strip()
                    if l.startswith('bind '):
                        parts = l.split()
                        if len(parts) >= 2:
                            key = parts[1].strip('"').lower()
                            if key in ['f', 'space', 'x', 'mouse1', 'mouse2']:
                                print(f"{os.path.relpath(full_path, game_dir)}: {l}")

