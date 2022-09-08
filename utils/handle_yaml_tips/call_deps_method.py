# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-08
# @File   : call_deps_method.py

import importlib
from conf.setting import setting


def call_deps_method(method_name: str, *args):
    """
    默认读取配置文件下conf.deps文件内的自定义方法，如果需要更改其他文件，
    在setting.DEPS_NAME更改路径
    :param method_name: 方法名称
    :param args: 方法需要传入的参数
    :return: 返回方法执行的结果
    """
    obj = importlib.import_module(setting.DEPS_NAME)
    method = getattr(obj, method_name)
    if args:
        return method(*args)
    else:
        return method()


