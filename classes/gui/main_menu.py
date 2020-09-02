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
        st_x,st_y = (5,10)
        self.app_objects['main_menu']['project_home'] = Btn(
            self.menu,(st_x,st_y),txt='Project Home',toggle=True,cmd=self.toggle_project_home,deact_cmd=lambda:self.toggle_project_home('destroy')
            )
        self.app_objects['main_menu']['settings'] = Btn(self.menu,(st_x,st_y + 20),txt='Settings',toggle=True)
        self.app_objects['main_menu']['quit'] = Btn(self.menu,(st_x,st_y + 40),txt='Quit',cmd=quit)
        self.menu.create_rectangle(0,0,110,80,fill='#1c1c1f')

    def destroy_all(self,obj_dict):
        find_dicts = lambda X: [x for x in X if type(X[x]) is dict]
        sub = find_dicts(obj_dict)
        for x in sub:
            _sub = find_dicts(obj_dict[x])
            for _x in _sub:
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
            self.project_home = Project_Home(self.menu,{'kill':self.kill,'destroy':self.destroy_all})
            self.project_home.setup()
        elif action == 'destroy':
            self.project_home.destroy_all(self.project_home.objects)


from mk_cbx import Cbx,Ent,Txt
from mk_lbl import Lbl

class Project_Home(Frame):

    def __init__(self,parent,tools):
        self.parent = parent;self.tools = tools
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        self.objects = {}
    
    def setup(self):        
        st_x,st_y = (5,105)
        self.objects['create'] = Btn(
            self.parent,(st_x,st_y),txt='Create',cmd=self.proj_create_menu,
            deact_cmd=lambda:self.destroy_all(self.create_menu.objects['create_menu']),toggle=True)
        self.objects['live_projects'] = Btn(self.parent,(st_x,st_y + 20),txt='Live Projects',
        cmd=self.live_proj_menu,deact_cmd=lambda:self.destroy_all(self.live_menu.objects['live_menu']),toggle=True)
        self.objects['bug_reporting'] = Btn(self.parent,(st_x,st_y + 40),txt='Bug Reporting')
        self.objects['view_archived'] = Btn(self.parent,(st_x,st_y + 60),txt='View Archived')
        self.objects['canvas'] = self.parent.create_rectangle(0,100,110,190,fill='#1c1c1f')

    def proj_create_menu(self):
        self.create_menu = Create_Menu(self.parent,self.objects,self.tools)

    def live_proj_menu(self):
        self.live_menu = Live_Menu(self.parent,self.objects,self.tools)

class Live_Menu():
    
    def __init__(self,parent,objects,tools):
        self.parent = parent
        self.objects = objects
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        self.live_menu()

    def live_menu(self):
        st_x,st_y = (260,25)
        self.objects['live_menu'] = {}
        self.objects['live_menu']['selector'] = Cbx(
            self.parent,(st_x,st_y),label=True,label_loc='above',size=(150,20),txt='Select Project')
        self.objects['live_menu']['accept_proj'] = Btn(
            self.parent,(st_x+150,st_y),txt='Accept',alt_clr=True)
        self.objects['live_menu']['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')


class Create_Menu():
    
    def __init__(self,parent,objects,tools):
        self.parent = parent
        self.objects = objects
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        self.create_menu()

    def create_menu(self):
        st_x,st_y = (5,215)
        self.objects['create_menu'] = {}
        self.objects['create_menu']['ad_hoc'] = Btn(
            self.parent,(st_x,st_y),txt='Ad Hoc',cmd=lambda:self.create_inputs('Ad Hoc'),
            toggle=True,deact_cmd=lambda:self.kill(self.objects['create_menu']['input_form'])
            )
        self.objects['create_menu']['full'] = Btn(
            self.parent,(st_x,st_y + 20),txt='Full Project',cmd=lambda:self.create_inputs(),
            toggle=True,deact_cmd=lambda:self.kill(self.objects['create_menu']['input_form'])
            )
        self.objects['create_menu']['canvas'] = self.parent.create_rectangle(0,210,110,260,fill='#1c1c1f')

    def create_inputs(self,category='Full Project'):
        st_x,st_y = (300,10)
        if self.objects['create_menu']['full'].active and self.objects['create_menu']['ad_hoc'].active:
            if category == 'Full Project': self.objects['create_menu']['ad_hoc'].toggle()
            else: self.objects['create_menu']['full'].toggle()
        self.objects['create_menu']['input_form'] = {}
        self.objects['create_menu']['input_form']['header'] = Lbl(
            self.parent,category,(st_x+(.5*len(category)),st_y))
        self.objects['create_menu']['input_form']['title'] = Ent(
            self.parent,(st_x,st_y+30),(150,20),label=True,txt='Title')
        self.objects['create_menu']['input_form']['desc'] = Txt(
            self.parent,(st_x,st_y+50),(150,100),label=True,txt='Description')
        self.objects['create_menu']['input_form']['lead'] = Cbx(
            self.parent,(st_x,st_y+150),(150,20),label=True,txt='Lead')
        self.objects['create_menu']['input_form']['cancel'] = Btn(
            self.parent,(st_x-100,st_y+200),txt='Cancel',alt_clr=True,
            cmd=lambda:[
                self.kill(self.objects['create_menu']['input_form']),
                self.objects['create_menu']['ad_hoc'].deactivate(),
                self.objects['create_menu']['full'].deactivate()
                ])
        self.objects['create_menu']['input_form']['accept'] = Btn(
            self.parent,(st_x+50,st_y+200),txt='Accept',alt_clr=True,
            cmd=lambda:print(self.get_create_inputs()))
        self.objects['create_menu']['input_form']['canvas'] = self.parent.create_rectangle(
            150,5,520,250,fill='#1c1c1f')

    def get_create_inputs(self):
        return {
            'type': self.objects['create_menu']['input_form']['header'].label['text'],
            'title': self.objects['create_menu']['input_form']['title'].get(),
            'desc': self.objects['create_menu']['input_form']['desc'].get(),
            'lead': self.objects['create_menu']['input_form']['lead'].get()
            }



Main_Menu()