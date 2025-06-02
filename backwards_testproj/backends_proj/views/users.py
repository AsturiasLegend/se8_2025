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
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.user  # ✅ 拿到验证通过的 user 实例

    return Response({
        "status": "success",
        "user_info": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        },
    })

# @api_view(['POST'])
# def login(request):
#     serializer = LoginSerializer(data=request.data)
    
#     if not serializer.is_valid():
#         return Response({
#             "status": "error",
#             "message": "用户名或密码错误"  # 统一错误提示
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         user = User.objects.get(username=serializer.validated_data['username'])
#         # 检查密码是否匹配
#         if not user.check_password(serializer.validated_data['password']):
#             raise ValidationError("密码错误")
            
#     except User.DoesNotExist:
#         return Response({
#             "status": "error",
#             "message": "用户不存在"
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     except ValidationError as e:
#         return Response({
#             "status": "error",
#             "message": str(e)
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     # 登录成功逻辑
#     return Response({
#         "status": "success",
#         "user_info": {
#             "id": user.id,
#             "username": user.username,
#             "role": user.role
#         }
#     }, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    """
    处理用户注册请求（使用序列化器）
    """
    serializer = RegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        # 返回第一个验证错误信息
        error_msg = next(iter(serializer.errors.values()))[0]
        return Response({
            'status': 'error',
            'message': error_msg
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 检查是否是管理员注册
        if serializer.validated_data.get('role') == 'administrator':
            admin_code = request.data.get('admin_code')
            if not admin_code or admin_code != 'ADMIN2025':  # 设置一个固定的管理员注册码
                return Response({
                    'status': 'error',
                    'message': '管理员注册需要提供正确的注册码'
                }, status=status.HTTP_403_FORBIDDEN)
        
        # 创建用户
        user = serializer.save()
        
        # 返回成功响应
        return Response({
            'status': 'success',
            'message': '注册成功',
            'user_id': user.id,
            'username': user.username,
            'role': user.role
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        # 记录异常信息
        import logging
        logging.error(f"用户注册异常: {str(e)}", exc_info=True)
        
        # 返回错误响应
        return Response({
            'status': 'error',
            'message': f'注册失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)