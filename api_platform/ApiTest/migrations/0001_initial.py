# Generated by Django 2.1.3 on 2019-01-11 01:26

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiStep',
            fields=[
                ('api_id', models.AutoField(primary_key=True, serialize=False)),
                ('step_name', models.CharField(max_length=64, verbose_name='步骤名称')),
                ('step_level', models.CharField(max_length=32, verbose_name='接口步骤优先级')),
                ('method', models.CharField(max_length=8, verbose_name='请求方式')),
                ('params', models.CharField(max_length=512, verbose_name='请求数据')),
                ('headers', models.CharField(max_length=512, verbose_name='请求头信息')),
                ('files', models.CharField(max_length=512)),
                ('step_desc', models.CharField(max_length=256, verbose_name='接口描述')),
                ('assert_response', models.CharField(max_length=512, verbose_name='接口预期结果')),
                ('api_dependency', models.CharField(default='', max_length=512, verbose_name='接口依赖')),
                ('step_weights', models.IntegerField(default=0, verbose_name='接口权重')),
                ('status', models.BooleanField()),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='ApiTestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_result', models.CharField(max_length=256, verbose_name='测试用例结果')),
                ('error_info', models.CharField(max_length=256, verbose_name='错误信息')),
                ('response_body', models.CharField(max_length=512, verbose_name='测试返回结果')),
                ('case_start_time', models.DateTimeField(auto_now=True, verbose_name='用例开始执行时间')),
                ('case_end_time', models.DateTimeField(auto_now=True, verbose_name='用例执行结束时间')),
                ('case_run_time', models.DateTimeField(verbose_name='用例执行时间')),
            ],
        ),
        migrations.CreateModel(
            name='CarryTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=56, verbose_name='任务名称')),
                ('html_report', models.CharField(default='', max_length=256)),
                ('success_log_name', models.CharField(default='', max_length=256)),
                ('error_log_name', models.CharField(default='', max_length=256)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_type', models.CharField(max_length=8, verbose_name='数据库类型')),
                ('db_typename', models.CharField(default='', max_length=32, verbose_name='数据库类型名称')),
                ('db_name', models.CharField(max_length=64, verbose_name='数据库名称')),
                ('db_ip', models.CharField(max_length=16, verbose_name='数据库ip地址')),
                ('db_port', models.CharField(max_length=8, verbose_name='数据库端口')),
                ('db_user', models.CharField(max_length=32, verbose_name='数据库用户名')),
                ('db_password', models.CharField(max_length=32, verbose_name='数据库密码')),
                ('db_remak', models.CharField(max_length=128, verbose_name='描述')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=32, verbose_name='邮件发送者')),
                ('receivers', models.CharField(max_length=128, verbose_name='邮件接收者')),
                ('host_dir', models.CharField(max_length=32, verbose_name='目录')),
                ('email_port', models.CharField(default='', max_length=32, verbose_name='邮箱端口')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('Headerfrom', models.CharField(max_length=32, verbose_name='邮件显示的发送者')),
                ('Headerto', models.CharField(max_length=128, verbose_name='邮件显示的接收者')),
                ('subject', models.CharField(default='', max_length=128, verbose_name='邮件主题')),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('env_id', models.AutoField(primary_key=True, serialize=False)),
                ('env_ip', models.CharField(max_length=32, verbose_name='数据库ip地址')),
                ('env_host', models.CharField(max_length=32, verbose_name='数据库域名')),
                ('env_port', models.CharField(max_length=8, verbose_name='数据库端口')),
                ('evn_name', models.CharField(max_length=64, verbose_name='测试环境名称')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='LogAndHtmlFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_step', models.CharField(max_length=128, verbose_name='测试步骤')),
                ('test_status', models.IntegerField(verbose_name='测试结果')),
                ('test_response', models.CharField(max_length=512, verbose_name='测试返回值')),
                ('test_carry_Task_id', models.CharField(default='', max_length=56, verbose_name='第几次执行')),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modules_name', models.CharField(max_length=32, verbose_name='模块名称')),
                ('testers', models.CharField(max_length=256, verbose_name='测试负责人')),
                ('devloper', models.CharField(max_length=256, verbose_name='开发负责人')),
                ('status', models.BooleanField()),
                ('modules_desc', models.CharField(max_length=256, verbose_name='模块描述')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('prj_id', models.AutoField(primary_key=True, serialize=False)),
                ('prj_name', models.CharField(max_length=64, verbose_name='项目名称')),
                ('prj_desc', models.CharField(max_length=256, verbose_name='项目描述')),
                ('testers', models.CharField(max_length=256, verbose_name='测试负责人')),
                ('developer', models.CharField(max_length=256, verbose_name='开发负责人')),
                ('status', models.BooleanField()),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '项目管理',
                'verbose_name_plural': '项目管理',
            },
        ),
        migrations.CreateModel(
            name='ReferenceStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_name', models.CharField(max_length=128, verbose_name='步骤名称')),
                ('path', models.CharField(default='', max_length=128, verbose_name='目录路径')),
                ('reference_step_name', models.CharField(max_length=128, verbose_name='步骤依赖名称')),
                ('variable', models.CharField(max_length=256, verbose_name='变量')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.ApiStep')),
            ],
        ),
        migrations.CreateModel(
            name='Sql',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sql_condition', models.IntegerField()),
                ('is_select', models.BooleanField(verbose_name='是否查询')),
                ('variable', models.CharField(max_length=256, verbose_name='变量')),
                ('sql', models.CharField(max_length=256, verbose_name='查询的sql语句')),
                ('remake', models.CharField(max_length=256, verbose_name='重置')),
                ('status', models.BooleanField(verbose_name='状态')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.ApiStep')),
            ],
        ),
        migrations.CreateModel(
            name='StatisticsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.IntegerField(verbose_name='测试用例总数')),
                ('task_number', models.IntegerField(verbose_name='测试任务总数')),
                ('carry_number', models.IntegerField(verbose_name='执行用例数')),
                ('pass_number', models.IntegerField(verbose_name='测试通过的用例数')),
                ('assert_error_number', models.IntegerField(verbose_name='不通过的用例数')),
                ('fail_number', models.IntegerField(verbose_name='失败用例数')),
                ('error_ratio', models.IntegerField(verbose_name='失败率')),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('case_id', models.AutoField(primary_key=True, serialize=False)),
                ('case_name', models.CharField(max_length=64, verbose_name='用例名称')),
                ('api', models.CharField(max_length=128, verbose_name='接口url地址')),
                ('status', models.BooleanField()),
                ('case_weights', models.CharField(max_length=32, verbose_name='用例优先级')),
                ('version', models.CharField(max_length=32, verbose_name='接口版本')),
                ('case_desc', models.CharField(max_length=256, verbose_name='用例描述')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('modules', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.Modules')),
            ],
        ),
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('plan_name', models.CharField(max_length=64, verbose_name='测试计划名称')),
                ('plan_run_time_regular', models.CharField(max_length=128, verbose_name='测试计划执行时间')),
                ('ip', models.CharField(default='', max_length=56, verbose_name='ip地址')),
                ('db', models.CharField(default='', max_length=56, verbose_name='数据库')),
                ('email', models.CharField(default='', max_length=56, verbose_name='邮箱地址')),
                ('fail_count', models.CharField(default='', max_length=56, verbose_name='错误统计')),
                ('remark', models.CharField(max_length=256, verbose_name='重置')),
                ('db_remark', models.CharField(default='', max_length=128, verbose_name='数据重置')),
                ('plan_desc', models.CharField(max_length=256, verbose_name='测试计划描述')),
                ('subject', models.CharField(default='', max_length=128, verbose_name='主题')),
                ('status', models.BooleanField(verbose_name='状态')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.TestCase')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('telephone', models.CharField(max_length=11, null=True, unique=True)),
                ('avatar', models.FileField(default='/avatars/default.png', upload_to='avatars/')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='modules',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.Project'),
        ),
        migrations.AddField(
            model_name='apitestresult',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.TestCase'),
        ),
        migrations.AddField(
            model_name='apitestresult',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.ApiStep'),
        ),
        migrations.AddField(
            model_name='apitestresult',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.TestPlan'),
        ),
        migrations.AddField(
            model_name='apistep',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiTest.TestCase'),
        ),
    ]
