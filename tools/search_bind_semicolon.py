import os

for base_dir in [r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\base",
                 r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos"]:
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".cfg"):
                path = os.path.join(root, f)
                with open(path, "r", errors='ignore') as fp:
                    for l in fp:
                        if "bind" in l and ";" in l:
                            print(f"{path}: {l.strip()}")

