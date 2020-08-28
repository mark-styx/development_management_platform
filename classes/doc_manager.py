import _db_tools,__dev_mode___
import plotly.figure_factory as ff
import plotly
import pandas as pd

from glob import glob
from random import randint
from datetime import datetime

from _conf import config
from _doc_tools import doc_tools
from _sql_parser import sql_parser
from _repo_tools import git_conn


class doc_manager():

    def __init__(self,project):
        if __dev_mode___.dev_mode: self.db = _db_tools.local_dev()
        else: self.db = _db_tools.azure_conn()
        self.project = project
        self.conf = config()
        self.proj_path = self.conf.env_path / project
        self.gconn = git_conn()
        self.get_data(project)

    def get_data(self,project):
        self.outline = pd.read_sql(
            f"select * from dmp.project_outlines where project = '{project}'",
            self.db.engine
            )
        self.project_meta = pd.read_sql(
            f"select * from dmp.project_list where project = '{project}'",
            self.db.engine
            )
        self.tasks = self.db.xquery(f"select task_id,task_name from dmp.project_outlines where project = '{project}' order by task_id asc")
        self.doc_tools = doc_tools(self.project_meta,self.outline)
        self.repo_stats = self.gconn.get_repo_stats(project)

    def get_file_lengths(self):
        pth = self.proj_path/'unit_files'
        stats = {}
        for unit in pth.glob('*.sql'):
            with open(unit,'r') as f:
                stats[os.path.basename(unit)] = len(f.read())
        stats['total'] = sum(stats.values())
        return stats

    def build_stats(self):
        pth = self.proj_path/'docs'
        timestamp = str(datetime.now())
        file_stats = self.get_file_lengths()
        Stats = f'Stats as of {timestamp}\n'
        Stats += f"commits: {self.repo_stats['commits']}\n"
        Stats += f"total edits: {self.repo_stats['total_changes'] + file_stats['total']} characters\n"
        Stats += '\nfile: length\n' 
        for key in file_stats.keys():
            val = file_stats[key]
            Stats += f'{key}: {val}\n'
        Stats += '\nweekly updates\n'
        for (week,add,dlt) in zip(self.repo_stats['weeks'],self.repo_stats['additions'],self.repo_stats['deletions']):
            Stats += f'week: {week} | added: {add} | deleted: {dlt}\n'
        return Stats

    def build_technical_doc(self):
        pth = self.proj_path/'unit_files'
        tdoc = 'Technical Outline:\n__________\n\n'
        for task_id,task in self.tasks:
            parsed = sql_parser(pth/f'{task}.sql')
            for idx,comm in parsed.comments.items():
                tdoc += f'{idx}: {comm}\n'
            tdoc += '\nTables Referenced:\n\n'
            for idx,tbl in parsed.tbl_ref:
                tdoc += f'{idx}: {tbl}\n'
            tdoc += '\n-----\n\n'
        return tdoc

    def get_cireq(self):
        ci_req = list(self.proj_path.glob('*.pptx'))
        if ci_req: req = self.doc_tools.ci_request(ci_req[0])
        else: req = 'ci request doc not found\n__________\n\n\n'
        self.req = req

    def build_readme(self):
        self.get_cireq()
        readme = self.req + self.doc_tools.compiled_outline
        return readme

    def update_doc_package(self):
        readme = self.build_readme()
        with open(self.proj_path/'README.md','w') as f:
            f.write(readme)
        with open(self.proj_path/'Outline.txt','w') as f:
            f.write(self.doc_tools.compiled_outline)
        stats = self.build_stats()
        with open(self.proj_path/'Stats.txt','w') as f:
            f.write(stats)
        tdoc = self.build_technical_doc()
        with open(self.proj_path/'Tech.txt','w') as f:
            f.write(tdoc)

    def ci_deliverables(self):

        self.get_cireq()
        g_data = self.outline[['task_name','create_date','est_completion','owner']]
        g_data.columns = ['Task','Start','Finish','Resource']
        rand_color = lambda: f'rgb({randint(0,255)},{randint(0,255)},{randint(0,255)})'
        owner_colors = {x:rand_color() for x in g_data['Resource'].tolist()}
        fig_plotly = ff.create_gantt(g_data,colors=owner_colors,index_col='Resource',title='Gantt Chart',show_colorbar=True,bar_width=0.4,showgrid_x=True,showgrid_y=True)
        #fig_plotly.show()
        html = plotly.io.to_html(fig_plotly)
        html_tbl = self.outline[['task_id','task_name','task_desc','owner','est_completion','est_risks','est_risk_penalty']].to_html(index=False)
        head_html = f'''
            <h1 
            style="text-align: left;">
            <span style="color: #444;" </span>
            <span style="letter-spacing: -3px;" </span>
            <span style="font-family: times, Times New Roman, times-roman, georgia, serif;" </span>
            <span style="margin: 0;" </span>
            <span style="padding: 0px 0px 6px 0px;" </span>
            <span style="font-size: 51px;" </span>
            <span style="line-height: 44px;" </span>
            <span style="font-weight: bold;" </span>
            {self.project}
            </h1>
            <p style="text-align: left;"><span style="font-family: times, Times New Roman, times-roman, georgia, serif;"> <span style="color: #444;"> <span style="margin: 0;"> <span style="padding: 0px 0px 6px 0px;"> <span style="font-size: 20px;"> <span style="line-height: 44px;"> <span style="letter-spacing: 0px;"> Task outline, risk assessment, and estimated completion time.</span></span></span></span></span></span></span></p>
        '''
        table_style = '''
        <head>
            <style>
            table, tr, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            }
            th, td {
            text-align: left;
            }
            #t01 {
            width: 100%;
            }
            #t01 tr:nth-child(even) {
            background-color: #eee;
            }
            #t01 tr:nth-child(odd) {
            background-color: #fff;
            }
            #t01 th {
            color: white;
            background-color: #444;
            }
            </style>
        </head>
        '''
        ci_req = '''<p
        style="text-align: left;"><span style="font-family: times, Times New Roman, times-roman, georgia, serif;"> <span style="color: #444;"> <span style="margin: 0;"> <span style="font-size: 15px;"> <span style="letter-spacing: 0px;">''' + self.req.replace('\n','<br>') + '</p>'
        html_tbl = table_style + '<table id=t01' + html_tbl[6:]
        with open(self.proj_path/r'docs/CI_Estimated_Timing.html','w') as f:
            f.write(head_html)
            f.write(ci_req)
            f.write(html)
            f.write(html_tbl)
