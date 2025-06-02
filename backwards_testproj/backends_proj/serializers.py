from rest_framework import serializers
from backends_proj.models import User, Department, DoctorDepartment, DepartmentSchedule, SystemMetrics

class UserSerializer(serializers.ModelSerializer): # 注册的序列化器，需要验证所有属性，实际上没有用到，注册功能的序列化器由RegisterSerializer类实现
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

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    role = serializers.CharField()

    def validate(self, data):
        # 手动验证逻辑（无需模型关联）
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        
        # 检查用户是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("用户不存在")
        
        # 简单密码比较（仅限测试环境）
        if user.password != password:
            raise serializers.ValidationError("密码错误")

        if user.role != role:
            raise serializers.ValidationError("用户角色不匹配")
        
        self.user = user
            
        return data  # 返回验证通过的数据

class RegisterSerializer(serializers.Serializer):
    """
    用户注册序列化器，与修改后的前端表单对应
    """
    username = serializers.CharField(max_length=50)
    real_name = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=20)
    id_card = serializers.CharField(max_length=18, required=False, allow_blank=True, allow_null=True)
    gender = serializers.ChoiceField(choices=['M', 'F', 'O'])
    age = serializers.IntegerField(min_value=1, max_value=120)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=['patient', 'doctor', 'administrator'], default='patient')
    
    def validate_username(self, value):
        """验证用户名是否唯一"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value
        
    def validate_phone(self, value):
        """验证手机号是否唯一且长度正确"""
        if len(value) != 11:
            raise serializers.ValidationError("手机号必须为11位")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("该手机号已被注册")
        return value
        
    def validate_id_card(self, value):
        """验证身份证号是否唯一且长度正确（如果提供）"""
        if value is None or value == "":
            return None
            
        if len(value) != 18:
            raise serializers.ValidationError("身份证号必须为18位")
        if User.objects.filter(id_card=value).exists():
            raise serializers.ValidationError("该身份证号已被注册")
        return value
    
    def create(self, validated_data):
        """创建并保存用户"""
        user = User(
            username=validated_data['username'],
            real_name=validated_data['real_name'],
            phone=validated_data['phone'],
            id_card=validated_data.get('id_card'),
            gender=validated_data['gender'],
            age=validated_data['age'],
            role=validated_data.get('role', 'patient')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DoctorDepartmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.real_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = DoctorDepartment
        fields = ['id', 'doctor', 'doctor_name', 'department', 'department_name', 'is_primary', 'created_at']

class DepartmentScheduleSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = DepartmentSchedule
        fields = ['id', 'department', 'department_name', 'date', 'time_slot', 
                 'total_quota', 'remaining_quota', 'is_active', 'created_at']

class SystemMetricsSerializer(serializers.ModelSerializer):
    completion_rate = serializers.FloatField(read_only=True)
    no_show_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = SystemMetrics
        fields = ['id', 'date', 'total_appointments', 'completed_appointments',
                 'canceled_appointments', 'no_show_appointments', 'completion_rate',
                 'no_show_rate', 'created_at']
