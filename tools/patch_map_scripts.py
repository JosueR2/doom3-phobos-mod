import os
import re

script_to_map = {
    'map_intro.script': 'intro',
    'map_e1m1.script': 'e1m1',
    'map_e1m1_scanner.script': 'e1m1',
    'map_e1m1_1.script': 'e1m1_1',
    'map_e1m1_train.script': 'e1m1_1',
    'map_e1m1_2.script': 'e1m1_2',
    'map_e1m2.script': 'e1m2',
    'map_e1m3.script': 'e1m3',
    'map_e1m3_1.script': 'e1m3_1',
    'map_e1m3_1_intro.script': 'e1m3_1_intro',
    'map_e1m3_2.script': 'e1m3_2',
    'map_e1m3_outro.script': 'e1m3_outro',
    'map_e1m4.script': 'e1m4',
    'map_e1m4_1.script': 'e1m4_1',
    'map_e1m4_2.script': 'e1m4_2',
    'map_e1m4_3.script': 'e1m4_3',
    'map_e1m4_4.script': 'e1m4_4',
    'map_e1m4_4_intro.script': 'e1m4_4',
    'map_e1m5.script': 'e1m5',
    'map_e1m5_2.script': 'e1m5_2',
    'map_e1m5_3.script': 'e1m5_3',
    'map_e1m5_3b.script': 'e1m5_2',
    'map_e1m5_4.script': 'e1m5_4',
    'map_e1m5_5.script': 'e1m5_5',
    'map_e1m5_6.script': 'e1m5_6',
    'map_e1m5_6_outro.script': 'e1m5_6',
}

script_dir = r"E:\MisApps\Reverse\doom3phobos\src\script"
total_patched = 0
total_replacements = 0

for fname, map_key in sorted(script_to_map.items()):
    fpath = os.path.join(script_dir, fname)
    if not os.path.exists(fpath):
        print(f"File not found: {fname}")
        continue
    with open(fpath, "r", encoding="latin-1") as f:
        content = f.read()
    
    # Count occurrences
    matches = len(re.findall(r'sys\.showSubtitle\s*\(', content))
    if matches > 0:
        new_content = re.sub(r'sys\.showSubtitle\s*\(', f'PhobosShowSubtitle_{map_key}(', content)
        with open(fpath, "w", encoding="latin-1") as f:
            f.write(new_content)
        total_patched += 1
        total_replacements += matches
        print(f"Patched {fname:30}: {matches} calls replaced with PhobosShowSubtitle_{map_key}")
    else:
        print(f"No direct sys.showSubtitle calls in {fname}")

print(f"\nTotal scripts patched: {total_patched}, Total calls replaced: {total_replacements}")

