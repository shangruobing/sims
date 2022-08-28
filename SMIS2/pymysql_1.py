# FileName: pymysql_1.py  文件名不能为pymysql

import pymysql as ps

config = {
    "host": "localhost",
    "port": 3306,  # 端口
    "user": "root",  # 用户名
    "password": "010209",  # 密码
    "database": "simsdb",  # 数据库名
}
db = ps.connect(**config)

cursor = db.cursor()

sql = '''select * from student
         where name='张三丰'
      '''
cursor.execute(sql)
results = cursor.fetchall()  # fetchone() 取第一个结果记录
for i in results:
    print(i)

cursor.close()
db.close()
