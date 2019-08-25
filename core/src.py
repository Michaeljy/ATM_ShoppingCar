## src.py（主界面，主要是和用户交互的界面）
from libs import common 
from db import db_handler
from interface import user
from interface import bank
from confs import settings



#设置一个字典类型的全局变量，用于判断是否登录
user_info = {
    'user': None
} 



# 注销功能
def logout():
    user_info['user'] = None   # 将values值设置为空
    print('注销成功')

# 登录模块
def login():
    count = 0 #计数，连续三次注册失败，退出功能
    print("欢迎来到登录功能")
    while True:
        username, pwd = common.input_username_pwd() # 调用输入接口，接收输入信息
        flag = common.check_user(username) # 调用核对用户接口，验证用户是否已经存在
        if not flag:
            print('未注册')
            break
        flag, msg = user.login_interface(username, pwd)
        if flag:
            user_info['user'] = username #登录成功，赋值
            print(user_info['user'])
            print(msg)
            break
        else:
            print(msg)
            count += 1
        if count == 3:
            break

#注册模块
def register():
    print("欢迎来到注册模块")

    username, pwd = common.input_username_pwd()
    flag = common.check_user(username) #先判断是否存在
    if flag:
        print("无需注册，用户已经存在")
    else:
        msg = user.register_interface(username, pwd) # 调用注册接口
        print(msg)

@common.login_auth   # 加语法糖，查看余额前先登录
def check_extra():
    print("欢迎来到查看余额模块")
    msg = user.check_extra(user_info.get('user'))  # 调用查看余额接口
    print(msg)

# 转账，需要有发起人，接收人和钱
@common.login_auth
def transfer():
    print("欢迎来到转账模块")

    while True:
        from_username = user_info.get('user')
        to_username = input('请输入你要转账的用户名：')
        flag = common.check_user(to_username) #先判断用户是否存在
        if flag:
            money = input("请输入你要转账的金额").strip()
            if not money.isdigit():
                print("请输入数字")
                continue
            money = int(money)
            msg = bank.transfer_interface(from_username, to_username, money) #调用转账接口
            print(msg)
            break
        print("用户不存在")

@common.login_auth
#还款模块
def repay():
    print("欢迎来到还款模块")

    msg = bank.repay_interface(user_info['user']) #调用还款接口
    print(msg)

@common.login_auth
#取现功能
def withdraw(): 
    print("欢迎来到取现功能")
    while True:
        money = input("请输入取现金额：")
        if not money.isdigit():
            print("输入必须是数字")
            continue
        else:
            money = int(money)
            msg = bank.withdraw_interface(user_info['user'], money)#调用取现模块
            print(msg)
            break
@common.login_auth
#查看流水模块
def history():
    print("欢迎来到查看流水模块")

    msg = bank.bank_flow_interface(user_info['user'])#调用查看流水模块
    print(msg)

@common.login_auth
#购物模块
def shopping():
    print("欢迎来到购物模块")
    while True:
        for index, goods in enumerate(settings.SHOP_DIST): #用列表存储的商品输出，得到索引和有两个元素的商品小列表
            print(f'{index} {goods}')
        goods_n = input("请输入你要的商品编号,按q退出:")
        if goods_n == 'q':
            break
        if not goods_n.isdigit():
            print("输入有误")
            continue
        goods_n = int(goods_n)
        goods = settings.SHOP_DIST[goods_n] # 拿到的商品是一个有两个值（第一个是商品名，第二个是价格）的列表
        goods_name = goods[0] # 列表第一个元素是商品名
        user_dic = db_handler.read_json(user_info['user']) # 拿到当前用户的数据字典
        my_money = user_dic['extra'] # 把用户字典中的查看额度取出来
        if goods[-1] <= my_money: # 如果商品金额小于额度，可以买
            if goods_name in user_dic['shop_car']:
                user_dic['shop_car'][goods_name] += goods[-1] # 如果我的字典里面的购物车字典有该商品，把价格加上去
            else:
                user_dic['shop_car'][goods_name] = goods[-1] # 如果我的字典里面的购物车字典没有该商品，把商品名加上去，价格加上去
            db_handler.save_json(user_dic) # 做完修改要保存
            print(f'{goods_name}加入购物车成功')
        else:
            print("余额不足")
            break
    print(f"你的购物车是{user_dic['shop_car']}") # 买完之后要打印一下


@common.login_auth
# 购物车模块
def shopping_car():
    print("欢迎来到购物车模块")

    while True:
        user_dic = db_handler.read_json(user_info['user']) #用户数据读取
        goods_dic = user_dic['shop_car'] # 拿到用户数据字典的购物车字典
        cost_choice = input(f"购物车是{goods_dic}，是否选择购买y/n:") # 判断是否购买
        if cost_choice == 'n':
            break
        elif cost_choice == 'y':
            cost = sum(goods_dic.values()) # 把用户购物车字典中的值求和得到总价
            if cost > user_dic['extra']:
                print('余额不足，支付失败')
                break
            user_dic['extra'] -= cost # 支付就是把用户字典的额度减去总价
            db_handler.save_json(user_dic) # 操作完了保存
            print("支付成功")
            break




def run():

    FUNC_DICT = {
        '0':logout,
        '1':login,
        '2':register,
        '3':check_extra,
        '4':transfer,
        '5':repay,
        '6':withdraw,
        '7':history,
        '8':shopping,
        '9':shopping_car,
    }
    from confs.settings import FUNC_MSG
    while True:
        for k, v in FUNC_MSG.items(): # 把功能列表打印出来展示给用户，包括序号和值
            print(f'{k}: {v}')

        func_choice = input("请输入你需要的功能，按q退出>>>>>").strip()
        if func_choice == 'q':
            break

        if not FUNC_DICT.get(func_choice):
            print('输入有误，请重新输入')
            continue

        func = FUNC_DICT.get(func_choice)
        func()

if __name__ == '__main__':
    run()
