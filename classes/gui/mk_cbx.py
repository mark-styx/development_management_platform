from tkinter import Entry,Label,Text,WORD,END
from tkinter.ttk import Combobox,Style

class Cbx():

    def __init__(self,parent,loc,size=(100,20),label=False,txt=None,label_loc='left',values=None,lbl_size=None):
        self.combo = Combobox(parent)
        x,y = loc; w,h = size
        self.combo.place(x=x,y=y,height=h,width=w)
        self.combo['values'] = values
        if label:
            if not lbl_size:
                lh,lw = h,w
            else:
                lw,lh = lbl_size
            self.add_label(parent,txt,label_loc,(x,y),lh,lw)

    def add_label(self,parent,label_txt,label_loc,loc,h,w):
        self.label = Label(parent,bg='#1c1c1f',fg='white',text=label_txt)
        location = {
            'left':lambda x:(x[0]-w,x[1]),
            'right':lambda x:(x[0]+w,x[1]),
            'below':lambda x:(x[0],x[1]+h),
            'above':lambda x:(x[0],x[1]-h)
            }
        x,y = location[label_loc](loc)
        self.label.place(x=x,y=y,width=w,height=h)

    def add_values(self,values):
        self.combo['values'] = values

    def destroy(self):
        try:
            self.label.destroy()
            self.combo.destroy()
        except Exception:
            self.combo.destroy()

    def get(self):
        val = self.combo.get()
        if val: return val.strip()
        else: return ''

    def insert(self,choice):
        print(choice)
        if type(choice) is int:
            self.combo.current(self.combo['values'][choice])
        else: self.combo.current(self.combo['values'].index(choice))


class Ent():
    def __init__(
        self,parent,loc,size=(100,20),label=False,txt=None,label_loc='left'
        ):

        self.entry = Entry(parent,bg='#292e30',fg='white')
        x,y = loc; w,h = size
        self.entry.place(x=x,y=y,height=h,width=w)
        if label:
            self.add_label(parent,txt,label_loc,(x,y),h,w)

    def add_label(self,parent,label_txt,label_loc,loc,h,w):
        self.label = Label(parent,bg='#1c1c1f',fg='white',text=label_txt)
        location = {
            'left':lambda x:(x[0]-w,x[1]),
            'right':lambda x:(x[0]+w,x[1]),
            'below':lambda x:(x[0],x[1]+h),
            'above':lambda x:(x[0],x[1]-h)
            }
        x,y = location[label_loc](loc)
        self.label.place(x=x,y=y,width=w,height=h)

    def destroy(self):
        try:
            self.label.destroy()
            self.entry.destroy()
        except Exception:
            self.entry.destroy()

    def get(self):
        val = self.entry.get()
        if val: return val.strip()
        else: return ''

    def insert(self,txt):
        try:
            self.entry.delete(0, END)
        except Exception:
            ''
        self.entry.insert(END,txt)

class Txt():
    def __init__(
        self,parent,loc,size=(100,20),label=False,txt=None,label_loc='left',width=None,height=None,lbl_size=None
        ):

        self.text = Text(
            parent,bg='#292e30',fg='white',wrap=WORD,#width=width,height=height,
            font=('TkDefaultFont',8)
            )
        x,y = loc; w,h = size
        self.text.place(x=x,y=y,height=h,width=w)
        if label:
            if not lbl_size:
                lh,lw = h,w
            else:
                lw,lh = lbl_size
            self.add_label(parent,txt,label_loc,(x,y),lh,lw)

    def add_label(self,parent,label_txt,label_loc,loc,h,w):
        self.label = Label(parent,bg='#1c1c1f',fg='white',text=label_txt)
        location = {
            'left':lambda x:(x[0]-w,x[1]),
            'right':lambda x:(x[0]+w,x[1]),
            'below':lambda x:(x[0],x[1]+h),
            'above':lambda x:(x[0],x[1]-h)
            }
        x,y = location[label_loc](loc)
        self.label.place(x=x,y=y,width=w,height=h)

    def destroy(self):
        try:
            self.label.destroy()
            self.text.destroy()
        except Exception:
            self.text.destroy()

    def get(self):
        val = self.text.get('1.0',END)
        if val: return val.strip()
        else: return ''

    def insert(self,txt):
        try:
            self.text.delete('1.0', END)
        except Exception:
            ''
        self.text.insert(END,txt)