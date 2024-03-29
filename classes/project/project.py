import sys,os
sys.path.append(r'C:\Users\mstyx\Anchor\development_management_platform\classes')

from datetime import datetime as dt

# development mode status
from __dev_mode___ import dev_mode

# modules
import _db_tools as dbtools
from _file_ops import file_ops
from _repo_tools import git_conn

class Project():

    def __init__(self,title=None,desc=None,lead=None,rkey=None,find=False):
        self.dev_mode = dev_mode
        self.gconn = git_conn()
        self.fops = file_ops()
        if dev_mode: self.dbcon = dbtools.local_dev()
        else: self.dbcon = dbtools.azure_com()

        self.title = title
        self.desc = desc
        self.lead = lead
        if not find:
            if rkey:
                self.get_attrs(rkey)
            else:
                self.get_rkey()

    def refresh(self):
        self.get_attrs(self.rkey)

    def get_attrs(self,rkey):
        meta = self.dbcon.xquery(
            f'''
            select 
                project,project_desc,project_status,project_lead,total_tasks,completed_tasks,
                create_date,est_completion
            from dmp.project_list
            where rkey = {rkey}'''
            ).pop()
        self.title,self.desc,self.status,self.lead,self.tasks,self.comp,self.created,self.est_comp = meta

    def get_rkey(self):
        res,_ = self.view_all()
        rkey = [x[0] for x in res if x[1] in self.title]
        if rkey:
            self.rkey = rkey.pop()
            self.get_attrs(self.rkey)

    def view_all(self):
        fields = 'rkey,project,project_status,project_lead,dev_status'
        results = self.dbcon.xquery(f'select {fields} from dmp.project_list')
        return results,fields

    def change_title(self,new_name):
        if self.title != new_name:
            repo = self.gconn.org.get_repo(self.title)
            repo.edit(name=new_name)
            self.fops.rename_folder(self.title,new_name)
            self.dbcon.xquery(f"update dmp.project_list set project = '{new_name}' where project = '{self.title}'")
            self.dbcon.xquery(f"update dmp.project_outlines set project = '{new_name}' where project = '{self.title}'")
            self.title = new_name

    def change_desc(self,new_desc):
        if self.desc != new_desc:
            repo = self.gconn.org.get_repo(self.title)
            repo.edit(description=new_desc)
            self.dbcon.xquery(f"update dmp.project_list set project_desc = '{new_desc}' where project = '{self.title}'")
            self.desc = new_desc

    def change_lead(self,new_lead):
        if self.lead != new_lead:
            self.dbcon.xquery(f"update dmp.project_list set project_lead = '{new_lead}' where project = '{self.title}'")
            self.lead = new_lead

    def change_status(self,new_stat):
        if self.status != new_stat:
            self.dbcon.xquery(f"update dmp.project_list set project_status = '{new_stat}' where project = '{self.title}'")
            self.dbcon.xquery(f"update dmp.project_outlines set task_status = '{new_stat}' where project = '{self.title}'")
            self.stat = new_stat

    def report_bug(self,bug_title,desc,analyst,reported_by):
        q = f'''insert into dmp.bug_reports (
            project,title,bug_description,analyst_assigned,reported_by
        )
        values
            ('{self.title}','{bug_title}','{desc}','{analyst}','{reported_by}')
        '''
        self.dbcon.xquery(q)
        self.gconn.create_issue(self.title,bug_title,desc,analyst)

    def get_issues(self):
        return self.gconn.list_issues(self.title)
    
    def close_issue(self):
        self.issue.edit(state='closed')
        self.dbcon.xquery(f'''
            update dmp.bug_reports
            set status = 'Closed'
            where project = '{self.title}' and title = '{self.issue.title}'
            ''')

    def update_issue(self,body,assignee):
        self.dbcon.xquery(f'''
            update dmp.bug_reports
            set last_update = '{dt.now().date()}'
            where project = '{self.title}' and title = '{self.issue.title}'
            ''')
        self.issue.create_comment(body)
        if self.issue.assignee.name != assignee:
            self.issue.remove_from_assignees(self.issue.assignee.login)
            self.issue.add_to_assignees(self.gconn.get_user(assignee))

    def select_issue(self,issue):
        self.issue = self.gconn.get_issue(self.title,issue)

    def last_issue_update(self):
        return self.gconn.get_last_issue_update(self.title,issue=self.issue)