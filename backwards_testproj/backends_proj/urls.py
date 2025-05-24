from django.urls import path
from backends_proj import views

urlpatterns = [path('login/', views.users.login),
               path('register/', views.users.register),
               path('doctor_dashboard/', views.doctors.doctor_dashboard),  # 医生仪表盘
               ] # 需要填充路由接口，注意方法的名称本身组成路径的一部分