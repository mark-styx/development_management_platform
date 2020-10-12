from tkinter import Toplevel,IntVar,Radiobutton,Canvas
from mk_cbx import Cbx,Ent,Txt
from mk_btn import Btn
from mk_lbl import Lbl

class Unit_Window():

    def __init__(self,parent,objects,tools,proj_home,active_project,app_data):
        self.app_data = app_data
        self.parent = parent
        self.objects = objects
        self.project = active_project
        self.fields,self.records = active_project.ui_outline()
        self.proj_home = proj_home
        self.unit_wdw = Toplevel(parent)
        self.unit_wdw.title('Unit Compiler')
        self.unit_viewer = Canvas(self.unit_wdw)
        self.unit_viewer.pack(expand=True,fill='both')
        self.unit_viewer.config(bg='#292e30')
        self.unit = 'inactive'
        self.viewer()

    def viewer(self):
        self.objects['unit_viewer'] = {}
        self.objects['unit_viewer']['units'] = {}
        data = self.objects['unit_viewer'].get('units')
        self.unit_var = IntVar()
        for idx,unit in enumerate([x[1] for x in self.records]):
            data[f'radio_{idx}'] = Radiobutton(
                self.unit_viewer, 
                text=unit,bg='#292e30',fg='white',selectcolor='#856c14',
                indicatoron=0,height=1,
                variable=self.unit_var,
                command=lambda:print(self.unit_var.get()),
                value=idx
            )
        for idx,rad in enumerate(data):
            data[rad].place(x=30,y=26.5*idx)
        ly = 30+(26*len(data))
        data['cancel'] = Btn(
            self.unit_viewer,(30,ly),(50,20),'Cancel',cmd=self.unit_wdw.destroy,alt_clr=True
        )
        data['confirm'] = Btn(
            self.unit_viewer,(82,ly),(50,20),'Confirm',cmd=self.set_unit,alt_clr=True
        )
        self.unit_wdw.geometry(f'300x{ly+30}')
        self.objects['unit_viewer']['canvas'] = self.unit_viewer.create_rectangle(
            25,0,275,ly+20,fill='#1c1c1f'
        )

    def set_unit(self):
        self.unit = self.records[self.unit_var.get()][1]
        print(self.unit)
        self.app_data.last_compile(self.unit)
        self.project.compile_unit(self.proj_home,self.unit)
        self.unit_wdw.destroy()