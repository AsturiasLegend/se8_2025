from django.urls import path
from backends_proj import views

urlpatterns = [path('login/', views.users.login),
               path('register/', views.users.register),
               path('doctor/dashboard/', views.doctors.doctor_dashboard),  # 医生仪表盘, 修改挂号单状态（取消/完成）
               path('doctor/create/', views.doctors.create_appointment_slot),    # 新增号源路由
               path('doctor/cancel/', views.doctors.cancel_appointment_slot),   # 取消号源路由
               ] # 需要填充路由接口，注意方法的名称本身组成路径的一部分