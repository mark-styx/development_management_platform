from tkinter import Toplevel,IntVar,Radiobutton,Canvas
from mk_cbx import Cbx,Ent,Txt
from mk_btn import Btn
from mk_lbl import Lbl

class Edit_Window():
    def __init__(self,parent,objects,tools,proj_home,active_project,window):
        self.kill,self.destroy_all = tools['kill'],tools['destroy']
        self.parent = parent
        self.objects = objects
        self.project = active_project
        self.proj_home = proj_home
        self.edit_wdw = Toplevel(parent)
        self.edit = Canvas(self.edit_wdw)
        self.edit.pack(expand=True,fill='both')
        self.edit.config(bg='#292e30')
        opts = {
            'meta':self.meta_editor,
            'outline':self.outline_menu
            }
        opts[window]()
    
    def meta_editor(self):
        st_x,st_y = (30,15)
        self.edit_wdw.geometry('375x250')
        self.edit_wdw.title('Edit Meta')
        self.objects['edit_meta'] = {}
        data = self.objects.get('edit_meta')
        data['canvas'] = self.edit.create_rectangle(25,10,350,245,fill='#1c1c1f')
        data['header'] = Lbl(self.edit,'Edit Meta',(175,st_y+5))
        data['title'] = Ent(self.edit,(st_x+150,st_y+35),(150,20),label=True,txt='Title')
        data['desc'] = Txt(self.edit,(st_x+150,st_y+55),(150,100),label=True,txt='Description')
        data['lead'] = Cbx(
            self.edit,(st_x+150,st_y+175),(150,20),label=True,txt='Lead',
            values=['Mathew Augusthy','Jeff Brown','Mark Styx']
        )
        data['title'].insert(str(self.project.title))
        data['desc'].insert(str(self.project.desc))
        data['lead'].insert(str(self.project.lead))
        data['confirm'] = Btn(
            self.edit,(st_x+125,st_y+200),(50,20),txt='Accept',alt_clr=True,
            cmd=lambda:[
                self.project.change_title(data['title'].get().strip()),
                self.project.change_desc(data['desc'].get().strip()),
                self.project.change_lead(data['lead'].get().strip()),
                self.edit_wdw.destroy()
            ]
        )
        data['cancel'] = Btn(
            self.edit,(st_x+75,st_y+200),(50,20),'Cancel',
            cmd=self.edit_wdw.destroy,alt_clr=True
        )

    def outline_menu(self):
        st_x,st_y = (5,5)
        self.edit_wdw.geometry('400x250')
        self.edit_wdw.title('Update Outline')
        self.objects['update_outline'] = {}
        data = self.objects.get('update_outline')
        data['canvas0'] = self.edit.create_rectangle(0,0,80,110,fill='#1c1c1f')
        data['canvas1'] = self.edit.create_rectangle(0,340,80,400,fill='#1c1c1f')
        data['canvas2'] = self.edit.create_rectangle(90,5,375,245,fill='#1c1c1f')
        data['add_entry'] = Btn(
            self.edit,(st_x,st_y),(70,20),txt='Add Entry',alt_clr=False,
            cmd=lambda:[
                self.csa(data,'add_entry'),
                self.add_entry_menu()
                ],
            toggle=True,deact_cmd=lambda:[self.kill(data['add_form'])]
        )
        data['rem_entry'] = Btn(
            self.edit,(st_x,st_y+20),(70,20),txt='Rem Entry',alt_clr=False,
            cmd=lambda:[
                self.csa(data,'rem_entry'),
                self.rem_entry_menu()
            ],
            toggle=True,deact_cmd=lambda:[self.kill(data['rem_form'])]
        )
        data['edit_outline'] = Btn(
            self.edit,(st_x,st_y+40),(70,20),txt='Edit Outline',alt_clr=False,
            cmd=lambda:[
                self.csa(data,'edit_outline'),
                self.outline_editor()
            ],
            toggle=True,deact_cmd=lambda:[self.kill(data['edit_form'])]
        )
        data['timing'] = Btn(
            self.edit,(st_x,st_y+60),(70,20),txt='Edit Timing',alt_clr=False,
            cmd=lambda:[
                self.csa(data,'timing'),
                self.timing_menu()
            ],
            toggle=True,deact_cmd=lambda:[self.kill(data['edit_timing_menu'])]
        )
        data['status'] = Btn(
            self.edit,(st_x,st_y+80),(70,20),txt='Edit Status',alt_clr=False,
            cmd=lambda:[
                self.csa(data,'status'),
                self.status_menu()
            ],
            toggle=True,deact_cmd=lambda:[self.kill(data['edit_status_menu'])]
        )
        data['cancel'] = Btn(
            self.edit,(st_x,st_y+195),(70,20),txt='Cancel',alt_clr=False,
            cmd=lambda:[self.edit_wdw.destroy()]
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

    def add_entry_menu(self):
        st_x,st_y = 210,10
        self.objects['update_outline']['add_form'] = {}
        data = self.objects['update_outline'].get('add_form')
        data['header'] = Lbl(self.edit,'Add Entry',(142.5,st_y+5))
        data['task_name'] = Ent(self.edit,(st_x+5,st_y+25),(125,20),label=True,txt='Title')
        data['desc'] = Txt(self.edit,(st_x+5,st_y+45),(125,100),label=True,txt='Description')
        data['lead'] = Cbx(
            self.edit,(st_x+5,st_y+145),(125,20),label=True,txt='Lead',
            values=['Mathew Augusthy','Jeff Brown','Mark Styx']
        )
        data['lead'].insert(str(self.project.lead))
        data['confirm'] = Btn(
            self.edit,(5,220),(70,20),txt='Confirm',alt_clr=False,
            cmd=lambda:[
                self.project.add_to_outline(
                    data['task_name'].get().strip(),
                    data['desc'].get().strip(),
                    data['lead'].get().strip()
                    ),
                self.objects['update_outline']['add_entry'].toggle()
            ]
        )

    def rem_entry_menu(self):
        fld,res = self.project.ui_outline()
        st_x,st_y = 210,10
        self.objects['update_outline']['rem_form'] = {}
        data = self.objects['update_outline'].get('rem_form')
        data['header'] = Lbl(self.edit,'Remove Entry',(142.5,st_y+5))
        data['task'] = Cbx(
            self.edit,(st_x-50,st_y+25),(200,20),label=True,txt='Task',lbl_size=(20,40),
            values=[f'{x[0]} | {x[1]}' for x in res]
        )
        data['confirm'] = Btn(
            self.edit,(5,220),(70,20),txt='Confirm',alt_clr=False,
            cmd=lambda:[
                print( data['task'].get().split('|')[0].strip() ),
                self.project.rem_outline( data['task'].get().split('|')[0].strip() ),
                self.objects['update_outline']['rem_entry'].toggle()
            ]
        )

    def timing_menu(self):
        fld,res = self.project.est_timing()
        st_x,st_y = 210,10
        self.objects['update_outline']['edit_timing_menu'] = {}
        data = self.objects['update_outline'].get('edit_timing_menu')
        data['header'] = Lbl(self.edit,'Project Timing',(142.5,st_y+5))
        data['task'] = Cbx(
            self.edit,(st_x-50,st_y+25),(200,20),label=True,txt='Task',lbl_size=(20,40),
            values=[f'{x[0]} | {x[1]}' for x in res]
        )
        data['est_completion'] = Ent(self.edit,(st_x+5,st_y+70),(125,20),label=True,txt='Est Completion')
        data['est_risks'] = Ent(self.edit,(st_x+5,st_y+90),(125,20),label=True,txt='Est Risks')
        data['est_risk_penalty'] = Ent(self.edit,(st_x+5,st_y+110),(125,20),label=True,txt='Est Penalty')
        idx = lambda X: [x[0] for x in res].index(int(X))
        data['accept'] = Btn(
            self.edit,(st_x+100,st_y+45),(50,20),txt='Select',alt_clr=True,
            cmd=lambda:[
                data['est_completion'].insert( str(res[idx(str(data['task'].get().split('|')[0].strip()))][2]) ),
                data['est_risks'].insert( str(res[idx(str(data['task'].get().split('|')[0].strip()))][3]) ),
                data['est_risk_penalty'].insert( str(res[idx(str(data['task'].get().split('|')[0].strip()))][4]) )
            ]
        )
        data['confirm'] = Btn(
            self.edit,(5,220),(70,20),txt='Confirm',alt_clr=False,
            cmd=lambda:[
                self.project.update_outline(
                    'est_completion',
                    str(data['task'].get().split('|')[1].strip()),
                    data['est_completion'].get()
                ),
                self.project.update_outline(
                    'est_risks',
                    str(data['task'].get().split('|')[1].strip()),
                    str(data['est_risks'].get())
                ),
                self.project.update_outline(
                    'est_risk_penalty',
                    str(data['task'].get().split('|')[1].strip()),
                    data['est_risk_penalty'].get()
                ),
                self.objects['update_outline']['timing'].toggle()
            ]
        )

    def status_menu(self):
            fld,res = self.project.ui_outline()
            st_x,st_y = 210,10
            self.objects['update_outline']['edit_status_menu'] = {}
            data = self.objects['update_outline'].get('edit_status_menu')
            data['header'] = Lbl(self.edit,'Project Status',(142.5,st_y+5))
            data['task'] = Cbx(
                self.edit,(st_x-50,st_y+25),(200,20),label=True,txt='Task',lbl_size=(20,40),
                values=[f'{x[0]} | {x[1]}' for x in res]
            )
            data['status'] = Cbx(
                self.edit,(st_x+5,st_y+70),(150,20),label=True,txt='Status',lbl_size=(20,40),
                values=[f'{x[1]}' for x in self.project.get_status_opts()]
            )
            idx = lambda X: [x[0] for x in res].index(int(X))
            data['accept'] = Btn(
                self.edit,(st_x+100,st_y+45),(50,20),txt='Select',alt_clr=True,
                cmd=lambda:[
                    data['status'].insert( str(res[idx(str(data['task'].get().split('|')[0].strip()))][2]) )
                ]
            )
            data['confirm'] = Btn(
                self.edit,(5,220),(70,20),txt='Confirm',alt_clr=False,
                cmd=lambda:[
                    self.project.update_outline(
                        'task_status',
                        str(data['task'].get().split('|')[1].strip()),
                        data['status'].get()
                    ),
                    self.objects['update_outline']['status'].toggle()
                ]
            )

    def outline_editor(self):
        fld,res = self.project.ui_outline_edit()
        st_x,st_y = 210,10
        self.objects['update_outline']['edit_form'] = {}
        data = self.objects['update_outline'].get('edit_form')
        data['header'] = Lbl(self.edit,'Edit Entry',(142.5,st_y+5))
        data['task'] = Cbx(
            self.edit,(st_x-50,st_y+25),(200,20),label=True,txt='Task',lbl_size=(20,40),
            values=[f'{x[0]} | {x[1]}' for x in res]
        )
        data['task_name'] = Ent(self.edit,(st_x+5,st_y+70),(125,20),label=True,txt='Title')
        data['desc'] = Txt(self.edit,(st_x+5,st_y+90),(125,100),label=True,txt='Description')
        data['lead'] = Cbx(
            self.edit,(st_x+5,st_y+190),(125,20),label=True,txt='Lead',
            values=['Mathew Augusthy','Jeff Brown','Mark Styx']
        )
        idx = lambda X: [x[0] for x in res].index(int(X))
        data['accept'] = Btn(
            self.edit,(st_x+100,st_y+45),(50,20),txt='Select',alt_clr=True,
            cmd=lambda:[
                data['task_name'].insert( str(data['task'].get().split('|')[1].strip()) ),
                data['desc'].insert( str(res[idx(str(data['task'].get().split('|')[0].strip()))][2]) ),
                data['lead'].insert( res[idx(str(data['task'].get().split('|')[0].strip()))][3] )
            ]
        )
        data['confirm'] = Btn(
            self.edit,(5,220),(70,20),txt='Confirm',alt_clr=False,
            cmd=lambda:[
                self.project.update_outline(
                    'task_name',
                    str(data['task'].get().split('|')[1].strip()),
                    data['task_name'].get()
                ),
                self.project.update_outline(
                    'task_desc',
                    str(data['task'].get().split('|')[1].strip()),
                    str(data['desc'].get())
                ),
                self.project.update_outline(
                    'owner',
                    str(data['task'].get().split('|')[1].strip()),
                    data['lead'].get()
                ),
                self.objects['update_outline']['edit_outline'].toggle()
            ]
        )

class Project_Status():
    def __init__(self,parent,objects,active_project):
        self.parent = parent
        self.objects = objects
        self.project = active_project
        self.fields,self.records = active_project.ui_outline()
        self.status_wdw = Toplevel(parent)
        self.status_wdw.title('Set Project Status')
        self.status_wdw.geometry('300x200')
        self.status = Canvas(self.status_wdw)
        self.status.pack(expand=True,fill='both')
        self.status.config(bg='#292e30')
        self.editor()

    def editor(self):
        st_x,st_y = (25,10)
        self.objects['update_status'] = {}
        data = self.objects.get('update_status')
        data['canvas1'] = self.status.create_rectangle(25,10,275,190,fill='#1c1c1f')
        data['header'] = Lbl(self.status,self.project.title,(100,st_y+5))
        data['curr_stat'] = Cbx(
                self.status,(95,st_y+30),(150,20),label=True,txt='Status',lbl_size=(20,40),
                values=[f'{x[1]}' for x in self.project.get_status_opts()]
            )
        data['curr_stat'].insert(self.project.status)
        data['cancel'] = Btn(
                self.status,(73,st_y+55),(75,20),txt='Cancel',alt_clr=True,
                cmd=lambda:[
                    self.objects.pop('update_status', None),
                    self.status_wdw.destroy()
                ]
            )
        data['confirm'] = Btn(
                self.status,(152,st_y+55),(75,20),txt='Confirm',alt_clr=True,
                cmd=lambda:[
                    self.project.change_status(str(data['curr_stat'].get())),
                    self.objects.pop('update_status', None),
                    self.status_wdw.destroy()
                ]
            )