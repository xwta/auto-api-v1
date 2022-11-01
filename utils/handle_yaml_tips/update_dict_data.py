# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-27
# @File   : update_dict_data.py

from typing import Dict


def update_dict_data(data: Dict, k, val):
    """
    修改字典中某个key的值
    :param data: 需要修改的字典数据
    :param k: 字典中对应的key
    :param val: key对应需要修改的值
    :return:
    """

    for key,value in data.items():
        if k == key:
            data[k]=val
            return data
        else:
            if isinstance(value,dict):
                update_dict_data(value,k,val)
    return data



