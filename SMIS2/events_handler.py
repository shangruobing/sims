"""
==============================================================
@In Project: SIMS
@File Name: events_handler.py
@Author: Shihan Yang
@Create Date: 2021/06/12
@Update Date: ----/--/--
@Version: 2.0.0
@Functions: 
    1. All functions of handling events from UI.
    2. Notes:
          It is main window of the application with menubar
          after logging in the system.
==============================================================
"""
import tkinter as tk
import tkinter.messagebox as tkm
import platform as pf  # get operation system information
from importlib import reload  # used for module reload
from tkinter import font

from dbm import *
import dbm  # for using database variables like dbm.db, dbm.cursor etc.
import dialog
from input_dialog import input_dialog


def quit(window):
    window.destroy()


def osinfo():
    info = pf.platform()
    info += ' @ ' + pf.machine()
    tkm.showinfo(title='OS information --- SIMS', message=info)


def connectdb(window):
    cdb_dialog = tk.Toplevel(window)
    cdb_dialog.geometry('+320+200')
    cdb_dialog.grab_set()  # set the model dialog
    font = ('consolas', 16, 'bold')
    color = '#EE3030'
    tk.Label(cdb_dialog, text="Host:", font=font, fg=color).grid(row=0, column=0, sticky=tk.E)
    tk.Label(cdb_dialog, text="Port:", font=font, fg=color).grid(row=1, column=0, sticky=tk.E)
    tk.Label(cdb_dialog, text="User:", font=font, fg=color).grid(row=2, column=0, sticky=tk.E)
    tk.Label(cdb_dialog, text="Password:", font=font, fg=color).grid(row=3, column=0, sticky=tk.E)
    tk.Label(cdb_dialog, text="Database:", font=font, fg=color).grid(row=4, column=0, sticky=tk.E)

    host = tk.Entry(cdb_dialog, textvariable=tk.StringVar(value='localhost'), font=font)
    host.grid(row=0, column=1, sticky=tk.W, padx=10)
    port = tk.Entry(cdb_dialog, textvariable=tk.StringVar(value='3306'), font=font)
    port.grid(row=1, column=1, sticky=tk.W, padx=10)
    user = tk.Entry(cdb_dialog, textvariable=tk.StringVar(value='root'), font=font)
    user.grid(row=2, column=1, sticky=tk.W, padx=10)
    password = tk.Entry(cdb_dialog, textvariable=tk.StringVar(value='010209'), font=font, show='*')
    password.grid(row=3, column=1, sticky=tk.W, padx=10)
    database = tk.Entry(cdb_dialog, textvariable=tk.StringVar(value='simsdb'), font=font)
    database.grid(row=4, column=1, sticky=tk.W, padx=10)
    if port.get() == '':
        port = 3306
    else:
        port = int(port.get())
    config = {
        'host': host.get(),
        'port': port,
        'user': user.get(),
        'password': password.get(),
        'database': database.get()
    }

    bnConnect = tk.Button(cdb_dialog, text="连接", width=15, command=lambda: connect(config, cdb_dialog), font=font,
                          fg=color)
    bnConnect.grid(row=5, column=0, sticky=tk.W, padx=5, pady=8)
    bnQuit = tk.Button(cdb_dialog, text="退出", width=15, command=lambda: quit(cdb_dialog), font=font, fg=color)
    bnQuit.grid(row=5, column=1, sticky=tk.E, padx=5, pady=8)


def dbinfo():
    if dbm.db is not None:
        dbm.cursor.execute('select concat(@@version_comment , \' \' , @@version) from dual')
        info = str(dbm.cursor.fetchall()[0][0])
        sql = '''select @@hostname,@@datadir, 
                       @@innodb_data_file_path,@@innodb_data_home_dir, 
                       @@innodb_log_file_size/1024/1024 from dual
              '''
        dbm.cursor.execute(sql)
        info += '\n\r' + str(dbm.cursor.fetchall()[0])
    else:
        info = 'Database server did not be connected yet.'
    tkm.showinfo(title='Database information --- SIMS', message=info)


def others():
    info = 'You can extend other functions from here.'
    tkm.showinfo(title='Other information --- SIMS', message=info)


def userinfo():
    if dialog.username is None:
        tkm.showinfo(title='User information --- SIMS', message='请先登录')
    else:
        info = 'Username: ' + dialog.username + '\r\n' + \
               'Usertype: ' + dialog.usertype
        tkm.showinfo(title='User information --- SIMS', message=info)


def changepsw(window):
    pass_dialog = tk.Toplevel(window)
    pass_dialog.geometry('+320+200')
    pass_dialog.grab_set()  # set the model dialog
    font = ('consolas', 16, 'bold')
    color = '#EE3030'
    tk.Label(pass_dialog, text="Old password:", font=font, fg=color).grid(row=0, column=0, sticky=tk.E)
    tk.Label(pass_dialog, text="New password:", font=font, fg=color).grid(row=1, column=0, sticky=tk.E)
    tk.Label(pass_dialog, text="Confirm NEW:", font=font, fg=color).grid(row=2, column=0, sticky=tk.E)
    old = tk.Entry(pass_dialog, font=font)
    old.grid(row=0, column=1, sticky=tk.W, padx=10)
    new = tk.Entry(pass_dialog, font=font)
    new.grid(row=1, column=1, sticky=tk.W, padx=10)
    confirm = tk.Entry(pass_dialog, font=font)
    confirm.grid(row=2, column=1, sticky=tk.W, padx=10)

    pinfo = {
        'user': dialog.username,
        'old': old.get(),
        'new': new.get()
    }

    def changepassword(pinfo, pass_dialog):
        if new.get() != confirm.get():
            tkm.showinfo(title='Password change information --- SIMS', message='两次输入的口令不一致')
            return
        if dbm.db is None:
            tkm.showinfo(title='Password change information --- SIMS', message='请先连接数据库')
        else:
            # dbm.cursor.execute('SET SQL_SAFE_UPDATES=0')  # needed when first execute
            sql = 'update user set password=\'%s\' where name=\'%s\' and password=\'%s\'' % (
                new.get(), pinfo['user'], old.get())
            print(sql)
            res = dbm.cursor.execute(sql)  # 0 if fail, 1 if success
            if res:
                dbm.db.commit()
                tkm.showinfo(title='Password change information --- SIMS', message='密码已经修改好')
                pass_dialog.destroy()
            else:
                tkm.showinfo(title='Password change information --- SIMS', message='密码修改失败了')

    bnChange = tk.Button(pass_dialog, text="修改", width=15, command=lambda: changepassword(pinfo, pass_dialog),
                         font=font, fg=color)
    bnChange.grid(row=5, column=0, sticky=tk.W, padx=5, pady=8)
    bnQuit = tk.Button(pass_dialog, text="退出", width=15, command=lambda: quit(pass_dialog), font=font, fg=color)
    bnQuit.grid(row=5, column=1, sticky=tk.E, padx=5, pady=8)


def logout():
    dbm.cursor.close()
    dbm.db.close()
    dialog.username = None
    dialog.usertype = None
    tkm.showinfo(title='Log out information --- SIMS', message='退出登录后请重新连接数据库服务器')


def relog():
    reload(dialog)  # can not repeat more than 2 times


def basicinfo(window):
    if dbm.db is not None:
        sql = 'select * from student'
        dbm.cursor.execute(sql)
        results = dbm.cursor.fetchall()
        showResults_Treeview(window, results)
    else:
        info = 'Database server did not be connected yet.'
        tkm.showinfo(title='Searching information --- SIMS', message=info)


def scoreinfo(window):
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

    def select():
        sql = f"SELECT * FROM student WHERE studentID='{sid.get()}' AND name='{name.get()}'"
        dbm.cursor.execute(sql)
        result = dbm.cursor.fetchall()
        showResults_Treeview(window, result)
        quit()

    def quit():
        enter.destroy()

    bnSure = tk.Button(enter, text="确认", width=10, command=select, font=font, fg=color)
    bnSure.grid(row=5, column=0, padx=25, pady=18)
    bnQuit = tk.Button(enter, text="退出", width=10, command=quit, font=font, fg=color)
    bnQuit.grid(row=5, column=2, padx=25, pady=18)


def newrecord(window):
    enter = tk.Toplevel(window)
    enter.title('录入学生信息')
    enter.geometry('+320+200')
    enter.grab_set()
    font = ('consolas', 16, 'bold')
    color = '#EE3030'
    tk.Label(enter, text=' 学  号 ', font=font, fg=color).grid(row=0, column=0, sticky=tk.E)
    tk.Label(enter, text=' 姓  名 ', font=font, fg=color).grid(row=1, column=0, sticky=tk.E)
    tk.Label(enter, text=' 电  话 ', font=font, fg=color).grid(row=2, column=0, sticky=tk.E)
    tk.Label(enter, text=' 邮  箱 ', font=font, fg=color).grid(row=3, column=0, sticky=tk.E)
    tk.Label(enter, text=' 宿  舍 ', font=font, fg=color).grid(row=4, column=0, sticky=tk.E)
    sid = tk.Entry(enter, font=font, textvariable=tk.StringVar(value='一定不能为空'), bg='#FFA0A0')
    sid.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    name = tk.Entry(enter, font=font)
    name.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    phone = tk.Entry(enter, font=font)
    phone.grid(row=2, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    email = tk.Entry(enter, font=font)
    email.grid(row=3, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    dorm = tk.Entry(enter, font=font)
    dorm.grid(row=4, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)

    def append():
        record = {
            'sid': sid.get(),
            'name': name.get(),
            'phone': phone.get(),
            'email': email.get(),
            'dorm': dorm.get()
        }
        if dbm.db is not None:
            sql = 'insert into student (studentID, name, phone, email, dorm) VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\')' \
                  % (int(record['sid']), record['name'], record['phone'], record['email'], record['dorm'])
            print(sql)
            res = dbm.cursor.execute(sql)
            dbm.db.commit()
            if res:
                tkm.showinfo(title='Entering records information --- SIMS', message='增加一条新记录成功')
                enter.destroy()
            else:
                tkm.showinfo(title='Entering records information --- SIMS', message='增加记录不成功')
        else:
            info = 'Database server did not be connected yet.'
            tkm.showinfo(title='Entering records information --- SIMS', message=info)

    def cls():
        sid.delete(0, 'end')
        name.delete(0, 'end')
        phone.delete(0, 'end')
        email.delete(0, 'end')
        dorm.delete(0, 'end')

    def quit():
        enter.destroy()

    bnAdd = tk.Button(enter, text="增加", width=10, command=append, font=font, fg=color)
    bnAdd.grid(row=5, column=0, padx=25, pady=18)
    bnCls = tk.Button(enter, text="清空", width=10, command=cls, font=font, fg=color)
    bnCls.grid(row=5, column=1, padx=25, pady=18)
    bnQuit = tk.Button(enter, text="退出", width=10, command=quit, font=font, fg=color)
    bnQuit.grid(row=5, column=2, padx=25, pady=18)


def scoresentry(window):
    enter = tk.Toplevel(window)
    enter.title('录入学生成绩')
    enter.geometry('+320+200')
    enter.grab_set()
    font = ('consolas', 16, 'bold')
    color = '#EE3030'
    tk.Label(enter, text=' 学  号 ', font=font, fg=color).grid(row=0, column=0, sticky=tk.E)
    tk.Label(enter, text=' 姓  名 ', font=font, fg=color).grid(row=1, column=0, sticky=tk.E)
    tk.Label(enter, text=' 成绩 1 ', font=font, fg=color).grid(row=2, column=0, sticky=tk.E)
    tk.Label(enter, text=' 成绩 2 ', font=font, fg=color).grid(row=3, column=0, sticky=tk.E)
    tk.Label(enter, text=' 成绩 3 ', font=font, fg=color).grid(row=4, column=0, sticky=tk.E)
    sid = tk.Entry(enter, font=font, textvariable=tk.StringVar(value='一定不能为空'), bg='#FFA0A0')
    sid.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    name = tk.Entry(enter, font=font)
    name.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    score1 = tk.Entry(enter, font=font)
    score1.grid(row=2, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    score2 = tk.Entry(enter, font=font)
    score2.grid(row=3, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
    score3 = tk.Entry(enter, font=font)
    score3.grid(row=4, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)

    def isValid():
        sql = f"SELECT * FROM student WHERE studentID='{sid.get()}' AND name='{name.get()}'"
        print(sql)
        print(dbm.cursor.execute(sql))
        if dbm.cursor.execute(sql) != 0:
            return True
        else:
            return False

    def save_score():
        if isValid():
            sql = f"UPDATE student SET score_1={score1.get()},score_2={score2.get()},score_3={score3.get()} " \
                  f"WHERE studentID='{sid.get()}' AND name='{name.get()}'"
            dbm.cursor.execute(sql)
            dbm.db.commit()
            tkm.showinfo(title='成绩录入 --- SIMS', message='录入成绩成功!')
            quit()
        else:
            tkm.showinfo(title='成绩录入 --- SIMS', message='成绩录入失败，查无此人')

    def quit():
        enter.destroy()

    bnAdd = tk.Button(enter, text="录入", width=10, command=save_score, font=font, fg=color)
    bnAdd.grid(row=5, column=0, padx=25, pady=18)
    bnQuit = tk.Button(enter, text="退出", width=10, command=quit, font=font, fg=color)
    bnQuit.grid(row=5, column=2, padx=25, pady=18)


def revise(window):
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

    def select():
        sql = f"SELECT * FROM student WHERE studentID='{sid.get()}' AND name='{name.get()}'"
        dbm.cursor.execute(sql)
        result = dbm.cursor.fetchall()
        showResults_Treeview(window, result)
        quit()
        update_info(result)

    def quit():
        enter.destroy()

    bnSure = tk.Button(enter, text="确认", width=10, command=select, font=font, fg=color)
    bnSure.grid(row=5, column=0, padx=25, pady=18)
    bnQuit = tk.Button(enter, text="退出", width=10, command=quit, font=font, fg=color)
    bnQuit.grid(row=5, column=2, padx=25, pady=18)

    def update_info(result):
        enter = tk.Toplevel(window)
        enter.title('修改学生信息')
        enter.geometry('+320+200')
        enter.grab_set()
        font = ('consolas', 16, 'bold')
        color = '#EE3030'
        tk.Label(enter, text=' 学  号 ', font=font, fg=color).grid(row=0, column=0, sticky=tk.E)
        tk.Label(enter, text=' 姓  名 ', font=font, fg=color).grid(row=1, column=0, sticky=tk.E)
        tk.Label(enter, text=' 电  话 ', font=font, fg=color).grid(row=2, column=0, sticky=tk.E)
        tk.Label(enter, text=' 邮  箱 ', font=font, fg=color).grid(row=3, column=0, sticky=tk.E)
        tk.Label(enter, text=' 宿  舍 ', font=font, fg=color).grid(row=4, column=0, sticky=tk.E)
        id = tk.Entry(enter, font=font, textvariable=tk.StringVar(value=f'{result[0][0]}'), bg='#FFA0A0',
                      state='readonly')
        id.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
        name = tk.Entry(enter, textvariable=tk.StringVar(value=f'{result[0][1]}'), font=font)
        name.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
        phone = tk.Entry(enter, textvariable=tk.StringVar(value=f'{result[0][2]}'), font=font)
        phone.grid(row=2, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
        email = tk.Entry(enter, textvariable=tk.StringVar(value=f'{result[0][3]}'), font=font)
        email.grid(row=3, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
        dorm = tk.Entry(enter, textvariable=tk.StringVar(value=f'{result[0][4]}'), font=font)
        dorm.grid(row=4, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)
        print(name.get(), phone.get(), email.get(), dorm.get())

        def update():
            sid=id.get()
            sql = f"UPDATE student SET name='{name.get()}',phone='{phone.get()}',email='{email.get()}'," \
                  f"dorm='{dorm.get()}'" \
                  f"WHERE studentID='{sid}'"
            print(sql)
            dbm.cursor.execute(sql)
            dbm.db.commit()
            quit()
            sql = f"SELECT * FROM student WHERE studentID='{sid}'"
            dbm.cursor.execute(sql)
            result = dbm.cursor.fetchall()
            showResults_Treeview(window, result)
            tkm.showinfo(title='信息修改 --- SIMS', message='修改信息成功!')

        def quit():
            enter.destroy()

        bnAdd = tk.Button(enter, text="修改", width=10, command=update, font=font, fg=color)
        bnAdd.grid(row=5, column=0, padx=25, pady=18)
        bnQuit = tk.Button(enter, text="退出", width=10, command=quit, font=font, fg=color)
        bnQuit.grid(row=5, column=2, padx=25, pady=18)


def delete(window):
    enter = tk.Toplevel(window)
    enter.title('删除学生信息')
    enter.geometry('+320+200')
    enter.grab_set()
    font = ('consolas', 16, 'bold')
    color = '#EE3030'
    tk.Label(enter, text=' 学  号 ', font=font, fg=color).grid(row=0, column=0, sticky=tk.E)
    sid = tk.Entry(enter, font=font, textvariable=tk.StringVar(value='一定不能为空'), bg='#FFA0A0')
    sid.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=30, pady=7)

    def append():
        if dbm.db is not None:
            sql = 'delete from student where studentID = %d' % int(sid.get())
            print(sql)
            res = dbm.cursor.execute(sql)
            dbm.db.commit()
            if res:
                tkm.showinfo(title='Deleting records information --- SIMS', message='删除一条新记录成功')
                enter.destroy()
            else:
                tkm.showinfo(title='Deleting records information --- SIMS', message='删除记录不成功')
        else:
            info = 'Database server did not be connected yet.'
            tkm.showinfo(title='Deleting records information --- SIMS', message=info)

    def cls():
        sid.delete(0, 'end')

    def quit():
        enter.destroy()

    bnAdd = tk.Button(enter, text="删除", width=10, command=append, font=font, fg=color)
    bnAdd.grid(row=1, column=0, padx=25, pady=18)
    bnCls = tk.Button(enter, text="清空", width=10, command=cls, font=font, fg=color)
    bnCls.grid(row=1, column=1, padx=25, pady=18)
    bnQuit = tk.Button(enter, text="退出", width=10, command=quit, font=font, fg=color)
    bnQuit.grid(row=1, column=2, padx=25, pady=18)


def history():
    pass


def recover():
    pass


if __name__ == '__main__':
    window = tk.Tk()
    # osinfo()
    # dbinfo()
    newrecord(window)
    pass
