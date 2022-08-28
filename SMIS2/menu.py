# FileName: menu.py

import tkinter as tk

window = tk.Tk()
window.title('SIMS')
window.geometry('1024x700')


def quit():
    window.destroy()


args = {'background': "#ffff00",
        'font': "TkMenuFont",
        'foreground': "#000000"}

menubar = tk.Menu(window)

# 二级菜单
adminMenu = tk.Menu(menubar)
for item in ['操作系统信息', '数据服务器信息', '数据库信息', '退出系统', '其它']:
    adminMenu.add_command(label=item, command=quit, **args)
userMenu = tk.Menu(menubar)
for item in ['用户信息', '口令修改', '退出登录']:
    userMenu.add_command(label=item)
aboutMenu = tk.Menu(menubar)
for item in ['版权信息', '系统更新', '联系我们']:
    aboutMenu.add_command(label=item)

# 三级菜单
studentMenu = tk.Menu(menubar)
for item in ['基本信息查询', '学生成绩查询', '其它查询']:
    studentMenu.add_command(label=item)
studentMenu.add_separator()
for item in ['录入学生信息', '录入学生成绩', '修改']:
    studentMenu.add_command(label=item)
studentMenu.add_separator()
for item in ['删除学生信息', '删除历史', '恢复', '其它']:
    studentMenu.add_command(label=item)
studentMenu.add_separator()
statMenu = tk.Menu(studentMenu)
for item in ['学生总成绩', '单科总分平均分', '年级成绩汇总统计',
             '不及格学生统计', '优秀学生统计']:
    statMenu.add_command(label=item)
studentMenu.add_cascade(label='统计', menu=statMenu)

# 一级菜单
for each in [('系统管理', adminMenu),
             ('学生信息管理', studentMenu),
             ('用户管理', userMenu),
             ('关于', aboutMenu)]:
    menubar.add_cascade(label=each[0], menu=each[1])

window['menu'] = menubar
window.mainloop()
