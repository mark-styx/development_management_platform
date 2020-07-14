# general overhead
import pickle
import importlib.util

# path tools
from os.path import dirname
from pathlib import Path
from os.path import abspath
from inspect import getsourcefile

# database connection engine
import urllib,pyodbc
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

# instantiate configuration dictionary
data = {
    'control':{
        'key':1928,
        'encrypt':False
    },
    'azure': {
        'user':'',
        'cred':'',
        'encrypt':True
    },
    
    'git':{
        'token':'',
        'encrypt':True
    },
    
    'paths':{
        'dev_path':'',
        'encrypt':False
        },
    'server':{
        'name':'tcp:opfinancedbsvr.database.windows.net',
        'prod':'opfinancedb',
        'encrypt':False
    }
}

def build_azure_engine(server,database,user,password):
    '''Creates the connection engine used to make the connection to the Azure Server'''
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='+ database + ';UID='+user+';PWD='+ password)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    return engine
    
def prod_engine():
    '''Gets the credentials from the config dictionary, decrypts values and returns a connection engine for the production server/database'''
    with open(current_dir/'data.cfg','rb') as f: d = pickle.load(f)
    with open(current_dir/'dmp_k.cfg','rb') as f: key = pickle.load(f)
    server = d['server']['name']
    database = d['server']['prod']
    user = cm.decrypt(d['azure']['user'],key)
    password = cm.decrypt(d['azure']['cred'],key)
    engine = build_azure_engine(server,database,user,password)
    return engine

def new_cipher():
    '''Creates a new encryption/decryption cipher to translate data'''
    key = cm.create_cipher()
    with open(current_dir/'dmp_k.cfg','wb') as f: pickle.dump(key,f)
    return key

def setup(azure_user,azure_pass,git_token,project_parent_dir=None):
    '''Initialize the setup process, accepts azure user/pass and git token. Project parent directory is optional, if not passed uses the current parent.
    Creates a dictionary of configuration data.'''
    if not project_parent_dir: project_parent_dir = toplevel
    server = data.get('server')
    key = new_cipher()
    data['azure']['user'] = cm.encrypt(azure_user,key)
    data['azure']['cred'] = cm.encrypt(azure_pass,key)
    data['git']['token'] = cm.encrypt(git_token,key)
    data['paths']['dev_path'] = project_parent_dir
    with open(current_dir/'data.cfg','wb') as f: pickle.dump(data,f)

def update_cred(azure_user=None,azure_pass=None,git_token=None):
    '''Updates a credential; all credentials will receive a new cipher key whether or not it was updated'''
    with open(current_dir/'data.cfg','rb') as f: d = pickle.load(f)
    with open(current_dir/'dmp_k.cfg','rb') as f: old_key = pickle.load(f)
    key = new_cipher()
    # get previous value if none passed
    if not azure_user: azure_user = cm.decrypt(d['azure']['user'],old_key)
    if not azure_pass: azure_pass = cm.decrypt(d['azure']['cred'],old_key)
    if not git_token: git_token = cm.decrypt(d['git']['token'],old_key)
    # update configuration dictionary
    d['azure']['user'] = cm.encrypt(azure_user,key)
    d['azure']['cred'] = cm.encrypt(azure_pass,key)
    d['git']['token'] = cm.encrypt(git_token,key)
    with open(current_dir/'data.cfg','wb') as f: pickle.dump(d,f)

def display_config():
    '''Loads the config dictionary and unencrypts the credentials, then displays the dictionary'''
    with open(current_dir/'data.cfg','rb') as f: d = pickle.load(f)
    with open(current_dir/'dmp_k.cfg','rb') as f: k = pickle.load(f)
    d['azure']['cred'] = cm.decrypt(d['azure']['cred'],k)
    d['azure']['user'] = cm.decrypt(d['azure']['user'],k)
    d['git']['token'] = cm.decrypt(d['git']['token'],k)
    for key in d: print(d[key])


if __name__ == "__main__":
    pass