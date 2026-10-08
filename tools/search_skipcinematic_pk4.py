import zipfile

for pak_path in [r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak000.pk4",
                 r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak001.pk4",
                 r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak002.pk4"]:
    z = zipfile.ZipFile(pak_path)
    for n in z.namelist():
        if n.endswith(('.gui', '.script', '.def')):
            c = z.read(n).decode('utf-8', errors='ignore')
            if "snd_skipcinematic" in c or "skipcinematic" in c.lower() or "skip_cinematic" in c.lower():
                print(f"Found in {pak_path} -> {n}")
                for line in c.splitlines():
                    if "skip" in line.lower() and "cinematic" in line.lower():
                        print("  ", line.strip())

