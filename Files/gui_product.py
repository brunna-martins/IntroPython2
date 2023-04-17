from tkinter import *
import sqlite3
import ctypes

class DataBase():
    def __init__(self):
        self.c = sqlite3.connect('database.db')
        self.createTable()

    def createTable(self):
        cursor = self.c.cursor()
        cursor.execute("""create table if not exists products
        (id text primary key, name text)""")
        self.c.commit()
        cursor.close()

class MyScreen:
    def __init__(self, master=None):
        self.frame1 = Frame(master)
        self.frame1["padx"] = 20
        self.frame1.pack(side=TOP)

        self.frame2 = Frame(master)
        self.frame2["pady"] = 20
        self.frame2.pack(side=BOTTOM)

        self.idLabel = Label(self.frame1,text="Id: ")
        self.idLabel.pack(side=TOP,anchor="w");
        self.idText = Entry(self.frame1);
        self.idText["width"] = 10
        self.idText.pack(side=TOP,anchor="w")
        self.idText.focus_set()

        self.nameLabel = Label(self.frame1, text="Name: ")
        self.nameLabel.pack(side=TOP,anchor="w")
        self.nameText = Entry(self.frame1)
        self.nameText["width"] = 30
        self.nameText.pack(side=TOP,anchor="w")

        self.save = Button(self.frame2,text="Insert",width=12)
        self.save["command"] = self.insert
        self.save.pack(side=LEFT)

        self.consult = Button(self.frame2,text="Consult",width=12)
        self.consult["command"] = self.see
        self.consult.pack(side=LEFT)

    def see(self):
        try:
            database = DataBase()
            cursor = database.c.cursor()
            cursor.execute("select * from products")
            products = cursor.fetchall()
            for product in products:
                print(product)
            print("Products registered in database: "+str(len(products)))
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, str(e), "Error", 0)
        finally:
            cursor.close()


    def insert(self):
        try:
            database = DataBase()
            cursor = database.c.cursor()
            sql = "insert into products (id,name) values(?,?)"
            cursor.execute(sql,(self.idText.get(),self.nameText.get()))
            database.c.commit()
            ctypes.windll.user32.MessageBoxW(0,"Sucessfully added","Info",0)
            self.clear()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0,str(e),"Error",0)
        finally:
            cursor.close()

    def clear(self):
        self.idText.delete(0,'end')
        self.nameText.delete(0,'end')
        self.idText.focus_set()

window = Tk()
window.title("Product Registration")
window.geometry("300x200+500+300") # width x height + right + down
MyScreen(window)
window.mainloop()