from django.urls import path
from backends_proj import views

urlpatterns = [path('login/', views.users.login),
               path('register/', views.users.register),
               path('doctor/dashboard/', views.doctors.doctor_dashboard),  # 医生仪表盘, 修改挂号单状态（取消/完成）
               path('doctor/create/', views.doctors.create_appointment_slot),    # 新增号源路由
               path('doctor/cancel/', views.doctors.cancel_appointment_slot),   # 取消号源路由
               path('doctor/profile/update', views.doctors.update_doctor_profile),  # 更新简介
               path('doctor/profile/', views.doctors.get_doctor_profile),      # 查看简介

               # 患者相关API
               path('patient/get_doctors/', views.patients.get_doctors_by_department, name='get_doctors_by_department'),   # 获取医生列表
               path('patient/get_slots/', views.patients.get_slots_by_doctor_and_date, name='get_slots_by_doctor_and_date'),   # 获取医生的号源
               path('patient/create-registration/', views.patients.create_registration, name='create_registration'),   # 患者创建挂号
               path('patient/available-slots/', views.patients.get_available_slots, name='get_available_slots'),   # 获取可预约时间段
               path('patient/orders/', views.patients.get_patient_orders, name='get_patient_orders'),
               path('patient/register/', views.patients.create_registration, name='patient_register'),
               path('patient/records/', views.patients.get_patient_orders, name='patient_records'),
                path('patient/cancel/', views.patients.cancel_registration, name='cancel_registration'),
                path('patient/order-detail/', views.patients.get_order_detail, name='get_order_detail'),
                path('patient/profile/', views.patients.get_patient_profile, name='get_patient_profile'),
               ] # 需要填充路由接口，注意方法的名称本身组成路径的一部分