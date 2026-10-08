import glob, zipfile, re, json

scripts_in_pak = {}
for p in sorted(glob.glob("F:/SteamLibrary/steamapps/common/Doom 3 Phobos/tfphobos/pak*.pk4"), reverse=True):
    if "pak003" in p: continue
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            if n.endswith('.script') and n not in scripts_in_pak:
                scripts_in_pak[n] = z.read(n).decode('utf-8', errors='ignore')

script_subs = {}
for sc in sorted(scripts_in_pak.keys()):
    txt = scripts_in_pak[sc]
    matches = re.findall(r'(?:sys\.showSubtitle|ShowNPCSubtitles(?:Train)?|ShowSubtitles(?:2)?)\s*\(\s*"([^"]*)"\s*,\s*"([^"]*)"', txt)
    if matches:
        script_subs[sc] = matches
        print(f"{sc}: {len(matches)} subtitle calls")

total = sum(len(m) for m in script_subs.values())
print(f"Total subtitle calls: {total}")

with open("doom3phobos/script_ordered_subs.json", "w", encoding="utf-8") as f:
    json.dump(script_subs, f, indent=2, ensure_ascii=False)

