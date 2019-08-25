## db_handler（数据处理模块，主要是用户存取数据，格式是json）

import os
import json
from confs import settings
import sys

def save_json(user_dic): #存数据，记得存的是字典，所有拼接名字的时候要把字典里面的用户名取出来
    user_path = os.path.join(settings.DB_PATH,
                             f'{user_dic.get("username")}.json') #拼接路径
    with open(user_path, 'w', encoding='utf8') as fw:
        json.dump(user_dic, fw) # 存进去，第一个参数是数据，第二个是文件，就是把第一个数据存到第二个文件中

def read_json(username):# 读数据， 拼路径，读出来数据就可以了，记得返回
    user_path = os.path.join(settings.DB_PATH, f'{username}.json')
    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf8') as fr:
            data = json.load(fr)
        return data
