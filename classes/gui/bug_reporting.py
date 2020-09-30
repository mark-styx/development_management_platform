import webbrowser

from project.project import Project
from project.outline import Outline

from mk_cbx import Cbx,Ent,Txt
from mk_btn import Btn
from mk_lbl import Lbl

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
            toggle=True,deact_cmd=lambda:[
                self.kill(data['view_issues']),
                self.kill(data['issue_sub_menu'])
                ]
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
        data['analyst_assigned'].insert(self.active_project.issue.assignee.name)
        data['desc'].insert(self.active_project.last_issue_update())
        data['submit'] = Btn(
            self.parent,(337,st_y+180),(75,20),alt_clr=True,txt='Update',
            cmd=lambda:[
                self.active_project.update_issue(
                    data['desc'].get(),
                    data['analyst_assigned'].get()
                ),
                self.objects['bug_menu']['existing'].toggle()
            ]
        )
        data['cancel'] = Btn(
            self.parent,(258,st_y+180),(75,20),alt_clr=True,txt='Cancel',
            cmd=lambda:[self.objects['bug_menu']['existing'].toggle()]
        )
        self.issue_sub_menu()

    def issue_sub_menu(self):
        self.objects['bug_menu']['issue_sub_menu'] = {}
        data = self.objects['bug_menu'].get('issue_sub_menu')
        st_x,st_y = (5,285)
        data['issue_link'] = Btn(
            self.parent,(st_x,st_y),txt='Issue Link',
            cmd=lambda:[webbrowser.open(
                f'https://github.com/Dentsu-Aegis-Reporting-and-Automation/testing004/issues/{self.active_project.issue.number}'
            )]
            )
        data['close_issue'] = Btn(
            self.parent,(st_x,st_y + 20),txt='Close Issue',
            cmd=lambda:[self.active_project.close_issue()]
            )
        data['canvas'] = self.parent.create_rectangle(0,280,110,340,fill='#1c1c1f')

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