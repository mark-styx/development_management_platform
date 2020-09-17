from tkinter import Frame,Scrollbar,N,S,E,W
from tkinter.ttk import Treeview

class Tree(Frame):
    '''Main Tree class, displaying data formatted as a table'''

    def __init__(self,parent,data):
        Frame.__init__(self,parent)
        self.data = data
        self.tree()
        self.add_rows()
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)
        
    def tree(self):
        '''Create the tree view based on the object fields attr'''

        tv = Treeview(self,selectmode='extended')
        tv['columns'] = self.data['fields']
        tv.heading("#0", text='#', anchor='w')
        tv.column("#0", anchor='center',width=35)
        for x in tv['columns']:
            tv.heading(x, text=x)
            if 'key' in x: wdth = 35
            elif 'desc' in x: wdth = 200
            else: wdth = 115
            tv.column(x,anchor='center',width=wdth)
        tv.pack(side='left',fill='x')
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        verscrlbar = Scrollbar(self,  
                                   orient ="vertical",  
                                   command = tv.yview) 
        verscrlbar.pack(side ='right', fill ='x') 
        tv.configure(xscrollcommand = verscrlbar.set) 

    def add_rows(self):
        '''Add rows to the tree view based of the input object records attr'''
        
        for idx,x in enumerate(self.data['records']):
            self.treeview.insert('','end',text=idx,values=x)