with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

idx = data.find(b"snd_skipcinematic")
if idx != -1:
    chunk = data[idx-200:idx+300]
    print("Found around snd_skipcinematic:")
    print(chunk.replace(b'\x00', b' | '))

