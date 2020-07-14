from _conf import config
from github import Github
import os

class git_conn():
    '''Main git connection class object'''

    def __init__(self):
        '''Initializes the git connection object. Loads the configuration module and extracts the decrypted access token.'''

        conf = config()
        self.tkn = conf.get_git_token()
        self.git = Github(self.tkn)
        self.user = self.git.get_user()
        self.name,self.login = self.user.name,self.user.login
        self.org = self.git.get_organization('Dentsu-Aegis-Reporting-and-Automation')

        

    def create_repo(self,project_name):
        '''Creates a new git repository.
        input:
            project_name (str, new project's name)'''

        print(f'creating repository for {project_name}...')
        self.user.create_repo(project_name,private=True)
        print('done')

    def add_files_to_repo(self,path,project):
        chpath = f'cd {path}'
        commands = [
            'git init','git add .',f'git commit -m "{project}"',
            f'git remote add origin https://github.com/{user}/{project}',
            'git push -u origin master'
            ]
        for cmd in commands:
            print(f'sending {cmd} to terminal at {chpath}')
            os.system('cmd /c "%s & %s"' % (chpath, cmd))