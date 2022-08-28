# FileName: win.py

import tkinter as tk
import tkinter.messagebox as tmbox

window = tk.Tk()  # 创建主窗口对象
window.title('SIMS')
window.geometry('800x600')
# window.state('zoomed') 
# window.attributes("-fullscreen", True)  # maxize window without title

banner = tk.Label(window, text='学生信息管理系统\n\rVersion 2.0',
                  font=('幼圆', 42, 'bold'), fg='#E02022',
                  height=4).pack()


def sayhi():
    tmbox.showinfo(title='Hi', message='Hello Python World.')


def saybye():
    tmbox.showwarning(title='bye', message='See you again!')


hi = tk.Button(window, text='Say Hello',
               font=('consolas', 18, 'bold'), fg='#5020EE',
               command=sayhi)
# hi.pack(side='left')
hi.place(x=180, y=400)
bye = tk.Button(window, text=' Bye Bye ',
                font=('consolas', 18, 'bold'), fg='#3050EE',
                command=saybye)
# bye.pack(side='right')
bye.place(x=520, y=400)

footnote = tk.Label(window, text='昆明理工大学管经学院信息管理与信息系统专业2019级暑期实践课程\n\rCopyright @ 2021.08-2021.10\n\r',
                    font=('幼圆', 16)).pack(side='bottom')

window.mainloop()  # 启动窗口事件的主循环 进入到消息循环，一旦检测到事件，就刷新组件。
