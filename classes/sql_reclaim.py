from glob import glob
from pathlib import Path
from os.path import basename
from _sql_parser import sql_parser

class Reclaim():
    
    def __init__(self,dir_path,project):
        source = Path(dir_path)/project/'unit_files'
        lib = {}
        for x in source.glob('*.sql'):
            print(x)
            lib[basename(x).replace('.sql','')] = sql_parser(x)
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