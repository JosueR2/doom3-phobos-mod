# -*- coding: utf-8 -*-
import os
import re

base_dir = r"tools/phobos_weapons"
out_dir = r"src_flashlight"
os.makedirs(os.path.join(out_dir, "def"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "script"), exist_ok=True)

# -------------------------------------------------------------
# 1. Modify script/weapon_base.script
# -------------------------------------------------------------
with open(os.path.join(base_dir, "script/weapon_base.script"), "r", encoding="latin-1") as f:
    wb = f.read()

# Add _BUTTON5 and dfm_flashlight_on before object weapon_base
prefix = """#ifndef _BUTTON5
#define _BUTTON5			( getOwner() ).getButtons()&32
#endif

boolean dfm_flashlight_on;

"""
wb = prefix + wb

# Add void ToggleOnOff(); inside object weapon_base
wb = wb.replace(
    "\tstring\t\tGetFireAnim();\n};",
    "\tstring\t\tGetFireAnim();\n\tvoid\t\tToggleOnOff();\n};"
)

# Add implementation at bottom
toggle_impl = """
/*
=====================
weapon_base::ToggleOnOff
=====================
*/
void weapon_base::ToggleOnOff() {
	dfm_flashlight_on = !dfm_flashlight_on;
	startSound( "snd_click", SND_CHANNEL_ITEM, true );
	flashlight( dfm_flashlight_on );
	sys.wait( 0.2 );
	weaponState( "Idle", 3 );
}
"""
wb = wb + toggle_impl

with open(os.path.join(out_dir, "script/weapon_base.script"), "w", encoding="latin-1") as f:
    f.write(wb)
print("Generated src_flashlight/script/weapon_base.script")


# -------------------------------------------------------------
# Helper for patching weapon scripts
# -------------------------------------------------------------
def patch_weapon_script(filename, classname, blend_time="3"):
    with open(os.path.join(base_dir, "script", filename), "r", encoding="latin-1") as f:
        code = f.read()

    # Prepend _BUTTON5 definition guard so all compilation units have access to _BUTTON5
    btn_macro = """#ifndef _BUTTON5
#define _BUTTON5			( getOwner() ).getButtons()&32
#endif

"""
    code = btn_macro + code

    # 1. In Raise(), add flashlight( dfm_flashlight_on );
    raise_decl = f"void {classname}::Raise() {{"
    code = code.replace(
        raise_decl,
        f"{raise_decl}\n\tflashlight( dfm_flashlight_on );"
    )

    # 2. In Lower(), add flashlight( dfm_flashlight_on );
    lower_decl = f"void {classname}::Lower() {{"
    code = code.replace(
        lower_decl,
        f"{lower_decl}\n\tflashlight( dfm_flashlight_on );"
    )

    # 3. In Idle(), add check for _BUTTON5 inside the while loop
    # We look for while( 1 ) or while( !animDone or while ( 1 )
    btn_check = f"""\t\tif ( _BUTTON5 ) {{
\t\t\tweaponState( "ToggleOnOff", {blend_time} );
\t\t}}
"""
    # Insert into Idle() before WEAPON_LOWERWEAPON
    if f"void {classname}::Idle()" in code:
        code = code.replace(
            "if ( WEAPON_LOWERWEAPON )",
            f"{btn_check}\t\tif ( WEAPON_LOWERWEAPON )",
            1
        )
    # Insert into Idle2() before WEAPON_LOWERWEAPON if Idle2 exists
    if f"void {classname}::Idle2()" in code:
        parts = code.split("void " + classname + "::Idle2()")
        idle2_code = parts[1].replace(
            "if ( WEAPON_LOWERWEAPON )",
            f"{btn_check}\t\tif ( WEAPON_LOWERWEAPON )",
            1
        )
        code = parts[0] + "void " + classname + "::Idle2()" + idle2_code

    with open(os.path.join(out_dir, "script", filename), "w", encoding="latin-1") as f:
        f.write(code)
    print(f"Generated src_flashlight/script/{filename}")


# Patch all weapon scripts
patch_weapon_script("weapon_pistol.script", "weapon_pistol", "PISTOL_IDLE_TO_RELOAD")
patch_weapon_script("weapon_shotgun.script", "weapon_shotgun", "SHOTGUN_IDLE_TO_RELOAD")
patch_weapon_script("weapon_shotgun_double.script", "weapon_shotgun_double", "SHOTGUN_DOUBLE_IDLE_TO_IDLE")
patch_weapon_script("weapon_machinegun.script", "weapon_machinegun", "MACHINEGUN_IDLE_TO_RELOAD")
patch_weapon_script("weapon_chaingun.script", "weapon_chaingun", "3")
patch_weapon_script("weapon_plasmagun.script", "weapon_plasmagun", "PLASMAGUN_IDLE_TO_RELOAD")
patch_weapon_script("weapon_rocketlauncher.script", "weapon_rocketlauncher", "ROCKETLAUNCHER_IDLE_TO_RELOAD")
patch_weapon_script("weapon_bfg.script", "weapon_bfg", "BFG_IDLE_TO_RELOAD")
patch_weapon_script("weapon_fists.script", "weapon_fists", "FISTS_IDLE_TO_LOWER")
patch_weapon_script("weapon_handgrenade.script", "weapon_handgrenade", "HANDGRENADE_IDLE_TO_LOWER")


# -------------------------------------------------------------
# Helper for patching weapon defs
# -------------------------------------------------------------
flash_block = """\t"mtr_flashShader"			"lights/flashlight5"
\t"flashColor"				"1 1 1"
\t"flashRadius"				"400"
\t"flashAngle"				"18.0"
\t"flashTarget"				"1380 0 0"
\t"flashUp"					"0 480 0"
\t"flashRight"				"0 0 -480"
\t"flashPointLight"			"0"
\t"snd_click"					"player_pistol_empty"
"""

def patch_weapon_def(filename, entity_name):
    with open(os.path.join(base_dir, "def", filename), "r", encoding="latin-1") as f:
        code = f.read()

    # If entity has mtr_flashShader, replace the flash section
    target = f"entityDef {entity_name} {{"
    assert target in code, f"{target} not found in {filename}"

    # Remove existing mtr_flashShader, flashColor, flashRadius if present inside the entity
    # Split code around target
    parts = code.split(target, 1)
    ent_part = parts[1]
    
    # Remove existing keys from the entity
    for k in ["mtr_flashShader", "flashColor", "flashRadius", "flashAngle", "flashTarget", "flashUp", "flashRight", "flashPointLight", "snd_click"]:
        ent_part = re.sub(rf'\t*"{k}"[^\n]*\n', '', ent_part)

    # Insert our flash block right after entityDef opening
    parts[1] = "\n" + flash_block + ent_part
    code = target.join(parts)

    with open(os.path.join(out_dir, "def", filename), "w", encoding="latin-1") as f:
        f.write(code)
    print(f"Generated src_flashlight/def/{filename}")


patch_weapon_def("weapon_pistol.def", "weapon_pistol")
patch_weapon_def("weapon_shotgun.def", "weapon_shotgun")
patch_weapon_def("weapon_shotgun_double.def", "weapon_shotgun_double")
patch_weapon_def("weapon_machinegun.def", "weapon_machinegun")
patch_weapon_def("weapon_chaingun.def", "weapon_chaingun")
patch_weapon_def("weapon_plasmagun.def", "weapon_plasmagun")
patch_weapon_def("weapon_rocketlauncher.def", "weapon_rocketlauncher")
patch_weapon_def("weapon_bfg.def", "weapon_bfg")
patch_weapon_def("weapon_fists.def", "weapon_fists")
patch_weapon_def("weapon_handgrenade.def", "weapon_handgrenade")

print("\nAll flashlight mod sources successfully generated in src_flashlight/!")

