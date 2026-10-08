"""
Script to apply savegame persistence hotfixes to gamex86.dll:
1. Patch 1 (CompileFile): If ReadFile returns < 0 (missing file, e.g. "console"),
   gracefully return (pop edi; pop esi; ret 4) instead of crashing with gameLocal.Error.
2. Patch 2 (idProgram::Restore): Bypass checksum check (nop nop) so modified scripts don't abort restore.
3. Patch 3 (idProgram::Save): Bypass extra files writing (write 0 files, skip file loop)
   so console commands never poison future savegames with "console".
"""
import os
import shutil

DLL_ORIG = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll.orig"
DLL_TARGET = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll"
DLL_MOD = r"E:\MisApps\Reverse\doom3phobos\mod\tfphobos\gamex86.dll"

def apply_patches():
    if not os.path.exists(DLL_ORIG):
        raise FileNotFoundError(f"Original backup not found: {DLL_ORIG}")

    with open(DLL_ORIG, "rb") as f:
        data = bytearray(f.read())

    print(f"Read {len(data)} bytes from {DLL_ORIG}")

    # --- Patch 1: CompileFile missing file graceful return ---
    # Raw 0x181051 (VA 0x10181c51)
    # Original: 56 68 c8 46 22 10 68 60 2f 25 10 e8 2f 6b eb ff 83 c4 0c (push esi; push fmt; push gameLocal; call Error; add esp, 0xc)
    # Target:   5f 5e c2 04 00 90... (pop edi; pop esi; ret 4; 14x nop)
    p1_expected = bytes.fromhex("56 68 c8 46 22 10 68 60 2f 25 10 e8 2f 6b eb ff 83 c4 0c")
    p1_actual = data[0x181051:0x181051+len(p1_expected)]
    assert p1_actual == p1_expected, f"Patch 1 mismatch: got {p1_actual.hex()} expected {p1_expected.hex()}"
    p1_replacement = bytes([0x5f, 0x5e, 0xc2, 0x04, 0x00]) + b"\x90" * 14
    data[0x181051:0x181051+len(p1_replacement)] = p1_replacement
    print("Patch 1 applied: CompileFile graceful return on missing file.")

    # --- Patch 2: idProgram::Restore Checksum bypass ---
    # Raw 0x18120a (VA 0x10181e0a)
    # Original: 75 04 (jne 0x10181e10)
    # Target:   90 90 (nop nop)
    p2_expected = bytes.fromhex("75 04")
    p2_actual = data[0x18120a:0x18120a+len(p2_expected)]
    assert p2_actual == p2_expected, f"Patch 2 mismatch: got {p2_actual.hex()} expected {p2_expected.hex()}"
    p2_replacement = b"\x90\x90"
    data[0x18120a:0x18120a+len(p2_replacement)] = p2_replacement
    print("Patch 2 applied: idProgram::Restore checksum validation bypass.")

    # --- Patch 3: idProgram::Save extra files bypass ---
    # Raw 0x17e262 (VA 0x1017ee62): sub eax, edi; push eax (2b c7 50) -> xor eax, eax; push eax (31 c0 50)
    p3a_expected = bytes.fromhex("2b c7 50")
    p3a_actual = data[0x17e262:0x17e262+len(p3a_expected)]
    assert p3a_actual == p3a_expected, f"Patch 3a mismatch: got {p3a_actual.hex()} expected {p3a_expected.hex()}"
    p3a_replacement = bytes([0x31, 0xc0, 0x50])
    data[0x17e262:0x17e262+len(p3a_replacement)] = p3a_replacement

    # Raw 0x17e26e (VA 0x1017ee6e): jge 0x1017ee8c (7d 1c) -> jmp 0x1017ee8c (eb 1c)
    p3b_expected = bytes.fromhex("7d 1c")
    p3b_actual = data[0x17e26e:0x17e26e+len(p3b_expected)]
    assert p3b_actual == p3b_expected, f"Patch 3b mismatch: got {p3b_actual.hex()} expected {p3b_expected.hex()}"
    p3b_replacement = bytes([0xeb, 0x1c])
    data[0x17e26e:0x17e26e+len(p3b_replacement)] = p3b_replacement
    print("Patch 3 applied: idProgram::Save extra files writing bypass.")

    # Write target DLL in Steam game directory
    with open(DLL_TARGET, "wb") as f:
        f.write(data)
    print(f"Successfully wrote patched DLL to {DLL_TARGET}")

    # Rebuild game00.pk4 in Steam game directory with patched gamex86.dll
    import zipfile
    pk4_target = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\game00.pk4"
    pk4_orig = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\game00.pk4.orig"
    if not os.path.exists(pk4_orig):
        shutil.copy2(pk4_target, pk4_orig)
        print(f"Backed up {pk4_target} to {pk4_orig}")

    # Read binary.conf from original
    with zipfile.ZipFile(pk4_orig, "r") as z_orig:
        binary_conf = z_orig.read("binary.conf")

    # Write new game00.pk4
    with zipfile.ZipFile(pk4_target, "w") as z_out:
        z_out.writestr("binary.conf", binary_conf, compress_type=zipfile.ZIP_STORED)
        z_out.writestr("gamex86.dll", bytes(data), compress_type=zipfile.ZIP_DEFLATED)
    print(f"Successfully rebuilt {pk4_target} with patched gamex86.dll")

    # Write copy to mod distribution directory
    os.makedirs(os.path.dirname(DLL_MOD), exist_ok=True)
    with open(DLL_MOD, "wb") as f:
        f.write(data)
    print(f"Successfully synced patched DLL to {DLL_MOD}")

    mod_game00 = os.path.join(os.path.dirname(DLL_MOD), "game00.pk4")
    shutil.copy2(pk4_target, mod_game00)
    print(f"Successfully synced {mod_game00}")

if __name__ == "__main__":
    apply_patches()

