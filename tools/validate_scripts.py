import os
import re

def check_script(path):
    fname = os.path.basename(path)
    print(f"Checking {fname}...")
    with open(path, "r", encoding="latin-1") as f:
        lines = f.readlines()
    
    brace_depth = 0
    paren_depth = 0
    errors = []
    
    for idx, line in enumerate(lines, 1):
        clean = line.split("//")[0].strip()
        if not clean:
            continue

        # Check quote balance
        # Remove escaped backslashes and escaped quotes
        s = clean.replace('\\\\', '').replace('\\"', '')
        quote_count = s.count('"')
        if quote_count % 2 != 0:
            errors.append(f"Line {idx}: Unbalanced double quotes ({quote_count}): {clean[:80]}")

        # Check if if (...) return ... lines end with ;
        if clean.startswith("if (") and "return " in clean and not clean.endswith(";"):
            errors.append(f"Line {idx}: Return statement missing semicolon: {clean[:80]}")

        # Check braces and parens
        in_str = False
        escape = False
        for ch in clean:
            if escape:
                escape = False
                continue
            if ch == '\\':
                escape = True
                continue
            if ch == '"':
                in_str = not in_str
                continue
            if in_str:
                continue

            if ch == '{':
                brace_depth += 1
            elif ch == '}':
                brace_depth -= 1
                if brace_depth < 0:
                    errors.append(f"Line {idx}: Negative brace depth")
            elif ch == '(':
                paren_depth += 1
            elif ch == ')':
                paren_depth -= 1
                if paren_depth < 0:
                    errors.append(f"Line {idx}: Negative paren depth")
    
    if brace_depth != 0:
        errors.append(f"Unmatched braces at EOF: depth={brace_depth}")
    if paren_depth != 0:
        errors.append(f"Unmatched parens at EOF: depth={paren_depth}")
        
    if errors:
        print("  Errors found:")
        for e in errors:
            print("   ", e)
        return False
    else:
        print("  Syntax check PASSED!")
        return True

script_dir = r"E:\MisApps\Reverse\doom3phobos\src\script"
all_ok = True
for root, dirs, files in os.walk(script_dir):
    for f in sorted(files):
        if f.endswith('.script'):
            ok = check_script(os.path.join(root, f))
            if not ok:
                all_ok = False

if all_ok:
    print("\nALL SCRIPTS PASSED COMPREHENSIVE SYNTAX VALIDATION!")
else:
    print("\nSOME SCRIPTS FAILED SYNTAX VALIDATION!")
