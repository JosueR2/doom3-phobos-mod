import re

with open(r"e:\MisApps\Reverse\doom3phobos\src\script\phobos_subtitles_es.script", "r", encoding="latin-1") as f:
    lines = f.readlines()

bad_escapes = []
for idx, line in enumerate(lines, 1):
    # Search for any backslash not followed by n, t, ", or \
    matches = re.finditer(r'\\([^nt"\\])', line)
    for m in matches:
        bad_escapes.append((idx, m.group(1), line.strip()))

print(f"Total bad escapes in phobos_subtitles_es.script: {len(bad_escapes)}")
for idx, char, text in bad_escapes:
    print(f"Line {idx} (\\{char}): {text}")

