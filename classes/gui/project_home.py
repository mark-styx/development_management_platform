from tkinter import Frame

from create_menu import Create_Menu
from archived_menu import Arch_Menu
from bug_reporting import Bug_Menu
from live_menu import Live_Menu

from mk_cbx import Cbx,Ent,Txt
from mk_btn import Btn
from mk_lbl import Lbl

class Project_Home(Frame):

    def __init__(self,parent,tools,proj_home,app_objects):
        self.proj_home = proj_home
        self.app_objects = app_objects
        self.parent = parent;self.tools = tools
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        app_objects['project_home'] = {}
        self.objects = app_objects.get('project_home')

    def setup(self):
        st_x,st_y = (5,105)
        self.objects['create'] = Btn(
            self.parent,(st_x,st_y),txt='Create',cmd=self.proj_create_menu,
            deact_cmd=lambda:self.destroy_all(self.create_menu.objects['create_menu']),toggle=True)
        self.objects['live_projects'] = Btn(
            self.parent,(st_x,st_y + 20),txt='Live Projects',
            cmd=self.live_proj_menu,
            deact_cmd=lambda:self.destroy_all(self.live_menu.objects['live_menu']),
            toggle=True
        )
        self.objects['bug_reporting'] = Btn(
            self.parent,(st_x,st_y + 40),txt='Bug Reporting',
            cmd=self.bug_report_menu,
            deact_cmd=lambda:self.destroy_all(self.objects['bug_menu']),
            toggle=True
        )
        self.objects['view_archived'] = Btn(
            self.parent,(st_x,st_y + 60),txt='View Archived',
            cmd=self.arch_proj_menu,
            deact_cmd=lambda:self.destroy_all(self.objects['arch_menu']),
            toggle=True
        )
        self.objects['canvas'] = self.parent.create_rectangle(0,100,110,190,fill='#1c1c1f')

    def clear_switches(self,tg_btn):
        for btn in ['create','live_projects','bug_reporting','view_archived']:
            if tg_btn not in btn:
                if self.objects[btn].active:
                    self.objects[btn].toggle()

    def proj_create_menu(self):
        self.clear_switches('create')
        self.create_menu = Create_Menu(self.parent,self.objects,self.tools)

    def live_proj_menu(self):
        self.clear_switches('live_projects')
        self.live_menu = Live_Menu(self.parent,self.objects,self.tools,self.proj_home,self.app_objects['app_data'])

    def bug_report_menu(self):
        self.clear_switches('bug_reporting')
        self.bug_menu = Bug_Menu(self.parent,self.objects,self.tools,self.proj_home)

    def arch_proj_menu(self):
        self.clear_switches('view_archived')
        self.arch_menu = Arch_Menu(self.parent,self.objects,self.tools,self.proj_home)
