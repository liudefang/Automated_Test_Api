import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from ApiTest.forms import RegForm
from ApiTest.models import *


def index(request):
    """
    系统首页
    :param request:
    :return:
    """

    return render(request, "index.html")


# 注册
def register(request):
    if request.is_ajax():
        print(request.POST)
        form = RegForm(request.POST)

        response = {"username": None, "msg": None}
        if form.is_valid():
            response["username"] = form.cleaned_data.get("username")

            # 生成一条用户数据
            username = form.cleaned_data.get("username")
            print("username", username)
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")

            UserInfo.objects.create_user(username=username, password=password, email=email)


        else:
            print(form.cleaned_data)
            print(form.errors)
            response["msg"] = form.errors

        return JsonResponse(response)

    form = RegForm()
    return render(request, "register.html", {"form": form})


# 登录
def login(request):
    """
    登录视图函数：
        get请求相应页面
        post(Ajax)请求相应字典
    :param request:
    :return:
    """
    if request.method == "POST":

        response = {"username": None, "msg": None}
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            response["username"] = user.username

        else:
            response["msg"] = "用户名或者密码错误!"

        return JsonResponse(response)

    return render(request, "login.html")



def logout(request):
    """
    退出系统
    :param request:
    :return:
    """
    auth.logout(request)

    return redirect("/login/")


@login_required
def home(request):
    """
    登录后的首页
    :param request:
    :return:
    """

    return render(request, "base.html")


@login_required
def project(request):
    """
    项目
    :param request:
    :return:
    """
    project_list = Project.objects.filter().all()

    return render(request, "project/index.html", {"project_list": project_list})


@login_required
def add_project(request):
    """
    新增项目
    :param request:
    :return:
    """

    if request.method == "POST":

        prj_name = request.POST.get("prj_name")
        prj_desc = request.POST.get("prj_desc")
        testers = request.POST.get("testers")
        developer = request.POST.get("developer")
        status = request.POST.get("status")

        print("status:", type(status))

        if len(prj_name) != 0 and prj_name != str(Project.objects.filter(prj_name=prj_name).first()):
            if status == '1':

                Project.objects.create(prj_name=prj_name, prj_desc=prj_desc, testers=testers, developer=developer,
                                       status=1)
            else:
                Project.objects.create(prj_name=prj_name, prj_desc=prj_desc, testers=testers, developer=developer,
                                       status=0)

            response = {"status": 0, "msg": "项目添加成功!"}

            # return redirect("/project")
        elif len(prj_name) == 0:
            response = {"status": 1, "msg": "项目名称不能为空!"}
        else:
            response = {"status": 2, "msg": "项目名称已存在!"}

        return JsonResponse(response)

    return render(request, "project/index.html")


@login_required
def edit_project(request, prj_id, option):
    """
    编辑项目
    :param request:
    :return:
    """
    print("prj_id:", prj_id)
    edit_project_list = Project.objects.filter(prj_id=prj_id).first()
    if edit_project_list and option == "delete":
        try:
            edit_project_list.delete()
            reg = {'status': 0, 'msg': '删除成功!'}
        except Exception as e:
            reg = {'status': 1, 'msg': '删除失败!'}

        return HttpResponse(json.dumps(reg))
    elif edit_project_list and option == "edit":

        if request.method == "POST":

            prj_name = request.POST.get("prj_name")
            prj_desc = request.POST.get("prj_desc")
            testers = request.POST.get("testers")
            developer = request.POST.get("developer")
            status = request.POST.get("status")

            print("status:", status)

            print(len(prj_name))

            if len(prj_name) != 0:

                Project.objects.filter(prj_id=prj_id).update(prj_name=prj_name, prj_desc=prj_desc, testers=testers,
                                                             developer=developer, status=status)

                response = {"status": 0, "msg": "编辑成功!"}

                # return redirect("/project")
            else:
                response = {"status": 1, "msg": "项目名称不能为空!"}

            return JsonResponse(response)

        return render(request, "project/edit.html", {"edit_project_list": edit_project_list})
    else:
        return render(request, "not_found.html")


@login_required
def module(request):
    """
    模块
    :param request:
    :return:
    """
    module_list = Modules.objects.filter().all()
    project_list = Project.objects.filter().all()

    return render(request, "modules/index.html", {"module_list": module_list, "project_list": project_list})


@login_required
def add_module(request):
    """
    新增模块
    :param request:
    :return:
    """

    if request.method == "POST":

        modules_name = request.POST.get("modules_name")
        modules_desc = request.POST.get("modules_desc")
        project_id = request.POST.get("project_id")
        testers = request.POST.get("testers")
        developer = request.POST.get("developer")
        status = request.POST.get("status")

        if len(modules_name) != 0 and modules_name != str(Modules.objects.filter(modules_name=modules_name).first()):
            Modules.objects.create(modules_name=modules_name, modules_desc=modules_desc, project_id=project_id,
                                   developer=developer, testers=testers, status=status)

            response = {"status": 0, "msg": "模块添加成功!"}

        elif len(modules_name) == 0:
            response = {"status": 1, "msg": "模块名称不能为空!"}
        else:
            response = {"status": 2, "msg": "模块名称已存在!"}

        return JsonResponse(response)

    return render(request, "modules/index.html")


@login_required
def edit_module(request, mod_id, option):
    """
    编辑模块
    :param request:
    :return:
    """
    print("prj_id:", mod_id)
    edit_module_list = Modules.objects.filter(id=mod_id).first()
    if edit_module_list and option == "delete":
        try:
            edit_module_list.delete()
            reg = {'status': 0, 'msg': '删除成功!'}
        except Exception as e:
            reg = {'status': 1, 'msg': '删除失败!'}

        return HttpResponse(json.dumps(reg))
    elif edit_module_list and option == "edit":

        if request.method == "POST":

            modules_name = request.POST.get("modules_name")
            modules_desc = request.POST.get("modules_desc")
            project_id = request.POST.get("project_id")
            testers = request.POST.get("testers")
            developer = request.POST.get("developer")
            status = request.POST.get("status")

            if len(modules_name) != 0:

                Modules.objects.filter(id=mod_id).update(modules_name=modules_name, modules_desc=modules_desc, testers=testers,
                                                         developer=developer, project_id=project_id, status=status)

                response = {"status": 0, "msg": "编辑成功!"}

            else:
                response = {"status": 1, "msg": "模块名称不能为空!"}

            return JsonResponse(response)
        project_list = Project.objects.filter().all()
        return render(request, "modules/edit.html", {"edit_module_list": edit_module_list, "project_list": project_list})
    else:
        return render(request, "not_found.html")


@login_required
def api_case(request):
    """
    接口用例
    :param request:
    :return:
    """
    module_list = Modules.objects.filter().all()
    project_list = Project.objects.filter().all()
    case_list = TestCase.objects.filter().all()

    return render(request, "api_case/index.html", {"case_list": case_list, "module_list": module_list, "project_list": project_list})


@login_required
def add_case(request):
    """
    新增用例
    :param request:
    :return:
    """

    if request.method == "POST":

        case_name = request.POST.get("case_name")
        case_desc = request.POST.get("case_desc")
        modules_id = request.POST.get("modules_id")
        api = request.POST.get("api")
        version = request.POST.get("version")
        status = request.POST.get("status")
        project_id = request.POST.get("project_id")

        if len(case_name) != 0 and case_name != str(TestCase.objects.filter(case_name=case_name).first()):
            TestCase.objects.create(case_name=case_name, case_desc=case_desc, modules_id=modules_id,
                                    api=api, version=version, status=status, project_id=project_id)

            response = {"status": 0, "msg": "用例添加成功!"}

        elif len(case_name) == 0:
            response = {"status": 1, "msg": "用例名称不能为空!"}
        else:
            response = {"status": 2, "msg": "用例名称已存在!"}

        return JsonResponse(response)

    return render(request, "api_case/index.html")


@login_required
def edit_case(request, case_id, option):
    """
    编辑用例
    :param request:
    :return:
    """
    print("prj_id:", case_id)
    edit_case_list = TestCase.objects.filter(case_id=case_id).first()
    if edit_case_list and option == "delete":
        try:
            edit_case_list.delete()
            reg = {'status': 0, 'msg': '删除成功!'}
        except Exception as e:
            reg = {'status': 1, 'msg': '删除失败!'}

        return HttpResponse(json.dumps(reg))
    elif edit_case_list and option == "edit":

        if request.method == "POST":

            case_name = request.POST.get("case_name")
            case_desc = request.POST.get("case_desc")
            modules_id = request.POST.get("modules_id")
            api = request.POST.get("api")
            version = request.POST.get("version")
            status = request.POST.get("status")
            project_id = request.POST.get("project_id")

            if len(case_name) != 0:

                TestCase.objects.filter(case_id=case_id).update(case_name=case_name, case_desc=case_desc,
                                                                modules_id=modules_id, api=api, version=version,
                                                                status=status, project_id=project_id)

                response = {"status": 0, "msg": "编辑成功!"}

            else:
                response = {"status": 1, "msg": "用例名称不能为空!"}

            return JsonResponse(response)
        project_list = Project.objects.filter().all()
        module_list = Modules.objects.filter().all()

        return render(request, "api_case/edit.html", {"edit_case_list": edit_case_list, "project_list": project_list,
                                                      "module_list": module_list})
    else:
        return render(request, "not_found.html")


@login_required
def api_step(request):
    """
    项目
    :param request:
    :return:
    """
    api_list = ApiStep.objects.filter().all()
    case_list = TestCase.objects.filter().all()

    return render(request, "api_step/step.html", {"case_list": case_list, "api_list": api_list})


@login_required
def add_step(request):
    """
    新增用例步骤
    :param request:
    :return:
    """
    if request.method == "POST":

        step_name = request.POST.get('step_name')
        case_id = request.POST.get('case_id')
        method = request.POST.get('method')
        headers = request.POST.get('headers')
        params = request.POST.get('params')
        assert_response = request.POST.get('assert_response')
        api_dependency = request.POST.get('dependency')
        step_level = request.POST.get('step_level')
        step_desc = request.POST.get('step_desc')

        params_body = request.POST.get('params_body')
        status = request.POST.get("status")
        print("case_id:", case_id)
        print("params:", params)
        if len(step_name) != 0 and step_name != str(ApiStep.objects.filter(step_name=step_name).first()):
            if method == "get" or method == "post_form":
                ApiStep.objects.create(case_id=case_id, step_name=step_name, step_level=step_level, method=method,
                                       params=params, headers=headers, assert_response=assert_response,
                                       step_desc=step_desc, api_dependency=api_dependency, status=status)
            elif method == "post_body":
                ApiStep.objects.create(case_id=case_id, step_name=step_name, step_level=step_level, method=method,
                                       params=params_body, headers=headers, assert_response=assert_response,
                                       step_desc=step_desc, api_dependency=api_dependency, status=status)

            response = {"status": 0, "msg": "测试接口添加成功!"}

        elif len(step_name) == 0:
            response = {"status": 1, "msg": "接口名称不能为空!"}
        else:
            response = {"status": 2, "msg": "接口名称已存在!"}

        return JsonResponse(response)

    return render(request, "api_step/index.html")


@login_required
def edit_step(request):
    """
    编辑用例步骤
    :param request:
    :return:
    """

    if request.method == "POST":
        step_id = request.POST.get("step_id")
        step_name = request.POST.get('step_name')
        case_name = request.POST.get('case_name')
        method = request.POST.get('method')
        headers = request.POST.get('headers')
        params = request.POST.get('params')
        assert_response = request.POST.get('assert_response')
        api_dependency = request.POST.get('dependency')
        step_level = request.POST.get('step_level')
        step_desc = request.POST.get('step_desc')

        params_body = request.POST.get('params_body')
        status = request.POST.get("status")
        print("case_name:", case_name)
        print("params:", params)
        print("step_id:", step_id)
        case_id = TestCase.objects.get(case_name=case_name)
        print("case_id:", case_id)
        if len(step_name) != 0:
            if method == "get" or method == "post_form":
                ApiStep.objects.filter(api_id=step_id).update(case_id=case_id, step_name=step_name, step_level=step_level,
                                                              method=method,params=params, headers=headers, assert_response=assert_response,
                                                              step_desc=step_desc, api_dependency=api_dependency, status=status)
            elif method == "post_body":
                ApiStep.objects.filter(api_id=step_id).update(case_id=case_id, step_name=step_name, step_level=step_level, method=method,
                                                              params=params_body, headers=headers, assert_response=assert_response,
                                                              step_desc=step_desc, api_dependency=api_dependency, status=status)

            response = {"status": 0, "msg": "编辑成功!"}

            # return redirect("/project")
        else:
            response = {"status": 1, "msg": "用例步骤名称不能为空!"}

        return JsonResponse(response)

    case_list = TestCase.objects.filter().all()

    return render(request, "api_step/step.html", {"case_list": case_list})


@login_required
def del_step(request, env_id):
    edit_step_list = ApiStep.objects.filter(api_id=env_id).first()

    try:
        edit_step_list.delete()
        reg = {'status': 0, 'msg': '删除成功!'}
    except Exception as e:
        reg = {'status': 1, 'msg': '删除失败!'}

    return HttpResponse(json.dumps(reg))



@login_required
def environment(request):
    """
    项目
    :param request:
    :return:
    """
    env_list = Environment.objects.filter().all()

    return render(request, "plan/index.html", {"env_list": env_list})


@login_required
def add_env(request):
    """
    新增项目
    :param request:
    :return:
    """

    if request.method == "POST":

        env_ip = request.POST.get("env_ip")
        evn_name = request.POST.get("evn_name")
        env_port = request.POST.get("env_port")
        env_host = request.POST.get("env_host")

        if len(evn_name) != 0 and evn_name != str(Environment.objects.filter(evn_name=evn_name).first()):

            Environment.objects.create(evn_name=evn_name, env_ip=env_ip, env_port=env_port, env_host=env_host)

            response = {"status": 0, "msg": "测试环境添加成功!"}

            # return redirect("/project")
        elif len(evn_name) == 0:
            response = {"status": 1, "msg": "环境名称不能为空!"}
        else:
            response = {"status": 2, "msg": "环境名称已存在!"}

        return JsonResponse(response)

    return render(request, "plan/index.html")


@login_required
def edit_env(request):
    """
    编辑项目
    :param request:
    :return:
    """

    if request.method == "POST":
        env_id = request.POST.get("env_id")
        env_ip = request.POST.get("env_ip")
        evn_name = request.POST.get("evn_name")
        env_port = request.POST.get("env_port")
        env_host = request.POST.get("env_host")

        if len(evn_name) != 0:

            Environment.objects.filter(env_id=env_id).update(evn_name=evn_name, env_host=env_host, env_ip=env_ip, env_port=env_port)

            response = {"status": 0, "msg": "编辑成功!"}

            # return redirect("/project")
        else:
            response = {"status": 1, "msg": "环境名称不能为空!"}

        return JsonResponse(response)

    edit_env_list = Environment.objects.filter().all()

    return render(request, "system/plan.html", {"edit_env_list": edit_env_list})


# 删除测试环境配置
def del_env(request, env_id):

    edit_env_list = Environment.objects.filter(env_id=env_id).first()

    try:
        edit_env_list.delete()
        reg = {'status': 0, 'msg': '删除成功!'}
    except Exception as e:
        reg = {'status': 1, 'msg': '删除失败!'}
    return HttpResponse(json.dumps(reg))


@login_required
def email(request):
    """
    签名方式
    :param request:
    :return:
    """
    email_list = Email.objects.filter().all()

    return render(request, "system/email.html", {"email_list": email_list})


@login_required
def add_email(request):
    """
    新增签名方式
    :param request:
    :return:
    """
    if request.method == "POST":

        sender = request.POST.get("sender")
        receivers = request.POST.get("receivers")
        host_dir = request.POST.get("host_dir")
        email_port = request.POST.get("email_port")
        username = request.POST.get("username")
        password = request.POST.get("password")
        header_from = request.POST.get("Header_from")
        header_to = request.POST.get("Header_to")
        subject = request.POST.get("subject")

        print("project_name:", sender)

        if len(sender) != 0 and len(receivers) != 0 and len(host_dir) != 0 and len(email_port) != 0 and \
                len(username) != 0 and len(password) != 0 and len(header_from) != 0 and len(header_to) != 0 and len(subject) != 0:

            Email.objects.create(sender=sender, receivers=receivers, host_dir=host_dir, email_port=email_port, username=username,
                                 password=password, Headerfrom=header_from, Headerto=header_to, subject=subject)

            response = {"status": 0, "msg": "添加成功!"}

            # return redirect("/project")

        else:
            response = {"status": 1, "msg": "请填写必填信息!"}

        return JsonResponse(response)

    return render(request, "system/email.html")


@login_required
def edit_email(request):
    """
    新增签名方式
    :param request:
    :return:
    """
    if request.method == "POST":
        email_id = request.POST.get("id")
        sender = request.POST.get("sender")
        receivers = request.POST.get("receivers")
        host_dir = request.POST.get("host_dir")
        email_port = request.POST.get("email_port")
        username = request.POST.get("username")
        password = request.POST.get("password")
        header_from = request.POST.get("Header_from")
        header_to = request.POST.get("Header_to")
        subject = request.POST.get("subject")

        print("project_name:", sender)

        if len(sender) != 0 and len(receivers) != 0 and len(host_dir) != 0 and len(email_port) != 0 and \
                len(username) != 0 and len(password) != 0 and len(header_from) != 0 and len(header_to) != 0 and len(subject) != 0:

            Email.objects.filter(id=email_id).update(sender=sender, receivers=receivers, host_dir=host_dir,
                                                     email_port=email_port, username=username,password=password,
                                                     Headerfrom=header_from, Headerto=header_to, subject=subject)

            response = {"status": 0, "msg": "编辑成功!"}

            # return redirect("/project")

        else:
            response = {"status": 1, "msg": "请填写必填信息!"}

        return JsonResponse(response)

    return render(request, "system/email.html")


# 删除邮箱地址信息
def del_email(request, env_id):

    edit_email_list = Email.objects.filter(id=env_id).first()

    try:
        edit_email_list.delete()
        reg = {'status': 0, 'msg': '删除成功!'}
    except Exception as e:
        reg = {'status': 1, 'msg': '删除失败!'}
    return HttpResponse(json.dumps(reg))


@login_required
def database(request):
    """
    签名方式
    :param request:
    :return:
    """
    db_list = Database.objects.filter().all()

    return render(request, "system/db.html", {"db_list": db_list})


@login_required
def add_db(request):
    """
    新增签名方式
    :param request:
    :return:
    """
    if request.method == "POST":

        db_type = request.POST.get("db_type")
        db_name = request.POST.get("db_name")
        db_ip = request.POST.get("db_ip")
        db_port = request.POST.get("db_port")
        db_user = request.POST.get("db_user")
        db_password = request.POST.get("db_password")
        db_remak = request.POST.get("db_remak")

        print("db_name:", db_name)

        if len(db_type) != 0 and len(db_name) != 0 and len(db_ip) != 0 and len(db_port) != 0 and \
                len(db_user) != 0 and len(db_password) :

            Database.objects.create(db_type=db_type, db_name=db_name, db_ip=db_ip, db_port=db_port, db_user=db_user,
                                    db_password=db_password, db_remak=db_remak)

            response = {"status": 0, "msg": "添加成功!"}

            # return redirect("/project")

        else:
            response = {"status": 1, "msg": "请填写必填信息!"}

        return JsonResponse(response)

    return render(request, "system/email.html")


@login_required
def edit_db(request):
    """
    新增签名方式
    :param request:
    :return:
    """
    if request.method == "POST":
        id = request.POST.get("id")
        db_type = request.POST.get("db_type")
        db_name = request.POST.get("db_name")
        db_ip = request.POST.get("db_ip")
        db_port = request.POST.get("db_port")
        db_user = request.POST.get("db_user")
        db_password = request.POST.get("db_password")
        db_remak = request.POST.get("db_remak")

        if len(db_type) != 0 and len(db_name) != 0 and len(db_ip) != 0 and len(db_port) != 0 and \
                len(db_user) != 0 and len(db_password) :

            Database.objects.filter(id=id).update(db_type=db_type, db_name=db_name, db_ip=db_ip, db_port=db_port,
                                                  db_user=db_user,db_password=db_password, db_remak=db_remak)

            response = {"status": 0, "msg": "编辑成功!"}

            # return redirect("/project")

        else:
            response = {"status": 1, "msg": "请填写必填信息!"}

        return JsonResponse(response)

    return render(request, "system/db.html")


# 删除邮箱地址信息
def del_db(request, env_id):

    edit_db_list = Database.objects.filter(id=env_id).first()

    try:
        edit_db_list.delete()
        reg = {'status': 0, 'msg': '删除成功!'}
    except Exception as e:
        reg = {'status': 1, 'msg': '删除失败!'}
    return HttpResponse(json.dumps(reg))