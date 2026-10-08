import glob, zipfile, re, json

all_subs = []
for p in sorted(glob.glob("F:/SteamLibrary/steamapps/common/Doom 3 Phobos/tfphobos/pak*.pk4"), reverse=True):
    if "pak003" in p: continue
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            if n.endswith('.script'):
                txt = z.read(n).decode('utf-8', errors='ignore')
                # Find all calls to sys.showSubtitle, ShowNPCSubtitles, ShowSubtitles
                m1 = re.findall(r'sys\.showSubtitle\s*\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*\)', txt)
                m2 = re.findall(r'ShowNPCSubtitles(?:Train)?\s*\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*[^,\)]+\)', txt)
                m3 = re.findall(r'ShowSubtitles(?:2)?\s*\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*[^,\)]+\)', txt)
                for speaker, text in m1 + m2 + m3:
                    if speaker == "name" and text in ("titles", "text"):
                        continue
                    all_subs.append({"script": n, "speaker": speaker, "text": text})

print(f"Total extracted subtitle instances: {len(all_subs)}")
unique_subs = {}
for item in all_subs:
    k = (item["speaker"], item["text"])
    if k not in unique_subs:
        unique_subs[k] = []
    unique_subs[k].append(item["script"])

print(f"Unique speaker+text pairs: {len(unique_subs)}")
with open("extracted_subtitles.json", "w", encoding="utf-8") as f:
    json.dump([{"speaker": k[0], "text": k[1], "scripts": sorted(list(set(v)))} for k, v in unique_subs.items()], f, indent=2, ensure_ascii=False)
print("Saved to extracted_subtitles.json")
