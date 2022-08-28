from append import db_append
from search import db_search
from update import db_update
from delete import db_delete
from stati import db_stat  # no stat, which conflicts with stat package


class AdminMenu:

    def __init__(self, db=[]):
        student_DB = db
        main_menu = '''

        ====================================================

                Student Information Management System

                              Version 1.0

        ====================================================

              1 查 看 学 生 信 息
              2 增 加 学 生 信 息
              3 修 改 学 生 信 息
              4 删 除 学 生 信 息
              5 统 计 
              0 退 出  

        '''
        while True:
            print(main_menu)
            option = input('\nEnter your option:')
            if option.isdigit():
                choose = int(option)
            else:
                print('Warning, Please Enter a DIGIT!')
                continue
            if choose == 1:
                db_search(student_DB)
                continue
            elif choose == 2:
                student_DB = db_append(student_DB)
                continue
            elif choose == 3:
                student_DB = db_update(student_DB)
                continue
            elif choose == 4:
                student_DB = db_delete(student_DB)
                continue
            elif choose == 5:
                db_stat(student_DB)
                continue
            elif choose == 0:
                break
            else:
                print('Inputting WRONG!')
                continue
