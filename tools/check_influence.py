import zipfile

z = zipfile.ZipFile(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\pak002.pk4")
data = z.read("maps/ep1/e1m1.map").decode('utf-8', errors='ignore')
idx = data.find('"intro_target_setinfluence_1"')
if idx != -1:
    print(data[idx-50:idx+300])

