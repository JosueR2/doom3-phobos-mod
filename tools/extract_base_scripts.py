import zipfile
import os

pak_path = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak002.pk4"
dest_dir = r"E:\MisApps\Reverse\doom3phobos\src\script"
os.makedirs(dest_dir, exist_ok=True)

with zipfile.ZipFile(pak_path, 'r') as z:
    for name in ["script/map_intro.script", "script/map_e1m1.script"]:
        data = z.read(name)
        fname = os.path.basename(name)
        out_path = os.path.join(dest_dir, fname)
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"Extracted {name} to {out_path} ({len(data)} bytes)")

