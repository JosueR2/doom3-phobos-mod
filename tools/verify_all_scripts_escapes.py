import os
import re

script_dir = r"e:\MisApps\Reverse\doom3phobos\src\script"
total_bad = 0

for fname in sorted(os.listdir(script_dir)):
    if not fname.endswith('.script'):
        continue
    fpath = os.path.join(script_dir, fname)
    with open(fpath, "r", encoding="latin-1") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        clean = line.split("//")[0]
        # Find any backslash inside quotes that is not followed by n, t, ", or \
        for m in re.finditer(r'\\([^nt"\\])', clean):
            print(f"Error in {fname} line {idx} (\\{m.group(1)}): {clean.strip()[:100]}")
            total_bad += 1

print(f"\nTotal bad escape sequences across all scripts: {total_bad}")

