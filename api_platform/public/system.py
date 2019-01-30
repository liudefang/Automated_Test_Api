# -*- encoding: utf-8 -*-
# @Time    : 2019-01-30 09:08
# @Author  : mike.liu
# @File    : system.py

import os
import shutil


# 判断一个文件夹是否存在，不存在就创建
def create_dir(dir):
    is_exist = os.path.isdir(dir)
    if not is_exist:
        os.mkdir(dir)
    else:
        pass


# 判断是否存在一个文件，如果存在先删除
def rm_file(name):
    if os.path.exists(name):
        os.remove(name)


# 创建一个文件
def create_file(file_name):
    with open(file_name, "w") as fp:
        fp.close()