from django.db import models
from django.utils import timezone as datetime


class Student(models.Model):
    studentid = models.IntegerField(db_column='studentID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    dorm = models.CharField(max_length=45, blank=True, null=True)
    score_1 = models.FloatField(blank=True, null=True, default=0.0)
    score_2 = models.FloatField(blank=True, null=True, default=0.0)
    score_3 = models.FloatField(blank=True, null=True, default=0.0)

    class Meta:
        managed = False
        db_table = 'student'

    def __str__(self):  # 重写类的__str__方法，注意字段名是大小写敏感的
        return '学号：%d, 姓名：%s, 电话：%s, 电邮：%s, 宿舍：%s, 科目1：%4.2f, 科目2：%4.2f, 科目3：%4.2f' % \
               (int(self.studentid), self.name, self.phone, self.email, self.dorm,
                self.score_1, self.score_2, self.score_3)


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return '(User {%d, %s, %s})' % (self.id, self.name, self.type)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    courseNo = models.IntegerField(default=0, null=False)
    name = models.CharField(max_length=60, blank=True, null=True)
    teacher = models.CharField(max_length=45, blank=True, null=True)
    term = models.IntegerField(default=4, null=True)
    period = models.IntegerField(default=36, null=True)
    credit = models.IntegerField(default=2, null=True)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return '(Course {%d, %s, %s, in %d term, with %d credits})' % (
            self.courseNo, self.name, self.teacher, self.term, self.credit)


class Selection(models.Model):
    id = models.AutoField(primary_key=True)
    courseid = models.ForeignKey(to='Course', to_field='id', on_delete=models.CASCADE)
    studentid = models.ForeignKey(to='Student', to_field='studentid', on_delete=models.CASCADE)

    class Meta:
        db_table = 'selection'

    def __str__(self):
        return '(Selection {%d, %d, %d})' % (self.id, self.courseid_id, self.studentid_id)


class Log(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    username = models.CharField(db_column='userName', max_length=255, blank=True, null=True)
    functionname = models.CharField(db_column='functionName', max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'

    def __str__(self):
        return f"Log {self.time} {self.username} {self.functionname} {self.content}"

    def logging(username, functionname, content, time=datetime.now().strftime('%F %T')):
        record = Log(time=time, username=username, functionname=functionname, content=content)
        record.save()
