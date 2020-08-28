from tkinter import Label

class Lbl():

    def __init__(self,parent_obj,txt,grid_loc):

        self.lable = Label(parent_obj,text=txt,bg='#161e29',fg='white')
        r,c = grid_loc
        self.lable.grid(row=r,column=c)