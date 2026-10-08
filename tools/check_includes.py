import glob, zipfile, re

scripts_in_pak = {}
for p in sorted(glob.glob("F:/SteamLibrary/steamapps/common/Doom 3 Phobos/tfphobos/pak*.pk4"), reverse=True):
    if "pak003" in p: continue
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            if n.endswith('.script') and n not in scripts_in_pak:
                scripts_in_pak[n] = z.read(n).decode('utf-8', errors='ignore')

# 1. Check which scripts include other scripts
for n, txt in scripts_in_pak.items():
    incs = re.findall(r'#include\s+"([^"]+)"', txt)
    if incs:
        print(f"{n} includes:")
        for inc in incs:
            print(f"  {inc}")

# 2. Check where each script is included
included_by = {}
for n, txt in scripts_in_pak.items():
    incs = re.findall(r'#include\s+"([^"]+)"', txt)
    for inc in incs:
        if inc not in included_by:
            included_by[inc] = []
        included_by[inc].append(n)

print("\nScripts NOT included by anything:")
for n in sorted(scripts_in_pak.keys()):
    if n not in included_by and not n.startswith('script/phobos_main'):
        print(f"  {n}")

