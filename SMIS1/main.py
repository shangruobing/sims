"""
==============================================================
@In Project: SIMS
@File Name: main.py
@Author: Shihan Yang
@Create Date: 2021/06/08
@Update Date: ----/--/--
@Version: 1.0.8
@Functions: 
    1. Main user interface
    2. Notes:
          Command line interface
==============================================================
"""
from pathlib import Path

from AdminMenu import *
from UserMenu import *
from db import loaddb, dumpdb

student_DB = list()
db_file = 'student.data'
if Path(db_file).exists():
    student_DB = loaddb(db_file)
else:
    header = {'number': None, 'studentID': None, 'name': None, 'dorm': None,
              'phone': None, 'email': None, 'score_1': 0, 'score_2': 0,
              'score_3': 0}
    # student_DB.append(header)
    dumpdb(student_DB, db_file)


def login():
    print('Welcome to Student Information Management System')
    username = input('\nEnter your username:')
    password = input('\nEnter your password:')
    with open('account.txt') as file:
        lines = file.readlines()
        for line in lines:
            name, word, login_type = line.strip().split(' ')
            if name == username and word == password:
                return login_type


if login() == 'admin':
    admin = AdminMenu(db=student_DB)
else:
    user = UserMenu(db=student_DB)

dumpdb(student_DB, db_file)

print('\nEnd. Welcome again.\n\n')
