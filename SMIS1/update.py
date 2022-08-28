"""
==============================================================
@In Project: SIMS
@File Name: update.py
@Author: Shihan Yang
@Create Date: 2021/06/08
@Update Date: ----/--/--
@Version: 1.0.0
@Functions: 
    1. Update records
    2. Notes:
          
==============================================================
"""

update_submenu = '''

    3 修改 ---|---  1 修改学生信息
              |---  2 批量修改
              |---  0 返回

'''


def search_by_id(db, id):
    record = dict()
    for i in db:
        if i['studentID'] == id:
            record = i
    return record


def change_record(db, record):
    # can not change keywords
    new_db = db
    old_record = search_by_id(db, record['studentID'])
    new_db.remove(old_record)
    new_db.append(record)
    return new_db


def update_batch(db, ids, info_type, values):
    records = []
    new_db = db
    for i in ids:
        records.append(search_by_id(new_db, i))
        new_db.remove(search_by_id(new_db, i))

    # index = 0
    # while index < len(records):
    #     records[index][info_type] = values[index]
    #     index += 1

    for index, record in enumerate(records):
        record[info_type] = values[index]

    new_db += records
    return new_db


def db_update(db):
    new_db = db
    while True:
        print(update_submenu)
        option = input('  > Enter your option:')
        if option == '0':
            break
        elif option == '1':
            stid = input('  >> StudentID:')
            record = search_by_id(db, stid)
            if len(record) != 0:
                print('    ', record)
            else:
                print('  - StudentID is WRONG.')
                continue
            revise = input('  > What do you want to update (fieldname=value):')
            fieldname, value = revise.strip().split('=')
            if fieldname == 'studentID':
                print('  - Can not update keywords!')
                continue
            print(fieldname, value)
            record[fieldname] = value
            new_db = change_record(db, record)
            print('  - Updated already.')
            continue
        elif option == '2':
            sids = input('  >> Student ID to be deleted,separate with"," :').split(',')
            info_type = input('  > What type do you want to update:')
            values = input('  >> Value to be updated,separate with"," :').split(',')
            new_db = update_batch(db, sids, info_type, values)
            print('  - Updated already.')
            continue
        else:
            print('  - Inputting WRONG!')
            continue
    return new_db


if __name__ == '__main__':
    db = [{'studentID': '11', 'dorm': '209'}, {'studentID': '12', 'dorm': '208'},
          {'studentID': '13', 'dorm': '202'}]
    db_update(db)
