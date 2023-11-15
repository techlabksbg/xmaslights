import os
import glob
import time

class FileWatcher:
    def __init__(self):
        files = glob.glob("*.py") + ["3ddata.txt"] + glob.glob("animations_available/*.py")
        self.files = {}
        for file in files:
            if os.path.exists(file):
                self.files[file] = os.path.getmtime(file)
            else:
                self.files[file] = time.time()

    def new_files(self):
        for file in self.files.keys():
            if os.path.exists(file):
                if os.path.getmtime(file)>self.files[file]:
                    return True
        return False
    
