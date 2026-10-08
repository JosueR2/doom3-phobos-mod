import zipfile

z = zipfile.ZipFile(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak002.pk4")
p_def = z.read("def/player.def").decode('utf-8', errors='ignore')
lines = p_def.splitlines()
for idx, l in enumerate(lines):
    if "snd_skipcinematic" in l:
        print("\n".join(lines[max(0, idx-10):min(len(lines), idx+15)]))

