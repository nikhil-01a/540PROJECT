from tkinter import * # For GUI
from PIL import Image,ImageTk #pip install pillow.. Import this library to use Gifs and Jpeg type images
#from categories import categoriesClass

class IMS: # Making a class to provide structure, so that the widgets are defined in one place inside the constructor and the functions are defined later in the code.
    def __init__(self,root):               # Default constructor and passing the object 'root'
        self.root = root                   # Initializing the TK() object with self. so that it recognizes that the object belongs to class, otherwise the functions wouldn't be able to use this object
        self.root.geometry("1350x700+0+0") # Geometry helps to give width and height to window. Then giving starting point for x and y axes as 0 for both
        self.root.title("Equipment Checkout System | Developed by Team Group 2 (SSW540 Fall 2022) ") # Window title
        self.root.config(bg = "white")

        #===title===== title is an object of Label class . This class can be used to define static elements (Take username, password) in a form or html pages.
        title = Label(self.root, text="Equipment Checkout System",font=("Apple Symbols",35,"bold"),bg="#222222", fg="white" ,anchor="center",padx=10,pady=10).place(x=0,y=0,relwidth=1,height=70) # place is used to place the label in the frame, relwidth will refer our parent root object width

        #===btn_logout=====
        btn_logout = Button(self.root, text="Logout",font=("Apple Symbols",15,"bold"), bg="#55AAFF", cursor="hand2").place(x=1150,y=20,width=150,height=30)
        
        #===clock===== We will be making clock as self because we will use it further to configure
        self.lbl_clock = Label(self.root, text="Welcome\t\t Date: MM-DD-YYYY\t\t Time: HH:MM:SS", font=("Apple Symbols",15),bg="#808080", fg="white") 
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #===Left Menu=== Left FRAME
        self.MenuLogo = Image.open("images/Stevenslogo.png") #opening image to resize it
        self.MenuLogo = self.MenuLogo.resize((200,200),Image.ANTIALIAS) #Antialias will resize the image but it will preserve its quality
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo) #dynamically passing image to imagetk through photoimage

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white") # Frame means: just like root we are creating another frame inside root. bd = border, relief is border style
        LeftMenu.place(x=0,y=100,width=200,height=599)

        lbl_menulogo = Label(LeftMenu, image=self.MenuLogo) # to place the image in LeftMenu
        lbl_menulogo.pack(side=TOP,fill=X) # packing it so that it defines itself. side is to command where to keep it. fill = x will fill the Leftmenu with it horizontally

        self.icon_arrow = PhotoImage(file="images/arrow.png")

        lbl_menu = Label(LeftMenu, text="Menu",font=("Apple Symbols",20), bg="#808080",fg="white").pack(side=TOP,fill=X) #pack is to place but with features like fill x axis, side it to TOP. TOP here will place this label below the previous TOP.
        btn_category = Button(LeftMenu, text="Categories",command=self.categories,image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("Apple Symbols",20,"bold"), bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_equipments = Button(LeftMenu, text="Equipments",image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("Apple Symbols",20,"bold"), bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier = Button(LeftMenu, text="Suppliers",image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("Apple Symbols",20,"bold"), bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_checkouts = Button(LeftMenu, text="Checkouts",image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("Apple Symbols",20,"bold"), bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit = Button(LeftMenu, text="Exit",image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("Apple Symbols",20,"bold"), bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        #======CONTENT========
        self.lbl_categories = Label(self.root,text="Total Categories\n[ 0 ]",bd=5,relief="ridge",bg="#808080", fg="white")
        self.lbl_categories.place(x=300,y=170,height=160,width=300)

        self.lbl_equipments = Label(self.root,text="Total Equipments\n[ 0 ]",bd=5,relief="ridge",bg="#808080", fg="white")
        self.lbl_equipments.place(x=800,y=170,height=160,width=300)

        self.lbl_suppliers = Label(self.root,text="Total Suppliers\n[ 0 ]",bd=5,relief="ridge",bg="#808080", fg="white")
        self.lbl_suppliers.place(x=300,y=350,height=160,width=300)

        self.lbl_checkouts = Label(self.root,text="Total Checkouts\n[ 0 ]",bd=5,relief="ridge",bg="#808080", fg="white")
        self.lbl_checkouts.place(x=800,y=350,height=160,width=300)

        #===FOOTER===== This time no 'self.lbl_footer' required because we wont be configuring this label later
        lbl_footer = Label(self.root, text="Equipment Checkout System\nDeveloped by Team: Group 2 of SSW540 Class 2022", font=("Apple Symbols",15),bg="#808080", fg="white").pack(side=BOTTOM,fill=X) #using pack this time because it is easier

#========================================================================================

    def categories(self): # Now whatever we defined with 'self' can be used within this employee function
        self.new_win= Toplevel(self.root) #to use this 'root' here we had defined 'root' with 'self' earlier.
    #   self.new_obj= categoriesClass(self.new_win) 


if __name__=="__main__": # So if the name is 'main' then it should open dashboard. we are making dashboard our main function page
    root = Tk()                # Creating an object for Tkinter class, This root is like our frame in which we will work
    obj = IMS(root)            # Creating an object for IMS class and passing root into it so that Tkinter class is attached with it 
    root.mainloop()            # Using mainloop so that the window stays until it is closed otherwise the window just exits after the program is run and this is what makes the window stay on the screen until closed
