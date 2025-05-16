from django.urls import path
from backends_proj import views

urlpatterns = [path('', views.users.login)] # 需要填充路由接口，注意方法的名称本身组成路径的一部分