from tkinter import Button

class Btn():

    def __init__(self,parent_obj,grid_loc,cmd=None,icon=None,txt=None):
        self.button = Button(parent_obj,text=txt,command=cmd,bg='#36332e',fg='#658bbf')
        r,c = grid_loc
        self.button.grid(row=r,column=c)
        self.button.config(image=icon,width=32,height=32)