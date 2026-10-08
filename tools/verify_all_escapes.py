import json
import re

with open("translated_subtitles.json", "r", encoding="utf-8") as f:
    trans = json.load(f)

bad_vals = []
for k, v in trans.items():
    # In json string, \\ is a single backslash
    # Check if there are any backslashes not followed by 'n'
    for m in re.finditer(r'\\(.)', v):
        char = m.group(1)
        if char != 'n':
            bad_vals.append((k, v, char))

print(f"Total invalid escapes in values: {len(bad_vals)}")
for b in bad_vals:
    print(b)

bad_keys = []
for k in trans.keys():
    for m in re.finditer(r'\\(.)', k):
        char = m.group(1)
        if char != 'n':
            bad_keys.append((k, char))

print(f"Total invalid escapes in keys: {len(bad_keys)}")
for b in bad_keys:
    print(b)

