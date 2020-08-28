# database connection engine
import urllib,pyodbc
from sqlalchemy import create_engine

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
cf = module_from_file('_conf',project_level/'classes')

class azure_conn():

    def __init__(self):
        self.cf = cf.config()
        self.az_usr,self.az_pwd = self.cf.user,self.cf.password
        self.az_svr,self.pr_db = self.cf.az_svr,self.cf.pr_db

    def build_azure_engine(self,server,database,user,password):
        '''Creates the connection engine used to make the connection to the Azure Server'''

        params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='+ database + ';UID='+user+';PWD='+ password)
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        return engine

    def prod_engine(self):
        '''Gets the credentials from the config dictionary, decrypts values and returns a connection engine for the production server/database'''

        engine = self.build_azure_engine(self.az_svr,self.pr_db,self.az_usr,self.az_pwd)
        return engine

    def conn(self,server,dbname,usr,pwd):
        '''Creates odbc connection object:
        Accepts: server,database,user,password strings
        Returns: connection object'''

        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + dbname + ';UID=' + usr + ';PWD=' + pwd)
        return cnxn
    
    def xquery(self,target,query):
        '''Executes a query on a targetted database.
        target = ['prod'] | query = valid query string ('select * from dbo.example')'''

        db = {
            'prod':{'svr':self.az_svr,'db':self.pr_db,'usr':self.az_usr,'pwd':self.az_pwd}
        }
        targ = db.get(target)
        if not targ: return 'target not found, options include: [prod]'
        with self.conn(targ['svr'],targ['db'],targ['usr'],targ['pwd']) as cnxn:
            cur = cnxn.cursor()
            print('executing query')
            cur.execute(query)
            try:
                return cur.fetchall()
            except:
                cur.close()


class local_dev():

    def __init__(self):
        self.cf = cf.config()
        d = self.cf.open_conf()
        self.usr,self.pwd,_x = d['local_cred'].values()
        self.svr,self.db,_x = d['local_server'].values()
        self.engine = self.build_engine()

    def general_connection(self,usr,pwd,svr,db):

        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+svr+';DATABASE='+db+';UID='+usr+';PWD='+pwd)
        return cnxn

    def xquery(self,query):

        with self.general_connection(self.usr,self.pwd,self.svr,self.db) as cnxn:
            cur = cnxn.cursor()
            print('executing query')
            cur.execute(query)
            try:
                return cur.fetchall()
            except:
                cur.close()

    def build_local_engine(self,user,password,server,database):
        '''Creates the connection engine used to make the connection to the Local Server'''

        params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='+ database + ';UID='+user+';PWD='+ password)
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        return engine

    def build_engine(self):
        '''Gets the credentials from the config dictionary, decrypts values and returns a connection engine for the production server/database'''

        engine = self.build_local_engine(self.usr,self.pwd,self.svr,self.db)
        return engine