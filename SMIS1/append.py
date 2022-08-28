"""
==============================================================
@In Project: SIMS
@File Name: append.py
@Author: Shihan Yang
@Create Date: 2021/06/08
@Update Date: ----/--/--
@Version: 1.0.0
@Functions: 
    1. Append student information
    2. Notes:
         增加 ---|---  1 单个学生信息
                 |---  2 从excel导入学生信息
                 |---  0 返回上一级菜单
==============================================================
"""
import pandas as pd

append_submenu = '''

    2 增加 ---|---  1 单个学生信息
              |---  2 从excel导入学生信息
              |---  0 返回上一级菜单

'''


def db_append(db):
    new_db = db
    while True:
        print(append_submenu)
        choose = input('  > Enter your option:')
        if choose == '0':
            break
        elif choose == '1':
            record = dict()
            print('  - Using default values when entering nothing.')
            sid = input('  > Student ID:')
            record['studentID'] = sid
            name = input('  > Name:')
            record['name'] = name
            dorm = input('  > Dorm No.:')
            record['dorm'] = dorm
            phone = input('  > Phonenumber:')
            record['phone'] = phone
            email = input('  > Email:')
            record['email'] = email
            one = input('  > Score of ONE:')
            if one == '':
                record['score_1'] = 0
            else:
                record['score_1'] = float(one)
            two = input('  > Score of TWO:')
            if two == '':
                record['score_2'] = 0
            else:
                record['score_2'] = float(two)
            three = input('  > Score of THREE:')
            if three == '':
                record['score_3'] = 0
            else:
                record['score_3'] = float(three)
            new_db.append(record)
            print('\nThe Record was handled already.\n')
            continue
        elif choose == '2':
            records = load_by_excel()
            for record in records:
                new_db.append(record)
            print('  - Load Successfully.')
            continue
        else:
            print('  - Wrong Inputting.')
    return new_db


def load_by_excel():
    filepath = "C://Users//冰//Desktop//SMIS1//data.xlsx"
    df = pd.read_excel(io=filepath, engine='openpyxl')
    df = df.astype({'studentID': 'str', 'phone': 'str'})
    df = df.to_dict(orient='records')
    return df
