# -*-codeing = utf-8 -*-
# @Time : 2022-04-03 13:34
# @Author : 齐物逍遥游
# @File : decorators.py
# @Software : PyCharm
from flask import g,redirect,url_for
from functools import wraps


def login_required(func):
    #@wraps这个装饰器一定不要忘记写
    @wraps(func)
    def wrapper(*args,**kwargs):
        if hasattr(g,'user'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("user.login"))

    return wrapper