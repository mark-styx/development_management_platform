from tkinter import Label

class Lbl():

    def __init__(self,parent,txt,loc,size=(100,20)):

        self.label = Label(parent,text=txt,bg='#1c1c1f',fg='white')
        x,y = loc; w,h = size
        self.label.place(x=x,y=y,height=h,width=w)

    def get(self):
        return self.label['text']

    def destroy(self): self.label.destroy()