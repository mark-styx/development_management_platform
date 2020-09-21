from glob import glob
from pathlib import Path
from os.path import basename,dirname

from datetime import datetime as dt
from _sql_parser import sql_parser

class Reclaim():
    
    def __init__(self,dir_path,project):
        source = Path(dir_path)/project/'unit_files'
        lib = {}
        for x in source.glob('*.sql'):
            print(x)
            lib[basename(x).replace('.sql','')] = sql_parser(x)
        self.source = source
        self.lib = lib
        self.ref = self.build_references()

    def build_references(self):
        refs = {}
        for unit in self.lib:
            refs[unit] = []
            for tbl in self.lib[unit].temp_created:
                for _unit in self.lib:
                    if tbl[1] in [x[1] for x in self.lib[_unit].tbl_ref] and _unit != unit: refs[unit].append(_unit)
            for var in self.lib[unit].var_init:
                for _unit in self.lib:
                    if var[1] in [x[1] for x in self.lib[_unit].var_ref] and _unit != unit: refs[unit].append(_unit)
        for unit in refs: refs[unit] = list(set(refs[unit]))
        self_ref = {}
        for unit in refs:
            self_ref[unit] = []
            for _unit in refs:
                if unit in refs[_unit]:
                    self_ref[unit].append(_unit)
        return self_ref

    def reclaim_unit(self,unit):
        matches = {}
        files = {}
        for fl in Path(Path(dirname(self.source))/'working_files').glob('*.sql'):
            if unit in basename(fl):
                name,date = basename(fl).replace('.sql','').split('_compiled_')
                date = dt.strptime(date,'%Y-%m-%d')
                matches[date] = name
                files[date] = fl
        with open(files[sorted([x for x in files]).pop(-1)],'r') as f:
            data = f.readlines()
        for line in data:
            if '0001001000' in line: idx = data.index(line) + 2
        with open(self.source/f'{unit}.sql','w') as f:
            f.writelines(data[idx:])