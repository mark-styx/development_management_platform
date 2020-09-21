import shutil
from datetime import datetime as dt

from project.project import Project

class New_Project(Project):

    def __init__(self,title,desc=None,lead=None):
        '''Initializes the new project'''
        title = title.replace(' ','_')
        super().__init__(title,desc,lead)
        if not lead: self.lead = self.gconn.name
        self.create_dirs(title)
        self.create_repo(title)
        self.add_project_entry()

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
            project,project_desc,project_status,project_lead,create_date
            )
        values
            ('{self.title}','{self.desc}','Pending Analyst Review','{self.lead}','{str(dt.now().date())}')
        '''

        if self.dev_mode: self.dbcon.xquery(q)
        if not self.dev_mode:self.dbcon.xquery('prod',q)