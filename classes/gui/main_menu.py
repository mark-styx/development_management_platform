from tkinter import *

from root_app import Root
from project_home import Project_Home
from settings import Settings_Menu
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
            self.menu,(st_x,st_y),txt='Project Home',toggle=True,
            cmd=self.launch_project_home,
            deact_cmd=lambda:self.destroy_all(self.app_objects['project_home'])
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

    def clear_switches(self,active):
        data = self.app_objects['main_menu']
        for obj in data:
            if obj != active and type(data[obj]) == Btn:
                try:
                    if data[obj].active:
                        data[obj].toggle()
                except Exception:
                    continue

    def launch_project_home(self):
        self.clear_switches('project_home')
        self.project_home = Project_Home(
            self.menu,{'kill':self.kill,'destroy':self.destroy_all},
            self.conf.env_path,self.app_objects
            )
        self.project_home.setup()

    def launch_settings_menu(self):
        self.clear_switches('settings')
        self.settings_menu = Settings_Menu(
            self.menu,{'kill':self.kill,'destroy':self.destroy_all},
            self.conf.env_path,self.app_objects
            )

if __name__ == "__main__":
    Main_Menu()