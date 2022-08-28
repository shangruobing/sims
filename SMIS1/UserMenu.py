from search import db_search


class UserMenu:
    def __init__(self, db=[]):
        student_DB = db
        user_menu = '''
    
        ====================================================
    
                Student Information Management System
    
                              Version 1.0
    
        ====================================================
    
              1 查 看 学 生 信 息
              0 退 出  
    
        '''
        while True:
            print(user_menu)
            option = input('\nEnter your option:')
            if option.isdigit():
                choose = int(option)
            else:
                print('Warning, Please Enter a DIGIT!')
                continue
            if choose == 1:
                db_search(student_DB)
                continue
            elif choose == 0:
                break
            else:
                print('Inputting WRONG!')
                continue
