import glob

for p in glob.glob(r'F:/SteamLibrary/steamapps/common/Doom 3/base/*.cfg'):
    with open(p, encoding='latin-1') as f:
        for l in f:
            if any(k in l.lower() for k in ['button5', 'impulse11', 'bind "f"', 'bind f']):
                print(p, l.strip())

