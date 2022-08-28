"""
==============================================================
@In Project: SIMS
@File Name: stat.py
@Author: Shihan Yang
@Create Date: 2021/06/08
@Update Date: ----/--/--
@Version: 1.0.0
@Functions: 
    1. Do some statistics
    2. Notes:
          
==============================================================
"""

from search import search_by_id
import pandas as pd

stat_submenu = '''

    5 统计 ---|---  1 学生总分   
              |---  2 单科总成绩、平均分
              |---  3 单科最高分
              |---  4 总成绩排序
              |---  0 返回

'''


def scores_sum(db, sid):
    sum = 0
    if search_by_id(db, sid) == {}:
        print('  - %s does not exist.' % sid)
        sum = -1
    else:
        for i in db:
            if i['studentID'] == sid:
                sum = i['score_1'] + i['score_2'] + i['score_3']
    return sum


def object_sum(db, object_n):
    avg = 0
    sum = 0
    total = len(db)
    for i in db:
        sum += float(i[object_n])
    avg = sum / total
    return sum, avg


def object_max(db, object_n):
    max = 0
    for i in db:
        temp = float(i[object_n])
        if temp > max:
            max = temp
    return max


def total_scores_sort(db):
    records = db
    for record in records:
        record['total_scores'] = scores_sum(db, record['studentID'])

    new_list = sorted(records, key=lambda item: item['total_scores'], reverse=True)

    print('No.\t ID\t\tName\tScore1\tScore2\tScore3\tTotal')
    total = len(new_list)
    for i in range(total):
        print('%d\t%s\t%s\t%4.1f\t%4.1f\t%4.1f\t%4.1f' %
              (i + 1, new_list[i]['studentID'], new_list[i]['name'],
               float(new_list[i]['score_1']), float(new_list[i]['score_2']),
               float(new_list[i]['score_3']), float(new_list[i]['total_scores'])))
    save_score_excel(new_list)
    return new_list


def save_score_excel(db):
    df = pd.DataFrame(db)
    file = pd.ExcelWriter('score.xlsx')
    df.to_excel(file, encoding='UTF-8', index=False)
    file.save()
    print('Score has been export in score.xlsx')


def db_stat(db):
    temp_db = db
    while True:
        print(stat_submenu)
        option = input('  > Enter your option:')
        if option == '0':
            break
        elif option == '1':
            sid = input('  >> Student ID:')
            sum = scores_sum(db, sid.strip())
            if sum != -1:
                print('  - Sum_Score of %s is %f' % (sid, sum))
            continue
        elif option == '2':
            object_name = input('  > Object name:')
            sum, avg = object_sum(db, object_name.strip())
            print('  - Sum of the object %s is %f' % (object_name, sum))
            print('  - Average of the object %s is %f' % (object_name, avg))
            continue
        elif option == '3':
            object_name = input('  > Object name:')
            max = object_max(db, object_name.strip())
            print('  - The maximum of the object %s is %f' % (object_name, max))
            continue
        elif option == '4':
            total_scores_sort(db)
            continue
        else:
            print('  - Inputting WRONG!')
            continue


if __name__ == '__main__':
    db_stat([])
    pass
