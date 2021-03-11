import tkinter as tk
import tkinter.filedialog as fd
import sqlite3
import csv
import os
import pandas as pd
from openpyxl import load_workbook


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('JLC BOM')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.dialog_button1 = tk.Button(self, text='JLC DB open', command=jlc_open, fg='black', bg='yellow', width=60)
        self.dialog_button1.pack(anchor=tk.NW)
        self.dialog_button2 = tk.Button(self, text='Digi-Key BOM open', command=dk_open, fg='black', bg='yellow green', width=60)
        self.dialog_button2.pack(anchor=tk.NW)
        self.dialog_button3 = tk.Button(self, text='Result DB dump', command=db_dump, fg='black', bg='orange', width=60)
        self.dialog_button3.pack(anchor=tk.NW)

def jlc_open():
    jlcfile = fd.askopenfilename(filetypes=[('csv ', '*.csv'),('All ','*.*')])
    df = pd.read_csv(jlcfile, encoding = "shift-jis")
    df.to_sql('jlcdb', conn, if_exists='replace')
    conn.commit()
    
def dk_open():
    dkfile = fd.askopenfilename(filetypes=[('csv ', '*.csv'),('All ','*.*')])
    df = pd.read_csv(dkfile, encoding = "shift-jis")
    df.to_sql('dkdb', conn, if_exists='replace')
    conn.commit()
    
def db_dump():
    ret = fd.asksaveasfilename()
    cur.execute("select * from dkdb ;")
    list = cur.fetchall()
    for dkp in list:
        pn = dkp[1]
        print ("pn = ", pn)
        cur.execute("select * from jlcdb where MFR_Part = '%s' ;" % (pn))
        c = cur.fetchall()
        if c:
            for m in c:
                print ("fetch = ",m[1])
        else:
            print ("empty")

dbname = "jlcdb.sqlite3"
conn = sqlite3.connect(dbname)
cur = conn.cursor()
root = tk.Tk()
app = Application(master=root)
app.mainloop()
