import json
from datetime import datetime as dt

from os.path import basename,dirname,abspath,exists
from inspect import getsourcefile
from pathlib import Path


class App_Data():

    def __init__(self):
        self.get_meta_data()

    def get_meta_data(self):
        current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
        self._src = current_dir/'bin/app_data.json'
        if not exists(self._src):
            self.create_meta()
        with open(self._src,'r') as f:
            self.app_data = json.loads(f.read())

    def write(self):
        with open(self._src,'w') as f:
            f.write(json.dumps(self.app_data))
    
    def refresh(self): self.get_meta_data()

    def create_meta(self):
        self.app_data = {'last_compile':{'fname':'','date':''}}
        self.write()

    def last_compile(self,update=None):
        if not update:
            return self.app_data['last_compile']['fname']
        else:
            self.app_data['last_compile'].update({'fname':update,'date':str(dt.now())})
            self.write()

    def __call__(self,attribute):
        return self.app_data[attribute]