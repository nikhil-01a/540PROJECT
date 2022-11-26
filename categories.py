from tkinter import * # For GUI
from PIL import Image,ImageTk #pip install pillow.. Import this library to use Gifs and Jpeg type images
from tkinter import ttk,messagebox
import sqlite3
#from categories import categoriesClass


class categoryClass: # Making a class to provide structure, so that the widgets are defined in one place inside the constructor and the functions are defined later in the code.
    def __init__(self,root):               # Default constructor and passing the object 'root'
        self.root = root                   # Initializing the TK() object with self. so that it recognizes that the object belongs to class, otherwise the functions wouldn't be able to use this object
        self.root.geometry("1100x500+220+130") # Geometry helps to give width and height to window. Then giving starting point for x and y axes as 0 for both
        self.root.title("Equipment Checkout System | Developed by Team Group 2 (SSW540 Fall 2022) ") # Window title
        self.root.config(bg = "white")
        self.root.focus_force()

        #=======Variables===============
        self.var_cat_id=StringVar()
        self.var_name = StringVar()

        #==============title=========================
        lbl_title = Label(self.root,text="Manage Categories",font=("goudy old style",30),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18),bg="lightyellow").place(x=50,y=170,width=300)
        btn_add=Button(self.root,text="Add",command=self.add,font=("goudy old style",15),bg="#4caf50",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="red",cursor="hand2").place(x=520,y=170,width=150,height=30)

        #================Category TreeView==========================

        cat_frame = Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=350)

        scrolly = Scrollbar(cat_frame,orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.category_table = ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid", text="Category ID")
        self.category_table.heading("name", text="Name")
        
        self.category_table["show"]="headings" #To remove the extra column given by default and show only headings

        #fixing every column's width
        self.category_table.column("cid",width=5)
        self.category_table.column("name",width=190)

        self.category_table.pack(fill=BOTH,expand=1)

        self.category_table.bind("<ButtonRelease-1>",self.get_data) #This is a type of event in our bind function. whenever you click and release this button, it calls a certain function, in this case it is get_data()

        self.show()

#====================Functions==============================

    def add(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category name is required", parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","The category name already exists, try a different one",parent=self.root)
                else:
                    cur.execute("Insert into category (name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


    def show(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.category_table.delete(*self.category_table.get_children())
            for row in rows:
                self.category_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev): #we have passed an event in this function that is "ev". the bind function above which has an event will call this function "get_data" 
        f = self.category_table.focus() #whatever you click in the supplier table, that is the treeview goes into this variable 'f'.
        content = (self.category_table.item(f))
        row = content['values'] # using values in quotes we are filtering all the values that are present in the content tuple and putting them in row variable.
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Please select category from the list", parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","This Category doesn't exist",parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete this category?",parent=self.root)
                    if op== True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        



if __name__=="__main__": # So if the name is 'main' then it should open dashboard. we are making dashboard our main function page
    root = Tk()                # Creating an object for Tkinter class, This root is like our frame in which we will work
    obj = categoryClass(root)            # Creating an object for IMS class and passing root into it so that Tkinter class is attached with it 
    root.mainloop()            # Using mainloop so that the window stays until it is closed otherwise the window just exits after the program is run and this is what makes the window stay on the screen until closed
 