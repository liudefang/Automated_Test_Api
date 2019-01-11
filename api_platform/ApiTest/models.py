from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# 测试环境信息
class Environment(models.Model):
    env_id = models.AutoField(primary_key=True, null=False)
    env_ip = models.CharField('数据库ip地址', max_length=32)     # 测试环境的ip地址
    env_host = models.CharField('数据库域名', max_length=32)     # 测试环境的域名地址
    env_port = models.CharField('数据库端口', max_length=8)
    evn_name = models.CharField('测试环境名称', max_length=64)    # 测试环境名称
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间


# 数据库表
class Database(models.Model):
    db_type = models.CharField('数据库类型', max_length=8)
    db_typename = models.CharField('数据库类型名称', max_length=32, default='')
    db_name = models.CharField('数据库名称', max_length=64)
    db_ip = models.CharField('数据库ip地址', max_length=16)
    db_port = models.CharField('数据库端口', max_length=8)
    db_user = models.CharField('数据库用户名', max_length=32)
    db_password = models.CharField('数据库密码', max_length=32)
    db_remak = models.CharField('描述', max_length=128)


# 邮件配置表
class Email(models.Model):
    sender = models.CharField('邮件发送者', max_length=32)
    receivers = models.CharField('邮件接收者', max_length=128)
    host_dir = models.CharField('目录', max_length=32)
    email_port = models.CharField('邮箱端口', max_length=32, default='')
    username = models.CharField('用户名', max_length=32)
    password = models.CharField('密码', max_length=32)
    Headerfrom = models.CharField('邮件显示的发送者', max_length=32)
    Headerto = models.CharField('邮件显示的接收者', max_length=128)
    subject = models.CharField('邮件主题', max_length=128, default='')


# 项目信息
class Project(models.Model):
    prj_id = models.AutoField(primary_key=True, null=False)
    prj_name = models.CharField('项目名称', max_length=64)  # 项目名称
    prj_desc = models.CharField('项目描述', max_length=256)  # 项目描述
    testers = models.CharField('测试负责人', max_length=256)  # 项目负责人
    developer = models.CharField('开发负责人', max_length=256)
    status = models.BooleanField()
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间

    class Meta:
        verbose_name = '项目管理'
        verbose_name_plural = '项目管理'

    def __str__(self):
        return self.prj_name


# 模块表
class Modules(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)      # 关联项目表id
    modules_name = models.CharField('模块名称', max_length=32)
    testers = models.CharField('测试负责人', max_length=256)  # 项目负责人
    devloper = models.CharField('开发负责人', max_length=256)
    status = models.BooleanField()
    modules_desc = models.CharField('模块描述', max_length=256)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间

    def __str__(self):
        return self.modules_name


# 测试用例表
class TestCase(models.Model):
    case_id = models.AutoField(primary_key=True, null=False)
    case_name = models.CharField('用例名称', max_length=64)
    api = models.CharField('接口url地址', max_length=128)
    status = models.BooleanField()
    case_weights = models.CharField('用例优先级', max_length=32)
    version = models.CharField('接口版本', max_length=32)
    modules = models.ForeignKey('Modules', on_delete=models.CASCADE)
    case_desc = models.CharField('用例描述', max_length=256)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.case_name


# 接口步骤表
class ApiStep(models.Model):
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    api_id = models.AutoField(primary_key=True, null=False)
    step_name = models.CharField('步骤名称', max_length=64)
    step_level = models.CharField('接口步骤优先级', max_length=32)
    method = models.CharField('请求方式', max_length=8)
    params = models.CharField('请求数据', max_length=512)
    headers = models.CharField('请求头信息', max_length=512)
    files = models.CharField(max_length=512)
    step_desc = models.CharField('接口描述', max_length=256)
    assert_response = models.CharField('接口预期结果', max_length=512)
    api_dependency = models.CharField('接口依赖', max_length=512, default="")
    step_weights = models.IntegerField('接口权重', default=0)
    status = models.BooleanField()
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.step_name


# 步骤依赖表
class ReferenceStep(models.Model):
    step = models.ForeignKey(ApiStep, on_delete=models.CASCADE)
    step_name = models.CharField('步骤名称', max_length=128)
    path = models.CharField('目录路径', max_length=128, default='')
    reference_step_name = models.CharField('步骤依赖名称', max_length=128)
    variable = models.CharField('变量', max_length=256)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.step


# sql表
class Sql(models.Model):
    step = models.ForeignKey(ApiStep, on_delete=models.CASCADE)
    sql_condition = models.IntegerField()
    is_select = models.BooleanField('是否查询')
    variable = models.CharField('变量', max_length=256)
    sql = models.CharField('查询的sql语句', max_length=256)
    remake = models.CharField('重置', max_length=256)
    status = models.BooleanField('状态')
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.sql


# 测试计划表
class TestPlan(models.Model):
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    plan_id = models.AutoField(primary_key=True, null=False)
    plan_name = models.CharField('测试计划名称', max_length=64)
    plan_run_time_regular = models.CharField('测试计划执行时间', max_length=128)
    ip = models.CharField('ip地址', max_length=56, default='')
    db = models.CharField('数据库', max_length=56, default='')
    email = models.CharField('邮箱地址', max_length=56, default='')
    fail_count = models.CharField('错误统计', max_length=56, default='')
    remark = models.CharField('重置', max_length=256)
    db_remark = models.CharField('数据重置', max_length=128, default='')
    plan_desc = models.CharField('测试计划描述', max_length=256)
    subject = models.CharField('主题', max_length=128, default='')
    status = models.BooleanField('状态')
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.plan_name


# 测试结果表
class ApiTestResult(models.Model):
    task = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    step = models.ForeignKey(ApiStep, on_delete=models.CASCADE)
    case_result = models.CharField('测试用例结果', max_length=256)
    error_info = models.CharField('错误信息', max_length=256)
    response_body = models.CharField('测试返回结果', max_length=512)
    case_start_time = models.DateTimeField('用例开始执行时间', auto_now=True)
    case_end_time = models.DateTimeField('用例执行结束时间', auto_now=True)
    case_run_time = models.DateTimeField('用例执行时间')

    def __str__(self):
        return self.case_result


# 统计分析总表
# 任务表
class StatisticsData(models.Model):
    case_number = models.IntegerField('测试用例总数')
    task_number = models.IntegerField('测试任务总数')
    carry_number = models.IntegerField('执行用例数')
    pass_number = models.IntegerField('测试通过的用例数')
    assert_error_number = models.IntegerField('不通过的用例数')
    fail_number = models.IntegerField('失败用例数')
    error_ratio = models.IntegerField('失败率')

    def __str__(self):
        return self.casenumber


# 邮件和日志的反馈
class LogAndHtmlFeedback(models.Model):
    test_step = models.CharField('测试步骤', max_length=128)
    test_status = models.IntegerField('测试结果')
    test_response = models.CharField('测试返回值', max_length=512)
    test_carry_Task_id = models.CharField('第几次执行', max_length=56, default="")
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)


# 第几次执行任务
class CarryTask(models.Model):
    task_name = models.CharField('任务名称', max_length=56)
    html_report = models.CharField(max_length=256, default="")
    success_log_name = models.CharField(max_length=256, default="")
    error_log_name = models.CharField(max_length=256, default="")
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


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










