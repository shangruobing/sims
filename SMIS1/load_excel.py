import xlrd


def load_excel(file_name):
    """Give an excel file path, return the file data,
    the storage format is a dictionary list"""
    bk = xlrd.open_workbook(file_name)  # 首先打开workbook
    sh = bk.sheet_by_name("Sheet1")  # 定位到要操作的表Sheet1
    data = []  # 存储所有学生信息的列表
    for i in range(1, sh.nrows):  # 因第一行是表头 故从第二行开始读取学生信息
        info = {}  # 存储一个学生信息的字典
        for j in range(sh.ncols):  # 对于每一行学生信息 读取他每一列的信息
            key = sh.cell_value(0, j)  # 把表头例如学号这个属性作为字典的键
            value = sh.cell_value(i, j)  # 把记录中的每个字段值作为字典的值
            info[key] = value  # 字典的创建 字典名[键]=值
        data.append(info)  # 把一个完整的学生信息添加到总的学生表中
    print(data)  # 打印信息 可选
    return data  # 将整理好的数据返回待用


# 记得单元测试！
if __name__ == '__main__':
    file_name = "student_information.xlsx"
    load_excel(file_name)
