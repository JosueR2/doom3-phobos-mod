with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

# find references to snd_skipcinematic string
str_pos = data.find(b"snd_skipcinematic")
print("snd_skipcinematic string at:", hex(str_pos))

# In 32-bit x86 DLL, strings are referenced by their virtual address:
# image base + offset. Let's find PE image base
# Typically 0x10000000 or similar
import struct
pe_offset = struct.unpack_from("<I", data, 0x3c)[0]
image_base = struct.unpack_from("<I", data, pe_offset + 0x34)[0]
print("Image base:", hex(image_base))

va = image_base + str_pos
va_bytes = struct.pack("<I", va)
print("Looking for VA:", hex(va))

refs = [m.start() for m in re.finditer(re.escape(va_bytes), data)]
print("References found at:", [hex(r) for r in refs])

