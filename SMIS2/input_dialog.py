import tkinter as tk
from tkinter import *
from dbm import *
import dbm  # for using database variables like dbm.db, dbm.cursor etc.

"""输入学号信息"""


def input_dialog(window, command):
    enter = tk.Toplevel(window)
    enter.title('请输入相关信息')
    enter.geometry('+320+200')
    enter.grab_set()
    font = ('consolas', 16, 'bold')
    color = '#EE3030'
    tk.Label(enter, text=' 学  号 ', font=font, fg=color).grid(row=0, column=0, sticky=tk.E)
    tk.Label(enter, text=' 姓  名 ', font=font, fg=color).grid(row=1, column=0, sticky=tk.E)
    sid = tk.Entry(enter, font=font, textvariable=tk.StringVar(value='一定不能为空'), bg='#FFA0A0')
    sid.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    name = tk.Entry(enter, font=font)
    name.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)

    # def select():
    #     sql = f"SELECT * FROM student WHERE studentID='{sid.get()}' AND name='{name.get()}'"
    #     dbm.cursor.execute(sql)
    #     result = dbm.cursor.fetchall()
    #     return result

    def quit():
        enter.destroy()

    bnSure = tk.Button(enter, text="确认", width=10, command=command, font=font, fg=color)
    bnSure.grid(row=5, column=0, padx=25, pady=18)
    bnQuit = tk.Button(enter, text="退出", width=10, command=quit, font=font, fg=color)
    bnQuit.grid(row=5, column=2, padx=25, pady=18)
    return sid, name, enter
