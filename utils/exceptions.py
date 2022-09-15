# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-14
# @File   : exceptions.py



class BaseExceptions(Exception):
    pass

class NotFoundError(BaseExceptions):
    pass

class NotCaseKeyError(BaseExceptions):
    pass

class NotAllowCacheError(BaseExceptions):
    pass

