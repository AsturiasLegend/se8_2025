import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

# Create your models here.
# 对数据库进行操作的模型定义，类->SQL语句，经常使用

class User(models.Model):
    ROLE_CHOICES = [
        ('patient', '患者'),
        ('doctor', '医生'),
        ('admin', '管理员'),
    ]

    GENDER_CHOICES = [  # 新增性别选项
        ('M', '男'),
        ('F', '女'),
        ('O', '其他')
    ]

    # 基础信息
    username = models.CharField('username', max_length=50, unique=True)
    password = models.CharField('password', max_length=128)
    real_name = models.CharField('realname', max_length=30)
    phone = models.CharField('phonenumber', max_length=20, unique=True)
    role = models.CharField('role', max_length=10, choices=ROLE_CHOICES)
    id_card = models.CharField('idcard', max_length=18, unique=True, blank=True, null=True)
    
    # 状态字段
    is_active = models.BooleanField('is_active', default=True)
    
    age = models.PositiveIntegerField('年龄', null=True, blank=True)  # 允许为空
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, default='M')  # 默认男性

    class Meta:
        verbose_name = 'user'
        db_table = 'User' # 强制同步mysql中的表名，django默认使用的表名为"app名_model名"全小写

    def __str__(self):
        #return f"{self.real_name}({self.role})"
        return self.username

    # 密码处理方法
    def set_password(self, raw_password):
        #self.password = make_password(raw_password)
        self.password = raw_password
    
    def check_password(self, raw_password):
        #return check_password(raw_password, self.password)
        return raw_password == self.password
    
class PatientInfo(models.Model): # 只是PatientInfo的模型概念的定义，还没有相关的应用
    # 外键关联到User表
    user = models.OneToOneField(
        'User', 
        on_delete=models.CASCADE,
        related_name='patient_info',
        verbose_name='用户'
    )
    
    # 患者额外信息
    message = models.TextField(
        '个人描述', 
        max_length=2000, 
        blank=True, 
        null=True,
        help_text='患者可以添加个人的健康情况和其他相关描述'
    )
    
    # 添加其他专属于患者的字段（示例）
    medical_history = models.TextField('病史', blank=True, null=True)
    allergies = models.CharField('过敏史', max_length=255, blank=True, null=True)
    emergency_contact = models.CharField('紧急联系人', max_length=50, blank=True, null=True)
    emergency_phone = models.CharField('紧急联系电话', max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = '患者信息'
        verbose_name_plural = '患者信息'
        db_table = 'patientinfo'  # 指定表名为小写
    
    def __str__(self):
        return f"{self.user.username}的患者信息"
    
    # 属性方法，方便访问User表中的字段
    @property
    def username(self):
        return self.user.username
    
    @property
    def real_name(self):
        return self.user.real_name
    
    @property
    def gender(self):
        return self.user.gender
    
    @property
    def age(self):
        return self.user.age
    
    @property
    def id_card(self):
        return self.user.id_card
    
class AppointmentSlot(models.Model):
    # 号源模型
    doctor = models.ForeignKey(
        User,  # 关联到医生用户
        on_delete=models.CASCADE,
        related_name='doctor_slots',
        verbose_name='医生',
        limit_choices_to={'role': 'doctor'}  # 限制只能关联角色为医生的用户
    )
    time_start = models.DateTimeField('起始时间')  
    time_end = models.DateTimeField('结束时间')
    total_quota = models.PositiveIntegerField('总号量', default=20)
    remaining_quota = models.PositiveIntegerField('剩余号量', default=20)

    class Meta:
        verbose_name = '号源'
        verbose_name_plural = '号源'
        db_table = 'appointment_slot'

    def __str__(self):
        return f"{self.doctor.real_name} - {self.time_start.strftime('%Y-%m-%d %H:%M')} 至 {self.time_end.strftime('%Y-%m-%d %H:%M')} ({self.remaining_quota}/{self.total_quota})"



class RegistrationOrder(models.Model):
    # 挂号单模型
    STATUS_CHOICES = [
        ('pending', '待就诊'),
        ('completed', '已完成'),
        ('canceled', '已取消'),
        ('diagnosing', '正在就诊')
    ]

    order_id = models.BigAutoField('挂号单号', primary_key=True)  # 唯一标识
    patient = models.ForeignKey(
        User,  # 关联到患者用户
        on_delete=models.CASCADE,
        related_name='patient_orders',
        verbose_name='患者',
        limit_choices_to={'role': 'patient'}  # 限制只能关联角色为患者的用户
    )
    slot = models.ForeignKey(
        AppointmentSlot,
        on_delete=models.CASCADE,
        related_name='slot_orders',
        verbose_name='号源'
    )
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '挂号单'
        verbose_name_plural = '挂号单'
        db_table = 'registration_order'

    def __str__(self):
        return f"挂号单 {self.order_id} - {self.patient.real_name}"

    def save(self, *args, **kwargs):
        """重写 save 方法，处理剩余号量逻辑"""
        if not self.pk:  # 仅在创建时减少剩余号量
            if self.slot.remaining_quota <= 0:
                raise ValueError("号源已约满")
            self.slot.remaining_quota -= 1
            self.slot.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """删除时恢复剩余号量"""
        if self.status == 'pending':  # 仅处理未完成的订单
            self.slot.remaining_quota += 1
            self.slot.save()
        super().delete(*args, **kwargs)

class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name='医生',
        limit_choices_to={'role': 'doctor'}  # 只关联医生角色
    )
    biography = models.TextField(
        '医生简介',
        max_length=2000,
        blank=True,
        null=True,
        help_text='医生的专业背景、擅长领域等介绍'
    )
    department = models.CharField(
        '科室',
        max_length=100,
        blank=True,
        null=True,
        help_text='医生所属科室'
    )
    
    class Meta:
        verbose_name = '医生简介'
        verbose_name_plural = '医生简介'
        db_table = 'doctor_profile'
    
    def __str__(self):
        return f"{self.user.real_name}的简介"
