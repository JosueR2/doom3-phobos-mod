import json
import os

def generate_script():
    with open("extracted_subtitles.json", "r", encoding="utf-8") as f:
        extracted = json.load(f)
    with open("translated_subtitles.json", "r", encoding="utf-8") as f:
        translated = json.load(f)

    script_to_map = {
        'script/map_intro.script': 'intro',
        'script/map_e1m1.script': 'e1m1',
        'script/map_e1m1_scanner.script': 'e1m1',
        'script/map_e1m1_1.script': 'e1m1_1',
        'script/map_e1m1_train.script': 'e1m1_1',
        'script/map_e1m1_2.script': 'e1m1_2',
        'script/map_e1m2.script': 'e1m2',
        'script/map_e1m3.script': 'e1m3',
        'script/map_e1m3_1.script': 'e1m3_1',
        'script/map_e1m3_1_intro.script': 'e1m3_1_intro',
        'script/map_e1m3_2.script': 'e1m3_2',
        'script/map_e1m3_outro.script': 'e1m3_outro',
        'script/map_e1m4.script': 'e1m4',
        'script/map_e1m4_1.script': 'e1m4_1',
        'script/map_e1m4_2.script': 'e1m4_2',
        'script/map_e1m4_3.script': 'e1m4_3',
        'script/map_e1m4_4.script': 'e1m4_4',
        'script/map_e1m4_4_intro.script': 'e1m4_4',
        'script/map_e1m5.script': 'e1m5',
        'script/map_e1m5_2.script': 'e1m5_2',
        'script/map_e1m5_3b.script': 'e1m5_2',
        'script/map_e1m5_3.script': 'e1m5_3',
        'script/map_e1m5_4.script': 'e1m5_4',
        'script/map_e1m5_5.script': 'e1m5_5',
        'script/map_e1m5_6.script': 'e1m5_6',
        'script/map_e1m5_6_outro.script': 'e1m5_6',
    }

    map_to_subs = {}
    for item in extracted:
        orig = item['text']
        trans = translated.get(orig, orig)
        for sc in item['scripts']:
            m = script_to_map.get(sc, 'common')
            map_to_subs.setdefault(m, {})[orig] = trans

    lines = []
    lines.append("// =============================================================================")
    lines.append("// Phobos Subtitles - Spanish Localization System")
    lines.append("// Generated automatically for Doom 3: Phobos")
    lines.append("// =============================================================================")
    lines.append("")
    lines.append("void InitSubtitleCVars() {")
    lines.append('\tstring lang = sys.getcvar("g_subLang");')
    lines.append('\tif (lang != "spanish" && lang != "english") {')
    lines.append('\t\tsys.setcvar("g_subLang", "english");')
    lines.append('\t}')
    lines.append('\tstring size = sys.getcvar("g_subSize");')
    lines.append('\tif (size == "0" || size == "") {')
    lines.append('\t\tsys.setcvar("g_subSize", "0.275");')
    lines.append('\t} else if (size == "1") {')
    lines.append('\t\tsys.setcvar("g_subSize", "0.35");')
    lines.append('\t} else if (size == "2") {')
    lines.append('\t\tsys.setcvar("g_subSize", "0.43");')
    lines.append('\t}')
    lines.append("}")
    lines.append("")
    lines.append("string LocalizeSpeaker(string name) {")
    lines.append("\tif (sys.getcvar(\"g_subLang\") != \"spanish\") {")
    lines.append("\t\treturn name;")
    lines.append("\t}")
    lines.append("\tif (name == \"Girl\") return \"Chica\";")
    lines.append("\tif (name == \"Guy\") return \"Sujeto\";")
    lines.append("\tif (name == \"Security\") return \"Seguridad\";")
    lines.append("\tif (name == \"Tour Guide\") return \"Guía Turístico\";")
    lines.append("\tif (name == \"FCE Soldier\") return \"Soldado de la FCE\";")
    lines.append("\tif (name == \"Captain Rigel\") return \"Capitán Rigel\";")
    lines.append("\tif (name == \"Special Agent Simmons\" || name == \"Speical Agent Simmons\") return \"Agente Especial Simmons\";")
    lines.append("\tif (name == \"PA\") return \"Megafonía\";")
    lines.append("\treturn name;")
    lines.append("}")
    lines.append("")

    for map_key in sorted(map_to_subs.keys()):
        subs_dict = map_to_subs[map_key]
        lines.append(f"string LocalizeSubtitle_{map_key}(string text) {{")
        for orig, trans in subs_dict.items():
            clean_orig = orig.replace('\r', '').replace('\n', '\\n').replace('"', "'")
            clean_trans = trans.replace('\r', '').replace('\n', '\\n').replace('"', "'")
            lines.append(f'\tif (text == "{clean_orig}") return "{clean_trans}";')
        lines.append("\treturn text;")
        lines.append("}")
        lines.append("")
        lines.append(f"void PhobosShowSubtitle_{map_key}(string speaker, string text) {{")
        lines.append("\tInitSubtitleCVars();")
        lines.append('\tif (sys.getcvar("g_subLang") == "spanish") {')
        lines.append('\t\tspeaker = LocalizeSpeaker(speaker);')
        lines.append(f'\t\ttext = LocalizeSubtitle_{map_key}(text);')
        lines.append('\t}')
        lines.append('\tsys.showSubtitle(speaker, text);')
        lines.append("}")
        lines.append("")

    content = "\n".join(lines) + "\n"
    out_path = r"E:\MisApps\Reverse\doom3phobos\src\script\phobos_subtitles_es.script"
    with open(out_path, "w", encoding="latin-1") as f:
        f.write(content)
    print(f"Generated {out_path} ({len(lines)} lines, {len(content)} bytes)")

if __name__ == "__main__":
    generate_script()

