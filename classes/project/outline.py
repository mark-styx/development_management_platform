from project.project import Project

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
        self.dbcon.xquery(q)
        self.refresh()

    def ui_outline(self):
        fields = ['task_id','task_name','task_status','owner']
        reslts = self.dbcon.xquery(f"select {','.join(fields)} from dmp.project_outlines  where project = '{self.title}'")
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