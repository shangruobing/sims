from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 初始界面
    path('favicon.ico', RedirectView.as_view(url='/static/image/favicon.ico')),
    path('addinfo', views.add, name='addinfo'),
    path('deleteinfo', views.delete, name='deleteinfo'),
    path('updateinfo', views.update, name='updateinfo'),
    path('search/', views.search, name='search'),
    path('login', views.login, name='login'),  # 修改样式
    path('logout', views.logout, name='logout'),  # 修改样式
    path('register', views.register, name='register'),  # 修改样式
    path('student', views.student, name='student'),  # 主界面
    path('users', views.users, name='users'),  # 用户管理
    path('select', views.select, name='select'),  # 选课
    path('selected', views.selected, name='selected'),  # 已选课
    path('addscore', views.addscore, name='addscore'),  # 增加成绩
    path('report', views.report, name='report'),  # 报表打印
    path('stat', views.stat, name='stat'),  # 数据统计
    path('addcourse', views.addcourse, name='addcourse'),  # 课程发布
    path('adminsims3/', views.dbm, name='dbm'),  # 数据库管理
    path('adduser', views.adduser, name='adduser'),  # 新增用户
    path('deleteuser', views.deleteuser, name='deleteuser'),  # 新增用户
    path('revork', views.revork, name='revork'),  # 新增用户
    path('log/', views.log, name='log'),  # 新增用户
    path('sysinfo', views.sysinfo, name='sysinfo'),  # 新增用户
    path('courseinfo/', views.courseinfo, name='courseinfo'),  # 新增用户
    path('changePassword', views.changePassword, name='changePassword'),  # 新增用户
    path('sims3/adminView', views.adminView, name='adminView'),  # 新增用户
    path('sims3/teacherView', views.teacherView, name='teacherView'),  # 新增用户
    path('plan', views.plan, name='plan'),  # 新增用户
]
