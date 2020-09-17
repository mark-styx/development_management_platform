from mk_cbx import Cbx,Ent,Txt
from mk_btn import Btn
from mk_lbl import Lbl

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