import zipfile, glob, re

all_lines = []
for p in sorted(glob.glob("F:/SteamLibrary/steamapps/common/Doom 3 Phobos/tfphobos/pak*.pk4")):
    if "pak003" in p: continue
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            if name.endswith('.script'):
                txt = z.read(name).decode('utf-8', errors='ignore')
                for m in re.finditer(r'sys\.showSubtitle\s*\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*\)', txt):
                    all_lines.append((name, m.group(1), m.group(2)))

print(f"Total subtitle calls: {len(all_lines)}")
unique = set((s, l) for _, s, l in all_lines)
print(f"Unique subtitles: {len(unique)}")
for s, l in sorted(unique)[:15]:
    print(f"[{s}]: {repr(l)}")

