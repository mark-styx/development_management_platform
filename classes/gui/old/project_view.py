from tkinter import *

import sys
from os.path import basename,dirname,abspath
from inspect import getsourcefile
from pathlib import Path
from glob import glob

sys.path.append(dirname(dirname(abspath(getsourcefile(lambda:0)))))
from project.new_project import New_Project
from project.project import Project
from project.outline import Outline
from lbl import Lbl
from btn import Btn
from cbx import Cbx

from time import sleep

class Project_Home():

    def __init__(self,project):

        self.active_project = Project(project)
        current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
        self.main_color = '#2d3440'
        self.app_window = Tk()
        self.app_window.title('Project Home')
        self.app_window.config(bg=self.main_color)
        self.app_window.geometry('800x600')
        self.setup_interface()

    def main_menu(self):
        self.canvas = Canvas(self.app_window)
        self.canvas.config(bg=self.main_color)
        self.canvas.create_text(400,550,fill="white",font='40',text='Title Goes Here')
        b1 = rekt(self.canvas,(175,500),25,100)
        self.canvas.tag_bind(b1.btn_id,'<Button-1>',lambda x:b1.toggle())
        self.canvas.pack(expand=True,fill='both')

    def toggle(self,btn):
        self.canvas.itemconfig(btn,fill='#5555a3')
        self.canvas

    def draw(self):
        self.canvas.create_line(15, 25, 200, 25)
        self.canvas.pack()

    def clear(self):
        for x in self.canvas.winfo_children(): x.unpack()

    def setup_interface(self):
        self.main_menu()
        self.app_window.mainloop()

class rekt():
    def __init__(self,parent,start,height,width,fill='#20202e',cmd=None):
        self.active = False
        self.parent,self.start,self.height,self.width,self.fill= parent,start,height,width,fill
        x,y = start
        self.btn_id = parent.create_rectangle(x,y,x+width,y+height,fill=fill)
    
    def toggle(self):
        if self.active:
            self.active = False
            self.parent.itemconfig(self.btn_id,fill='#5555a3')
            fl = flares((400,540),self.start)
            self.lines = {}
            for idx,x in enumerate(fl.lines):
                self.lines[idx] = self.parent.create_line(x)
        else:
            self.active = True
            self.parent.itemconfig(self.btn_id,fill=self.fill)
            for x in self.lines.values: self.parent.delete(x)

class flares():

    def __init__(self,start,end):
        self.current = (0,0)
        self.start,self.end = start,end
        self.lines = self.get_path()
        
    def get_path(self):
        x,y = self.start
        w,h = self.end
        y_dist = int(y-h)
        x_dist = int(x-w)
        y_mid = int(y_dist*.2)
        y_mid = y-int(y_dist*.2)
        ln_1 = (x,y,x,y_mid)
        ln_2 = (x,y_mid,w,y_mid)
        ln_3 = (w,y_mid,w,h)
        return ln_1,ln_2,ln_3



if __name__ == "__main__":
    Project_Home('testing003')