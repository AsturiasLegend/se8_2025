from rest_framework import serializers
from backends_proj.models import User

class UserSerializer(serializers.ModelSerializer): # 注册的序列化器，需要验证所有属性
    # 显示角色名称（替代原始值）
    role_display = serializers.CharField(
        source='get_role_display', 
        read_only=True,
        label='角色显示'
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'real_name',
            'phone',
            'role',
            'role_display',
            'id_card',
            'is_active',
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # 密码不返回
            'is_active': {'read_only': True}    # 仅管理员可修改
        }
    
# class LoginSerializer(serializers.ModelSerializer): # 登录的序列化器，只需要验证用户名和密码
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'password'
#         ]
    
#     def validate(self, data):
#         # 手动验证用户名密码
#         try:
#             user = User.objects.get(username=data['username'])
#             if user.password != data['password']:  # 直接比较字符串（仅限测试环境！）
#                 raise serializers.ValidationError("密码错误")
#             return data
#         except User.DoesNotExist:
#             raise serializers.ValidationError("用户不存在")

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # 手动验证逻辑（无需模型关联）
        username = data.get('username')
        password = data.get('password')
        
        # 检查用户是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("用户不存在")
        
        # 简单密码比较（仅限测试环境）
        if user.password != password:
            raise serializers.ValidationError("密码错误")
            
        return data  # 返回验证通过的数据
