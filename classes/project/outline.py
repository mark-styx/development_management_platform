from datetime import datetime as dt
from os import startfile

from project.project import Project
from sql_reclaim import Reclaim

class Outline(Project):

    def __init__(self,title,rkey=None):
        assert(any([title,rkey]))
        super().__init__(title=title,rkey=rkey)

    def get_outline(self):
        fields = self.dbcon.xquery(
            "select column_name from information_schema.columns where table_name = 'project_outlines'"
            )
        outline = self.dbcon.xquery(
            f"select * from dmp.project_outlines where project = '{self.title}'"
            )
        return outline,fields

    def add_to_outline(self,task_name,desc,owner=None):
        if not owner: owner = self.lead
        status = self.status
        q = f"""insert into dmp.project_outlines (
            project,task_name,task_desc,task_status,owner
            )
            values ('{self.title}','{task_name}','{desc}','{status}','{owner}')"""
        self.dbcon.xquery(q)
        self.refresh()

    def rem_outline(self,tid):
        q = f"delete dmp.project_outlines where task_id = {tid} and project = '{self.title}'"
        self.dbcon.xquery(q)
        self.refresh()

    def update_outline(self,field,task,value):
        q = f"update dmp.project_outlines set {field} = '{value}' where project = '{self.title}' and task_name = '{task}'"
        print(q)
        self.dbcon.xquery(q)
        self.refresh()

    def ui_outline(self):
        fields = ['task_id','task_name','task_status','owner']
        reslts = self.dbcon.xquery(f"select {','.join(fields)} from dmp.project_outlines  where project = '{self.title}' order by task_id asc")
        return fields,reslts

    def ui_outline_edit(self):
        fields = ['task_id','task_name','task_desc','owner']
        reslts = self.dbcon.xquery(f"select {','.join(fields)} from dmp.project_outlines  where project = '{self.title}'")
        return fields,reslts


    def est_timing(self):
        fields = ['task_id','task_name','est_completion','est_risks','est_risk_penalty']
        reslts = self.dbcon.xquery(f"select {','.join(fields)} from dmp.project_outlines  where project = '{self.title}'")
        return fields,reslts

    def get_status_opts(self):
        return self.dbcon.xquery('select rkey,status from dmp.project_status_list')

    def create_unit_files(self,dir_path):
        try:
            for unit in self.dbcon.xquery(f"select task_name from dmp.project_outlines where project = '{self.title}'"):
                print(dir_path,self.title,str(unit[0]))
                self.fops.sql_unit(dir_path,self.title,str(unit[0]),self.gconn.name)
        except Exception as X:
            print(str(X))

    def get_references(self,dir_path):
        rec = Reclaim(dir_path,self.title)
        ref = rec.ref.copy()
        tid = self.dbcon.xquery(
            f"select task_name,task_id from dmp.project_outlines where project = '{self.title}'"
            )
        d = dict(tid)
        for unit in ref:
            ref[unit] = [d[x] for x in ref[unit]]
        for unit in ref:
            self.update_outline('task_dependencies',unit,','.join([str(x) for x in ref[unit]]))
        return ref,rec

    def compile_unit(self,dir_path,unit):
        ref,rec = self.get_references(dir_path)
        rnames = rec.ref[unit]
        ridx = []
        for name in rnames:
            print(name)
            ridx += ref[name]
        print(ridx)
        uid = self.dbcon.xquery(
            f"select task_id from dmp.project_outlines where project = '{self.title}' and task_name = '{unit}'"
        ).pop()
        print(uid)
        ridx.append(str(uid[0]))
        ridx = [str(x) for x in ridx]
        ridx = ','.join(list(set(sorted(ridx))))
        q = f"""
                select task_name from dmp.project_outlines
                where project = '{self.title}' and task_id in ({ridx})
                order by task_id asc
            """
        print(q)
        files = self.dbcon.xquery(q)
        output = ''
        for f in files:
            with open(dir_path/self.title/f'unit_files/{str(f[0])}.sql', 'r') as fn:
                if unit in f:
                    output += f'-- compile_header: 0001001000\n\n'
                output += fn.read() + '\n\n'
        fname = dir_path/self.title/f"working_files/{unit}_compiled_{str(dt.now().date())}.sql"
        with open(fname,'w') as f:
            f.write(output)
        startfile(str(fname))

    def reclaim(self,dir_path,unit):
        rec = Reclaim(dir_path,self.title)
        rec.reclaim_unit(unit)