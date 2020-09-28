from _conf import config
from github import Github
from pathlib import Path
from datetime import datetime as dt
import os,time

class git_conn():
    '''Main git connection class object'''

    def __init__(self):
        '''Initializes the git connection object. Loads the configuration module and extracts the decrypted access token.'''
        self.env()

    def env(self):
        '''Initialize the evironment variables and create attributes'''
        
        conf = config();self.conf=conf
        self.tkn = conf.get_git_token()
        self.git = Github(self.tkn)
        self.user = self.git.get_user()
        self.name,self.login = self.user.name,self.user.login
        self.org = self.git.get_organization('Dentsu-Aegis-Reporting-and-Automation')
        self.dev_team = [x for x in list(self.org.get_teams()) if 'dev_team' in x.name].pop()

    def set_repo_perm(self,entity,repo_name,perm):
        '''Update the repository permissions for a user or team.
        input:
            entity: (git team or user object)
            repo_name (str, name of repository)
            perm: (str, the permission level to be granted)'''

        print(f'updating permissions for {repo_name}')
        repo = self.org.get_repo(repo_name)
        entity.set_repo_permission(repo,perm)
        print('done')

    def create_repo(self,project_name):
        '''Creates a new git repository. Adds the dev_team as admins.
        input:
            project_name (str, new project's name)'''

        print(f'creating repository for {project_name}...')
        self.org.create_repo(project_name,private=True)
        print('done')

    def initialize_new_repo(self,path,project):
        '''Sends the git commands to initialize the target directory as a new repository, adds the full path to the commit, and adds the results to the target project repository.
        input:
            path (str, path of the files to add)
            project (str, name of the target project)'''

        chpath = f'cd {path}'
        commands = [
            'git init','git add .',f'git commit -m "{project}"',
            f'git remote add origin https://github.com/Dentsu-Aegis-Reporting-and-Automation/{project}',
            'git push -u origin master'
            ]
        for cmd in commands:
            print(f'sending {cmd} to terminal at {chpath}')
            os.system('cmd /c "%s & %s"' % (chpath, cmd))

    def add_all_files_to_repo(self,path,project):
        '''Adds the full path to the commit, and adds the results to the target project repository.
        input:
            path (str, path of the files to add)
            project (str, name of the target project)'''

        chpath = f'cd {path}'
        commands = [
            'git add .',f'git commit -m "{project}"',
            'git push -u origin master'
            ]
        for cmd in commands:
            print(f'sending {cmd} to terminal at {chpath}')
            os.system('cmd /c "%s & %s"' % (chpath, cmd))

    def add_file_to_repo(self,path,project,fname):
        '''Sends the git commands to initialize the target directory as a repository, adds the full path to the commit, and adds the results to the target project repository.
        input:
            path (str, path of the files to add)
            project (str, name of the target project)
            fname (str, the name of the target file)'''
            
        chpath = f'cd {path}'
        commands = [
            f'git add {Path(path)/Path(fname)}',f'git commit -a -m "{project}"',
            'git push -u origin master'
            ]
        for cmd in commands:
            print(f'sending {cmd} to terminal at {chpath}')
            os.system('cmd /c "%s & %s"' % (chpath, cmd))
    
    def update_repo(self,project):
        path = self.conf.env_path
        if not os.path.exists(f'{path}/{project}'):
            self.clone_repo(project)
        chpath = f'cd {path}/{project}'
        commands = [
            f'git commit -a -m "updates: {dt.now()}"',
            'git push -u origin master'
            ]
        for cmd in commands:
            print(f'sending {cmd} to terminal at {chpath}')
            os.system('cmd /c "%s & %s"' % (chpath, cmd))

    def pull_repo(self,project):
        path = self.conf.env_path
        if not os.path.exists(f'{path}/{project}'):
            self.clone_repo(project)
        chpath = f'cd {path}/{project}'
        commands = [
            f'git pull origin master'
            ]
        for cmd in commands:
            print(f'sending {cmd} to terminal at {chpath}')
            os.system('cmd /c "%s & %s"' % (chpath, cmd))

    def clone_repo(self,project):
        path = self.conf.env_path
        chpath = f'cd {path}'
        commands = [
            f'git clone https://github.com/Dentsu-Aegis-Reporting-and-Automation/{project}'
            ]
        for cmd in commands:
            print(f'sending {cmd} to terminal at {chpath}')
            os.system('cmd /c "%s & %s"' % (chpath, cmd))

    def get_repo_stats(self,proj):
        '''Get the repository additions, deletions, and the total changes for the repository.
        input:
            proj (str, the name of the project to pull stats from)'''

        repo_stats = {}
        repo = self.org.get_repo(proj)
        repo_stats['commits'] = len(repo.get_stats_commit_activity())
        stats = repo.get_stats_contributors()
        weeks = []
        additions,deletions = [],[]
        for cont in range(len(stats)):
            for i in range(len(stats[cont].weeks)):
                weeks.append(stats[cont].weeks[i].w)
            weeks = list(dict.fromkeys(weeks))
            for i in range(len(weeks)):
                try: additions[i] += stats[cont].weeks[i].a
                except: additions.append(stats[cont].weeks[i].a)
                try: deletions[i] += stats[cont].weeks[i].d
                except: deletions.append(stats[cont].weeks[i].d)
        repo_stats['weeks'] = list(weeks)
        repo_stats['additions'] = additions
        repo_stats['deletions'] = deletions
        repo_stats['total_changes'] = sum(repo_stats['additions']) + sum(repo_stats['deletions'])
        return repo_stats

    def create_issue(self,repo,issue_title,desc,assigned):
        repo = self.org.get_repo(repo)
        members = self.org.get_members()
        users = [usr.name for usr in members]
        user = members[users.index(assigned)].login
        repo.create_issue(issue_title,desc,user)

    def list_issues(self,repo):
        repo = self.org.get_repo(repo)
        issues = repo.get_issues()
        self.issues = issues
        return [issue.title for issue in issues]

    def get_issue(self,repo,issue_title):
        repo = self.org.get_repo(repo)
        try:
            issue = self.issues[[issue.title for issue in self.issues].index(issue_title)]
        except Exception:
            issues = repo.get_issues()
            issue = issues[[issue.title for issue in issues].index(issue_title)]
        return issue

    def get_last_issue_update(self,repo,issue=None,issue_title=None):
        if not issue:
            issue = self.get_issue(repo,issue_title)
        comments = issue.get_comments()
        if list(comments):
            last_update = comments[-1].body
        else:
            last_update = issue.body
        return last_update