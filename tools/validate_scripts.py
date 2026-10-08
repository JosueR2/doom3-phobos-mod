import os

def check_script(path):
    print(f"Checking {path}...")
    with open(path, "r", encoding="latin-1") as f:
        lines = f.readlines()
    
    brace_depth = 0
    paren_depth = 0
    errors = []
    
    for idx, line in enumerate(lines, 1):
        clean = line.split("//")[0].strip()
        for char in clean:
            if char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
                if brace_depth < 0:
                    errors.append(f"Line {idx}: Negative brace depth")
            elif char == '(':
                paren_depth += 1
            elif char == ')':
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
    else:
        print("  Syntax check PASSED (clean braces and parens)!")

script_dir = r"E:\MisApps\Reverse\doom3phobos\src\script"
for root, dirs, files in os.walk(script_dir):
    for f in sorted(files):
        if f.endswith('.script'):
            check_script(os.path.join(root, f))



