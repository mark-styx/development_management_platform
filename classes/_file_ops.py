import os
from datetime import datetime as dt
from glob import glob
from pathlib import Path
from os.path import abspath
from os.path import dirname
from inspect import getsourcefile

from _conf import config

class file_ops():
    '''Main project file interaction class.'''

    def __init__(self):
        self.current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
        self.project_level = Path(dirname(self.current_dir))
        self.projects_home = Path(dirname(self.project_level))

    def rename_folder(self,project,new_name):
        os.rename(self.projects_home/project,self.projects_home/new_name)

    def create_dir(self,dir_path,folder_name):
        '''Creates a directory, returns error if exists.
        input:
            dir_path (str, path of the target directory)
            folder_name (str, the target folder name )'''

        if Path.exists(dir_path/folder_name):
            return ('error','directory already exists')
        os.mkdir(dir_path/folder_name)
        new_dir = Path(dir_path/folder_name)
        print(f'directory {new_dir} created')
        return folder_name,new_dir

    def add_unit_file(self,dir_path,project_title,unit,author=None,ftype=None):
        '''Initializes a unit file creation routine based on the file type.
        input:
            dir_path (str, path of the target directory)
            project_title (str, name of the active project)
            unit (str, the name of the unit to be created)
            author (str, creator of the unit)
            ftype (str, the file extension name )'''

        create_date = str(dt.now().date)
        task_types = {
            'sql':self.sql_unit,'py':self.py_unit,'vba':None,'c#':None
        }
        task_types[ftype](dir_path,project_title,unit,create_date,author)

    def sql_unit(self,dir_path,project_title,unit,create_date,author=None):
        '''Creates a sql unit file.
        input:
            dir_path (str, path of the target directory)
            project_title (str, name of the active project)
            unit (str, the name of the unit to be created)
            create_date (str, string representation of the current data)
            author (str, creator of the unit)
            ftype (str, the file extension name )'''

        head = f'-- 0101010\n\n-- {project_title}\n\n'
        head += '-'*80;head += '\n'
        head += f'-- unit: {unit} | author: {author} | created: {create_date}\n'
        head += (('-'*80)+'\n')*2
        if Path.exists((dir_path) / f'{unit}.sql'): raise
        else:
            with open(dir_path/f'{unit}.sql','w') as f:
                f.write(head)

    def py_unit(self,dir_path,project_title,unit,create_date,author=None):
        '''Creates a python unit file.
        input:
            dir_path (str, path of the target directory)
            project_title (str, name of the active project)
            unit (str, the name of the unit to be created)
            create_date (str, string representation of the current data)
            author (str, creator of the unit)
            ftype (str, the file extension name )'''

        head = f'# {project_title}\n# unit: {unit} | author: {author} | created: {create_date}\n'
        if Path.exists((dir_path) / f'{unit}.sql'): raise
        else:
            with open(dir_path/f'{unit}.py','w') as f:
                f.write(head)