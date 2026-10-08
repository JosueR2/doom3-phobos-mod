import zipfile, re

z = zipfile.ZipFile(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\base\pak000.pk4")
evs = set(re.findall(r'scriptEvent\s+\w+\s+(\w+)\s*\(', z.read('script/doom_events.script').decode('utf-8')))

z2 = zipfile.ZipFile(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak002.pk4")
evs.update(re.findall(r'scriptEvent\s+\w+\s+(\w+)\s*\(', z2.read('script/phobos_events.script').decode('utf-8')))

print(f"Total script events: {len(evs)}")

for fpath in [r"E:\MisApps\Reverse\doom3phobos\src\script\map_intro.script",
              r"E:\MisApps\Reverse\doom3phobos\src\script\map_e1m1.script"]:
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, l in enumerate(lines, 1):
        # find variable declarations: float x, vector x, entity x, string x, boolean x
        matches = re.findall(r'\b(float|vector|entity|string|boolean)\s+([a-zA-Z0-9_]+)', l)
        for t, var in matches:
            if var in evs:
                print(f"Warning in {fpath} line {idx}: '{var}' conflicts with script event! Line: {l.strip()}")

