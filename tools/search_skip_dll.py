with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

import re
matches = re.findall(rb'([a-zA-Z0-9_]{3,30}[sS]kip[a-zA-Z0-9_]*)', data)
print("Matches with skip in dll:")
for m in set(matches):
    print(" ", m.decode('ascii', errors='ignore'))

