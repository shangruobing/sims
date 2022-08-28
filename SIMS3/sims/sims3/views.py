import codecs
import time
from django.utils.encoding import escape_uri_path
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from . import models
from django.contrib import messages as dm
from pyecharts.charts import Bar, Tab, Pie, Line, Timeline
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.globals import ThemeType
from django.contrib import auth
from datetime import datetime
import platform as pf
import psutil
from django.db import connection
import csv


def index(request):
    return render(request, 'index.html')


def login(request):
    users = models.Users.objects.all().values()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')
        true_user = False
        for i in users:
            if i['name'] == username and i['type'] == usertype and i['password'] == password:
                true_user = True
                break
        if true_user:
            dm.success(request, '登录成功')
            request.session['username'] = username
            request.session['usertype'] = usertype
            if usertype == "administrator":
                return redirect('adminView')
            if usertype == "teacher":
                return redirect('teacherView')
            # if usertype=="administrator":
            #     return redirect('index')
            return redirect('student')
        else:
            dm.error(request, '用户名或者密码错误')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, "index.html")


def register(request):
    valid = False
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        usertype = request.POST.get('usertype')
        passwd1 = request.POST.get('password1')
        passwd2 = request.POST.get('password2')
        if passwd2 == passwd1:
            try:
                record = models.Users.objects.get(name=username, type=usertype)
            except models.Users.DoesNotExist:
                valid = True
            else:
                dm.error(request, '用户已经存在')
        else:
            dm.error(request, '两次输入的密码不一致')
        if valid:
            total = models.Users.objects.all().count()
            obj = models.Users(id=total, name=username, type=usertype, password=passwd1)
            obj.save()
            dm.success(request, '注册成功')
            return render(request, 'login.html')
        else:
            if request.method != 'GET':
                dm.error(request, '注册失败')
    return render(request, 'register.html')


def student(request):
    """进入学生信息管理系统主界面"""
    return render(request, 'student.html')


def add(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        dorm = request.POST.get('park') + request.POST.get('building') + request.POST.get('room')
        obj = models.Student(studentid=studentid, name=name, phone=phone, email=email, dorm=dorm)
        record = obj.save()
        models.Log.logging(username=request.user.username, functionname='增加学生信息', content=obj)
        if record is None:
            dm.success(request, '增加信息成功')
            return redirect('search')
        else:
            dm.error(request, '出现了错误')
    return render(request, 'addinfo.html')


def addscore(request):
    students = models.Student.objects.all().values()
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        record = models.Student.objects.get(studentid=studentid)
        if record is not None:
            score_1 = request.POST.get('score_1')
            score_2 = request.POST.get('score_2')
            score_3 = request.POST.get('score_3')
            if request.POST.get('addscore') == ' 增  加 ':
                if score_1 == '':
                    score_1 = record.score_1
                if score_2 == '':
                    score_2 = record.score_2
                if score_3 == '':
                    score_3 = record.score_3
                models.Student.objects.filter(studentid=studentid). \
                    update(score_1=score_1, score_2=score_2, score_3=score_3)
                models.Log.logging(username=request.user.username, functionname='录入学生成绩',
                                   content={"学号": studentid, "分数1": score_1, "分数2": score_2, "分数3": score_3})
                record = models.Student.objects.get(studentid=studentid)
    return render(request, 'addscore.html', locals())


def delete(request):
    students = models.Student.objects.all().values()
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        record = models.Student.objects.get(studentid=studentid)
        if record is not None:
            name = request.POST.get('name')
            if name == '':
                name = record.name
            phone = request.POST.get('phone')
            if phone == '':
                phone = record.phone
            email = request.POST.get('email')
            if email == '':
                email = record.email
            dorm = request.POST.get('dorm')
            if dorm == '':
                dorm = record.dorm
        if request.POST.get('cutoff') == ' 删  除 ':
            models.Student.objects.filter(studentid=studentid).delete()
            models.Log.logging(username=request.user.username, functionname='删除学生信息',
                               content=f"删除了学号为{studentid}的学生信息")
            dm.success(request, message="删除成功")
            redirect('deleteinfo')
    return render(request, 'deleteinfo.html', locals())


def update(request):
    students = models.Student.objects.all().values()
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        record = models.Student.objects.get(studentid=studentid)
        if record is not None:
            name = request.POST.get('name')
            if name == '':
                name = record.name
            phone = request.POST.get('phone')
            if phone == '':
                phone = record.phone
            email = request.POST.get('email')
            if email == '':
                email = record.email
            dorm = request.POST.get('dorm')
            if dorm == '':
                dorm = record.dorm
        if request.POST.get('option') == '更新':
            models.Student.objects.filter(studentid=studentid).update(name=name, phone=phone, email=email, dorm=dorm)
            models.Log.logging(username=request.user.username, functionname='更改学生信息',
                               content=f'更改前信息为:{record},更改后信息为{studentid, name, phone, email, dorm}')
            record = models.Student.objects.get(studentid=studentid)
    return render(request, 'updateinfo.html', locals())


def search(request):
    studentid = request.GET.get('studentid', '')
    name = request.GET.get('name', '')
    if studentid == '' and name == '':
        students = models.Student.objects.all().values()
    # 若不加入 is not None 第二个页面id为None 会进入该循环 导致分页失败
    if studentid != '' and studentid != 0 and studentid is not None:
        students = models.Student.objects.filter(studentid=studentid)
    if name != '':
        students = models.Student.objects.filter(name=name)
    paginator = Paginator(students, 25)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    models.Log.logging(username=request.user.username, functionname='查询学生信息',
                       content='查询学生信息')
    return render(request, 'search.html', locals())


def courseinfo(request):
    name = request.GET.get('name', '')
    courses = models.Course.objects.all().values()
    teacher = request.GET.get('teacher', '')
    if name == '' and teacher == '':
        courses = models.Course.objects.all().values()
    # 若不加入 is not None 第二个页面id为None 会进入该循环 导致分页失败
    if name != '' and name != 0 and name is not None:
        courses = models.Course.objects.filter(name=name)
    if teacher != '':
        courses = models.Course.objects.filter(teacher=teacher)
    paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    models.Log.logging(username=request.user.username, functionname='查询课程信息',
                       content='查询课程信息')
    return render(request, 'courseinfo.html', locals())


def users(request):
    userid = request.GET.get('userid', '')
    type = request.GET.get('type', '')
    if userid == '' and type == '':
        users = models.Users.objects.all().values()
    if userid != '' and userid != 0:
        users = models.Users.objects.filter(id=userid)
    if type != '':
        users = models.Users.objects.filter(type=type)
    return render(request, 'users.html', locals())


def select(request):
    data = models.Course.objects.all().values()
    obj = models.Course.objects.all().values("name")
    courses = set()
    for i in obj:
        courses.add(i['name'])
    print(courses)
    courseName = request.POST.get('courseName')
    print(courseName)
    teachers = models.Course.objects.filter(name=courseName).values('teacher')
    print(teachers)
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        studentname = request.POST.get('name')
        course = request.POST.get('courseName')
        teacher = request.POST.get('teacher')
        courseNo = models.Course.objects.filter(name=courseName, teacher=teacher).values('courseNo')
        courseNo = courseNo[0]['courseNo']
        student = models.Student.objects.filter(studentid=studentid, name=studentname)
        if len(student) == 0:
            dm.error(request, '学生不存在')
        else:
            courserecord = models.Course.objects.filter(courseNo=courseNo, teacher=teacher)
            selection = models.Selection.objects.filter(courseid=courserecord[0], studentid=student[0])
            if len(selection) != 0:
                dm.info(request, '不能重复选同一门课')
            else:
                obj = models.Selection(courseid=courserecord[0], studentid=student[0])
                obj.save()
                dm.success(request, '选课成功')
                return redirect('selected')
    return render(request, 'selection.html', locals())


def selected(request):
    selections = []
    studentid = request.GET.get('studentid')
    courseno = request.GET.get('courseno')
    if studentid is None and courseno is None:
        select = models.Selection.objects.all().values()
        student = set()
        for i in select:
            student.add(i['studentid_id'])
        for j in student:
            objs = models.Selection.objects.filter(studentid=j)
            for i in objs:
                course = dict()
                course['studentid'] = i.studentid.studentid
                course['name'] = i.studentid.name
                course['courseNo'] = i.courseid.courseNo
                course['coursename'] = i.courseid.name
                course['teacher'] = i.courseid.teacher
                course['credit'] = i.courseid.credit
                course['term'] = i.courseid.term
                course['period'] = i.courseid.period
                selections.append(course)
    if studentid != '' and courseno != '':
        if studentid is not None:  # get all selected courses of this student
            objs = models.Selection.objects.filter(studentid=studentid)
            for i in objs:
                course = dict()
                course['studentid'] = i.studentid.studentid
                course['name'] = i.studentid.name
                course['courseNo'] = i.courseid.courseNo
                course['coursename'] = i.courseid.name
                course['teacher'] = i.courseid.teacher
                course['credit'] = i.courseid.credit
                course['term'] = i.courseid.term
                course['period'] = i.courseid.period
                selections.append(course)
        elif courseno is not None:  # get all students who selected this course
            course_obj = models.Course.objects.filter(courseNo=courseno).first()  # 只处理一个课程号的第一个老师
            # 如果相同的课程号有不同的老师，则需要循环course_obj变量
            objs = models.Selection.objects.filter(courseid=course_obj.id)
            for i in objs:
                student = dict()
                student['studentid'] = i.studentid.studentid
                student['name'] = i.studentid.name
                student['courseNo'] = i.courseid.courseNo
                student['coursename'] = i.courseid.name
                student['teacher'] = i.courseid.teacher
                student['credit'] = i.courseid.credit
                student['term'] = i.courseid.term
                student['period'] = i.courseid.period
                selections.append(student)
    return render(request, 'selected.html', locals())


def report(request):
    students = models.Student.objects.all().values()
    students = students[:18]

    data = models.Student.objects.all().values()
    dataset = []
    if request.method == 'POST':
        info = request.POST.getlist('info[]')
        str = ''
        for i in info:
            str += i + ','
        str = str[:-1]
        sql = f"select {str} from student"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="{}"'.format(escape_uri_path('学生信息.csv'))},
        )
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(info)
        writer.writerows([row for row in result])
        return response

    return render(request, 'report.html', locals())


# def save_score_excel(db):
#     df = pd.DataFrame(db)
#     file_path = os.path.abspath(os.path.dirname(os.getcwd()))
#     file = pd.ExcelWriter(f'{file_path}\\sims\\outputSheet\\学生信息.xlsx')
#     df.to_excel(file, encoding='UTF-8', index=False)
#     file.save()


def stat(request):
    score1 = statistics(field='score_1')
    score2 = statistics(field='score_2')
    score3 = statistics(field='score_3')
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.INFOGRAPHIC))
            .add_xaxis(["不及格", "60-69", "70-79", "80-89", "90-100"])
            .add_yaxis('分数1', [i for i in score1],
                       itemstyle_opts=opts.ItemStyleOpts(color='pink'))
            .add_yaxis('分数2', [i for i in score2],
                       itemstyle_opts=opts.ItemStyleOpts(color='lightgreen'))
            .add_yaxis('分数3', [i for i in score3],
                       itemstyle_opts=opts.ItemStyleOpts(color='lightskyblue'))
            .set_global_opts(title_opts=opts.TitleOpts(title='全校学生成绩分析'))
    )
    attr = ["不及格", "60-69", "70-79", "80-89", "90-100"]
    number_list = [i for i in score2]
    data = [list(i) for i in zip(attr, number_list)]

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.INFOGRAPHIC))
            .add_xaxis(["不及格", "60-69", "70-79", "80-89", "90-100"])
            .add_yaxis('分数1', [i for i in score1],
                       itemstyle_opts=opts.ItemStyleOpts(color='pink'))
            .add_yaxis('分数2', [i for i in score2],
                       itemstyle_opts=opts.ItemStyleOpts(color='lightgreen'))
            .add_yaxis('分数3', [i for i in score3],
                       itemstyle_opts=opts.ItemStyleOpts(color='lightskyblue'))
            .set_global_opts(title_opts=opts.TitleOpts(title='全校学生成绩分析'))
    )

    data = models.Student.objects.values("studentid", "name", "score_1", "score_2", "score_3")
    records = []
    for i in data:
        records.append(list(i.values()))

    table = Table()
    for i in records:
        i.append(i[2] + i[3] + i[4])

    result = sorted(records, key=lambda x: x[5], reverse=True)
    results = []
    count = 0
    for i in result:
        count += 1
        i.append(count)
        results.append(i)

    headers = ["学号", "姓名", "课程1", "课程2", "课程3", "总成绩", "排名"]
    rows = results[0:100]
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="学生总成绩排序", subtitle="仅显示全校前100名")
    )

    attr = ["不及格", "60-69", "70-79", "80-89", "90-100"]
    number_list = [i for i in score1]
    data = [list(i) for i in zip(attr, number_list)]
    p1 = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.INFOGRAPHIC))
            .add('各分数段人数', data)
            .set_global_opts(title_opts=opts.TitleOpts(title='全校学生成绩分析', subtitle='分数1'))
    )
    number_list = [i for i in score2]
    data = [list(i) for i in zip(attr, number_list)]
    p2 = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.INFOGRAPHIC))
            .add('各分数段人数', data)
            .set_global_opts(
            title_opts=opts.TitleOpts(title='全校学生成绩分析', subtitle='分数2'))
    )
    number_list = [i for i in score3]
    data = [list(i) for i in zip(attr, number_list)]
    p3 = (
        Pie(init_opts=opts.InitOpts(
            theme=ThemeType.INFOGRAPHIC))
            .add('各分数段人数', data)
            .set_global_opts(
            title_opts=opts.TitleOpts(title='全校学生成绩分析', subtitle='分数3'))
    )

    pie_line = Timeline().add_schema(is_auto_play=True)
    pie_line.add(p1, "分数1")
    pie_line.add(p2, "分数2")
    pie_line.add(p3, "分数3")

    tab = Tab()
    tab.add(bar, "柱状图")
    tab.add(pie_line, "饼图")
    tab.add(line, "折线图")
    tab.add(table, "总成绩")

    return HttpResponse(tab.render_embed())


def statistics(field="score_1"):
    data = models.Student.objects.values(field)
    data = sorted(data, key=lambda keys: keys[field], reverse=False)
    records = []
    for i in data:
        records.append(i[field])
    a, b, c, d, e = [], [], [], [], []
    for i in records:
        if i >= 90:
            a.append(i)
        elif 90 > i >= 80:
            b.append(i)
        elif 80 > i >= 70:
            c.append(i)
        elif 70 > i >= 60:
            d.append(i)
        elif 60 > i:
            e.append(i)
    return [len(a), len(b), len(c), len(d), len(e)]


def addcourse(request):
    if request.method == 'POST':
        courseNo = request.POST.get('courseNo')
        name = request.POST.get('name')
        teacher = request.POST.get('teacher')
        term = request.POST.get('term')
        period = request.POST.get('period')
        credit = request.POST.get('credit')
        obj = models.Course(courseNo=courseNo, name=name, teacher=teacher, term=term, period=period,
                            credit=credit)
        record = obj.save()
        if record is None:
            dm.success(request, '增加信息成功')
            return redirect('selected')
        else:
            dm.error(request, '出现了错误')
    return render(request, 'addcourse.html')


def dbm(request):
    """需要重写"""
    return render(request, 'adminsims3.html')


def adduser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        password = request.POST.get('password')
        repeat = request.POST.get('repeat')
        if password == repeat:
            obj = models.Users(name=name, type=type, password=password)
            record = obj.save()
            if record is None:
                dm.success(request, '增加信息成功')
                return redirect('users')
        else:
            dm.error(request, '出现了错误')
    return render(request, 'adduser.html')


def deleteuser(request):
    users = models.Users.objects.all().values()
    if request.method == 'POST':
        id = request.POST.get('id')
        record = models.Users.objects.get(id=id)
        if record is not None:
            name = request.POST.get('name')
            if name == '':
                name = record.name
            type = request.POST.get('type')
            if type == '':
                type = record.type

        if request.POST.get('cutoff') == ' 删  除 ':
            models.Users.objects.filter(id=id).delete()
            dm.success(request, message="删除成功")
            return redirect('deleteuser')
    return render(request, 'deleteuser.html', locals())


def revork(request):
    users = models.Users.objects.all().values()
    if request.method == 'POST':
        id = request.POST.get('id')
        record = models.Users.objects.get(id=id)
        if record is not None:
            name = request.POST.get('name')
            if name == '':
                name = record.name
            type = request.POST.get('type')
            if type == '':
                type = record.type

        if request.POST.get('cutoff') == '修改':
            models.Users.objects.filter(id=id).update(id=id, name=name, type=type)
            dm.success(request, message="成功")
            return redirect('revork')
    return render(request, 'revork.html', locals())


def log(request):
    function = request.GET.get('function', '')
    time = request.GET.get('time', '')
    if function == '' and time == '':
        logs = models.Log.objects.all().values()
    # 若不加入 is not None 第二个页面id为None 会进入该循环 导致分页失败
    if function != '' and function != 0 and function is not None:
        logs = models.Log.objects.filter(functionname=function)
    if time != '':
        print("test if")
        # 模糊查询 例如2021-9-5的日期 精确到天
        logs = models.Log.objects.filter(time__startswith=time)
    paginator = Paginator(logs, 10)
    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)
    return render(request, 'log.html', locals())


def sysinfo(request):
    system_info = pf.uname()
    node = system_info.node
    system = system_info.system
    boot_time = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time)
    now_time = datetime.fromtimestamp(time.time())
    run_time = now_time - boot_time
    now_time = now_time.strftime("%Y--%m--%d %H:%M:%S")
    boot_time = boot_time.strftime("%Y--%m--%d %H:%M:%S")
    kernel_name = system
    release = system_info.release
    version = system_info.version
    machine = system_info.machine
    cursor = connection.cursor()
    cursor.execute('select concat(@@version_comment , \' \' , @@version) from dual')
    db_version = cursor.fetchall()[0][0]
    return render(request, 'sysinfo.html', locals())


def changePassword(request):
    users = models.Users.objects.all().values()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        true_user = False
        for i in users:
            if i['name'] == username and i['password'] == password:
                true_user = True
                break
        if true_user:
            newpassword = request.POST.get('newpassword')
            repeat = request.POST.get('repeat')
            if newpassword == repeat:
                user = models.Users.objects.filter(name=username, password=password) \
                    .update(password=newpassword)
                dm.success(request, '修改密码成功')
            else:
                dm.error(request, '修改密码失败 两次密码不一致')
        else:
            dm.error(request, '用户名或者密码错误')
    return render(request, 'changePassword.html', locals())


def adminView(request):
    return render(request, 'adminView.html')


def teacherView(request):
    return render(request, "teacherView.html")


def plan(request):
    return render(request, "plan.html")
