## settings.py（主要存一些常量，主要是功能界面，商品列表，日志路径，数据路径）

import os
import sys

########
#功能展示#
#########
FUNC_MSG = {
    '0': "注销",
    '1': "登录",
    '2': "注册",
    '3': "查看余额",
    '4': "转账",
    '5': "还款",
    '6': "取现",
    '7': "查看流水",
    '8': "购物",
    '9': "购物车",
}

SHOP_DIST = [
    ['饼干', 10],
    ['薯片', 10],
    ['火腿肠', 20],
    ['雪糕', 10],
    ['别墅', 1000000]
]
# LOG_PATH = os.path
ATM_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ATM_PATH, 'db')
