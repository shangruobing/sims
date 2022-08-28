from django.contrib import admin
from . import models

# Register your models here. 应用注册
admin.site.register(models.Users)  # 使用默认的模型管理器
admin.site.register(models.Student)
admin.site.register(models.Course)
admin.site.register(models.Selection)
admin.site.register(models.Log)