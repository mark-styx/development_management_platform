# general overhead
import pickle
import importlib.util
from datetime import datetime as dt
from datetime import timedelta as td

# path tools
from os.path import dirname
from pathlib import Path
from os.path import abspath
from inspect import getsourcefile

# database connection engine
import urllib,pyodbc
import pandas as pd
from sqlalchemy import create_engine

# get the project parent directory
toplevel = Path(dirname(dirname(dirname(abspath(getsourcefile(lambda:0))))))
current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))

# module loader
def module_from_file(module_name,src_path=None):
    '''Imports a module from a file path and returns the module as an object'''

    if src_path is None: src_path = toplevel
    file_path = src_path/f'{module_name}.py'
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# load credential manager
cm = module_from_file('credential_management',toplevel/r'development_management_platform\classes')

class test_case():
    '''Test case superclass'''
    def __init__(self):
        '''Instantiate required class attributes and the config module'''
        self.name = self.tested = self.status = self.runtime = None
        self.pth = Path(r'C:\Users\mstyx\Anchor\development_management_platform\bin')
        self.cnf_module = module_from_file('config',self.pth)
    
    def grab_output(self,pth):
        '''Gets the output configuration dictionary and decrypts the credentials'''

        with open(pth/'data.cfg','rb') as f: d = pickle.load(f)
        with open(pth/'dmp_k.cfg','rb') as f: k = pickle.load(f)
        out_user = cm.decrypt(d['azure']['user'],k)
        out_cred = cm.decrypt(d['azure']['cred'],k)
        out_token = cm.decrypt(d['git']['token'],k)
        return out_user,out_cred,out_token

class config_setup_test(test_case):
    '''Tests setup function in config.py'''

    def __init__(self):
        start_time = dt.now()
        self.name = 'config_test';self.tested = 'setup() function'
        user,cred,token = 'test','1234','1234abcd'
        pth = Path(r'C:\Users\mstyx\Anchor\development_management_platform\bin')
        self.run_setup(user,cred,token,pth)
        u,c,t = self.grab_output(pth)
        outcome = []
        for x,y in zip((u,c,t),(user,cred,token)): outcome.append(x == y)
        end_time = dt.now();self.runtime = str(end_time-start_time)
        if all(outcome): self.status = 'passed'
        else: self.status = 'failed'

    def run_setup(self,user,cred,token,pth):
        '''Imports the configuration module and executes the setup function'''

        config = module_from_file('config',pth)
        config.setup(user,cred,token)
        return None
    
    def grab_output(self,pth):
        '''Gets the output configuration dictionary and decrypts the credentials'''

        with open(pth/'data.cfg','rb') as f: d = pickle.load(f)
        with open(pth/'dmp_k.cfg','rb') as f: k = pickle.load(f)
        out_user = cm.decrypt(d['azure']['user'],k)
        out_cred = cm.decrypt(d['azure']['cred'],k)
        out_token = cm.decrypt(d['git']['token'],k)
        return out_user,out_cred,out_token

class config_cred_update_test(test_case):
    '''Tests update_cred function in config.py'''

    def __init__(self):
        super().__init__()
        start_time = dt.now()
        self.name = 'config_test';self.tested = 'update_cred() function'
        pth = Path(r'C:\Users\mstyx\Anchor\development_management_platform\bin')
        user,cred,token = super().grab_output(pth)
        data = {
            'user':{'azure_user':user},'cred':{'azure_pass':cred},'token':{'git_token':token}
            }
        self.test(data,pth)
        end_time = dt.now();self.runtime = str(end_time-start_time)

    def test(self,data,pth):
        '''Imports config module, accepts dictionary of credentials and path of config dictionary. Updates each credential and executes the update_cred() function, then recollects the output and compares the input to the destination output.'''
        config = module_from_file('config',pth)
        udata = data.copy();outcome = []
        for rec in data:
            for a,b in data[rec].items():
                b += 'UD'
                config.update_cred(**{a:b})
                udata.update({a:b})
                user,cred,token = config_setup_test().grab_output(pth)
                u,c,t = (vals for val in data for vals in data[val].values())
                for x,y in zip((u,c,t),(user,cred,token)): outcome.append(x == y)
        if all(outcome): self.status = 'passed'
        else: self.status = 'failed'

class config_prod_engine_test(test_case):
    '''Tests prod_engine() and build_azure_engine() function in config.py'''

    def __init__(self):
        ''''''
        super().__init__()
        start_time = dt.now()
        self.name = 'config_test';self.tested = 'prod_engine() function'
        pth = Path(r'C:\Users\mstyx\Anchor\development_management_platform\bin')
        user,cred,token = super().grab_output(pth)
        outcome = []
        outcome.append(self.test_prod_engine())
        if all(outcome): self.status = 'passed'
        else: self.status = 'failed'
        end_time = dt.now();self.runtime = str(end_time-start_time)

    def test_prod_engine(self):
        '''Initialize the production connection engine and determine if values were returned. Also updates the credentials to valid ones from prev tests.'''
        self.cnf_module.update_cred('mstyx','MarControl2017')
        engine = self.cnf_module.prod_engine()
        try: df = pd.read_sql('select top(1) * from cfm.clientdetail',engine)
        except: return False
        else:
            if df.values.any(): return True
        

def save_test_outcome(data):
    '''Accepts a list of test classes and writes the attributes to a test case output file'''

    timestamp = str(dt.now()).replace(':','-').replace('.','_')
    with open(current_dir/f'test_outcomes/config_test__{timestamp}','w') as f:
        f.write(f'Unit Test Summary\nrundate:{timestamp}\n________________\n\n')
        for r in data:
            name,tested,status,runtime = r.name,r.tested,r.status,r.runtime
            f.write(f'\ttest: {name} | tested: {tested} | outcome: {status} | runtime: {runtime}\n')

if __name__ == "__main__":
    # instantiate test case classes
    setup = config_setup_test()
    update_cred = config_cred_update_test()
    prod_engine = config_prod_engine_test()
    # compiles classes in list
    test_cases = [setup,update_cred,prod_engine]
    # writes test output
    save_test_outcome(test_cases)
