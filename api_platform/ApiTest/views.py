from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from ApiTest.forms import RegForm
from ApiTest.models import Project, UserInfo, Sign


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
    sign_list = Sign.objects.filter().all()

    return render(request, "project/index.html", {"project_list": project_list, "sign_list": sign_list})


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
        sign_id = request.POST.get("sign_id")

        print("sign_id:", sign_id)

        if len(prj_name) != 0 and prj_name != str(Project.objects.filter(prj_name=prj_name).first()):

            Project.objects.create(prj_name=prj_name, prj_desc=prj_desc, testers=testers, sign_id=sign_id)

            response = {"status": 0, "msg": "添加成功!"}

            # return redirect("/project")
        elif len(prj_name) == 0:
            response = {"status": 1, "msg": "项目名称不能为空!"}
        else:
            response = {"status": 2, "msg": "项目名称已存在!"}

        return JsonResponse(response)

    return render(request, "project/index.html")


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