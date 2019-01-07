# -*- encoding: utf-8 -*-
# @Time    : 2018-09-29 23:20
# @Author  : mike.liu
# @File    : forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from ApiTest.models import UserInfo


class RegForm(forms.Form):
    username = forms.CharField(
        # 校验规则相关
        max_length=32,
        label="用户名",
        error_messages={
            "required": "该字段不能为空!",
        },
        # widget 控制的是生成HTML代码相关的
        widget=widgets.TextInput(attrs={"class": "form-control"},)
    )

    password = forms.CharField(
        min_length=6,
        max_length=16,
        label="密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码不能少于6位!",
            "max_length": "密码长度不能大于16位!",
            "required": "该字段不能为空!",
        }
    )

    re_password = forms.CharField(
        min_length=6,
        max_length=16,
        label="确认密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码不能少于6位!",
            "max_length": "密码长度不能大于16位!",
            "required": "该字段不能为空!",
        }
    )

    email = forms.EmailField(
        label="邮箱地址",
        max_length=64,
        widget=widgets.EmailInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "该字段不能为空!",
            "invalid": "邮箱格式错误!",
        }
    )

    # 局部钩子
    def clean_username(self):
        value = self.cleaned_data.get("username")

        username = UserInfo.objects.filter(username=value).first()

        if not username:
            return value
        else:
            raise ValidationError("该用户已注册!")

    # 全局钩子
    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if password and re_password:
            if password == re_password:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致!")

        else:
            return self.cleaned_data
