## common.py（通用模块）
import logging
import os
from db import db_handler
from confs import settings
import logging.config



def input_username_pwd():# 用户输入的模块
    username = input('请输入用户名>>>>').strip()
    pwd = input("请输入密码>>>>").strip()

    return username, pwd

def check_user(username): # 检查用户是否存在模块
    user_path = os.path.join(settings.DB_PATH, f'{username}.json') #拼接用户路径，判断是否有该路径
    if os.path.exists(user_path):
        return True
    else:
        return False


def login_auth(func):  # 装饰函数，用于验证是否登录，套用装饰函数模板
    from core import src  
    def inner(*args, **kwargs):
        if src.user_info.get('user'):  
            res = func(*args, **kwargs)
            return res
        else:
            print('未登录,请去登录!')
            src.login()

    return inner
