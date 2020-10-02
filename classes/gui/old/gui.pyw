from tkinter import *
from tkinter import messagebox

import sys
from os.path import basename,dirname,abspath
from inspect import getsourcefile
from pathlib import Path
from glob import glob

sys.path.append(dirname(dirname(abspath(getsourcefile(lambda:0)))))
from project.new_project import New_Project
from project.project import Project
from project.outline import Outline
from _conf import config
from lbl import Lbl
from btn import Btn
from cbx import Cbx
from project_view import Project_Home


class Gui():

    def __init__(self):

        current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
        self.main_color = '#161e29'
        self.current_settings = config()
        self.app_window = Tk()
        self.app_window.title('Development Manager')
        self.app_window.config(bg=self.main_color)
        self.app_window.geometry('300x120')
        self.icons = {}
        Up = lambda X: Path(dirname(X))
        for x in (Up(Up(current_dir))/'bin/icons').glob('*.png'):
            self.icons[basename(x).replace('.png','')] = PhotoImage(file=str(x))
        self.setup_interface()


    def main_menu(self):
        project = Btn(parent_obj=self.app_window,grid_loc=(0,0),cmd=self.project_menu,icon=self.icons['project_home'])
        Label(self.app_window,text='Projects Home',bg=self.main_color,fg='white').grid(row=0,column=1)
        settings = Btn(parent_obj=self.app_window,grid_loc=(1,0),cmd=self.settings_menu,icon=self.icons['settings'])
        Label(self.app_window,text='Settings',bg=self.main_color,fg='white').grid(row=1,column=1)
        leave = Btn(parent_obj=self.app_window,grid_loc=(2,0),cmd=self.app_window.quit,icon=self.icons['quit'])
        Label(self.app_window,text='Quit',bg=self.main_color,fg='white').grid(row=2,column=1)


    def add_project_window(self):
        self.project_window = Toplevel(self.app_window)
        self.project_window.title('Project Main')
        self.project_window.config(bg=self.main_color)
        self.project_window.geometry('300x200')


    def project_menu(self):
        self.add_project_window()
        create = Btn(parent_obj=self.project_window,grid_loc=(0,0),cmd=self.create_proj_popout,icon=self.icons['create'])
        Label(self.project_window,text='Create',bg=self.main_color,fg='white').grid(row=0,column=1)
        active = Btn(parent_obj=self.project_window,grid_loc=(1,0),cmd=lambda:self.sel_proj_popout('active'),icon=self.icons['active'])
        Label(self.project_window,text='Live Projects',bg=self.main_color,fg='white').grid(row=1,column=1)
        bugs = Btn(parent_obj=self.project_window,grid_loc=(2,0),cmd=None,icon=self.icons['bug'])
        Label(self.project_window,text='Bug Reporting',bg=self.main_color,fg='white').grid(row=2,column=1)
        arch = Btn(parent_obj=self.project_window,grid_loc=(3,0),cmd=lambda:self.sel_proj_popout('inactive'),icon=self.icons['archived'])
        Label(self.project_window,text='View Archived',bg=self.main_color,fg='white').grid(row=3,column=1)
        main_menu = Btn(parent_obj=self.project_window,grid_loc=(4,0),cmd=self.project_window.destroy,icon=self.icons['home'])
        Label(self.project_window,text='Main Menu',bg=self.main_color,fg='white').grid(row=4,column=1)

    
    def create_proj_popout(self):

        self.add_popout('Create',self.project_window)
        self.temp_window.geometry('300x120')
        main_menu = Btn(parent_obj=self.temp_window,grid_loc=(0,0),cmd=self.ad_hoc_popout,icon=self.icons['ad_hoc'])
        Label(self.temp_window,text='Ad Hoc Project',bg=self.main_color,fg='white').grid(row=0,column=1)
        main_menu = Btn(parent_obj=self.temp_window,grid_loc=(1,0),cmd=self.new_proj_popout,icon=self.icons['full_project'])
        Label(self.temp_window,text='Full Project',bg=self.main_color,fg='white').grid(row=1,column=1)
        main_menu = Btn(parent_obj=self.temp_window,grid_loc=(2,0),cmd=self.temp_window.destroy,icon=self.icons['home'])
        Label(self.temp_window,text='Return',bg=self.main_color,fg='white').grid(row=2,column=1)


    def ad_hoc_popout(self):

        self.temp_window.destroy()
        self.add_popout('New Ad Hoc',self.project_window)
        self.temp_window.geometry('300x130')

        title = Entry(self.temp_window)
        title.grid(row=0,column=1)
        Label(self.temp_window,text='Title',bg=self.main_color,fg='white').grid(row=0,column=0)

        desc = Entry(self.temp_window)
        desc.grid(row=1,column=1)
        Label(self.temp_window,text='Description',bg=self.main_color,fg='white').grid(row=1,column=0)

        owner = Entry(self.temp_window)
        owner.grid(row=2,column=1)
        Label(self.temp_window,text='Owner',bg=self.main_color,fg='white').grid(row=2,column=0)

        est_compl = Entry(self.temp_window)
        est_compl.grid(row=3,column=1)
        Label(self.temp_window,text='Est. Completion',bg=self.main_color,fg='white').grid(row=3,column=0)

        main_menu = Btn(parent_obj=self.temp_window,grid_loc=(4,0),cmd=lambda:[self.temp_window.destroy()],icon=self.icons['home'])
        save = Btn(parent_obj=self.temp_window,grid_loc=(4,1),cmd=self.temp_window.destroy,icon=self.icons['save'])

    
    def new_proj_popout(self):

        self.temp_window.destroy()
        self.add_popout('New Project',self.project_window)
        self.temp_window.geometry('300x130')

        title = Entry(self.temp_window)
        title.grid(row=0,column=1)
        Label(self.temp_window,text='Title',bg=self.main_color,fg='white').grid(row=0,column=0)

        desc = Entry(self.temp_window)
        desc.grid(row=1,column=1)
        Label(self.temp_window,text='Description',bg=self.main_color,fg='white').grid(row=1,column=0)

        lead = Entry(self.temp_window)
        lead.grid(row=2,column=1)
        Label(self.temp_window,text='Lead',bg=self.main_color,fg='white').grid(row=2,column=0)

        est_compl = Entry(self.temp_window)
        est_compl.grid(row=3,column=1)
        Label(self.temp_window,text='Est. Completion',bg=self.main_color,fg='white').grid(row=3,column=0)

        main_menu = Btn(parent_obj=self.temp_window,grid_loc=(4,0),cmd=lambda:[self.temp_window.destroy(),self.create_proj_popout()],icon=self.icons['home'])
        save = Btn(parent_obj=self.temp_window,grid_loc=(4,1),cmd=self.temp_window.destroy,icon=self.icons['save'])


    def sel_proj_popout(self,Filter):
        
        self.act_proj = Project(find=True)
        all_projs,_ = self.act_proj.view_all()
        projs = [x[1] for x in all_projs if x[4] in Filter]
        self.add_popout('Choose Project',self.project_window)
        self.temp_window.geometry('300x60')
        proj = Cbx(self.temp_window,(0,1),projs)
        Lbl(self.temp_window,'Project',(0,0))
        main_menu = Btn(parent_obj=self.temp_window,grid_loc=(1,0),cmd=lambda:[self.temp_window.destroy()],icon=self.icons['home'])        
        select = Btn(parent_obj=self.temp_window,grid_loc=(1,1),cmd=lambda:Project_Home(proj.get()),icon=self.icons['approve'])


    def settings_menu(self):

        self.add_settings_window()
        add_conf = Btn(parent_obj=self.settings_window,grid_loc=(0,0),cmd=self.add_configuration_popout,icon=self.icons['add'])
        Label(self.settings_window,text='Add Configuration',bg=self.main_color,fg='white').grid(row=0,column=1)
        rem_conf = Btn(parent_obj=self.settings_window,grid_loc=(1,0),cmd=self.rem_configuration_popout,icon=self.icons['delete'])
        Label(self.settings_window,text='Remove Configuration',bg=self.main_color,fg='white').grid(row=1,column=1)
        upd_conf = Btn(parent_obj=self.settings_window,grid_loc=(2,0),cmd=self.upd_configuration_popout,icon=self.icons['update'])
        Label(self.settings_window,text='Update Configuration',bg=self.main_color,fg='white').grid(row=2,column=1)
        view_conf = Btn(parent_obj=self.settings_window,grid_loc=(3,0),cmd=self.view_configurations,icon=self.icons['view'])
        Label(self.settings_window,text='View Settings',bg=self.main_color,fg='white').grid(row=3,column=1)
        main_menu = Btn(parent_obj=self.settings_window,grid_loc=(4,0),cmd=self.settings_window.destroy,icon=self.icons['home'])
        Label(self.settings_window,text='Main Menu',bg=self.main_color,fg='white').grid(row=4,column=1)


    def view_configurations(self):
        
        self.add_popout('View Configurations',self.settings_window)
        settings = self.current_settings.open_conf()
        max_row,cur_row = 0,0
        for catdx,cat in enumerate(settings):
            Label(self.temp_window,text=cat,bg=self.main_color,fg='white').grid(row=cur_row,column=0)
            for setdx,sname in enumerate(settings[cat]):
                cur_row += catdx + setdx
                Label(self.temp_window,text=sname,bg=self.main_color,fg='white').grid(row=cur_row,column=1)
                Label(self.temp_window,text=settings[cat][sname],bg=self.main_color,fg='white').grid(row=cur_row,column=2)
            cur_row += 1
            if cur_row > max_row: max_row = cur_row
            
        ret_to_main = Button(self.temp_window,text='Return',command=self.temp_window.destroy)
        ret_to_main.grid(row=max_row,column=0)


    def add_settings_window(self):
        self.settings_window = Toplevel(self.app_window)
        self.settings_window.title('Settings')
        self.settings_window.config(bg=self.main_color)
        self.settings_window.geometry('300x200')

    def add_popout(self,name,owner):
        self.temp_window = Toplevel(owner)
        self.temp_window.title(name)
        self.temp_window.config(bg=self.main_color)

    def add_configuration_popout(self):        
        self.add_popout('add configuration',self.settings_window)
        self.temp_window.geometry('300x100')
        cat_name_label = Label(self.temp_window,text='Category:',bg=self.main_color,fg='white')
        cat_name = Entry(self.temp_window)
        cat_name_label.grid(row=0,column=0)
        cat_name.grid(row=0,column=1)

        set_name_label = Label(self.temp_window,text='Setting Name:',bg=self.main_color,fg='white')
        set_name = Entry(self.temp_window)
        set_name_label.grid(row=1,column=0)
        set_name.grid(row=1,column=1)

        val_name_label = Label(self.temp_window,text='Value:',bg=self.main_color,fg='white')
        val_name = Entry(self.temp_window)
        val_name_label.grid(row=2,column=0)
        val_name.grid(row=2,column=1)

        get_vals = lambda: self.confirm_add_conf((cat_name.get(),set_name.get(),val_name.get()),'add')
        Button(self.temp_window,text='Cancel',command=self.temp_window.destroy).grid(row=3,column=0)
        Button(
            self.temp_window,text='Save',
            command=get_vals
            ).grid(row=3,column=1)
        

    def rem_configuration_popout(self):
        
        self.add_popout('remove configuration',self.settings_window)
        self.temp_window.geometry('300x50')
        cat_name_label = Label(self.temp_window,text='Category:',bg=self.main_color,fg='white')
        cat_name = Cbx(self.temp_window,(0,1))
        cat_name_label.grid(row=0,column=0)

        get_vals = lambda: self.confirm_del_conf(cat_name.get())
        Button(self.temp_window,text='Cancel',command=self.temp_window.destroy).grid(row=1,column=0)
        Button(
            self.temp_window,text='Save',
            command=get_vals
            ).grid(row=1,column=1)


    def upd_configuration_popout(self):
                
        self.add_popout('update configuration',self.settings_window)
        self.temp_window.geometry('300x100')
        cat_name_label = Label(self.temp_window,text='Category:',bg=self.main_color,fg='white')
        cat_name = Cbx(self.temp_window,(0,1))
        cat_name_label.grid(row=0,column=0)

        set_name_label = Label(self.temp_window,text='Setting Name:',bg=self.main_color,fg='white')
        set_name = Cbx(self.temp_window,(1,1))
        set_name_label.grid(row=1,column=0)

        val_name_label = Label(self.temp_window,text='Value:',bg=self.main_color,fg='white')
        val_name = Entry(self.temp_window)
        val_name_label.grid(row=2,column=0)
        val_name.grid(row=2,column=1)

        get_vals = lambda: self.confirm_add_conf((cat_name.get(),set_name.get(),val_name.get()),'chg')
        Button(self.temp_window,text='Cancel',command=self.temp_window.destroy).grid(row=4,column=0)
        Button(
            self.temp_window,text='Save',
            command=get_vals
            ).grid(row=4,column=1)


    def confirm_add_conf(self,values,command):

        cnm,snm,vnm = values
        payload = {cnm:{snm:vnm}}
        conf_add = messagebox.askquestion('Confirm Add',f'Add {payload}?')
        self.temp_window.destroy()
        self.settings_window.focus_force()


    def confirm_del_conf(self,value):

        cnm = value
        conf_add = messagebox.askquestion('Confirm Add',f'Rem {cnm}?')
        self.temp_window.destroy()
        self.settings_window.focus_force()


    def setup_interface(self):
        self.main_menu()
        self.app_window.mainloop()


if __name__ == "__main__":
    Gui()