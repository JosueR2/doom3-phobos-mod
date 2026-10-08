import glob, zipfile, re

scripts_in_pak = {}
for p in sorted(glob.glob("F:/SteamLibrary/steamapps/common/Doom 3 Phobos/tfphobos/pak*.pk4"), reverse=True):
    if "pak003" in p: continue
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            if n.endswith('.script') and n not in scripts_in_pak:
                scripts_in_pak[n] = z.read(n).decode('utf-8', errors='ignore')

non_literal = []
for n, txt in scripts_in_pak.items():
    matches = re.finditer(r'sys\.showSubtitle\s*\(([^;]+)\);', txt)
    for m in matches:
        args = m.group(1).strip()
        if not args.startswith('"'):
            non_literal.append((n, args))

print(f"Non-literal sys.showSubtitle calls: {len(non_literal)}")
for n, a in non_literal:
    print(f"  {n}: {a}")

