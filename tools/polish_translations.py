import json
import re

def polish():
    path = "doom3phobos/translated_subtitles.json"
    with open(path, "r", encoding="utf-8") as f:
        trans = json.load(f)

    # Names that should NEVER be translated as common nouns
    proper_names = [
        ("Samantha Millas", "Samantha Miles"),
        ("Millas", "Miles"),  # when used as proper name
        ("Dr. Nielsen", "Dr. Nielsen"),
        ("Calloway", "Calloway"),
        ("Benson", "Benson"),
        ("Rigel", "Rigel"),
        ("Simmons", "Simmons"),
        ("Bulwark", "Bulwark"),
        ("Phobos", "Fobos"),
        ("Mars", "Marte"),
    ]
    
    fixed = 0
    for k, v in trans.items():
        orig_v = v
        # Fix Samantha Millas -> Samantha Miles
        v = re.sub(r'\bSamantha Millas\b', 'Samantha Miles', v)
        # Fix Smiles (nickname for Samantha Miles)
        v = re.sub(r'\bSonrisas\b', 'Smiles', v)
        # Fix "Consiénteme. Es un procedimiento estándar." -> "Tómalo con calma. Es el procedimiento habitual."
        if "Consi" in v and "procedimiento" in v:
            v = v.replace("Consiénteme.", "Tómalo con calma.").replace("Consienteme.", "Tómalo con calma.")
            
        if v != orig_v:
            trans[k] = v
            fixed += 1
            
    print(f"Polished {fixed} translations for proper nouns and tone.")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(trans, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    polish()

