# general overhead
import pickle
import importlib.util

# path tools
from pathlib import Path
from os.path import dirname
from os.path import abspath
from inspect import getsourcefile

class config():
    '''Main configuration class. Handles all interactions with the configuration dictionary.'''

    def __init__(self):
        current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
        self.config_dir = Path(dirname(current_dir))/'bin'
        self.config = self.module_from_file('config',self.config_dir)
        self.crd_mgr = self.module_from_file('credential_management',current_dir)
        self.user,self.password = self.get_azure_cred()
        self.az_svr,self.pr_db = self.get_azure_server_and_db()

    # module loader
    def module_from_file(self,module_name,src_path=None):
        '''Imports a module from a file path and returns the module as an object'''
        
        file_path = src_path/f'{module_name}.py'
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    # get the user's azure credentials
    def get_git_token(self):
        '''Open the config dictionary and get git access token, then executes the decryption routine.
        Returns: git_token'''

        d = self.open_conf()
        with open(self.config_dir/'dmp_k.cfg','rb') as f: key = pickle.load(f)
        token = d['git']['token']
        return token

    # get the user's azure credentials
    def get_azure_cred(self):
        '''Open the config dictionary and get credentials for Azure, then executes the decryption routine.
        Returns: azure user and password'''

        d = self.open_conf()
        with open(self.config_dir/'dmp_k.cfg','rb') as f: key = pickle.load(f)
        user = self.crd_mgr.decrypt(d['azure']['user'],key)
        password = self.crd_mgr.decrypt(d['azure']['cred'],key)
        return user,password
    
    # get the azure server and databases from config
    def get_azure_server_and_db(self):
        '''Open the config dictionary and get connection criteria for Azure.
        Returns: azure server and production database'''

        d = self.open_conf()
        server = d['server']['name']
        prod_db = d['server']['prod']
        return server,prod_db

    # adds a custom key,value pair to configuration file with encryption status
    def add_configuration(self,payload,encrypt=None):
        '''Add a configuration to the conf dictionary.
        Accepts a dictionary payload formatted as {'category':{'sub category':'value'}}
        input: payload_dictionary,encrpytion:True/False
        updates: configuration dictionary'''

        d = self.open_conf()
        if encrypt: encrypt=True
        else: encrypt=False
        for k in payload: payload[k].update({'encrypt':encrypt})
        with open(self.config_dir/'dmp_k.cfg','rb') as f: dk = pickle.load(f)
        d.update(payload)
        self.save_conf(d)

    # removes a key from the configuration dictionary
    def rem_configuration(self,conf_to_rem):
        '''Removes the specified configuration from the config dictionary.
        input:
            conf_to_rem (str, correlating to a dictionary key)'''

        assert(conf_to_rem != 'control')
        d = self.open_conf()
        d.pop(conf_to_rem,None)
        self.save_conf(d)

    # update specified configuration value
    def update_conf(self,conf_to_upd):
        '''Update a specified configuration key
        input:
            conf_to_upd (dict, {key:{cat:val}})'''

        with open(self.config_dir/'dmp_k.cfg','rb') as f: c = pickle.load(f)
        d = self.open_conf()
        for key in conf_to_upd:
            d[key].update(conf_to_upd[key])
        self.save_conf(d)
    
    # adds encryption to all values that require
    def update_encryption(self,conf_dict):
        '''Updates the encryption of all values in the conf dictionary that require encryption.'''

        key = self.new_cipher()
        for k in conf_dict:
            if conf_dict[k].get('encrypt'):
                for _k in conf_dict[k]:
                    if _k != 'encrypt':
                        conf_dict[k][_k] = self.crd_mgr.encrypt(conf_dict[k][_k],key)
        return conf_dict

    # create a new cipher
    def new_cipher(self):
        '''Creates a new encryption/decryption cipher to translate data'''

        key = self.crd_mgr.create_cipher()
        with open(self.config_dir/'dmp_k.cfg','wb') as f: pickle.dump(key,f)
        return key

    # open configuration file and return the dictionary object
    def open_conf(self):
        '''Opens the conf dictionary and cipher, decrypts the values and returns the dictionary object.'''

        with open(self.config_dir/'data.cfg','rb') as f: d = pickle.load(f)
        with open(self.config_dir/'dmp_k.cfg','rb') as f: c = pickle.load(f)
        for key in d:
            if d[key].get('encrypt'):
                for k,v in d[key].items():
                    if k != 'encrypt': d[key][k] = self.crd_mgr.decrypt(v,c)
        return d
    
    # take a dictionary object and save as configuration file
    def save_conf(self,new_conf_dict):
        '''Takes a dictionary object and overwrites the configuration dictionary.'''

        assert(type(new_conf_dict) is dict)
        ctrl = new_conf_dict.get('control')
        assert(ctrl.get('key') == 1928)
        new_conf_dict = self.update_encryption(new_conf_dict)
        with open(self.config_dir/'data.cfg','wb') as f: pickle.dump(new_conf_dict,f)

if __name__ == "__main__":
    pass