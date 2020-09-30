from tkinter import *

from root_app import Root
from project_home import Project_Home
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
        self.app_objects['main_menu']['settings'] = Btn(
            self.menu,(st_x,st_y + 20),txt='Settings',toggle=True,
            cmd=self.launch_settings_menu,
            deact_cmd=lambda:[self.destroy_all(self.app_objects['settings_menu'])]
        )
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
            self.destroy_all(self.app_objects['project_home'])
    
    def launch_settings_menu(self):
        self.settings_menu = Settings_Menu(
            self.menu,{'kill':self.kill,'destroy':self.destroy_all},
            self.conf.env_path,self.app_objects
            )


import json

from _conf import config

from mk_cbx import Cbx,Ent,Txt
#from mk_btn import Btn
from mk_lbl import Lbl

class Settings_Menu():

    def __init__(self,parent,tools,proj_home,app_objects):
        self.proj_home = proj_home
        self.parent = parent;self.tools = tools
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        app_objects['settings_menu'] = {}
        self.objects = app_objects.get('settings_menu')
        self.conf = config()
        self.setup()

    def setup(self):
        st_x,st_y = (5,105)
        self.objects['add'] = Btn(
            self.parent,(st_x,st_y),txt='Add Config',
            cmd=lambda:[ self.add_menu() ],
            deact_cmd=lambda:[ self.kill(self.objects['add_menu']) ],
            toggle=True)
        self.objects['rem'] = Btn(
            self.parent,(st_x,st_y + 20),txt='Remove Config',
            cmd=lambda:[ self.rem_menu() ],
            deact_cmd=lambda:[ self.kill(self.objects['rem_menu']) ],
            toggle=True
        )
        self.objects['upd'] = Btn(
            self.parent,(st_x,st_y + 40),txt='Update Config',
            cmd=lambda:[ self.upd_menu() ],
            deact_cmd=lambda:[ self.kill(self.objects['upd_menu']) ],
            toggle=True
        )
        self.objects['view'] = Btn(
            self.parent,(st_x,st_y + 60),txt='View Settings',
            cmd=lambda:[ self.view_menu() ],
            deact_cmd=lambda:[ self.kill(self.objects['view_menu']) ],
            toggle=True
        )
        self.objects['canvas'] = self.parent.create_rectangle(0,100,110,190,fill='#1c1c1f')

    def add_menu(self):
        self.objects['add_menu'] = {}
        data = self.objects.get('add_menu')
        st_x,st_y = (260,25)
        data['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')
        data['title'] = Ent(
            self.parent,(st_x,st_y),txt='Title',label=True
        )
        data['key'] = Ent(
            self.parent,(st_x,st_y),txt='Key',label=True
        )
        data['value'] = Ent(
            self.parent,(st_x,st_y),txt='Value',label=True
        )
        data['cancel'] = Btn(
            self.status,(73,st_y+55),(75,20),txt='Cancel',alt_clr=True,
            cmd=lambda:[ self.objects['add'].toggle() ]
        )
        data['confirm'] = Btn(
            self.status,(152,st_y+55),(75,20),txt='Confirm',alt_clr=True,
            cmd=lambda:[
                self.conf.add_configuration(
                    { data['title'].get() : { data['key'] : data['value'] } }
                ),
                self.objects['add'].toggle()
            ]
        )

    def rem_menu(self):
        conf = self.conf.open_conf()
        self.objects['rem_menu'] = {}
        data = self.objects.get('rem_menu')
        st_x,st_y = (260,25)
        data['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')
        data['selector'] = Cbx(
            self.parent,(st_x,st_y),label=True,label_loc='above',size=(150,20),
            txt='Select Configuration',values=[x for x in conf]
        )
        data['accept'] = Btn(
            self.parent,(st_x+150,st_y),txt='Accept',alt_clr=True,
            cmd=lambda:[
                data['value'].insert(conf[data['selector'].get()])
            ]
        )
        data['value'] = Txt(
            self.parent,(st_x,st_y+40),size=(250,185)
        )
        data['cancel'] = Btn(
            self.status,(73,st_y+55),(75,20),txt='Cancel',alt_clr=True,
            cmd=lambda:[ self.objects['add'].toggle() ]
        )
        data['confirm'] = Btn(
            self.status,(152,st_y+55),(75,20),txt='Confirm Removal',alt_clr=True,
            cmd=lambda:[
                self.conf.rem_configuration( data['selector'].get() ),
                self.objects['rem'].toggle()
            ]
        )

    def upd_menu(self):
        conf = self.conf.open_conf()
        self.objects['upd_menu'] = {}
        data = self.objects.get('upd_menu')
        st_x,st_y = (260,25)
        data['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')
        data['selector'] = Cbx(
            self.parent,(st_x,st_y),label=True,label_loc='above',size=(150,20),
            txt='Select Configuration',values=[x for x in conf]
        )
        data['accept'] = Btn(
            self.parent,(st_x+150,st_y),txt='Accept',alt_clr=True,
            cmd=lambda:[
                data['key'].insert( str(conf[data['selector'].get()].keys()) ),
                data['value'].insert( str(conf[data['selector'].get()].values()) )
            ]
        )
        data['key'] = Ent(
            self.parent,(st_x,st_y),txt='Key',label=True
        )
        data['value'] = Ent(
            self.parent,(st_x,st_y),txt='Value',label=True
        )
        data['cancel'] = Btn(
            self.status,(73,st_y+55),(75,20),txt='Cancel',alt_clr=True,
            cmd=lambda:[ self.objects['add'].toggle() ]
        )
        data['confirm'] = Btn(
            self.status,(152,st_y+55),(75,20),txt='Confirm',alt_clr=True,
            cmd=lambda:[
                self.conf.upd_configuration(
                    { data['selector'].get() : { data['key'] : data['value'] } }
                ),
                self.objects['add'].toggle()
            ]
        )

    def view_menu(self):
        conf = self.conf.open_conf()
        for pth in conf['paths']:
            conf['paths'][pth] = str(conf['paths'][pth])
        print(conf)
        self.objects['view_menu'] = {}
        data = self.objects.get('view_menu')
        st_x,st_y = (260,25)
        data['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')
        data['data'] = Txt(
            self.parent,(st_x,st_y),(250,250)
        )
        data['data'].insert(json.dumps(conf))


Main_Menu()