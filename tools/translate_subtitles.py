import json
import os
import urllib.request
import urllib.parse
import time
import re
import sys

def translate_all():
    input_file = "doom3phobos/extracted_subtitles.json"
    output_file = "doom3phobos/translated_subtitles.json"
    
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            translations = json.load(f)
    else:
        translations = {}

    with open(input_file, "r", encoding="utf-8") as f:
        subs = json.load(f)
        
    print(f"Total subtitles: {len(subs)}", flush=True)
    print(f"Already translated: {len(translations)}", flush=True)
    
    needed = [s for s in subs if s["text"] not in translations]
    print(f"Remaining: {len(needed)}", flush=True)
    
    count = 0
    for s in needed:
        text = s["text"]
        for attempt in range(3):
            try:
                url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q=" + urllib.parse.quote(text)
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    tr = "".join([item[0] for item in data[0] if item[0]])
                    translations[text] = tr.strip()
                    break
            except Exception as e:
                time.sleep(0.5)
                
        count += 1
        if count % 50 == 0 or count == len(needed):
            print(f"Progress: {len(translations)} / {len(subs)} ({(len(translations)/len(subs))*100:.1f}%)", flush=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(translations, f, indent=2, ensure_ascii=False)
                
        time.sleep(0.05)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)
    print(f"Finished! Total translated: {len(translations)}", flush=True)

if __name__ == "__main__":
    translate_all()

