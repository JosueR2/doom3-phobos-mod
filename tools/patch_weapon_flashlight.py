"""Stop mounted weapon lights from lingering as muzzle flashes after firing."""

from __future__ import annotations

import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path


GAME_PAK = Path(
    r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak004_weapon_flashlight.pk4"
)
WEAPON_DEF = re.compile(r"def/weapon_[^/]+\.def$", re.IGNORECASE)
FLASH_SHADER = re.compile(rb'(?m)^\s*"mtr_flashShader"\s+"[^"]+"')
FLASH_RADIUS = re.compile(rb'(?m)^(\s*"flashRadius"\s+"[^"]+"\s*)$')
FLASH_TIME = re.compile(rb'(?m)^\s*"flashTime"\s+"[^"]+"\s*$')


def patch_definition(data: bytes) -> tuple[bytes, bool]:
    if not FLASH_SHADER.search(data):
        return data, False

    if FLASH_TIME.search(data):
        return FLASH_TIME.sub(b'\t"flashTime"\t\t\t"0"', data, count=1), True

    patched, count = FLASH_RADIUS.subn(rb'\1\r\n\t"flashTime"\t\t\t"0"', data, count=1)
    if count != 1:
        raise ValueError("Weapon definition has a flash shader but no flashRadius key")
    return patched, True


def main() -> None:
    if not GAME_PAK.is_file():
        raise FileNotFoundError(GAME_PAK)

    backup = GAME_PAK.with_suffix(GAME_PAK.suffix + ".before_flash_time_fix.bak")
    if backup.exists():
        raise FileExistsError(f"Refusing to overwrite existing backup: {backup}")

    patched_entries: list[str] = []
    with tempfile.NamedTemporaryFile(
        prefix="pak004_weapon_flashlight_", suffix=".pk4", dir=GAME_PAK.parent, delete=False
    ) as temp_file:
        temp_path = Path(temp_file.name)

    try:
        with zipfile.ZipFile(GAME_PAK, "r") as source, zipfile.ZipFile(
            temp_path, "w"
        ) as target:
            for entry in source.infolist():
                contents = source.read(entry.filename)
                if WEAPON_DEF.fullmatch(entry.filename):
                    contents, changed = patch_definition(contents)
                    if changed:
                        patched_entries.append(entry.filename)
                target.writestr(entry, contents)

        if len(patched_entries) != 10:
            raise RuntimeError(
                f"Expected 10 flashlight weapon definitions, patched {len(patched_entries)}"
            )

        shutil.copy2(GAME_PAK, backup)
        os.replace(temp_path, GAME_PAK)
    finally:
        if temp_path.exists():
            temp_path.unlink()

    print(f"Backed up original package to: {backup}")
    print("Set flashTime to 0 in:")
    for entry in patched_entries:
        print(f"  {entry}")


if __name__ == "__main__":
    main()
