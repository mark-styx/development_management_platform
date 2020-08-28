from __dev_mode___ import dev_mode
import argparse

# path tools
from pathlib import Path
from os.path import dirname
from os.path import abspath
from inspect import getsourcefile

class setup():
    '''First time setup tool'''

    def __init__(self,azure_user,azure_pass,git_token,project_parent_dir=None,dev_mode=dev_mode):
        self.azure_user,self.azure_pass = azure_user,azure_pass
        self.git_token,self.project_parent_dir = git_token,project_parent_dir
        self.current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
        self.config = self.module_from_file('config',Path(dirname(self.current_dir))/r'bin')
        if not dev_mode: self.config.setup(azure_user,azure_pass,git_token,project_parent_dir)
        conf = self.module_from_file('_conf',self.current_dir);conf=conf.config()
        d = conf.open_conf()
        self.env_dir = d['paths']['dev_path']
        self.add_env_path(dev_mode)
        print('done')

    # module loader
    def module_from_file(self,module_name,src_path=None):
        '''Imports a module from a file path and returns the module as an object'''

        import importlib.util
        file_path = src_path/f'{module_name}.py'
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def add_env_path(self,dev_mode):
        '''Initializes the add env path routine. Loads the db_tools module. Executes appropriate function based on dev_mode status.
        intput:
            dev_mode (boolean, status of development mode)'''

        db_tools = self.module_from_file('_db_tools',self.current_dir)
        if not dev_mode: self.prod_path(db_tools)
        if dev_mode: self.dev_path(db_tools)

    def prod_path(self,db_tools):
        '''Adds the environment path for the user to the production server. Executes query to delete the path record for the current user, followed by another query to insert the new path record for the user.
        input:
            db_tools module'''

        print('adding path to prod server')
        tools = db_tools.azure_conn()
        tools.xquery(
            'prod',
            f"delete dmp.environment_paths where usr = '{self.azure_user}'"
            )
        print('inserting record:')
        tools.xquery(
            'prod',
            f'''insert into dmp.environment_paths 
            values
                ('{self.azure_user}','{str(self.env_dir)}'
            '''
            )

    def dev_path(self,db_tools):
        '''Adds the environment path for the user to the development server. Executes query to delete the path record for the current user, followed by another query to insert the new path record for the user.
        input:
            db_tools module'''

        print('adding path to dev server')
        tools = db_tools.local_dev()
        print('checking for duplicates:')
        tools.xquery(
            f"delete dmp.environment_paths where usr = '{self.azure_user}'"
            )
        print('inserting record:')
        tools.xquery(
            f'''insert into dmp.environment_paths 
            values
                ('{self.azure_user}','{str(self.env_dir)}')
            '''
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('azure_user',help='The username used to log into the production server')
    parser.add_argument('azure_pass',help='The password used to log into the production server')
    parser.add_argument('git_token',help='Your personal Git access token. To locate, log into Git and navigate to the developer settings to produce a token.')
    args = parser.parse_args()
    print('user:',args.azure_user,'pass:',args.azure_pass,'git token:',args.git_token)
    setup(args.azure_user,args.azure_pass,args.git_token,dev_mode=dev_mode)