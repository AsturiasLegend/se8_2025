# from django.shortcuts import render
# from django.http import HttpResponse
# def login(request):
#     return HttpResponse("login page")

# views/users.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from backends_proj.serializers import *
from backends_proj.models import *
from rest_framework.exceptions import ValidationError

# @api_view(['POST'])
# def login(request):
#     """
#     简化版登录接口（仅用于开发测试）
#     请求示例：
#     POST /login/
#     {
#         "username": "test",
#         "password": "123456"
#     }
#     """
#     serializer = LoginSerializer(data=request.data)
    
#     if serializer.is_valid():
#         # 获取用户对象
#         user = User.objects.get(username=serializer.validated_data['username'])
        
#         return Response({
#             "status": "success",
#             "user_info": {
#                 "id": user.id,
#                 "username": user.username,
#                 "role": user.role
#             }
#         }, status=status.HTTP_200_OK)
    
#     print(serializer.errors)
#     return Response({
#         "status": "error",
#         "errors": serializer.errors
#     }, status=status.HTTP_400_BAD_REQUEST)

# views.py
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": "用户名或密码错误"  # 统一错误提示
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=serializer.validated_data['username'])
        # 检查密码是否匹配
        if not user.check_password(serializer.validated_data['password']):
            raise ValidationError("密码错误")
            
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "message": "用户不存在"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 登录成功逻辑
    return Response({
        "status": "success",
        "user_info": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }, status=status.HTTP_200_OK)