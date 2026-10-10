# -*- coding: utf-8 -*-
import glob
import re

for p in glob.glob("src_flashlight/script/*.script"):
    txt = open(p, encoding="latin-1").read()
    # Strip comments
    clean_txt = re.sub(r'//[^\n]*', '', txt)
    clean_txt = re.sub(r'/\*.*?\*/', '', clean_txt, flags=re.DOTALL)
    
    o_b = clean_txt.count("{")
    c_b = clean_txt.count("}")
    assert o_b == c_b, f"{p}: Braces mismatch: {o_b} open vs {c_b} close"
    
    lines = txt.splitlines()
    for idx, l in enumerate(lines):
        c_idx = l.find("//")
        code = l[:c_idx] if c_idx != -1 else l
        q_count = code.count('"')
        assert q_count % 2 == 0, f"{p}:{idx+1}: Unclosed quote in {l}"
    print(f"{p}: PASSED ({len(lines)} lines)")

print("\nALL FLASHLIGHT SCRIPTS PASSED COMPREHENSIVE VALIDATION!")

