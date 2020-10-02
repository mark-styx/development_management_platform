from tkinter.ttk import Combobox

class Cbx():

    def __init__(self,parent_obj,grid_loc,values=None):
        self.combo = Combobox(parent_obj)
        r,c = grid_loc
        self.combo.grid(row=r,column=c)
        self.combo['values'] = values
    
    def get(self): return self.combo.get()