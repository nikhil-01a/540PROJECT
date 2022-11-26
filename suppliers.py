from tkinter import * # For GUI
from PIL import Image,ImageTk #pip install pillow.. Import this library to use Gifs and Jpeg type images
from tkinter import ttk,messagebox
import sqlite3
#from categories import categoriesClass


class suppliersClass: # Making a class to provide structure, so that the widgets are defined in one place inside the constructor and the functions are defined later in the code.
    def __init__(self,root):               # Default constructor and passing the object 'root'
        self.root = root                   # Initializing the TK() object with self. so that it recognizes that the object belongs to class, otherwise the functions wouldn't be able to use this object
        self.root.geometry("1100x500+220+130") # Geometry helps to give width and height to window. Then giving starting point for x and y axes as 0 for both
        self.root.title("Equipment Checkout System | Developed by Team Group 2 (SSW540 Fall 2022) ") # Window title
        self.root.config(bg = "white")
        self.root.focus_force()

        #=====================================
        # All variables==========
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()


        self.var_sup_id=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()


        #======searchFrame========
        SearchFrame=LabelFrame(self.root,text="Search Supplier",font=("goudy old style",12,"bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

            #======options=======
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","SID","Name","Email"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search= Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search= Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #======title========
        title=Label(self.root,text="Supplier Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)


        #=====content=======
        #=====row1==========
        lbl_supid=Label(self.root,text="Supplier ID",font=("goudy old style",15),bg="white").place(x=50,y=150)
        txt_supid=Entry(self.root,textvariable=self.var_sup_id,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)

        #====row2==========
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)

        #====row3==========
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=50,y=230)
        lbl_pass=Label(self.root,text="Password",font=("goudy old style",15),bg="white").place(x=350,y=230)
        lbl_utype=Label(self.root,text="User Type",font=("goudy old style",15),bg="white").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",15),bg="lightyellow").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin","Supplier"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #=====buttons=========
        btn_add= Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update = Button(self.root, text="Update",command=self.update,font=("goudy old style",15), bg="#4caf50",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete = Button(self.root, text="Delete",command=self.delete,font=("goudy old style",15), bg="#f44336",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear = Button(self.root, text="Clear",command=self.clear,font=("goudy old style",15), bg="#607d8b",cursor="hand2").place(x=860,y=305,width=110,height=28)
        
        #=======Supplier Treeview ====

        sup_frame = Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly = Scrollbar(sup_frame,orient=VERTICAL)
        scrollx = Scrollbar(sup_frame, orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(sup_frame,columns=("sid","name","email","pass","utype"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("sid", text="Supplier ID")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("email", text="Email")
        self.SupplierTable.heading("pass", text="Password")
        self.SupplierTable.heading("utype", text="UType")
        self.SupplierTable["show"]="headings" #To remove the extra column given by default and show only headings

        #fixing every column's width
        self.SupplierTable.column("sid",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("email",width=100)
        self.SupplierTable.column("pass",width=100)
        self.SupplierTable.column("utype",width=100)

        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data) #This is a type of event in our bind function. whenever you click and release this button, it calls a certain function, in this case it is get_data()

        self.show()



#######################################################################################################################################################################################################################################

    def add(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error","Supplier ID is required", parent=self.root)
            else:
                cur.execute("Select * from suppliers where sid=?",(self.var_sup_id.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Supplier ID already exists, try a different one",parent=self.root)
                else:
                    cur.execute("Insert into suppliers (sid,name,email,pass,utype) values(?,?,?,?,?)",(
                        self.var_sup_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_pass.get(),
                        self.var_utype.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
            
    def show(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from suppliers")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev): #we have passed an event in this function that is "ev". the bind function above which has an event will call this function "get_data" 
        f = self.SupplierTable.focus() #whatever you click in the supplier table, that is the treeview goes into this variable 'f'.
        content = (self.SupplierTable.item(f))
        row = content['values'] # using values in quotes we are filtering all the values that are present in the content tuple and putting them in row variable.
        self.var_sup_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_pass.set(row[3])
        self.var_utype.set(row[4])

    def update(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error","Supplier ID is required", parent=self.root)
            else:
                cur.execute("Select * from suppliers where sid=?",(self.var_sup_id.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","This Supplier ID doesn't exist",parent=self.root)
                else:
                    cur.execute("update suppliers set name=?,email=?,pass=?,utype=? where sid=?",(
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.var_sup_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error","Supplier ID is required", parent=self.root)
            else:
                cur.execute("Select * from suppliers where sid=?",(self.var_sup_id.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","This Supplier ID doesn't exist",parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete this supplier?",parent=self.root)
                    if op== True:
                        cur.execute("delete from suppliers where sid=?",(self.var_sup_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_sup_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()


    def search(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By Option",parent = self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("Select * from suppliers where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    for row in rows:
                        self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    



if __name__=="__main__": # So if the name is 'main' then it should open dashboard. we are making dashboard our main function page
    root = Tk()                # Creating an object for Tkinter class, This root is like our frame in which we will work
    obj = suppliersClass(root)            # Creating an object for IMS class and passing root into it so that Tkinter class is attached with it 
    root.mainloop()            # Using mainloop so that the window stays until it is closed otherwise the window just exits after the program is run and this is what makes the window stay on the screen until closed
 