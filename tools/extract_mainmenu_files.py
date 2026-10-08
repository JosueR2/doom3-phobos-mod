import zipfile, os

pk4 = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak002.pk4"
dest_base = r"E:\MisApps\Reverse\doom3phobos\src\guis"

with zipfile.ZipFile(pk4, 'r') as z:
    for name in z.namelist():
        if name.startswith('guis/mainmenu'):
            # don't overwrite GameButton.pd if it already exists in src
            dest_path = os.path.join(dest_base, name[5:]) # strip 'guis/'
            if not os.path.exists(dest_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, 'wb') as f:
                    f.write(z.read(name))
                print(f"Extracted {name} -> {dest_path}")
            else:
                print(f"Skipping existing {dest_path}")
