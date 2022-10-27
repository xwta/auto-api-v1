# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-27
# @File   : update_dict_data.py

from typing import Dict


def update_dict_data(data: Dict, k, val):

    for key,value in data.items():
        if k == key:
            data[k]=val
            return data
        else:
            if isinstance(value,dict):
                update_dict_data(value,k,val)
    return data


data = {"code":12,"name":"zwx","students":{"addr":"nanjing"}}

result = update_dict_data(data,"addr","beijing")
print(result)


