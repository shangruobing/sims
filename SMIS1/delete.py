"""
==============================================================
@In Project: SIMS
@File Name: delete.py
@Author: Shihan Yang
@Create Date: 2021/06/10
@Update Date: ----/--/--
@Version: 1.0.0
@Functions: 
    1. Delete records
    2. Notes:
          Delete records by ID or by condition searching
==============================================================
"""

delete_submenu = '''

    4 删除 ---|---  1 单个学生信息
              |---  2 批量删除
              |---  3 条件删除
              |---  0 返回

'''


def delete_by_id(db, sid):
    for i in db:
        if i['studentID'] == sid:
            db.remove(i)
    return db


def delete_batch(db, sids):
    for i in sorted(sids):
        for j in db:
            if j['studentID'] == i:
                db.remove(j)
    return db


def delete_by_condition(db, info_type, condition):
    for i in db:
        if i[info_type] == condition:
            db.remove(i)
    return db


def db_delete(db):
    new_db = db
    while True:
        print(delete_submenu)
        option = input('  > Enter your option:')
        if option == '0':
            break
        elif option == '1':
            sid = input('  >> Student ID to be deleted:')
            new_db = delete_by_id(db, sid.strip())
            print('  - Deleted OK.')
            continue
        elif option == '2':
            sids = input('  >> Student ID to be deleted,separate with"," :').split(',')
            new_db = delete_batch(db, sids)
            print('  - Deleted OK.')
            continue
        elif option == '3':
            type_submenu = "StudentID   Name    Dorm    Phone   Email"
            info_type = input(f' >> Enter type({type_submenu}) of condition:').strip().lower()
            for i in db:
                if info_type in i.keys():
                    condition = input('  >> Condition to be deleted:').strip()
                    new_db = delete_by_condition(db, info_type, condition)
                    break
                else:
                    print('Type is incorrect')
                    break
        else:
            print('  - Inputting WRONG!')
            continue
    return new_db
