from tkinter import * # For GUI
from PIL import Image,ImageTk #pip install pillow.. Import this library to use Gifs and Jpeg type images
from tkinter import ttk,messagebox
import sqlite3
import time
import os

class checkingoutClass: # Making a class to provide structure, so that the widgets are defined in one place inside the constructor and the functions are defined later in the code.
    def __init__(self,root):               # Default constructor and passing the object 'root'
        self.root = root                   # Initializing the TK() object with self. so that it recognizes that the object belongs to class, otherwise the functions wouldn't be able to use this object
        self.root.geometry("1350x700+0+0") # Geometry helps to give width and height to window. Then giving starting point for x and y axes as 0 for both
        self.root.title("Equipment Checkout System | Developed by Team Group 2 (SSW540 Fall 2022) ") # Window title
        self.root.config(bg = "white")

        #===title===== title is an object of Label class . This class can be used to define static elements (Take username, password) in a form or html pages.
        title = Label(self.root, text="Equipment Checkout System",font=("Apple Symbols",35,"bold"),bg="#222222", fg="white" ,anchor="center",padx=10,pady=10).place(x=0,y=0,relwidth=1,height=70) # place is used to place the label in the frame, relwidth will refer our parent root object width

        #===btn_logout=====
        btn_logout = Button(self.root, text="Logout",command=self.logout,font=("Apple Symbols",15,"bold"), bg="#55AAFF", cursor="hand2").place(x=1150,y=20,width=150,height=30)
        
        #===clock===== We will be making clock as self because we will use it further to configure
        self.lbl_clock = Label(self.root, text="Welcome\t\t Date: MM-DD-YYYY\t\t Time: HH:MM:SS", font=("Apple Symbols",15),bg="#808080", fg="white") 
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #======Product_Frame===========
        
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=540)

        pTitle = Label(ProductFrame1,text="All Equipments",font=("goudy old style",20),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        #===========Product Search Frame====================

        self.var_search=StringVar()

        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search = Label(ProductFrame2,text="Search By Equipment Name ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        lbl_search=Label(ProductFrame2,text="Equipment Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=129,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",cursor="hand2").place(x=285,y=10,width=100,height=25)

        #===========Product details frame===============
        ProductFrame3 = Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly = Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3,columns=("pid","name","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid", text="Equipment ID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("qty", text="Quantity")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"]="headings" #To remove the extra column given by default and show only headings

        #fixing every column's width
        self.product_Table.column("pid",width=90)
        self.product_Table.column("name",width=100)
        self.product_Table.column("qty",width=80)
        self.product_Table.column("status",width=70)

        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data) #This is a type of event in our bind function. whenever you click and release this button, it calls a certain function, in this case it is get_data()
        #lbl_note=Label(ProductFrame1,text="Note: Enter 0 Qty to remove equipment from cart",font=("goudy old style",10),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #====================Checkout Details=======================
        self.var_name=StringVar()
        self.var_stid=StringVar()
        CheckingOutFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CheckingOutFrame.place(x=420,y=110,width=530,height=70)
        cTitle = Label(CheckingOutFrame,text="Checkout and Checkin",font=("goudy old style",20),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        lbl_name = Label(CheckingOutFrame,text="Student Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CheckingOutFrame,textvariable=self.var_name,font=("times new roman",13),bg="lightyellow").place(x=99,y=35,width=180)

        lbl_stid = Label(CheckingOutFrame,text="Student CWID",font=("times new roman",15),bg="white").place(x=283,y=35)
        txt_stid=Entry(CheckingOutFrame,textvariable=self.var_stid,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140)
     
        #========================Checkin/Checkout Frame=================

        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_stock = StringVar()


        CheckinCheckoutFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        CheckinCheckoutFrame.place(x=420,y=190,width=530,height=460)

        lbl_p_name = Label(CheckinCheckoutFrame,text="Equipment Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name = Entry(CheckinCheckoutFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_qty = Label(CheckinCheckoutFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_qty = Entry(CheckinCheckoutFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=230,y=35,width=150,height=22)

        self.lbl_instock = Label(CheckinCheckoutFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear = Button(CheckinCheckoutFrame,text="Clear",command=self.clear,font=("times new roman",15),bg="lightgray",cursor="hand2").place(x=230,y=65,width=150,height=22)
        self.btn_checkout = Button(CheckinCheckoutFrame,text="CheckOut",command=self.checkout,font=("times new roman",15),bg="lightgray",cursor="hand2")
        self.btn_checkout.place(x=40,y=150,width=150,height=22)
        self.btn_checkin = Button(CheckinCheckoutFrame,text="CheckIn",command=self.checkin,font=("times new roman",15),bg="lightgray",cursor="hand2")
        self.btn_checkin.place(x=230,y=150,width=150,height=22)

 #======Search BY EQUIPMENTS_Frame===========
        
        EquipFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        EquipFrame1.place(x=953,y=110,width=410,height=540)

        pTitle = Label(EquipFrame1,text="Students with Equipments",font=("goudy old style",20),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        #===========Product Search Frame====================

        self.var_search1=StringVar()

        EquipFrame2=Frame(EquipFrame1,bd=2,relief=RIDGE,bg="white")
        EquipFrame2.place(x=2,y=42,width=398,height=90)

        #lbl_search = Label(EquipFrame2,text="",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        lbl_search=Label(EquipFrame2,text="Student Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=5)
        txt_search=Entry(EquipFrame2,textvariable=self.var_search1,font=("times new roman",15),bg="lightyellow").place(x=105,y=8,width=150,height=22)
        btn_search=Button(EquipFrame2,text="Search",command=self.search1,font=("goudy old style",15),bg="#2196f3",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(EquipFrame2,text="Show All",command=self.show1,font=("goudy old style",15),bg="#083531",cursor="hand2").place(x=285,y=10,width=100,height=25)

        #===========Variables for All checkouts frame======
        self.var_chid = StringVar()
        self.var_stname = StringVar()
        self.var_stcwid = StringVar()
        self.var_checkoutqty = StringVar()


       #=======All Checkouts Frame and Treeview ====

        ch_frame = Frame(EquipFrame1,bd=3,relief=RIDGE)
        ch_frame.place(x=2,y=140,width=398,height=375)

        scrolly = Scrollbar(ch_frame,orient=VERTICAL)
        scrollx = Scrollbar(ch_frame, orient=HORIZONTAL)

        self.checkout_table = ttk.Treeview(ch_frame,columns=("chid","stname","stcwid","pname","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.checkout_table.xview)
        scrolly.config(command=self.checkout_table.yview)

        self.checkout_table.heading("chid", text="C ID")
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
        

        #===FOOTER===== This time no 'self.lbl_footer' required because we wont be configuring this label later
        lbl_footer = Label(self.root, text="Equipment Checkout System\nDeveloped by Team: Group 2 of SSW540 Class 2022", font=("Apple Symbols",15),bg="#808080", fg="white").pack(side=BOTTOM,fill=X) #using pack this time because it is easier

        self.show()

        self.date_and_time()
#==============================All Functions============================

    def show(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
     #  self.product_Table = ttk.Treeview(ProductFrame3,columns=("pid","name","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        try:
            cur.execute("Select pid,name,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show1(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
     #  self.product_Table = ttk.Treeview(ProductFrame3,columns=("pid","name","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        try:
            cur.execute("Select chid,stname,stcwid,pname,qty from checkouts")
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
                cur.execute("Select pid,name,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def search1(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_search1.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("Select chid,stname,stcwid,pname,qty from checkouts where stname LIKE '%"+self.var_search1.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.checkout_table.delete(*self.checkout_table.get_children())
                    for row in rows:
                        self.checkout_table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


    def get_data(self,ev): #we have passed an event in this function that is "ev". the bind function above which has an event will call this function "get_data" 
        f = self.product_Table.focus() #whatever you click in the supplier table, that is the treeview goes into this variable 'f'.
        content = (self.product_Table.item(f))
        row = content['values'] # using values in quotes we are filtering all the values that are present in the content tuple and putting them in row variable.
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_qty.set('1')
        self.lbl_instock.config(text=f"In Stock [{str(row[2])}]")
        self.var_stock.set(row[2])
        self.btn_checkout["state"] =NORMAL
        self.btn_checkin["state"] = DISABLED
        self.btn_checkin["cursor"] =""
        self.btn_checkout["cursor"] = "hand2"
        self.show1()


    def get_data1(self,ev): #we have passed an event in this function that is "ev". the bind function above which has an event will call this function "get_data" 
        f = self.checkout_table.focus() #whatever you click in the supplier table, that is the treeview goes into this variable 'f'.
        content = (self.checkout_table.item(f))
        row = content['values'] # using values in quotes we are filtering all the values that are present in the content tuple and putting them in row variable.
        self.var_chid.set(row[0])
        self.var_name.set(row[1])
        self.var_stid.set(row[2])
        self.var_pname.set(row[3])
        self.var_qty.set(row[4])
        self.var_checkoutqty.set(row[4])
        self.lbl_instock.config(text=f"")
        self.btn_checkin["state"] = NORMAL
        self.btn_checkout["state"] =DISABLED
        self.btn_checkout["cursor"] = ""
        self.btn_checkin["cursor"] ="hand2"
        self.show()


    def checkout(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=='':
                messagebox.showerror('Error',"Please Select Product From The List",parent=self.root)
            elif self.var_name.get()=='':
                messagebox.showerror('Error',"Please Enter Student Name",parent=self.root)
            elif self.var_stid.get()=='':
                messagebox.showerror('Error',"Please Enter Student CWID ",parent=self.root)
            elif self.var_qty.get()=='':
                messagebox.showerror('Error',"Quantity Is Required",parent=self.root)
            elif int(self.var_qty.get())>int(self.var_stock.get()):
                messagebox.showerror('Error',"Not Enough Equipments Left",parent=self.root)
            else:
                cur.execute("Insert into checkouts (stname,stcwid,pname,qty) values(?,?,?,?)",(
                        self.var_name.get(),
                        self.var_stid.get(),
                        self.var_pname.get(),
                        self.var_qty.get()
                        
                ))
                con.commit()
                messagebox.showinfo("Success","Equipment Checked Out Successfully", parent=self.root)
                self.backend_stock_update_checkout()
                self.clear()
                
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def checkin(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        
        try:
            if self.var_chid.get()=='':
                messagebox.showerror('Error',"Please Select A Checkout From The List",parent=self.root)
            elif self.var_stid.get()=='':
                messagebox.showerror('Error',"Please Enter Student CWID ",parent=self.root)
            elif self.var_name.get()=='':
                messagebox.showerror('Error',"Please Enter Student Name",parent=self.root)
            elif self.var_qty.get()=='':
                messagebox.showerror('Error',"Quantity Is Required",parent=self.root)
            elif int(self.var_qty.get())>int(self.var_checkoutqty.get()):
                messagebox.showerror('Error',"Invalid quantity entered",parent=self.root)
            else:
                cur.execute("Select * from checkouts where chid=?",(self.var_chid.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Checkin",parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you want to check this equipment in?",parent=self.root)
                    if op== True:
                        ch_qty = int(self.var_checkoutqty.get())
                        u_qty = int(self.var_qty.get())
                        if(int(u_qty)==int(ch_qty)):        
                            cur.execute("delete from checkouts where chid=?",(self.var_chid.get(),))
                            con.commit()
                            messagebox.showinfo("Delete","Equiment Checked-In Successfully", parent=self.root)
                            self.backend_stock_update_checkin()
                            self.clear()
                        else:
                            n_qty = int(ch_qty)-int(u_qty)
                            chhid = int(self.var_chid.get())
                            cur.execute('update checkouts set qty=? where chid=?',(
                                n_qty,
                                chhid,
                            ))
                            con.commit()
                            messagebox.showinfo("Delete","Equiment Checked-In Successfully", parent=self.root)
                            self.backend_stock_update_checkin()
                            self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def date_and_time(self):
        time_= time.strftime("%I:%M:%S %p")
        date_= time.strftime("%m-%d-%Y")
        self.lbl_clock.config(text=f"Welcome\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.date_and_time)


    def clear(self):
        self.var_search.set('')
        self.var_search1.set('')
        self.var_chid.set('')
        self.var_name.set('')
        self.var_stid.set('')
        self.var_pname.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_pid.set('')
        self.var_stock.set('')
        self.btn_checkin["state"] = NORMAL
        self.btn_checkout["state"] =NORMAL
        self.btn_checkin["cursor"] ="hand2"
        self.btn_checkout["cursor"] = "hand2"
        self.show()
        self.show1()
        
    def backend_stock_update_checkout(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            pid = self.var_pid.get()
            qty1 = int(self.var_qty.get())
            stc = int(self.var_stock.get())
            qty = int(stc) - int(qty1)
            if int(qty1)==int(stc):
                status = 'Inactive'                
            if int(qty1)!=int(stc):
                status = 'Active'

            cur.execute('update product set qty=?,Status=? where pid=?',(
                qty,
                status,
                pid

            ))
            con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def backend_stock_update_checkin(self):
        con= sqlite3.connect(database=r'ems.db')
        cur = con.cursor()
        try:
            pn=self.var_pname.get()
            qty1 = int(self.var_qty.get())
            cur.execute('select qty from product where name=?',(self.var_pname.get(),))
            qty_tuple = cur.fetchone()
            stc = int(qty_tuple[0])
            qty = int(stc) + int(qty1)
            status='Active'
            cur.execute('update product set qty=?,Status=? where name=?',(
                qty,
                status,
                pn

            ))
            con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__": # So if the name is 'main' then it should open dashboard. we are making dashboard our main function page
    root = Tk()                # Creating an object for Tkinter class, This root is like our frame in which we will work
    obj = checkingoutClass(root)            # Creating an object for IMS class and passing root into it so that Tkinter class is attached with it 
    root.mainloop()            # Using mainloop so that the window stays until it is closed otherwise the window just exits after the program is run and this is what makes the window stay on the screen until closed

