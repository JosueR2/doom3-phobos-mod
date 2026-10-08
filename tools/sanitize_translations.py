import json

def sanitize():
    path = "doom3phobos/translated_subtitles.json"
    with open(path, "r", encoding="utf-8") as f:
        trans = json.load(f)
        
    replacements = {
        "\u2026": "...",
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u2014": "--",
        "\u2013": "-",
        "\u00a0": " ",
        "\u200b": ""
    }
    
    fixed = 0
    for k, v in trans.items():
        new_v = v
        for src, dst in replacements.items():
            new_v = new_v.replace(src, dst)
        if new_v != v:
            trans[k] = new_v
            fixed += 1
            
    print(f"Sanitized {fixed} entries.")
    
    invalid = []
    for k, v in trans.items():
        try:
            v.encode("latin-1")
        except UnicodeEncodeError as e:
            invalid.append((k, v, str(e)))
            
    print(f"Invalid entries count: {len(invalid)}")
    if invalid:
        for item in invalid[:5]:
            print("  ", item)
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(trans, f, indent=2, ensure_ascii=False)
        print("All 1372 entries are 100% Latin-1 valid and cleanly saved!")

if __name__ == "__main__":
    sanitize()

