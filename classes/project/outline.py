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

    def add_to_outline(self,task_name,desc,status='new',owner=None):
        if not owner: owner = self.lead
        q = f"""insert into dmp.project_outlines (
            project,task_name,task_desc,task_status,owner
            )
            values ('{self.title}','{task_name}','{desc}','{status}','{owner}')"""
        self.dbcon.xquery(q)

    def update_outline(self,field,task,value):
        q = f"update dmp.project_outlines set {field} = '{value}' where project = '{self.title}' and task_name = '{task}'"
        self.dbcon.xquery(q)

    def ui_outline(self):
        fields = ['task_id','task_name','task_status','owner']
        reslts = self.dbcon.xquery(f"select {','.join(fields)} from dmp.project_outlines  where project = '{self.title}'")
        return fields,reslts