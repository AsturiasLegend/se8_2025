from django.db import models
from django.contrib.auth.hashers import make_password, check_password

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