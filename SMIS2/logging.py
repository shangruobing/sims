"""
==============================================================
@In Project: SIMS
@File Name: logging.py
@Author: Shihan Yang
@Create Date: 2021/06/12
@Update Date: ----/--/--
@Version: 2.0.0
@Functions: 
    1. Logging window
    2. Notes:
          There are 3 types user: administrator,
                                  student,
                                  teacher,
          who get different functions of the application.
==============================================================
"""
import sys
import tkinter as tk
import tkinter.messagebox as tmbox

window = tk.Tk()
window.title('SIMS')
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
window.geometry('%dx%d+%d+%d' %
                (880, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

banner = tk.Label(window, text='学生信息管理系统',
                  font=('幼圆', 42, 'bold'), fg='#E02022',
                  height=3).pack()
banner = tk.Label(window, text='Version 2.0',
                  font=('幼圆', 26, 'bold'), fg='#606060').pack()


def logging():
    window.destroy()
    import dialog  # enter logging-in dialog


def saybye():
    tmbox.showwarning(title='bye', message='See you again!')
    window.destroy()
    sys.exit()  # quit the application
    # exit()  # quit the python3 


bpar = {'font': ('幼圆', 18, 'bold'),
        'fg': '#3020EE',
        'width': 12,
        'height': 2,
        'relief': tk.GROOVE
        }
tk.Button(window, text=' 请 登 录 ', **bpar,
          cursor='heart',
          command=logging).place(x=150, y=400)
tk.Button(window, text=' 退    出 ', **bpar,
          cursor='spider',
          command=saybye).place(x=560, y=400)

tk.Label(window, text='昆明理工大学管经学院信息管理与信息系统专业2019级暑期实践课程\n\rCopyright @ 2021.08-2021.10\n\r',
         font=('幼圆', 16)).pack(side='bottom')

window.mainloop()
