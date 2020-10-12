from project.outline import Outline
from project.project import Project
from doc_manager import doc_manager
from _repo_tools import git_conn
from _file_ops import file_ops

from mk_cbx import Cbx,Ent,Txt
from mk_btn import Btn
from mk_lbl import Lbl
from unit_compiler import Unit_Window
from editor_view import Edit_Window,Project_Status

from tkinter.filedialog import askopenfilename
from subprocess import Popen
import os.path as osP
import webbrowser

class Live_Menu():
    
    def __init__(self,parent,objects,tools,proj_home,app_data):
        self.app_data = app_data
        self.gconn = git_conn()
        self.parent = parent
        self.objects = objects
        self.proj_home = proj_home
        self.tools = tools
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        proj_list,fields = Project(find=True).view_all()
        self.live_proj_list = [x for x in proj_list if x[4] == 'active']
        self.live_menu()

    def live_menu(self):
        st_x,st_y = (260,25)
        self.objects['live_menu'] = {}
        self.objects['live_menu']['selector'] = Cbx(
            self.parent,(st_x,st_y),label=True,label_loc='above',size=(150,20),txt='Select Project',values=[x[1] for x in self.live_proj_list])
        self.objects['live_menu']['accept_proj'] = Btn(
            self.parent,(st_x+150,st_y),txt='Accept',alt_clr=True,
            cmd=self.activate_project)
        self.objects['live_menu']['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')
        self.sub_menu()
    
    def activate_project(self):
        self.active_project = Outline(self.objects['live_menu']['selector'].get())
        self.doc_mgr = doc_manager(self.active_project.title)
        try:
            self.clear_switches('_all_')
        except Exception as X:
            print(str(X))
        self.active_project_menu()

    def active_project_menu(self):
        if self.objects['live_menu'].get('active'):
            self.clear_switches('_all_')
            self.destroy_all(self.objects['live_menu'].get('active'))
        st_x,st_y = (410,60)
        self.objects['live_menu']['active'] = {}
        data = self.objects['live_menu'].get('active')
        data['meta_btn'] = Btn(
            self.parent,txt='Meta',toggle=True,alt_clr=True,cmd=self.meta_view,deact_cmd=lambda: self.kill(data['meta']),
            loc=(st_x,st_y)
        )
        data['outline_btn'] = Btn(
            self.parent,txt='Outline',toggle=True,alt_clr=True,
            cmd=self.outline_view,
            deact_cmd=lambda: self.kill(data['outline']),
            loc=(st_x,st_y+20)
        )
        data['stats_btn'] = Btn(
            self.parent,txt='Stats',toggle=True,alt_clr=True,
            cmd=self.stats_view,
            deact_cmd=lambda: self.kill(data['stats']),
            loc=(st_x,st_y+40)
        )
        data['act_btn'] = Btn(
            self.parent,txt='Actions',toggle=True,alt_clr=True,
            cmd=self.actions_view,
            deact_cmd=lambda: self.kill(data['actions']),
            loc=(st_x,st_y+60)
        )
        for obj in self.objects['live_menu']['sub_menu'].values():
            if type(obj) is Btn: obj.button['state'] = 'normal'

    def sub_menu(self):
        st_x,st_y = (5,215)
        self.objects['live_menu']['sub_menu'] = {}
        data = self.objects['live_menu'].get('sub_menu')
        data['repo'] = Btn(
            self.parent,(st_x,st_y),txt='Goto Repo',
            cmd=lambda:[
                webbrowser.open(
                    f'https://github.com/Dentsu-Aegis-Reporting-and-Automation/{self.active_project.title}')
                ]
            )
        data['folder'] = Btn(
            self.parent,(st_x,st_y + 20),txt='Goto Folder',
            cmd=lambda:[
                Popen(f'''explorer /select,"{str(self.proj_home/self.active_project.title)}"''')
                ]
            )
        data['queue'] = Btn(
            self.parent,(st_x,st_y + 40),txt='Req Queue',
            cmd=lambda:[
                ]
            )
        data['queue'].button['state'] = 'disabled'
        data['canvas'] = self.parent.create_rectangle(0,210,110,280,fill='#1c1c1f')
        for obj in data.values():
            if type(obj) is Btn:
                obj.button['state'] = 'disabled'
        data['queue'].button['state'] = 'normal'

    def clear_switches(self,tg_btn):
        scope = self.objects['live_menu'].get('active')
        for btn in ['meta_btn','outline_btn','stats_btn','act_btn']:
            if tg_btn not in btn:
                try:
                    if scope[btn].active:
                        scope[btn].toggle()
                except Exception: continue

    def meta_view(self):
        self.clear_switches('meta')
        st_x,st_y = (155,60)
        self.objects['live_menu']['active']['meta'] = {}
        data = self.objects['live_menu']['active'].get('meta')
        data['title'] = Lbl(self.parent,'Title:',(st_x,st_y),size=(55,20))
        data['title_txt'] = Lbl(self.parent,f'{self.active_project.title}',(st_x+55,st_y),size=(200,20))
        data['desc'] = Lbl(self.parent,'Desc:',(st_x,st_y+20),size=(55,20))
        data['desc_txt'] = Lbl(self.parent,f'{self.active_project.desc}',(st_x+55,st_y+20),size=(200,20))
        data['status'] = Lbl(self.parent,'Status:',(st_x,st_y+40),size=(55,20))
        data['status_txt'] = Lbl(self.parent,f'{self.active_project.status}',(st_x+55,st_y+40),size=(200,20))
        data['tot_tasks'] = Lbl(self.parent,'Tasks:',(st_x,st_y+60),size=(55,20))
        data['tot_tasks_txt'] = Lbl(self.parent,f'{self.active_project.tasks}',(st_x+55,st_y+60),size=(200,20))
        data['comp_tasks'] = Lbl(self.parent,'Comp:',(st_x,st_y+80),size=(55,20))
        data['comp_tasks_txt'] = Lbl(self.parent,f'{self.active_project.comp}',(st_x+55,st_y+80),size=(200,20))
        data['lead'] = Lbl(self.parent,'Lead:',(st_x,st_y+100),size=(55,20))
        data['lead_txt'] = Lbl(self.parent,f'{self.active_project.lead}',(st_x+55,st_y+100),size=(200,20))
        data['created'] = Lbl(self.parent,'Created:',(st_x,st_y+120),size=(55,20))
        data['created_txt'] = Lbl(self.parent,f'{self.active_project.created}',(st_x+55,st_y+120),size=(200,20))
        data['est_comp'] = Lbl(self.parent,'Est_Comp:',(st_x,st_y+140),size=(55,20))
        data['est_comp_txt'] = Lbl(self.parent,f'{self.active_project.est_comp}',(st_x+55,st_y+140),size=(200,20))

    def outline_view(self):
        self.clear_switches('outline')
        st_x,st_y = (155,60)
        self.objects['live_menu']['active']['outline'] = {}
        data = self.objects['live_menu']['active'].get('outline')
        fields,records = self.active_project.ui_outline()
        outline = ''
        for rec in records:
            outline += f'{fields[0]}: {rec[0]}\n\t{fields[1]}: {rec[1]}\n\t{fields[2]}: {rec[2]}\n\t{fields[3]}: {rec[3]}\n\n'
        data['body'] = Txt(self.parent,(st_x,st_y),size=(250,185))
        data['body'].text.insert('end',outline)
        data['body'].text['state'] = 'disabled'

    def stats_view(self):
        self.clear_switches('stats')
        st_x,st_y = (155,60)
        self.objects['live_menu']['active']['stats'] = {}
        data = self.objects['live_menu']['active'].get('stats')
        try:
            stats = self.doc_mgr.build_stats()
        except Exception as X:
            stats = 'Stats incomplete for project.'
        data['body'] = Txt(self.parent,(st_x,st_y),size=(250,185))
        data['body'].text.insert('end',stats)
        data['body'].text['state'] = 'disabled'

    def actions_view(self):
        self.clear_switches('act_btn')
        st_x,st_y = (155,60)
        self.objects['live_menu']['active']['actions'] = {}
        data = self.objects['live_menu']['active'].get('actions')

        data['repo_head'] = Lbl(self.parent,'Repo',(st_x+25,st_y),size=(50,20))
        data['pull_repo'] = Btn(
            self.parent,(st_x,st_y+20),txt='Pull Repo',alt_clr=True,cmd=lambda:[
                    self.csa(data,'pull_repo'),
                    self.gconn.pull_repo(self.active_project.title)
                ]
            )
        data['clone_repo'] = Btn(
            self.parent,(st_x,st_y+40),txt='Clone Repo',alt_clr=True,cmd=lambda:[
                    self.csa(data,'clone_repo'),
                    self.gconn.clone_repo(self.active_project.title)
                ]
            )
        data['add_files'] = Btn(
            self.parent,(st_x,st_y+60),txt='Add Files',alt_clr=True,
            cmd=lambda:[self.csa(data,'add_files'),self.add_files()],
            deact_cmd=lambda:self.kill(data['add_files_sub']),toggle=True
            )
        data['update_repo'] = Btn(self.parent,(st_x,st_y+80),txt='Update Repo',alt_clr=True,cmd=lambda:[
                self.csa(data,'update_repo'),
                self.gconn.update_repo(self.active_project.title)
            ]
        )
        data['update_docs'] = Btn(self.parent,(st_x,st_y+100),txt='Update Docs',alt_clr=True,cmd=lambda:[
                self.csa(data,'update_docs'),
                self.doc_mgr.update_doc_package(),
                self.gconn.update_repo(self.active_project.title)
            ]
        )
        data['proj_head'] = Lbl(self.parent,'Project',(st_x+150,st_y+85),size=(50,20))
        data['edit_meta'] = Btn(self.parent,(st_x+125,st_y+105),txt='Edit Meta',alt_clr=True,cmd=lambda:[
                self.csa(data,'edit_meta'),
                self.edit_meta_wdw()
            ]
        )
        data['update_outline'] = Btn(self.parent,(st_x+125,st_y+125),txt='Update Outline',alt_clr=True,cmd=lambda:[
                self.csa(data,'update_outline'),
                self.update_outline_wdw()
            ]
        )
        data['update_status'] = Btn(self.parent,(st_x+125,st_y+145),txt='Update Status',alt_clr=True,cmd=lambda:[
                self.csa(data,'update_status'),
                self.proj_stat_wdw()
            ]
        )
        data['submit_to_testing'] = Btn(self.parent,(st_x+125,st_y+165),txt='Submit to Testing',alt_clr=True,cmd=lambda:[
                self.csa(data,'submit_to_testing')
            ]
        )
        data['submit_to_testing'].button['state'] = 'disabled'
        data['dvlp_head'] = Lbl(self.parent,'Develop',(st_x+150,st_y),size=(50,20))
        data['create_units'] = Btn(self.parent,(st_x+125,st_y+20),txt='Create Units',alt_clr=True,cmd=lambda:[
                #self.csa(data,'create_units')
                self.active_project.create_unit_files(
                    self.proj_home/self.active_project.title)
            ]
        )
        data['reclaim_units'] = Btn(self.parent,(st_x+125,st_y+40),txt='Reclaim Units',alt_clr=True,cmd=lambda:[
                self.reclaimation()
            ]
        )
        #data['reclaim_units'].button['state'] = 'disabled'
        data['compile_units'] = Btn(self.parent,(st_x+125,st_y+60),txt='Compile Units',
            alt_clr=True,cmd=lambda:[
                self.csa(data,'compile_units'),
                self.unit_wdw()
            ]
        )

    def csa(self,scope,tg_btn):
        btns = []
        for obj in scope:
            if type(scope[obj]) is Btn:
                btns.append(obj)
        for btn in btns:
            if tg_btn not in btn:
                try:
                    if scope[btn].active:
                        print(scope[btn],btn)
                        scope[btn].toggle()
                except Exception: continue

    def add_files(self):
        st_x,st_y = (155,185)
        data = self.objects['live_menu']['active'].get('actions')
        data['add_files_sub'] = {};data = data.get('add_files_sub')
        data['add_head'] = Lbl(self.parent,'Add Files',(st_x+25,st_y),size=(50,20))
        data['add_single'] = Btn(
            self.parent,(st_x,st_y+20),txt='Single File',alt_clr=True,cmd=self.add_single
            )
        data['add_all'] = Btn(
            self.parent,(st_x,st_y+40),txt='All Files',alt_clr=True,cmd=lambda:[
                self.gconn.add_all_files_to_repo(str(self.proj_home/self.active_project.title),self.active_project.title)
                ]
            )

    def add_single(self):
        fname = askopenfilename()
        if fname:
            pth = osP.dirname(fname)
            fn = osP.basename(fname)
            self.gconn.add_file_to_repo(pth,self.active_project.title,fn)

    def unit_wdw(self):
        self.unit_win = Unit_Window(self.parent,self.objects,self.tools,self.proj_home,self.active_project,self.app_data)

    def edit_meta_wdw(self):
        self.edit_meta = Edit_Window(self.parent,self.objects,self.tools,self.proj_home,self.active_project,'meta')

    def update_outline_wdw(self):
        self.outline_upd = Edit_Window(self.parent,self.objects,self.tools,self.proj_home,self.active_project,'outline')
    
    def proj_stat_wdw(self):
        self.proj_stat_upd = Project_Status(self.parent,self.objects,self.active_project)

    def reclaimation(self):
        unit = self.app_data.last_compile()
        self.active_project.reclaim(self.proj_home,unit)