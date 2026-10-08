import zipfile
import os
import sys
import shutil

def build():
    base_proj = r"E:\MisApps\Reverse\doom3phobos"
    src_dir = os.path.join(base_proj, "src")
    game_tfphobos_dir = r"F:\SteamLibrary\steamapps\common\Doom 3 Phobos\tfphobos"
    output_pk4 = os.path.join(game_tfphobos_dir, "pak003_skipcinematics.pk4")
    
    if not os.path.exists(game_tfphobos_dir):
        print(f"Error: Target directory does not exist: {game_tfphobos_dir}")
        sys.exit(1)
        
    print(f"Building mod package: {output_pk4}")
    
    # We use ZIP_DEFLATED (standard zip compression used by idTech4 pk4 files)
    with zipfile.ZipFile(output_pk4, 'w', compression=zipfile.ZIP_DEFLATED) as pk4:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, src_dir).replace("\\", "/")
                pk4.write(full_path, arcname=rel_path)
                print(f"  Added: {rel_path}")
                
    file_size = os.path.getsize(output_pk4)
    print(f"Mod successfully built! File size: {file_size} bytes ({file_size / 1024:.2f} KB)")
    
    # Automatic synchronization to mod/ distribution folder
    mod_tfphobos = os.path.join(base_proj, "mod", "tfphobos")
    os.makedirs(mod_tfphobos, exist_ok=True)
    
    # 1. Copy pk4
    shutil.copy2(output_pk4, os.path.join(mod_tfphobos, "pak003_skipcinematics.pk4"))
    
    # 2. Copy autoexec.cfg
    cfg_src = os.path.join(game_tfphobos_dir, "autoexec.cfg")
    if os.path.exists(cfg_src):
        shutil.copy2(cfg_src, os.path.join(mod_tfphobos, "autoexec.cfg"))
        
    # 3. Copy guis
    mod_guis = os.path.join(mod_tfphobos, "guis")
    if os.path.exists(mod_guis):
        shutil.rmtree(mod_guis)
    shutil.copytree(os.path.join(src_dir, "guis"), mod_guis)
    
    # 4. Copy script
    mod_script = os.path.join(mod_tfphobos, "script")
    if os.path.exists(mod_script):
        shutil.rmtree(mod_script)
    shutil.copytree(os.path.join(src_dir, "script"), mod_script)
    
    print(f"Successfully synchronized all updated files and folders to: {mod_tfphobos}")

if __name__ == "__main__":
    build()
