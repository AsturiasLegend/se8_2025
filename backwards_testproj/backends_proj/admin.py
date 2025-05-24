from django.contrib import admin

# Register your models here.

from .models import User, PatientInfo, AppointmentSlot, RegistrationOrder  # 新增导入

admin.site.register(User)
admin.site.register(PatientInfo)
admin.site.register(AppointmentSlot)  # 注册号源
admin.site.register(RegistrationOrder)  # 注册挂号单


# 默认内部后台管理的配置，最好不要动
