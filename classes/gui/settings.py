import json

from _conf import config

from mk_cbx import Cbx,Ent,Txt
from mk_btn import Btn
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
            self.parent,(st_x,st_y+20),txt='Key',label=True
        )
        data['value'] = Ent(
            self.parent,(st_x,st_y+40),txt='Value',label=True
        )
        data['cancel'] = Btn(
            self.parent,(st_x-50,st_y+60),(75,20),txt='Cancel',alt_clr=True,
            cmd=lambda:[ self.objects['add'].toggle() ]
        )
        data['confirm'] = Btn(
            self.parent,(st_x+50,st_y+60),(75,20),txt='Confirm',alt_clr=True,
            cmd=lambda:[
                self.conf.add_configuration(
                    { data['title'].get() : { data['key'].get() : data['value'].get() } }
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
            self.parent,(st_x-100,st_y+55),(75,20),txt='Cancel',alt_clr=True,
            cmd=lambda:[ self.objects['rem'].toggle() ]
        )
        data['confirm'] = Btn(
            self.parent,(st_x-100,st_y+75),(75,20),txt='Confirm',alt_clr=True,
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
                data['key'].add_values(( list(conf[data['selector'].get()].keys()) ))
            ]
        )
        data['key'] = Cbx(
            self.parent,(st_x,st_y+20),(150,20),label=True,txt='Key',lbl_size=(50,20)
        )
        data['accept2'] = Btn(
            self.parent,(st_x+150,st_y+20),txt='Accept',alt_clr=True,
            cmd=lambda:[
                data['value'].insert( conf[data['selector'].get()][data['key'].get()] )
            ]
        )
        data['value'] = Txt(
            self.parent,(st_x,st_y+40),(150,40),txt='Value',label=True,lbl_size=(50,20)
        )
        data['cancel'] = Btn(
            self.parent,(st_x,st_y+85),(75,20),txt='Cancel',alt_clr=True,
            cmd=lambda:[ self.objects['upd'].toggle() ]
        )
        data['confirm'] = Btn(
            self.parent,(st_x+80,st_y+85),(75,20),txt='Confirm',alt_clr=True,
            cmd=lambda:[
                self.conf.update_conf(
                    { data['selector'].get() : { data['key'].get() : data['value'].get() } }
                ),
                self.objects['upd'].toggle()
            ]
        )

    def view_menu(self):
        conf = self.conf.open_conf()
        for pth in conf['paths']:
            conf['paths'][pth] = str(conf['paths'][pth])
        print(conf)
        self.objects['view_menu'] = {}
        data = self.objects.get('view_menu')
        st_x,st_y = (210,15)
        data['canvas'] = self.parent.create_rectangle(150,5,520,250,fill='#1c1c1f')
        data['data'] = Txt(
            self.parent,(st_x,st_y),(250,220)
        )
        data['data'].insert(json.dumps(conf))

