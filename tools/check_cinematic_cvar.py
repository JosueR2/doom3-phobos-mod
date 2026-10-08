with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

idx = data.find(b"g_cinematicMaxSkipTime")
if idx != -1:
    chunk = data[idx-200:idx+400]
    print("Found around g_cinematicMaxSkipTime:")
    strings = [s.decode('ascii', errors='ignore') for s in chunk.split(b'\x00') if len(s) > 1]
    for s in strings:
        print("  ", s)

