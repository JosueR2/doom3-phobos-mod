with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

# Let's see the strings around this function or inspect the bytes
# In Doom 3, idPlayer::EnterCinematic or idPlayer::SkipCinematic or similar
# Let's search for nearest function or strings referenced in range 0x75d00 to 0x75f00
import struct

# Let's find any string pointers referenced in this code range:
ptrs = []
for i in range(0x75d00, 0x75f00, 4):
    val = struct.unpack_from("<I", data, i)[0]
    if 0x10200000 <= val < 0x10250000:
        offset = val - 0x10000000
        # read null terminated string
        end = data.find(b"\x00", offset)
        if end != -1 and end - offset < 50:
            s = data[offset:end].decode('ascii', errors='ignore')
            ptrs.append((hex(i), hex(val), s))

for p in ptrs:
    print(p)

