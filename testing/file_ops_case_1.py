# general overhead
import pandas as pd
import random as rand
from string import ascii_letters
from datetime import datetime as dt
from time import sleep

# path tools
from os.path import dirname
from pathlib import Path
from os.path import abspath
from inspect import getsourcefile
import importlib.util

# get the project parent directory
current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
project_level = Path(dirname(current_dir))

# module loader
def module_from_file(module_name,src_path=None):
    '''Imports a module from a file path and returns the module as an object'''

    if src_path is None: src_path = project_level
    file_path = src_path/f'{module_name}.py'
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# import the test_case class
test_case = module_from_file('__dmp_test_case',project_level/'classes')

class file_ops_case_1(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs(
            'git_conn','set_repo_perm',
            'Test that the set_repo_perm() updates the repo permissions'
            )
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def test_op(self):
        tests = []
        try:
            gconn = self.repo_tools.git_conn()
            repos = list(gconn.org.get_repos())
            repos = [x.full_name[x.full_name.find('/')+1:] for x in repos]
            repos.remove('development_manager')
            tests.append(1)
        except Exception as X:
            error = str(X)
            return ('failed',error)
        try:
            for repo in repos:
                gconn.set_repo_perm(gconn.dev_team,repo,'admin')
            tests.append(1)
        except Exception as X:
            error = str(X)
            return ('failed',error)
        if all(tests): return ('passed','values match')
        else:
            fail = tests.index(0)
            return ('failed',f'test {fail} failed')


config_tests = [
    git_conn_case_3
]

if __name__ == "__main__":
    for test in config_tests: test()