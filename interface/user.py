## user.py（用户接口）
from db import db_handler
from confs import settings
import os

def register_interface(username, pwd): #注册接口
    #新生成的用户的信息字典
    user_dic = {
        'username': username,
        'pwd': pwd,
        'extra': 1500000,
        'bank_flow':[],
        'shop_car':{}
    }
    db_handler.save_json(user_dic) #保存数据
    return f'{username}注册成功'

def login_interface(username, pwd): #登录模块
    user_data = db_handler.read_json(username) # 拿数据

    if user_data['pwd'] == pwd:
        return True, '登录成功'
    else:
        return False, '密码输入错误'

def check_extra(username):# 查看余额接口
    user_data = db_handler.read_json(username) # 拿数据
    extra = user_data['extra']
    return f'{username}查看了余额，余额为{extra}元'
