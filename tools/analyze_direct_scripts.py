import glob, zipfile, re

scripts_in_pak = {}
for p in sorted(glob.glob("F:/SteamLibrary/steamapps/common/Doom 3 Phobos/tfphobos/pak*.pk4"), reverse=True):
    if "pak003" in p: continue
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            if n.endswith('.script') and n not in scripts_in_pak:
                scripts_in_pak[n] = z.read(n).decode('utf-8-sig', errors='ignore')

# 1. Scripts with wrappers
wrapper_scripts = []
for sc, txt in sorted(scripts_in_pak.items()):
    if 'void ShowNPCSubtitles' in txt or 'void ShowSubtitles' in txt:
        wrapper_scripts.append(sc)

# 2. Check direct calls that are NOT inside ShowNPCSubtitles / ShowSubtitles definition
direct_scripts = {}
for sc, txt in sorted(scripts_in_pak.items()):
    calls = [l.strip() for l in txt.splitlines() if 'sys.showSubtitle("' in l]
    if calls:
        direct_scripts[sc] = len(calls)

print(f"Scripts with direct string literal calls ({len(direct_scripts)}):")
for sc, cnt in direct_scripts.items():
    print(f"  {sc}: {cnt} direct calls (has wrapper? {sc in wrapper_scripts})")

