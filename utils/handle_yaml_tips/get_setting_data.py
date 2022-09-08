# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-08
# @File   : get_setting_data.py

from conf.setting import setting


def get_setting_data(setting_name: str):
    """
    获取配置文件中配置信息
    :param setting_name:
    :return:
    """
    return getattr(setting, setting_name)
