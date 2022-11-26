from tkinter import * # For GUI
from PIL import Image,ImageTk #pip install pillow.. Import this library to use Gifs and Jpeg type images
from tkinter import ttk,messagebox
import sqlite3
#from categories import categoriesClass


class productClass: # Making a class to provide structure, so that the widgets are defined in one place inside the constructor and the functions are defined later in the code.
    def __init__(self,root):               # Default constructor and passing the object 'root'
        self.root = root                   # Initializing the TK() object with self. so that it recognizes that the object belongs to class, otherwise the functions wouldn't be able to use this object
        self.root.geometry("1100x500+220+130") # Geometry helps to give width and height to window. Then giving starting point for x and y axes as 0 for both
        self.root.title("Equipment Checkout System | Developed by Team Group 2 (SSW540 Fall 2022) ") # Window title
        self.root.config(bg = "white")
        self.root.focus_force()

        #=====================================

        #===================Variables========================

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()

        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()

        self.var_name=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        #===================Frame===================
        product_Frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #======column1========
        title=Label(product_Frame,text=" Manage Equipment Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_name=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_quantity=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=260)

        #======column2=======
        cmb_category=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_category.place(x=150,y=60,width=200)
        cmb_category.current(0)

        cmb_supplier=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_supplier.place(x=150,y=110,width=200)
        cmb_supplier.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=160,width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=150,y=210,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=260,width=200)
        cmb_status.current(0)

        #=====buttons=========
        btn_add= Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update = Button(product_Frame, text="Update",command=self.update,font=("goudy old style",15), bg="#4caf50",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete = Button(product_Frame, text="Delete",command=self.delete,font=("goudy old style",15), bg="#f44336",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear = Button(product_Frame, text="Clear",command=self.clear,font=("goudy old style",15), bg="#607d8b",cursor="hand2").place(x=340,y=400,width=100,height=40)
     
        #======searchFrame========
        SearchFrame=LabelFrame(self.root,text="Search Equipment",font=("goudy old style",12,"bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

            #======options=======
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search= Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search= Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",cursor="hand2").place(x=410,y=9,width=150,height=30)

       #=======Supplier Treeview ====

        p_frame = Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)

        scrolly = Scrollbar(p_frame,orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame,columns=("pid","Category","Supplier","name","qty","Status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="Equipment ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("qty", text="Quantity")
        self.product_table.heading("Status", text="Status")
        self.product_table["show"]="headings" #To remove the extra column given by default and show only headings

        #fixing every column's width
        self.product_table.column("pid",width=90)
        self.product_table.column("Category",width=100)
        self.product_table.column("Supplier",width=100)
        self.product_table.column("name",width=100)
        self.product_table.column("qty",width=100)
        self.product_table.column("Status",width=100)

        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data) #This is a type of event in our bind function. whenever you click and release this button, it calls a certain function, in this case it is get_data()

        self.show()
        


#######################################################################################################################################################################################################################################

    def fetch_cat_sup(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        try:     
            cur.execute("Select name from category")
            cat=cur.fetchall()
            if len(cat)>0: 
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from suppliers")
            sup=cur.fetchall()
            if len(sup)>0: 
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)
     

    def add(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Equipment already exists",parent=self.root)
                else:
                    cur.execute("Insert into product (Category,Supplier,name,qty,Status) values(?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_qty.get(),
                        self.var_status.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Equipment Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)
            
    def show(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev): #we have passed an event in this function that is "ev". the bind function above which has an event will call this function "get_data" 
        f = self.product_table.focus() #whatever you click in the supplier table, that is the treeview goes into this variable 'f'.
        content = (self.product_table.item(f))
        row = content['values'] # using values in quotes we are filtering all the values that are present in the content tuple and putting them in row variable.
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_qty.set(row[4])
        self.var_status.set(row[5])

    def update(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select Equipment from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Equipment",parent=self.root)
                else:
                    cur.execute("update product set Category=?,Supplier=?,name=?,qty=?,Status=? where pid=?",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Equipment Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def delete(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select Equipment from the list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Equipment",parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete this Equipment?",parent=self.root)
                    if op== True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Equipment Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
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
                cur.execute("Select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    
 

if __name__=="__main__": # So if the name is 'main' then it should open dashboard. we are making dashboard our main function page
    root = Tk()                # Creating an object for Tkinter class, This root is like our frame in which we will work
    obj = productClass(root)            # Creating an object for IMS class and passing root into it so that Tkinter class is attached with it 
    root.mainloop()            # Using mainloop so that the window stays until it is closed otherwise the window just exits after the program is run and this is what makes the window stay on the screen until closed
 