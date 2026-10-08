with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

idx = data.find(b"executes a line of script")
if idx != -1:
    print("Found around 'executes a line of script':")
    print(data[idx-100:idx+200].replace(b'\x00', b' | '))

