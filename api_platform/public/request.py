# -*- encoding: utf-8 -*-
# @Time    : 2019/1/29 19:42
# @Author  : mike.liu
# @File    : request.py
import requests
import json


class Http:
    def __init__(self, model):
        self.model = model

    def __request(self, **kwargs):
        try:
            if self.model.lower() == "get":
                response = requests.request("get", kwargs["url"], params=kwargs["params"], headers=kwargs["headers"])
                # post的参数名要为data
            elif self.model.lower() == "post_body":
                # 转换成字符串传入
                params = json.dumps(kwargs["params"], ensure_ascii=False)
                response = requests.request("post", kwargs["url"], data=params, headers=kwargs["headers"])
            elif self.model.lower() == "post_form":
                response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"])
            elif self.model.lower == "post_file":
                response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"], files=kwargs["files"])
            return response
        except BaseException as e:
            print("error{0}".format(str(e)))

    # 文本转换成json字符串
    def __change_Json(self, response):
        response_json = json.loads(requests.text)
        return response_json

    def __call__(self, fuc):
        def wrapper(*args, **kwargs):
            fuc(*args, **kwargs)
            response = self.__request(**kwargs)
            response_json = self.__change_Json(response)
            return response_json
        return wrapper


@Http(model="GET")
def get(url, params, headers):
    pass


@Http(model="POST_FORM")
def post_form(url, params, headers):
    pass


@Http(model="POST_BODY")
def post_body(url, params, headers):
    pass


@Http(model="POST_FILE")
def post_file(url, params, headers):
    pass
