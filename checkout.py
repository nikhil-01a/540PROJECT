from tkinter import * # For GUI
from PIL import Image,ImageTk #pip install pillow.. Import this library to use Gifs and Jpeg type images
from tkinter import ttk,messagebox
import sqlite3
import os 


class checkoutClass: # Making a class to provide structure, so that the widgets are defined in one place inside the constructor and the functions are defined later in the code.
    def __init__(self,root):               # Default constructor and passing the object 'root'
        self.root = root                   # Initializing the TK() object with self. so that it recognizes that the object belongs to class, otherwise the functions wouldn't be able to use this object
        self.root.geometry("1100x500+220+130") # Geometry helps to give width and height to window. Then giving starting point for x and y axes as 0 for both
        self.root.title("Equipment Checkout System | Developed by Team Group 2 (SSW540 Fall 2022) ") # Window title
        self.root.config(bg = "white")
        self.root.focus_force()

        #=============title======================== 
        lbl_title = Label(self.root,text="View Checkouts",font=("goudy old style",30),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        #========variables============
        self.var_search=StringVar()
        

        #======searchFrame========
        SearchFrame=LabelFrame(self.root,text="Search Equipment",font=("goudy old style",12,"bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250,y=60,width=600,height=80)

        #======options=======
       
        
        lbl_search=Label(SearchFrame,text="Equipment Name",font=("times new roman",15,"bold"),bg="white").place(x=60,y=0,width=150,height=28)
        txt_search= Entry(SearchFrame,textvariable=self.var_search,font=("goudy old style",15),bg="lightyellow").place(x=230,y=0,width=150,height=28)
        btn_clear = Button(SearchFrame,text="Clear",command=self.clear,font=("times new roman",15),bg="lightgray",cursor="hand2").place(x=230,y=30,width=150,height=28)
        btn_search= Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",cursor="hand2").place(x=410,y=0,width=150,height=28)
        btn_show_all=Button(SearchFrame,text="Show All",command=self.show1,font=("goudy old style",15),bg="#083531",cursor="hand2").place(x=410,y=30,width=150,height=28)

       #=======Supplier Treeview ==== ,command=self.search

        ch_frame = Frame(self.root,bd=3,relief=RIDGE)
        ch_frame.place(x=250,y=150,width=600,height=330)

        scrolly = Scrollbar(ch_frame,orient=VERTICAL)
        scrollx = Scrollbar(ch_frame, orient=HORIZONTAL)

        self.checkout_table = ttk.Treeview(ch_frame,columns=("chid","pname","qty","stname","stcwid"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.checkout_table.xview)
        scrolly.config(command=self.checkout_table.yview)

        self.checkout_table.heading("chid", text="Checkout ID")
        self.checkout_table.heading("stname", text="St. Name")
        self.checkout_table.heading("stcwid", text="St. CWID")
        self.checkout_table.heading("pname", text="Equipment")
        self.checkout_table.heading("qty", text="Quantity")
        
        self.checkout_table["show"]="headings" #To remove the extra column given by default and show only headings

        #fixing every column's width
        self.checkout_table.column("chid",width=30)
        self.checkout_table.column("stname",width=80)
        self.checkout_table.column("stcwid",width=80)
        self.checkout_table.column("pname",width=80)
        self.checkout_table.column("qty",width=50)

        self.checkout_table.pack(fill=BOTH,expand=1)
        self.checkout_table.bind("<ButtonRelease-1>",self.get_data1) #This is a type of event in our bind function. whenever you click and release this button, it calls a certain function, in this case it is get_data()

        self.show1()

#================================Functions=================================
    def show1(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        #  self.product_Table = ttk.Treeview(ProductFrame3,columns=("pid","name","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        try:
            cur.execute("Select chid,pname,qty,stname,stcwid from checkouts")
            rows=cur.fetchall()
            self.checkout_table.delete(*self.checkout_table.get_children())
            for row in rows:
                self.checkout_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def search(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("Select chid,pname,qty,stname,stcwid from checkouts where pname LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.checkout_table.delete(*self.checkout_table.get_children())
                    for row in rows:
                        self.checkout_table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


    def clear(self):
        self.var_search.set('')
        self.show1()

    def get_data1(self,ev): #we have passed an event in this function that is "ev". the bind function above which has an event will call this function "get_data" 
        f = self.checkout_table.focus() #whatever you click in the supplier table, that is the treeview goes into this variable 'f'.
        content = (self.checkout_table.item(f))
        row = content['values'] # using values in quotes we are filtering all the values that are present in the content tuple and putting them in row variable.
        self.var_search.set(row[1])



if __name__=="__main__": # So if the name is 'main' then it should open dashboard. we are making dashboard our main function page
    root = Tk()                # Creating an object for Tkinter class, This root is like our frame in which we will work
    obj = checkoutClass(root)            # Creating an object for IMS class and passing root into it so that Tkinter class is attached with it 
    root.mainloop()            # Using mainloop so that the window stays until it is closed otherwise the window just exits after the program is run and this is what makes the window stay on the screen until closed
 