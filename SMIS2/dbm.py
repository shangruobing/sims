"""
==============================================================
@In Project: SIMS
@File Name: dbm.py
@Author: Shihan Yang
@Create Date: 2021/06/12
@Update Date: ----/--/--
@Version: 2.0.0
@Functions: 
    1. Manipulate databases 
    2. Notes:
          
==============================================================
"""
import pymysql as ps
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm

dbconfig = dict()
db = None
cursor = None


def connect(config, cdbd):
    global dbconfig
    dbconfig = config
    global db
    db = ps.connect(**config)
    if db is False:
        return False
    else:
        info = 'Connect database is successful.'
        print(info)
        print(db)
        tkm.showinfo(title='Connected Database --- SIMS', message=info)
        window = cdbd._root()  # get main window handler
        window.title('SIMS ———— 学生信息管理系统（信管专业小学期实践工程项目） 已连接数据库')
        children = window.winfo_children()  # get all direct children widgets
        print(children)
        global cursor
        cursor = db.cursor()
        sql = 'select * from student'
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        # showResults(children[2], results)  # the index of list_box is 2
        showResults_Treeview(window, results)
        cdbd.destroy()
        return True


def showResults(list_box, results):
    list_box.delete(0, 'end')
    header = '  学号   姓名       电话          Email地址     宿舍号  成绩-1 成绩-2 成绩-3'
    list_box.insert(0, header)
    for i in results:
        info = '  '
        long = len(i)
        for j in range(long):
            info += str(i[j]) + '  '
        list_box.insert('end', info)
    list_box.select_set(1, 1)


def showResults_Treeview(window, results):
    children = window.winfo_children()
    children[2].destroy()
    tree = ttk.Treeview(window, columns=('1', '2', '3', '4', '5', '6', '7', '8'),
                        show='headings',  # hidden fist column
                        yscrollcommand=children[1].set)  # children[1] is Scrollbar object
    args = {
        'width': 100,
        'anchor': 'center'
    }
    for i in [('1', '学号'), ('2', '姓名'), ('3', '电话'),
              ('4', 'Email地址'), ('5', '宿舍'),
              ('6', '成绩1'), ('7', '成绩2'), ('8', '成绩3')]:
        tree.column(i[0], **args)
        tree.heading(i[0], text=i[1])
    for i in results:
        tree.insert('', 'end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
    tree.pack(expand=True, fill=tk.BOTH)
    children[1].config(command=tree.yview)
    style_head = ttk.Style()
    style_head.configure('Treeview.Heading', font=('幼圆', 18, 'bold'), foreground='#2020FF')
    style_head.configure('Treeview', rowheight=30, font=('幼圆', 16))


def closedb():
    cursor.close()
    db.close()


if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '010209',
        'database': 'simsdb'
    }
    dialog = tk.Tk()
    connect(config, dialog)
    print('database =', db)
    print('cursor = ', cursor)
    print('config =', dbconfig)
