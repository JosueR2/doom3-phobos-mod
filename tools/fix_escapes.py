import json
import re

with open("translated_subtitles.json", "r", encoding="utf-8") as f:
    trans = json.load(f)

fixed_count = 0
for k, v in list(trans.items()):
    # Check for bad backslashes
    # We only want valid escape \n
    # Any backslash followed by a letter other than n should probably be fixed
    # In line 1541: civilización\o al menos -> civilización\no al menos (or \ny al menos)
    # Let's see all matches
    matches = list(re.finditer(r'\\([^n])', v))
    if matches:
        print(f"Key: {repr(k)}")
        print(f"Original val: {repr(v)}")
        # Let's fix specific occurrences
        # e.g. \o -> \no
        new_v = v.replace(r'\o al menos', r'\no al menos')
        # Check any other
        remaining = list(re.finditer(r'\\([^n])', new_v))
        if remaining:
            print(f"Remaining in val: {remaining}")
        trans[k] = new_v
        fixed_count += 1
        print(f"Fixed val: {repr(new_v)}")

print(f"Total fixed: {fixed_count}")

with open("translated_subtitles.json", "w", encoding="utf-8") as f:
    json.dump(trans, f, indent=2, ensure_ascii=False)

