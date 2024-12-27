# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-08
# @File   : deps.py

"""
自定义方法，可以在yaml文件中以${{XXX()}}方式调用

!!!
注意，如果方法有参数时，传入的参数都是字符串，是数字的话，需要函数内部自己转换
"""
from utils.common import main
