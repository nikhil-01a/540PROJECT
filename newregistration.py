from tkinter import * # For GUI
from PIL import Image,ImageTk #pip install pillow.. Import this library to use Gifs and Jpeg type images
from tkinter import ttk,messagebox
import sqlite3
import os

class suppliersClass: # Making a class to provide structure, so that the widgets are defined in one place inside the constructor and the functions are defined later in the code.
    def __init__(self,root):               # Default constructor and passing the object 'root'
        self.root = root                   # Initializing the TK() object with self. so that it recognizes that the object belongs to class, otherwise the functions wouldn't be able to use this object
        self.root.geometry("1100x500+220+130") # Geometry helps to give width and height to window. Then giving starting point for x and y axes as 0 for both
        self.root.title("Equipment Checkout System | Developed by Team Group 2 (SSW540 Fall 2022) ") # Window title
        self.root.config(bg = "white")
        self.root.focus_force()

        #=====================================
        # All variables==========

        self.var_sup_id=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        
        #======title========
        title=Label(self.root,text="Admin Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)


        #=====content=======
        #=====row1==========
        lbl_supid=Label(self.root,text="Admin ID",font=("goudy old style",15),bg="white").place(x=50,y=150)
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
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #=====buttons=========
        btn_add= Button(self.root,text="Register",command=self.add,font=("goudy old style",15),bg="#2196f3",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_clear = Button(self.root, text="Clear",command=self.clear,font=("goudy old style",15), bg="#607d8b",cursor="hand2").place(x=620,y=305,width=110,height=28)
        

#######################################################################################################################################################################################################################################

    def add(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error","Admin ID is required", parent=self.root)
            else:
                cur.execute("Select * from suppliers where sid=?",(self.var_sup_id.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Admin ID already exists, try a different one",parent=self.root)
                else:
                    cur.execute("Insert into suppliers (sid,name,email,pass,utype) values(?,?,?,?,?)",(
                        self.var_sup_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_pass.get(),
                        self.var_utype.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Admin Added Successfully", parent=self.root)
                    os.system("python login.py")
                    self.root.destroy()
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


if __name__=="__main__": # So if the name is 'main' then it should open dashboard. we are making dashboard our main function page
    root = Tk()                # Creating an object for Tkinter class, This root is like our frame in which we will work
    obj = suppliersClass(root)            # Creating an object for IMS class and passing root into it so that Tkinter class is attached with it 
    root.mainloop()            # Using mainloop so that the window stays until it is closed otherwise the window just exits after the program is run and this is what makes the window stay on the screen until closed
 