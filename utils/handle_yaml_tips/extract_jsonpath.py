# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-11
# @File   : extract_jsonpath.py


import jsonpath
from typing import Dict


def extract_jsonpath(data: Dict, rule: str):
    """
    根据 jsonpath 提取json中key对应的数据
    :param data: 需要提取数据的对象
    :param rule: jsonpath 提取规则 eg: $.code
    :return:
    """

    result = jsonpath.jsonpath(data, rule)
    if result is not False:
        return result[0]
    else:
        return result

