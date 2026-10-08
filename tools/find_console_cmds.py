with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

# Let's find "enables god mode" and print all strings around it
idx = data.find(b"enables god mode")
if idx != -1:
    chunk = data[idx-2000:idx+2000]
    # split by null bytes
    strings = [s.decode('ascii', errors='ignore') for s in chunk.split(b'\x00') if len(s) > 1]
    print("Strings around 'enables god mode':")
    for s in strings:
        if len(s) < 30:
            print("  ", s)

