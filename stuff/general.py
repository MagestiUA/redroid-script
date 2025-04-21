

import os
import zipfile
import hashlib
from pathlib import Path
import subprocess
import tempfile
import shutil


from tools.helper import bcolors, download_file, print_color

class General:
    
    
    def download(self):
        loc_md5 = ""
        if os.path.isfile(self.dl_file_name):
            with open(self.dl_file_name,"rb") as f:
                bytes = f.read()
                loc_md5 = hashlib.md5(bytes).hexdigest()
        while not os.path.isfile(self.dl_file_name) or loc_md5 != self.act_md5:
            if os.path.isfile(self.dl_file_name):
                os.remove(self.dl_file_name)
                print_color("md5 mismatches, redownloading now ....",bcolors.YELLOW)
            loc_md5 = download_file(self.dl_link, self.dl_file_name)
        
    def extract(self):
        print_color("Extracting archive...", bcolors.GREEN)
        print(self.dl_file_name)
        print(self.extract_to)
        with zipfile.ZipFile(self.dl_file_name) as z:
            z.extractall(self.extract_to)
    def copy(self):
        pass
    def install(self):
        # pass
        self.download()
        self.extract()
        self.copy()
    
    def install_custom_modules(self):
        mod_dir = Path("custom_modules")
        target = Path(self.work_dir) / "magisk" / "modules"
        
        if not mod_dir.exists():
            print_color("No custom modules found", bcolors.WARNING)
            return
        
        target.mkdir(parents=True, exist_ok=True)
        
        for mod in mod_dir.glob("*.zip"):
            print_color(f"Installing custom module: {mod.name}", bcolors.OKBLUE)
            with tempfile.TemporaryDirectory() as tmp:
                subprocess.run(["unzip", "-q", str(mod), "-d", tmp], check=True)
                shutil.copytree(tmp, target / mod.stem, dirs_exist_ok=True)
