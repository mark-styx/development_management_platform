from tkinter import *
from tkinter.ttk import Style

import sys
from os.path import basename,dirname,abspath
from inspect import getsourcefile
from pathlib import Path
from glob import glob

sys.path.append(dirname(dirname(abspath(getsourcefile(lambda:0)))))

from _conf import config
from app_data import App_Data

class Root():

    def __init__(self):
        self.root = Tk()
        self.conf = config()
        self.app_objects = {
            'images':{},
            'icons':{},
            'app_data':App_Data()
        }
        self.get_images()
        self.app_color = '#292e30' #'#1a1a1f'#222233'
        self.style = Style()
        self.style.theme_create(
            'combostyle',
            parent='alt',
            settings = {
                'TCombobox':{
                    'configure':{
                        'selectbackground': self.app_color,
                        'fieldbackground': self.app_color,
                        'background': '#856c14',
                        'foreground':'white',
                        'focusfill':self.app_color
                                }
                            },
                'Treeview':{
                    'configure':{
                        'background':self.app_color,
                        'fieldbackground':self.app_color,
                        'foreground':'white'
                        }
                    }
                }
            )
        self.style.theme_use('combostyle') 
        self.build_interface()

    def get_images(self):
        current_dir = Path(dirname(abspath(getsourcefile(lambda:0))))
        Up = lambda X: Path(dirname(X))
        for x in (Up(Up(current_dir))/'bin/icons').glob('*.png'):
            self.app_objects['icons'][basename(x).replace('.png','')] = PhotoImage(file=str(x))
        for x in (Up(Up(current_dir))/'bin/images').glob('*.png'):
            self.app_objects['images'][basename(x).replace('.png','')] = PhotoImage(file=str(x))

    def build_interface(self):
        self.root.title('Development Manager')
        self.root.config(bg=self.app_color)
        self.root.geometry('600x337')