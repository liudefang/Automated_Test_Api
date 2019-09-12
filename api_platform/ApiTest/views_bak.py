# -*- encoding: utf-8 -*-
# @Time    : 2019-09-12 09:45
# @Author  : mike.liu
# @File    : views_bak.py

import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.


from ApiTest.forms import RegForm
from ApiTest.models import Modules, Project, UserInfo, ApiInfo


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

def api_record(request):
    """
    登录后的首页
    :param request:
    :return:
    """

    return render(request, "api_record.html")

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
        prj_type = request.POST.get("type")
        prj_desc = request.POST.get("prj_desc")
        testers = request.POST.get("testers")
        developer = request.POST.get("developer")
        status = request.POST.get("status")
        version = request.POST.get("version")
        print("version:", version)
        print("type:", prj_type)
        print("status:", status)
        print("developer:", developer)

        if len(prj_name) != 0 and prj_name != str(Project.objects.filter(prj_name=prj_name).first()):
            if prj_type == '1':

                Project.objects.create(prj_name=prj_name, description=prj_desc, testers=testers, developer=developer,
                                       status=status, type='web', version=version)

            else:
                Project.objects.create(prj_name=prj_name, description=prj_desc, testers=testers, developer=developer,
                                       status=status, type='APP', version=version)

            response = {"status": 0, "msg": "项目添加成功!"}

            # return redirect("/project")
        elif len(prj_name) == 0:
            response = {"status": 1, "msg": "项目名称不能为空!"}
        else:
            response = {"status": 2, "msg": "项目名称已存在!"}

        return JsonResponse(response)

    return render(request, "project/index.html")


@login_required
def edit_project(request):
    """
    编辑项目
    :param request:
    :return:
    """


    if request.method == "POST":
        prj_id = request.POST.get("prj_id")
        prj_name = request.POST.get("prj_name")
        prj_type = request.POST.get("type")
        prj_desc = request.POST.get("prj_desc")
        testers = request.POST.get("testers")
        developer = request.POST.get("developer")
        status = request.POST.get("status")
        version = request.POST.get("version")

        if len(prj_name) != 0:
            if prj_type == '1':
                Project.objects.filter(id=prj_id).update(prj_name=prj_name, description=prj_desc, testers=testers,
                                                        developer=developer, status=status, type='web', version=version)
            else:
                Project.objects.filter(id=prj_id).update(prj_name=prj_name, description=prj_desc, testers=testers,
                                                        developer=developer, status=status, type='APP', version=version)

            response = {"status": 0, "msg": "编辑成功!"}

            # return redirect("/project")
        else:
            response = {"status": 1, "msg": "项目名称不能为空!"}

        return JsonResponse(response)

    edit_project_list = Project.objects.filter().all()

    return render(request, "project/index.html", {"edit_project_list": edit_project_list})


@login_required
def prj_det(request, prj_id):
    print("prj_id:", prj_id)
    project_list = Project.objects.filter(id=prj_id).first()
    if request.method == "GET":
        print("访问成功")

        return render(request, "modules/index.html", {"edit_project_list": project_list})

@login_required
def del_project(request, env_id):
    edit_project_list = Project.objects.filter(id=env_id).first()

    try:
        edit_project_list.delete()
        reg = {'status': 0, 'msg': '删除成功!'}
    except Exception as e:
        reg = {'status': 1, 'msg': '删除失败!'}

    return HttpResponse(json.dumps(reg))

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
    case_list = ApiInfo.objects.filter().all()

    return render(request, "api_case/index.html", {"case_list": case_list, "module_list": module_list, "project_list": project_list})


@login_required
def add_api_case(request):
    """
    新增用例
    :param request:
    :return:
    """

    if request.method == "POST":

        case_name = request.POST.get("case_name")
        case_desc = request.POST.get("case_desc")
        modules_id = request.POST.get("modules_id")
        url = request.POST.get("api")
        paras = request.POST.get("paras")
        status = request.POST.get("status")
        project_id = request.POST.get("project_id")

        if len(case_name) != 0 and case_name != str(Api.objects.filter(name=case_name).first()):
            Api.objects.create(name=case_name, description=case_desc, modules_id=modules_id,
                               url=url, paras=paras, status=status, project_id=project_id)

            response = {"status": 0, "msg": "用例添加成功!"}

        elif len(case_name) == 0:
            response = {"status": 1, "msg": "用例名称不能为空!"}
        else:
            response = {"status": 2, "msg": "用例名称已存在!"}

        return JsonResponse(response)

    return render(request, "api_case/index.html")