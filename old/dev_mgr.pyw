import sys,os
from os.path import dirname,abspath
from inspect import getsourcefile
from pathlib import Path
current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
sys.path.append(str(current_dir/'classes'))

from _conf import config
from initialize_environment import setup
from new_project_initializer import new_project
from _project_tools import proj_tools
from doc_manager import doc_manager

class Dev_Mgr():

    def create_env(
        self,azure_user,azure_pass,git_token,project_parent_dir=None,dev_mode=dev_mode
        ):
        setup(azure_user,azure_pass,git_token,project_parent_dir=None,dev_mode=dev_mode)

    def create_project(self,project):
        new_project(project)

    def configure(self,action,payload,encrypt=None):
        conf = config()
        available = ['add_configuration','rem_configuration','update_conf']
        commands = [conf.add_configuration,conf.rem_configuration,conf.update_conf]
        if action not in available:
            raise KeyError('selection not available, options are: add_configuration, rem_configuration, update_conf')
        if action in ('add_configuration','update_conf'):
            assert(type(payload) is dict)
        if action in ('rem_configuration'):
            assert(type(payload) is str)
        if encrypt:
            commands[available.index(action)](payload,encrypt)
        else: commands[available.index(action)](payload)

    