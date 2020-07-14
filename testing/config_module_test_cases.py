# general overhead
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

# Configuration Tests
class config_get_azure_cred_test(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs('config','get_azure_cred','Test that the get_azure_cred() function returns proper values.')
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def test_op(self):
        try:
            conf = self.config.config()
            usr,pwd = conf.get_azure_cred()
        except Exception as X:
            error = str(X)
            return ('failed',error)
        if (self.user,self.password) == (usr,pwd):
            return ('passed','successfully executed')
        else: return ('failed','return does not match')

class config_get_azure_server_and_db_test(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs('config','get_azure_server_and_db','Test that the get_azure_server_and_db() function returns proper values.')
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def test_op(self):
        try:
            conf = self.config.config()
            svr,db = conf.get_azure_server_and_db()
        except Exception as X:
            error = str(X)
            return ('failed',error)
        if (self.az_svr,self.pr_db) == (svr,db):
            return ('passed','successfully executed')
        else: return ('failed','return does not match')

class config_add_configuration(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs('config','add_configuration','Test that the add_configuration() function returns proper values.')
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def payload(self):
        cn = '_test_'
        letters = list(ascii_letters);rand.shuffle(letters)
        cn += ''.join(letters[:rand.randint(0,len(ascii_letters)-1)])
        cn += str(rand.randint(0,999999))
        payload = {cn:{'key':'value'}}
        return payload

    def test_op(self):
        pay1 = self.payload()
        pay2 = self.payload()
        pay3 = self.payload()
        try:
            conf = self.config.config()
            conf.add_configuration(pay1,encrypt=True)
            conf.add_configuration(pay2,encrypt=False)
            conf.add_configuration(pay3)
        except Exception as X:
            error = str(X)
            return ('failed',error)
        d = conf.open_conf()
        for pay,enc in zip([pay1,pay2,pay3],[True,False,False]):
            pay[list(pay.keys())[0]].update({'encrypt':enc})
        if (
            pay1.items() <= d.items() and
            pay2.items() <= d.items() and
            pay3.items() <= d.items()
            ):
            return ('passed','successfully executed')
        else:
            self.debug(pay1,pay2,d)
            return ('failed','return does not match')

    def debug(self,pay1,pay2,d):
        print(pay1)
        print(pay2)
        print(d)

class config_save_conf(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs('config','save_conf','Test that the save_conf() function refuses improper input.')
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def test_op(self):
        t1 = {'garbage'}
        t2 = 'garbage'
        t3 = ['garbage']
        passed = []
        try:
            conf = self.config.config()
            t4 = conf.open_conf()
            for t in [t1,t2,t3]:
                try:
                    conf.save_conf(t)
                    passed.append(False)
                except Exception: passed.append(True)
            try:
                conf.save_conf(t4)
                passed.append(True)
            except Exception: passed.append(False)
        except Exception as X:
            error = str(X)
            return ('failed',error)
        if all(passed):
            return ('passed','successfully executed')
        else: return ('failed','return does not match')

class config_rem_configuration(test_case.test_case):
    def __init__(self):
        super().__init__()
        super().test_attrs('config','rem_configuration','Test that the rem_configuration() function deletes requested keys and fails if control is requested to be removed.')
        outcome,narrative = self.test_op()
        super().end_test(outcome,narrative)
    
    def test_op(self):
        conf = self.config.config()
        d = conf.open_conf()
        passed = []
        rem = [k for k in d if '_test_' in k]
        try:
            for r in rem: conf.rem_configuration(r)
            chk = [x for x in rem if x in list(d.keys())]
            if not chk: passed.append(True)
            else: passed.append(False)
            try:
                conf.rem_configuration('control')
                passed.append(False)
            except Exception: passed.append(True)
        except Exception as X:
            error = str(X)
            return ('failed',error)
        if all(passed):
            return ('passed','successfully executed')
        else:
            failed = passed.index(True)
            return ('failed',f'test {failed} failed')

config_tests = [
    config_get_azure_cred_test,
    config_get_azure_server_and_db_test,
    config_add_configuration,
    config_save_conf,
    config_rem_configuration
]

if __name__ == "__main__":
    for test in config_tests: test()