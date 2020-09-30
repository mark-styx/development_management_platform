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

class Arch_Menu():
    
    def __init__(self,parent,objects,tools,proj_home):
        self.gconn = git_conn()
        self.parent = parent
        self.objects = objects
        self.proj_home = proj_home
        self.tools = tools
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        proj_list,fields = Project(find=True).view_all()
        self.arch_proj_list = [x for x in proj_list if x[4] == 'inactive']
        self.arch_menu()

    def arch_menu(self):
        st_x,st_y = (260,25)
        self.objects['arch_menu'] = {}
        self.objects['arch_menu']['selector'] = Cbx(
            self.parent,(st_x,st_y),label=True,label_loc='above',size=(150,20),txt='Select Project',values=[x[1] for x in self.arch_proj_list])
        self.objects['arch_menu']['accept_proj'] = Btn(
            self.parent,(st_x+150,st_y),txt='Accept',alt_clr=True,
            cmd=self.activate_project)
        self.objects['arch_menu']['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')
        self.sub_menu()
    
    def activate_project(self):
        self.active_project = Outline(self.objects['arch_menu']['selector'].get())
        self.doc_mgr = doc_manager(self.active_project.title)
        try:
            self.clear_switches('_all_')
        except Exception as X:
            print(str(X))
        self.active_project_menu()

    def active_project_menu(self):
        if self.objects['arch_menu'].get('active'):
            self.clear_switches('_all_')
            self.destroy_all(self.objects['arch_menu'].get('active'))
        st_x,st_y = (410,60)
        self.objects['arch_menu']['active'] = {}
        data = self.objects['arch_menu'].get('active')
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
        data['react_btn'] = Btn(
            self.parent,txt='Reactivate',alt_clr=True,
            cmd=lambda:self.active_project.change_status('Active Development'),
            loc=(st_x,st_y+60)
        )
        for obj in self.objects['arch_menu']['sub_menu'].values():
            if type(obj) is Btn: obj.button['state'] = 'normal'

    def sub_menu(self):
        st_x,st_y = (5,215)
        self.objects['arch_menu']['sub_menu'] = {}
        data = self.objects['arch_menu'].get('sub_menu')
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
        scope = self.objects['arch_menu'].get('active')
        for btn in ['meta_btn','outline_btn','stats_btn','act_btn']:
            if tg_btn not in btn:
                try:
                    if scope[btn].active:
                        scope[btn].toggle()
                except Exception: continue

    def meta_view(self):
        self.clear_switches('meta')
        st_x,st_y = (155,60)
        self.objects['arch_menu']['active']['meta'] = {}
        data = self.objects['arch_menu']['active'].get('meta')
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
        self.objects['arch_menu']['active']['outline'] = {}
        data = self.objects['arch_menu']['active'].get('outline')
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
        self.objects['arch_menu']['active']['stats'] = {}
        data = self.objects['arch_menu']['active'].get('stats')
        try:
            stats = self.doc_mgr.build_stats()
        except Exception as X:
            stats = 'Stats incomplete for project.'
        data['body'] = Txt(self.parent,(st_x,st_y),size=(250,185))
        data['body'].text.insert('end',stats)
        data['body'].text['state'] = 'disabled'

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