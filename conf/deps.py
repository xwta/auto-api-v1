# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-08
# @File   : deps.py

"""
自定义方法，可以在yaml文件中以${{XXX()}}方式调用
"""


def add(a,b=3):
    print(a+b)