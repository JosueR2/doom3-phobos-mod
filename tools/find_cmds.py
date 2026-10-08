with open(r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos\gamex86.dll", "rb") as f:
    data = f.read()

# find all console commands registered with cmdSystem->AddCommand
# In Doom 3, commands are usually:
# AddCommand( "trigger", ... )
# AddCommand( "call", ... )
# AddCommand( "testmap", ... )
import re
cmds = re.findall(rb'([a-z_]{3,20})\x00[^\x00]{1,50}\x00[^\x00]{1,50}\x00', data)
for c in set(cmds):
    try:
        cs = c.decode('ascii')
        if any(w in cs for w in ['script', 'trigger', 'call', 'skip', 'cam', 'cut']):
            print("Found cmd:", cs)
    except:
        pass

