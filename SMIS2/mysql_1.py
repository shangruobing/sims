# FileName: mysql_1.py  注意文件名不能为mysql
import mysql.connector as mc

db = mc.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="010209",  # 数据库密码
    database="simsdb"  # 指定数据库
)

cursor = db.cursor()  # 操作句柄（游标）

sql = 'show tables'
cursor.execute(sql)
for item in cursor:
    print(item)

sql = 'select * from student limit 0,3'
cursor.execute(sql)
for item in cursor:
    print(item)

db.commit()  # 如果数据库有变化，必须commit之后才能持久化    
cursor.close()
db.close()
