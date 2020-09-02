from tkinter import Button,Label

class Btn():

    def __init__(
            self,parent,loc,size=(100,20),txt=None,img=None,
            cmd=lambda:print('undefined'),
            deact_cmd=lambda:print('undefined'),
            label=False,label_loc='left',label_txt=None,toggle=False,
            border=True,alt_clr=False
        ):
        if not alt_clr:
            bg = '#1c1c1f';fg='white'
        else:
            bg = '#292e30';fg='white'
        self.cmd,self.deact_cmd = cmd,deact_cmd
        if toggle: cmd = self.toggle
        self.button = Button(
            parent,image=img,bg=bg,fg=fg,command=cmd,text=txt,
            highlightthickness=0,borderwidth=0)
        self.button.place(x=loc[0],y=loc[1],width=size[0],height=size[1])
        if label:
            self.label = Label(parent,bg=bg,fg=fg,text=label_txt)
            location = {
                'left':lambda x:(x[0]-size[0],x[1]),
                'right':lambda x:(x[0]+size[0],x[1]),
                'below':lambda x:(x[0],x[1]+size[1]),
                'above':lambda x:(x[0],x[1]-size[1])
                }
            x,y = location[label_loc](loc)
            if img:
                w = 50 + (len(label_txt)*3)
            else: w = size[0]
            self.label.place(x=x,y=y,width=w,height=size[1])
        self.active = False
        if not border: self.button['border'] = '0'
    
    def toggle(self):
        if not self.active:
            self.active = True
            self.button.config(relief='sunken',bg='#856c14',fg='black')
            self.cmd()

        elif self.active:
            self.active = False
            self.button.config(relief='raised',bg='#1c1c1f',fg='white')
            self.deact_cmd()
    
    def deactivate(self):
        self.active = False
        self.button.config(relief='raised',bg='#1c1c1f',fg='white')

    def destroy(self):
        self.button.destroy()
'''
class fBtn(tk.Canvas):
    def __init__(self,
            parent, width=100, height=20, cornerradius=2, padding=2,
            color='#1c1c1f',bg='#292e30', command=lambda: print('unbound')
        ):

        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="raised", highlightthickness=0, bg=bg)
        self.parent = parent
        self.command = command
        self.color = color
        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None
        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None
        rad = 2*cornerradius
        self.ids = [
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding   +cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,   width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding    +cornerradius,height-padding), fill=color, outline=color),
            self.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color,     outline=color),
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90,  fill=color, outline=color),
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270,     extent=90, fill=color, outline=color),
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90,  fill=color, outline=color)
        ]
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.active=False

    def _on_press(self, event):
        self.configure(relief="sunken")
        for i in self.ids:
            self.itemconfig(i,fill='#856c14')
        self.command()

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            for i in self.ids:
                self.itemconfig(i,fill=self.color)
            self.command()'''