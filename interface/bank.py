## bank.py
from db import db_handler

def transfer_interface(from_username, to_username, money):# 转账接口，
    from_user_dic = db_handler.read_json(from_username) # 读当前用户数据
    to_user_dict = db_handler.read_json(to_username) # 读要转账用户数据
    my_money = from_user_dic['extra'] # 把用户的钱单独拿出来

    if money > my_money:
        return  '钱不够'

    else:
        from_user_dic['extra'] -= money # 我减钱
        to_user_dict['extra'] += money # 对方加钱
        msg_f = f'已向{to_username}转账{money}元' #记录我的信息
        msg_t = f'已收到{from_username}转账{money}元' #记录对方信息

        from_user_dic['bank_flow'].append(msg_f) #加我流水
        to_user_dict['bank_flow'].append(msg_t) #加对方流水

        db_handler.save_json(from_user_dic) #存数据
        db_handler.save_json(to_user_dict) #存数据
        return msg_f #返回操作信息
