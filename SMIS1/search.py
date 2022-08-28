"""
==============================================================
@In Project: SIMS
@File Name: search.py
@Author: Shihan Yang
@Create Date: 2021/06/10
@Update Date: ----/--/--
@Version: 1.0.0
@Functions: 
    1. Searching information from database
    2. Notes:
          Command line interface
==============================================================
"""

search_submenu = '''

    1 查看 ---|---  1 全部学生信息
              |---  2 按学号查询
              |---  3 按姓名查询
              |---  4 其它条件查询
              |---  0 返回

'''


def search_by_id(db, id):
    record = dict()
    for i in db:
        if i['studentID'] == id:
            record = i
    return record


def search_by_name(db, name):
    records = list()
    for i in db:
        if i['name'] == name:
            records.append(i)
    return records


def search_by_condition(db, info_type, condition):
    records = list()
    for i in db:
        if i[info_type] == condition:
            records.append(i)
    return records


def showall(data):
    total = len(data)
    print('======================================================================================')
    print('                      There are %d records in the database       ' % total)
    print('======================================================================================')
    print('No.\t ID\t\tName\t\t\tEmail\t\t\tPhone\tScore1\tScore2\tScore3')
    for i in range(total):
        print('--------------------------------------------------------------------------------------')
        print('%d\t%s\t%s\t%s\t%s\t%4.1f\t%4.1f\t%4.1f ' %
              (i + 1, data[i]['studentID'], data[i]['name'], data[i]['email'],
               data[i]['phone'], float(data[i]['score_1']),
               float(data[i]['score_2']), float(data[i]['score_3'])))
    print('--------------------------------------------------------------------------------------')


def show_results(records):
    number = len(records)
    print('======================================================================================')
    print('                       Searched %d result records in the database       ' % number)
    print('======================================================================================')
    print('No.\t ID\t\tName\t\t\tEmail\t\t\tPhone\tScore1\tScore2\tScore3')
    for i in range(number):
        print('--------------------------------------------------------------------------------------')
        print('%d\t%s\t%s\t%s\t%s\t%4.1f\t%4.1f\t%4.1f ' %
              (i + 1, records[i]['studentID'], records[i]['name'], records[i]['email'],
               records[i]['phone'], float(records[i]['score_1']),
               float(records[i]['score_2']), float(records[i]['score_3'])))
    print('--------------------------------------------------------------------------------------')


def db_search(db):
    while True:
        print(search_submenu)
        option = input('  > Enter your option:')
        if option == '0':
            break
        elif option == '1':
            showall(db)
            continue
        elif option == '2':
            sid = input('  > Student ID:')
            record = search_by_id(db, sid.strip())
            if record != {}:
                records = [record]
                show_results(records)
            else:
                print('  - There are no results!')
                show_results([])
            continue
        elif option == '3':
            name = input('  > Name:')
            records = search_by_name(db, name.strip())
            show_results(records)
            continue
        elif option == '4':
            type_submenu = "StudentID   Name    Dorm    Phone   Email"
            info_type = input(f'  > Type({type_submenu}):').strip().lower()
            for i in db:
                if info_type in i.keys():
                    condition = input('  > Condition:').strip()
                    records = search_by_condition(db, info_type, condition)
                    show_results(records)
                    break
                else:
                    print('Type is incorrect')
                break
        else:
            print('  - Inputting WRONG.')
            continue
    return
