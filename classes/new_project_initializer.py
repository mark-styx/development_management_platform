# general overhead
import shutil,argparse
from datetime import datetime as dt

# development mode status
from __dev_mode___ import dev_mode

# modules
import _db_tools as dbtools
from _file_ops import file_ops
from _repo_tools import git_conn


class new_project():
    '''Class object representing a new project'''

    def __init__(self,project):
        '''Initializes the new project'''

        self.project_name = project
        self.env()
        self.create_dirs(project)
        self.create_repo(project)
        self.add_project_entry()
        print(f'new project, {project} initialized')

    def env(self):
        '''Initializes the new project evironment variables.
        instantiates the db,gconn,and fops attributes'''

        # direct to db based on dev mode status
        if dev_mode: self.db = dbtools.local_dev()
        else: self.db = dbtools.azure_conn()
        
        # instantiate git connection
        self.gconn = git_conn()
        self.fops = file_ops()

    def create_dirs(self,project):
        '''Copies the new project template folder tree to the new project path.
        input:
            project (str, name of new project)
        instantiates the proj_path attribute'''

        shutil.copytree(
            self.fops.project_level/'bin/new_proj_template',
            self.fops.projects_home/project
            )
        self.proj_path = self.fops.projects_home/project

    def create_repo(self,project):
        '''Creates the git repository for the project, initializes the local directory as a repo.'''

        self.gconn.create_repo(project)
        self.gconn.initialize_new_repo(self.proj_path,project)

    def add_project_entry(self):
        '''Adds the project to the dmp.project_list sql table.'''

        q = f'''insert into dmp.project_list (
            project,project_status,project_lead,create_date
            )
        values
            ('{self.project_name}','new','{self.gconn.name}','{str(dt.now().date())}')
        '''

        if dev_mode: self.db.xquery(q)
        if not dev_mode:self.db.xquery('prod',q)

if __name__ == "__main__":
    '''Command line input tool to add a new project'''

    parser = argparse.ArgumentParser()
    parser.add_argument('project_name',help='The name of the new project')
    args = parser.parse_args()
    new_project(args.project_name)