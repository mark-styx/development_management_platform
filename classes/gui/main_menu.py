from tkinter import *

from root_app import Root
from mk_btn import Btn

class Main_Menu(Root):
    
    def __init__(self):
        super().__init__()
        self.app_objects['main_menu'] = {}
        self.build_menu()
        self.root.mainloop()

    def build_menu(self):
        self.menu = Canvas(self.root)
        self.menu.config(bg=self.app_color)
        self.menu.pack(expand=True,fill='both')
        self.bknd = self.menu.create_image(300,168.5,image=self.app_objects['images']['bkgd2'])
        st_x,st_y = (5,10)
        self.app_objects['main_menu']['project_home'] = Btn(
            self.menu,(st_x,st_y),txt='Project Home',toggle=True,cmd=self.toggle_project_home,deact_cmd=lambda:self.toggle_project_home('destroy')
            )
        self.app_objects['main_menu']['settings'] = Btn(self.menu,(st_x,st_y + 20),txt='Settings',toggle=True)
        self.app_objects['main_menu']['settings'].button['state'] = 'disabled'
        self.app_objects['main_menu']['quit'] = Btn(self.menu,(st_x,st_y + 40),txt='Quit',cmd=quit)
        self.menu.create_rectangle(0,0,110,80,fill='#1c1c1f')

    def destroy_all(self,obj_dict):
        print(obj_dict)
        find_dicts = lambda X: [x for x in X if type(X[x]) is dict]
        sub = find_dicts(obj_dict)
        for x in sub:
            _sub = find_dicts(obj_dict[x])
            for _x in _sub:
                __sub = find_dicts(obj_dict[x][_x])
                for __x in __sub:
                    ___sub = find_dicts(obj_dict[x][_x][__x])
                    for ___x in ___sub:
                        self.kill(obj_dict[x][_x][__x].pop(___x))
                    self.kill(obj_dict[x][_x].pop(__x))
                self.kill(obj_dict[x].pop(_x))
            self.kill(obj_dict.pop(x))
        self.kill(obj_dict)

    def kill(self,obj_dict):
        for obj in obj_dict:
            if 'canvas' not in obj:
                obj_dict[obj].destroy()
            else:
                self.menu.delete(obj_dict[obj])
        
    def toggle_project_home(self,action='create'):
        if action == 'create':
            self.project_home = Project_Home(
                self.menu,{
                    'kill':self.kill,'destroy':self.destroy_all
                    },self.conf.env_path,self.app_objects
                )
            self.project_home.setup()
        elif action == 'destroy':
            self.project_home.destroy_all(self.project_home.objects)


from create_menu import Create_Menu
from live_menu import Live_Menu
from mk_cbx import Cbx,Ent,Txt
#from mk_btn import Btn
from mk_lbl import Lbl

class Project_Home(Frame):

    def __init__(self,parent,tools,proj_home,app_objects):
        self.proj_home = proj_home
        self.parent = parent;self.tools = tools
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        self.objects = app_objects
    
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
        self.objects['view_archived'] = Btn(self.parent,(st_x,st_y + 60),txt='View Archived')
        self.objects['view_archived'].button['state'] = 'disabled'
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
        self.live_menu = Live_Menu(self.parent,self.objects,self.tools,self.proj_home)

    def bug_report_menu(self):
        self.clear_switches('bug_reporting')
        self.bug_menu = Bug_Menu(self.parent,self.objects,self.tools,self.proj_home)


from project.project import Project
from project.outline import Outline

# from mk_cbx import Cbx,Ent,Txt
# from mk_btn import Btn
# from mk_lbl import Lbl

class Bug_Menu():
    
    def __init__(self,parent,objects,tools,proj_home):
        self.parent = parent
        self.objects = objects
        self.proj_home = proj_home
        self.tools = tools
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        proj_list,fields = Project(find=True).view_all()
        self.live_proj_list = proj_list
        self.sub_menu()

    def sub_menu(self):
        self.objects['bug_menu'] = {}
        data = self.objects.get('bug_menu')
        st_x,st_y = (5,215)
        data['new'] = Btn(
            self.parent,(st_x,st_y),txt='New Issue',
            cmd=lambda:[self.bug_menu()],
            toggle=True,deact_cmd=lambda:[self.kill(data['create_issue'])]
            )
        data['existing'] = Btn(
            self.parent,(st_x,st_y + 20),txt='View Issues',
            cmd=lambda:[self.view_issues()],
            toggle=True,deact_cmd=lambda:[]
            )
        data['canvas'] = self.parent.create_rectangle(0,210,110,260,fill='#1c1c1f')

    def bug_menu(self):
        st_x,st_y = (260,25)
        self.objects['bug_menu']['create_issue'] = {}
        data = self.objects['bug_menu'].get('create_issue')
        data['selector'] = Cbx(
            self.parent,(st_x,st_y),label=True,label_loc='above',size=(150,20),txt='Select Project',values=[x[1] for x in self.live_proj_list])
        data['accept_proj'] = Btn(
            self.parent,(st_x+150,st_y),txt='Accept',alt_clr=True,
            cmd=self.activate_project)
        data['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')
    
    def view_issues(self):
        st_x,st_y = (260,25)
        self.objects['bug_menu']['view_issues'] = {}
        data = self.objects['bug_menu'].get('view_issues')
        data['selector'] = Cbx(
            self.parent,(st_x,st_y),label=True,label_loc='above',size=(150,20),txt='Select Project',values=[x[1] for x in self.live_proj_list])
        data['accept_proj'] = Btn(
            self.parent,(st_x+150,st_y),txt='Accept',alt_clr=True,
            cmd=lambda:[self.activate_project(True)])
        data['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')

    def activate_project(self,viewer=False):
        if viewer:
            self.active_project = Outline(self.objects['bug_menu']['view_issues']['selector'].get())
            self.issue_selector()
        else: 
            self.active_project = Outline(self.objects['bug_menu']['create_issue']['selector'].get())
            self.bug_form()

    def bug_form(self):
        st_x,st_y = (300,50)
        data = self.objects['bug_menu'].get('create_issue')
        data['title'] = Ent(
            self.parent,(st_x,st_y),(150,20),label=True,txt='Bug Title'
        )
        data['desc'] = Txt(
            self.parent,(st_x,st_y+20),(150,100),label=True,txt='Description'
        )
        data['analyst_assigned'] = Cbx(
            self.parent,(st_x,st_y+120),(150,20),label=True,txt='Analyst Assigned',
            values=['Mathew Augusthy','Jeff Brown','Mark Styx']
        )
        data['reported_by'] = Ent(
            self.parent,(st_x,st_y+140),(150,20),label=True,txt='Reported By'
        )
        data['submit'] = Btn(
            self.parent,(337,st_y+180),(75,20),alt_clr=True,txt='Submit',
            cmd=lambda:[
                self.active_project.report_bug(
                    data['title'].get(),data['desc'].get(),
                    data['analyst_assigned'].get(),data['reported_by'].get()
                ),
                self.objects['bug_menu']['new'].toggle()
            ]
        )
        data['cancel'] = Btn(
            self.parent,(258,st_y+180),(75,20),alt_clr=True,txt='Cancel',
            cmd=lambda:[self.objects['bug_menu']['new'].toggle()]
        )

    def viewer_form(self):
        st_x,st_y = (300,30)
        data = self.objects['bug_menu'].get('view_issues')
        data['desc'] = Txt(
            self.parent,(st_x,st_y+20),(150,100),label=True,txt='Last Update'
        )
        data['analyst_assigned'] = Cbx(
            self.parent,(st_x,st_y+120),(150,20),label=True,txt='Analyst Assigned',
            values=['Mathew Augusthy','Jeff Brown','Mark Styx']
        )
        data['analyst_assigned'].insert(self.active_project.issue.assignee)
        data['desc'].insert(self.active_project.last_issue_update())
        data['submit'] = Btn(
            self.parent,(337,st_y+180),(75,20),alt_clr=True,txt='Update',
            cmd=lambda:[
                self.active_project.report_bug(
                    data['title'].get(),data['desc'].get(),
                    data['analyst_assigned'].get(),data['reported_by'].get()
                ),
                self.objects['bug_menu']['new'].toggle()
            ]
        )
        data['cancel'] = Btn(
            self.parent,(258,st_y+180),(75,20),alt_clr=True,txt='Cancel',
            cmd=lambda:[self.objects['bug_menu']['new'].toggle()]
        )

    def issue_selector(self):
        st_x,st_y = (260,25)
        data = self.objects['bug_menu'].get('view_issues')
        data['selector'].destroy()
        data['accept_proj'].destroy()
        data['title'] = Cbx(
            self.parent,(st_x,st_y),label=True,label_loc='above',size=(150,20),
            txt='Select Bug',values=self.active_project.get_issues()
        )
        data['accept_bug'] = Btn(
            self.parent,(st_x+150,st_y),txt='Accept',alt_clr=True,
            cmd=lambda:[
                self.active_project.select_issue(data['title'].get()),
                self.viewer_form()
            ]
        )

Main_Menu()