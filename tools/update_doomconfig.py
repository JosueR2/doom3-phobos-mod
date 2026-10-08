p = r'F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\DoomConfig.cfg'
with open(p, 'r', encoding='latin-1') as f:
    txt = f.read()
txt = txt.replace('seta g_subSize "0"', 'seta g_subSize "0.275"')
with open(p, 'w', encoding='latin-1') as f:
    f.write(txt)
print('Updated DoomConfig.cfg')

