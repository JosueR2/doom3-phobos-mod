import zipfile, os

src_pk4 = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak000.pk4"
dest_dir = r"E:\MisApps\Reverse\doom3phobos\src\fonts\english"
os.makedirs(dest_dir, exist_ok=True)

with zipfile.ZipFile(src_pk4, 'r') as z:
    for size in ['12', '24', '48']:
        name = f"fonts/english/bank/fontimage_7_{size}.tga"
        data = z.read(name)
        out_path = os.path.join(dest_dir, f"fontimage_7_{size}.tga")
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"Extracted {name} -> {out_path} ({len(data)} bytes)")

        # Also place in bank/ folder
        bank_dir = os.path.join(dest_dir, "bank")
        os.makedirs(bank_dir, exist_ok=True)
        out_bank = os.path.join(bank_dir, f"fontimage_7_{size}.tga")
        with open(out_bank, "wb") as f:
            f.write(data)
        print(f"Also saved {out_bank}")
