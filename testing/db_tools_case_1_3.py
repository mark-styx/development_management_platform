# general overhead
import pandas as pd
import random as rand
from string import ascii_letters

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

# Database Tool Tests
class azure_conn_test_config_inheritence(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs(
            'azure_conn','config_call',
            'Test that the __init__() function returns proper attributes.'
            )
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def test_op(self):
        tests = []
        try:
            az_con = self.db_tools.azure_conn()
            usr,pwd = az_con.az_usr,az_con.az_pwd
            svr,db = az_con.az_svr,az_con.pr_db
        except Exception as X:
            error = str(X)
            return ('failed',error)
        try:
            conf = self.config.config()
            if conf.get_azure_cred() == (usr,pwd):
                tests.append(1)
            if conf.get_azure_server_and_db() == (svr,db): tests.append(1)
            else: tests.append(0)
            if all(tests): return ('passed','successfully executed')
            else:
                fail = tests.index(0)
                return ('failed',f'test {fail} failed')
        except: return ('failed','return does not match')

class prod_engine_test(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs(
            'azure_conn','prod_engine',
            'Test that the prod_engine() function returns a working engine.'
            )
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def test_op(self):
        az_con = self.db_tools.azure_conn()
        try:
            engine = az_con.prod_engine()
            df = pd.read_sql('select top(10) * from cfm.clientdetail',engine)
            if len(df) > 0: return ('passed','successfully executed')
            else: return ('failed','no values returned from sql')
        except Exception as X:
            error = str(X)
            return ('failed',error)
        
class xquery_test(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs(
            'azure_conn','xquery',
            'Test that the xquery() function returns valid query results.'
            )
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def test_op(self):
        az_con = self.db_tools.azure_conn()
        try:
            query = 'select top(10) * from cfm.clientdetail'
            results = az_con.xquery('prod',query)
            if len(results) > 0: return ('passed','successfully executed')
            else: return ('failed','no values returned from sql')
        except Exception as X:
            error = str(X)
            return ('failed',error)

tests = [
    azure_conn_test_config_inheritence,
    prod_engine_test,
    xquery_test
]

if __name__ == "__main__":
    for test in tests: test()