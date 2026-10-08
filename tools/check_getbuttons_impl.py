with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

# find Event_GetButtons
idx = data.find(b"Event_GetButtons")
if idx != -1:
    print("Found Event_GetButtons at", hex(idx))
    print(data[idx-100:idx+200])
else:
    print("Event_GetButtons not found by name")

# Let's search getButtons
idx = data.find(b"getButtons")
while idx != -1:
    print("Found getButtons at", hex(idx))
    idx = data.find(b"getButtons", idx + 1)

