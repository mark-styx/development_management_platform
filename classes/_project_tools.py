# overhead
import pandas as pd
from string import digits
from distutils.util import strtobool
from datetime import datetime as dt

# dmp tools
import _db_tools
from __dev_mode___ import dev_mode

class proj_tools():
    ''''''

    def __init__(self,project=None):
        ''''''

        if dev_mode: self.db = _db_tools.local_dev()
        else: self.db = _db_tools.azure_conn()
        self.active_project = None
        if project: self.select_project(project)
        self.proj_fields = list(pd.read_sql(
                'select top(1) * from dmp.project_list',self.db.engine
                ).columns
            )
        self.outline_fields = list(pd.read_sql(
                'select top(1) * from dmp.project_outlines',self.db.engine
                ).columns
            )

    def add_to_outline(self,project=None,fields=[],values=[]):
        ''''''

        autofields = ['rkey','project','task_id','create_date','tbls_affected']
        if not project: project = self.active_project
        if not fields: fields = [x for x in self.outline_fields if x not in autofields]
        if not values:
            print(fields)
            fields = input('fields to update:\n').split(',')
            cont = True
            while cont:
                values.append(input('values to add:\n').split(','))
                cont = strtobool(input('continue (T/F):\n'))
        assert(all([True for x in fields if x in self.outline_fields]))
        print(f'adding {values} to {project} outline')
        ins_st = f'''
insert into dmp.project_outlines (
    project,{",".join(fields)}
)
values
'''
        depth = isinstance(values[0],list)
        if depth:
            for idx,rec in enumerate(values):
                assert(len(fields)==len(rec))
                record = f"\t('{project}','" + "','".join(rec) + "')"
                if idx + 1 != len(values): record += ','
                ins_st += (record + '\n')
        else:
            assert(len(fields)==len(values))
            ins_st += f"\t('{project}','" + "','".join(values) + "')"
        print('old outline:\n')
        self.view_outline(project)
        self.db.xquery(ins_st)
        print('\nnew outline:\n')
        self.view_outline(project)


    def update_project(self,field,value,project=None):
        ''''''

        if not project: project = self.active_project
        assert(project)
        assert(field in self.proj_fields)
        print('old values:')
        self.view_project(project)
        upd_query = f'''
            update dmp.project_list
            set {field} = '{value}'
            where project = '{project}'
        '''
        self.db.xquery(upd_query)
        print('\nnew values:')
        self.view_project(project)

    def update_outline(self,project=None,section=None,field=None,new_val=None):
        ''''''

        if not project: project = self.active_project
        if not section: section = self.select_outline_sect(project)
        if not field: field = self.choose_field(project,section)
        if not new_val: new_val = input('please add update value\n')
        assert(project);assert(new_val)
        print('\n\n\nold entry:\n')
        self.view_outline(project,section=section)
        upd_query = f'''
            update dmp.project_outlines
            set {field} = '{new_val}'
            where project = '{project}'
                and task_name = '{section}'
        '''
        self.db.xquery(upd_query)
        print('\n\n\nnew entry:\n')
        self.view_outline(project,section=section)

    def choose_field(self,project,section):

        autofields = ['rkey','project','task_id','create_date','tbls_affected']
        fields = [x for x in self.outline_fields if x not in autofields]
        ask = lambda: input(f'please select from {list(zip(range(len(fields)),fields))}')
        valid = lambda X: (X in digits) and (int(X) < len(fields))
        usr_chc = ask()
        while not valid(usr_chc):
            usr_chc = ask()
        return fields[int(usr_chc)]
        
        
    def select_outline_sect(self,project=None):
        ''''''
        
        if not project: project = self.active_project
        outline = self.view_outline(project,ret=True)
        if not outline: return None
        usr_sel = lambda: input(f'select a section number:\n{[(x[0],x[3]) for x in outline]}\n')
        sel_chk = lambda X: X in [x[0] for x in outline]
        usr_chc = None
        while not sel_chk(usr_chc):
            usr_chc = usr_sel()
            try: usr_chc = int(usr_chc)
            except Exception: print('please enter integer\n')
        out = [x[3] for x in outline if x[0] == usr_chc].pop()
        print('\n\nselected section:',out,'\n')
        return out
    
    def view_project(self,project,ret=None):
        ''''''

        get_proj = lambda: self.db.xquery(
            f"select * from dmp.project_list where project = '{project}'"
            ).pop()
        for key,val in zip(self.proj_fields,get_proj()): print(f'{key}: {val}')

    def view_outline(self,project,ret=None,section=None):
        ''''''
        query = f"select * from dmp.project_outlines where project = '{project}'"
        if section: query += f" and task_name = '{section}'"
        outline = self.db.xquery(query)
        if not outline:
            print('current outline is empty')
            return None
        for row in outline:
            for key,val in zip(self.outline_fields,row): print(f'{key}: {val}')
        if ret: return outline

    def update_local(self):
        ''''''

        p_list = pd.read_sql('select * from dmp.project_list',self.db.engine)
        outline = pd.read_sql('select * from dmp.project_outlines',self.db.engine)
        p_list.to_json('../bin/project_list.json',orient='table',index=False)
        outline.to_json('../bin/outline.json',orient='table',index=False)

    def display_projects(self,ret=None):
        ''''''

        projects = self.db.xquery(
            '''
                select 
                    project,project_desc,project_status,project_lead,create_date
                from dmp.project_list
            '''
        )
        for proj in projects:
            project,project_desc,project_status,project_lead,create_date = proj
            print(
                f'name: {project}\ncreated: {create_date}\ndesc: {project_desc}\ncontact: {project_lead}\nstatus: {project_status}\n\n'
                )
        if ret: return projects


    def select_project(self,proj=None):
        ''''''

        if not proj:
            projects = self.display_projects(ret=True)
            names = list(zip(range(len(projects)),[x[0] for x in projects]))
            print(names)
            usr_sel = lambda: input(f'select a project number:\n{names}\n')
            sel_chk = lambda X: X in [x[0] for x in names]
            usr_chc = None
            while not sel_chk(usr_chc):
                usr_chc = usr_sel()
                try: usr_chc = int(usr_chc)
                except Exception: print('please enter integer\n')
            proj = [x[1] for x in names if x[0] == usr_chc].pop()
        self.active_project = proj
        print(f'active project: {self.active_project}')