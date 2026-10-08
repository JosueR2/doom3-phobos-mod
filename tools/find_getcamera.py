with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

# In Player.cpp:
# if ( gameLocal.GetCamera() ) { ... }
# What happens to idPlayer when a camera is active?
idx = data.find(b"GetCamera")
while idx != -1:
    print("Found GetCamera at", hex(idx))
    idx = data.find(b"GetCamera", idx + 1)

