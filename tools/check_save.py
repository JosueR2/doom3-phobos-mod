import os, time
p = 'F:/SteamLibrary/steamapps/common/Doom 3 Phobos/tfphobos/savegames'
for f in os.listdir(p):
    full = os.path.join(p, f)
    print(f, os.path.getsize(full), time.ctime(os.path.getmtime(full)))

