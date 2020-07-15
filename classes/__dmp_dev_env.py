# database connection engine
import urllib,pyodbc
from sqlalchemy import create_engine

# config
from _conf import config
cf = config()

# add local db connection to config dict
def add_local_config():
    usr,pwd = 'meow','1928'
    cf.add_configuration(
        {'local_cred':{
            'user':usr,
            'cred':pwd}
            },encrypt=False)

def add_local_config2():
    cf.add_configuration(
        {'local_server':{
            'name':'LPDTW1007890\SQLEXPRESS',
            'db':'dmp_dev_env'
        }},encrypt=False)

# defines the local database connection object
def general_connection(usr,pwd,dbname=None):
    if not dbname: dbname='master'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LPDTW1007890\SQLEXPRESS;DATABASE='+dbname+';UID='+usr+';PWD='+pwd)
    return cnxn

# creates a local database
def create_local_db(dbname):
    try:
        with general_connection(usr,pwd) as cnxn:
            cnxn.autocommit = True
            cur = cnxn.cursor()
            create_database = f'Create Database {dbname}'
            cur.execute(create_database)
            cur.close()
    except Exception as X:
        print('Command failed with response:\n',X)

def xquery(query,db=None):
    with general_connection(usr,pwd,db) as cnxn:
        cur = cnxn.cursor()
        print('executing query')
        cur.execute(query)
        try:
            return cur.fetchall()
        except:
            cur.close()


# add_local_config()
d = cf.open_conf()
usr,pwd,_x = d['local_cred'].values()

# create_local_db('dmp_dev_env')
# add_local_config2()
d = cf.open_conf()
svr,db,_x = d['local_server'].values()

# xquery('create schema dmp;','dmp_dev_env')
# xquery('''
# create table dmp.environment_paths (
#     usr nvarchar(255),
#     env_path nvarchar(255)
# )
# ''','dmp_dev_env')

# create project outline table
# xquery('''
# create table dmp.project_outlines (
#     rkey int identity,
#     project nvarchar(255),
#     task_id int,
#     task_name nvarchar(255),
#     task_desc nvarchar(max),
#     task_dependancies nvarchar(255),
#     task_status nvarchar(255),
#     owner nvarchar(255),
#     create_date date,
#     est_completion date,
#     tbls_affected nvarchar(max)
# )
# ''','dmp_dev_env')

xquery('''
create table dmp.project_list (
    rkey int identity,
    project nvarchar(255),
    project_desc nvarchar(255),
    project_status nvarchar(255),
    total_tasks int,
    completed_tasks int,
    project_lead nvarchar(255),
    create_date date,
    est_completion date
)
''','dmp_dev_env')