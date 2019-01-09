from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# 签名信息
class Sign(models.Model):
    sign_id = models.AutoField(primary_key=True, null=False)
    sign_name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.sign_name


# 项目信息
class Project(models.Model):
    prj_id = models.AutoField(primary_key=True, null=False)
    prj_name = models.CharField('项目名称', max_length=64)  # 项目名称
    prj_desc = models.CharField('项目描述', max_length=256)  # 项目描述
    testers = models.CharField('测试负责人', max_length=256)  # 项目负责人
    sign = models.ForeignKey('Sign', on_delete=models.CASCADE)  # 签名信息
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间

    class Meta:
        verbose_name = '项目管理'
        verbose_name_plural = '项目管理'

    def __str__(self):
        return self.prj_name


# 测试环境信息
class Environment(models.Model):
    env_id = models.AutoField(primary_key=True, null=False)
    evn_name = models.CharField('测试环境名称', max_length=64)    # 测试环境名称
    project = models.ForeignKey('Project', on_delete=models.CASCADE)    # 关联项目id
    evn_desc = models.CharField('测试环境描述', max_length=128)   # 测试环境描述
    url = models.CharField('项目URL地址', max_length=256)   # 测试环境的URL地址
    private_key = models.CharField('签名值', max_length=64)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间


# 接口步骤表
class ApiStep(models.Model):
    api_id = models.AutoField(primary_key=True, null=False)
    api_name = models.CharField('接口名称', max_length=64)
    url = models.CharField('接口URL地址', max_length=256)
    method = models.CharField('请求方式', max_length=8)
    data_type = models.CharField('数据类型', max_length=8)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    is_sign = models.IntegerField('是否签名')
    api_desc = models.CharField('接口描述', max_length=256)
    request_header_param = models.TextField('请求头信息')
    request_body_param = models.TextField('请求体内容信息')
    response_header_param = models.TextField('返回头信息')
    response_body_param = models.TextField('返回体内容信息')
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间

    def __str__(self):
        return self.api_name


# 测试用例表
class TestCase(models.Model):
    case_id = models.AutoField(primary_key=True, null=False)
    case_name = models.CharField('用例名称', max_length=64)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    case_desc = models.CharField('用例描述', max_length=256)
    content = models.TextField('用例内容')
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间

    def __str__(self):
        return self.case_name


# 测试计划表
class TestPlan(models.Model):
    plan_id = models.AutoField(primary_key=True, null=False)
    plan_name = models.CharField('测试计划名称', max_length=64)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    environment = models.ForeignKey('Environment', on_delete=models.CASCADE)
    plan_desc = models.CharField('测试计划描述', max_length=256)
    content = models.TextField()
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间

    def __str__(self):
        return self.plan_name


# 测试报告表
class TestReport(models.Model):
    report_id = models.AutoField(primary_key=True, null=False)
    report_name = models.CharField('测试报告名称', max_length=256)
    plan = models.ForeignKey('TestPlan', on_delete=models.CASCADE)
    content = models.TextField()
    case_num = models.IntegerField(null=True)
    pass_num = models.IntegerField(null=True)
    fail_num = models.IntegerField(null=True)
    error_num = models.IntegerField(null=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间

    def __str__(self):
        return self.report_name


class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default="/avatars/default.png")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.username










