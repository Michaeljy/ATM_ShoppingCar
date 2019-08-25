#start.py （开始模块，项目的起始点）

from core import src
import os
import sys

sys.path.append(os.path.dirname(__file__)) #一定要把当前路径加入环境变量里
if __name__ == '__main__':
    src.run()
