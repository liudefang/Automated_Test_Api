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

    return render(request, "api_step/index.html", {"case_list": case_list, "api_list": api_list})


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
def edit_step(request, env_id, option):
    """
    编辑用例步骤
    :param request:
    :return:
    """

    edit_step_list = ApiStep.objects.filter(api_id=env_id).first()
    if edit_step_list and option == "delete":
        try:
            edit_step_list.delete()
            reg = {'status': 0, 'msg': '删除成功!'}
        except Exception as e:
            reg = {'status': 1, 'msg': '删除失败!'}

        return HttpResponse(json.dumps(reg))
    elif edit_step_list and option == "edit":

        if request.method == "POST":

            evn_name = request.POST.get("evn_name")
            evn_desc = request.POST.get("evn_desc")
            url = request.POST.get("url")
            project_id = request.POST.get("project_id")
            private_key = request.POST.get("private_key")

            if len(evn_name) != 0:

                Environment.objects.filter(env_id=env_id).update(evn_name=evn_name, evn_desc=evn_desc, url=url, project_id=project_id, private_key=private_key)

                response = {"status": 0, "msg": "编辑成功!"}

                # return redirect("/project")
            else:
                response = {"status": 1, "msg": "环境名称不能为空!"}

            return JsonResponse(response)

        api_list = ApiStep.objects.filter().all()

        return render(request, "api_step/edit.html", {"edit_step_list": edit_step_list, "api_list": api_list})
    else:
        return render(request, "not_found.html")


@login_required
def environment(request):
    """
    项目
    :param request:
    :return:
    """
    env_list = Environment.objects.filter().all()

    return render(request, "env/index.html", {"env_list": env_list})


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

    return render(request, "env/index.html")


@login_required
def edit_env(request, env_id, option):
    """
    编辑项目
    :param request:
    :return:
    """

    edit_env_list = Environment.objects.filter(env_id=env_id).first()
    if edit_env_list and option == "delete":
        try:
            edit_env_list.delete()
            reg = {'status': 0, 'msg': '删除成功!'}
        except Exception as e:
            reg = {'status': 1, 'msg': '删除失败!'}

        return HttpResponse(json.dumps(reg))
    elif edit_env_list and option == "edit":

        if request.method == "POST":

            evn_name = request.POST.get("evn_name")
            evn_desc = request.POST.get("evn_desc")
            url = request.POST.get("url")
            project_id = request.POST.get("project_id")
            private_key = request.POST.get("private_key")

            if len(evn_name) != 0:

                Environment.objects.filter(env_id=env_id).update(evn_name=evn_name, evn_desc=evn_desc, url=url, project_id=project_id, private_key=private_key)

                response = {"status": 0, "msg": "编辑成功!"}

                # return redirect("/project")
            else:
                response = {"status": 1, "msg": "环境名称不能为空!"}

            return JsonResponse(response)

        project_list = Project.objects.filter().all()

        return render(request, "env/edit.html", {"edit_env_list": edit_env_list, "project_list": project_list})
    else:
        return render(request, "not_found.html")




@login_required
def sign(request):
    """
    签名方式
    :param request:
    :return:
    """
    sign_list = Sign.objects.filter().all()

    return render(request, "system/sign.html", {"sign_list": sign_list})


@login_required
def add_sign(request):
    """
    新增签名方式
    :param request:
    :return:
    """
    if request.method == "POST":

        sign_name = request.POST.get("sign_name")
        description = request.POST.get("description")

        print("project_name:", sign_name)

        if len(sign_name) != 0 and sign_name != str(Sign.objects.filter(sign_name=sign_name).first()):

            Sign.objects.create(sign_name=sign_name, description=description)

            response = {"status": 0, "msg": "添加成功!"}

            # return redirect("/project")
        elif len(sign_name) == 0:
            response = {"status": 1, "msg": "签名方式名称不能为空!"}
        else:
            response = {"status": 2, "msg": "签名方式名称已存在!"}

        return JsonResponse(response)

    return render(request, "system/sign.html")