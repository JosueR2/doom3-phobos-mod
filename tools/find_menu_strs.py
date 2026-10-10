import glob
import zipfile

for d in [r'F:\SteamLibrary\steamapps\common\Doom 3 Phobos\base', r'F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos']:
    for zpath in glob.glob(d + '/*.pk4'):
        with zipfile.ZipFile(zpath, 'r') as z:
            for name in z.namelist():
                if name.endswith('.lang'):
                    txt = z.read(name).decode('latin-1')
                    for term in ['OPTIONS', 'LOAD GAME', 'SAVE GAME', 'EXIT GAME', 'BACK TO GAME']:
                        needle = f'"{term}"'
                        if needle in txt:
                            for l in txt.splitlines():
                                if needle in l:
                                    print(f"{zpath} {name}: {l.strip()}")

