with open(r'e:\MisApps\Reverse\doom3phobos\src\guis\mainmenu\Options\GameButton.pd', 'r', encoding='latin-1') as f:
    txt = f.read()

txt = txt.replace('values\t\t"0;1;2"', 'values\t\t"0.275;0.35;0.43"')

with open(r'e:\MisApps\Reverse\doom3phobos\src\guis\mainmenu\Options\GameButton.pd', 'w', encoding='latin-1') as f:
    f.write(txt)

print('Updated GameButton.pd successfully!')

