############# tkinter app to send and view crypto prices with (#TREEVIEW )################


from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import smtplib
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup as bs
import csv
from tkinter.simpledialog import askstring

root = Tk()
root.geometry("600x400+350+160")
root.title("Crypto $")
root.configure(bg = "#707b7c")

l = Label(root,text = "Get crypto information!",padx = 70,pady = 6,bd = 3,relief = "raised",fg = "green",font = 32)
l.place(x = 130,y = 10)


def get_info():
    global my_tree
    global rows
    names = []
    prices = []
    rows = []
    try:
        req = requests.get("https://www.coingecko.com/")
        soup = bs(req.text,"lxml")
    except :
        messagebox.showerror("error","check connection!")
    else:
        for i in soup.find_all(class_="tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between"):
            names.append(i.text.strip())
        for x in soup.find_all(class_="td-price price text-right pl-0"):
            prices.append(x.text.strip())

        rows = [(i,x) for i,x in zip(names,prices)]
        
        my_tree = ttk.Treeview(root)
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview",background = "silver",fieldbackground = "silver")
        style.map("Treeview",background = [("selected","green")])
        my_tree["columns"] = ["name","price"]
        my_tree["show"] = "headings"

        my_tree.column("name",width = 255)
        my_tree.column("price",width = 255)


        my_tree.heading("name",text = "name")
        my_tree.heading("price",text = "price")

        for i,x in rows:
            my_tree.insert("","end",values = [i,x])
        my_tree.place(width = 560,height = 250,x = 20,y = 50)


b1 = Button(root,text = "get info!",fg = "green",bd = 2,relief = "raised",padx = 20,command = get_info)
b1.place(x = 250,y = 300)

def send():
    row = ["name","price"]
    global rows2
    rows2 = []
    
    try:
        
        for child in my_tree.get_children():
            rows2.append(my_tree.item(child)["values"])
        
    except:
        messagebox.showerror("error","click show info first!")
    
    else:
        s_em = askstring("message","enter your email!")
        
        with open("cr.csv","w") as f:
            writer = csv.writer(f)
            writer.writerow(row)
            writer.writerows(rows2)
        
        msg = EmailMessage()
        msg["subject"] = "crypto info"
        msg["from"] = "wael.althawadi@gmail.com"
        msg["to"] = s_em
        msg.set_content(" ....crypto prices! ")
    
        with open("cr.csv","rb") as f2:
            content = f2.read()
            msg.add_attachment(content,maintype = "csv",subtype = "csv",filename = "cr.csv")
        if s_em != None:
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as conn:
                conn.login("wael.althawadi@gmail.com","khystpedseqzieyk")
                conn.send_message(msg)
            messagebox.showinfo("message!","email has been sent succesfully!")
        else:
            pass
    
b2 = Button(root,text = "Send it via email!",fg = "green",bd = 2,relief = "raised",padx = 60,command = send)
b2.place(x = 180,y = 330)

mainloop()
