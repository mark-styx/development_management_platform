# general overhead
import json,sys
from datetime import datetime as dt

# path tools
from glob import glob
from pathlib import Path
from os.path import dirname
from os.path import abspath
from inspect import getsourcefile

class test_case():
    '''Main testing class.'''

    def __init__(self):
        # overhead
        current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
        sys.path.append(str(current_dir))
        self.test_dir = Path(dirname(current_dir))/r'testing/test_outcomes'
        self.config = self.module_from_file('_conf',current_dir)
        self.crd_mgr = self.module_from_file('credential_management',current_dir)
        self.db_tools = self.module_from_file('_db_tools',current_dir)
        self.repo_tools = self.module_from_file('_repo_tools',current_dir)
        self.proj_tools = self.module_from_file('_project_tools',current_dir)
        self.fops = self.module_from_file('_file_ops',current_dir)
        self.env_params()

    def env_params(self):
        conf = self.config.config()
        self.user,self.password = conf.get_azure_cred()
        self.az_svr,self.pr_db = conf.get_azure_server_and_db()

    def test_attrs(self,test_module,test_function,test_desc):
        self.test_module = test_module
        self.test_function = test_function
        self.test_desc = test_desc
        self.test_runtime = None
        self.test_start = dt.now()
        self.outcome = None
        self.narrative = None

    def end_test(self,outcome,narrative):
        self.test_end = dt.now()
        self.test_runtime = str(self.test_end - self.test_start)
        self.outcome = outcome
        self.narrative = narrative
        self.test_logger()

    def test_logger(self):
        res = list(self.test_dir.glob('test_results.json'))
        if not res: res = {}
        else:
            with open(list(res).pop(),'r') as f: res = json.load(f)
        test_res = {str(self.test_start):{
            'test_module':self.test_module,
            'test_function':self.test_function,
            'test_desc':self.test_desc,
            'test_runtime':self.test_runtime,
            'outcome':self.outcome,
            'narrative':self.narrative
            }
        }
        res.update(test_res)
        with open(self.test_dir/'test_results.json','w') as f: json.dump(res,f)

    # module loader
    def module_from_file(self,module_name,src_path=None):
        '''Imports a module from a file path and returns the module as an object'''
        import importlib.util
        file_path = src_path/f'{module_name}.py'
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module