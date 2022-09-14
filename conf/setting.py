# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-02
# @File   : setting.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__))+"/conf/")
class Setting:

    host = "192.168.2.31"
    DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_FILE_PATH = DIR + "/data/"   # yaml存放路径
    CACHE_FILE_PATH = DIR + "/cache/"  # cache缓存文件存放路径
    CONF_FILE_PATH = DIR + "/conf/"  # 配置文件存放路径
    DEPS_NAME = "conf.deps"  # 自定义方法的py文件路径


    YAML_CASE_STARTSWITH = "case"  # yaml文件中用例序号默认以case开头格式
    YAML_REQUIRED_KEYS = ["host","url","method","title","assert"]  # yaml配置文件中必填项

    GLOBAL_ENCODING: str = 'utf-8'  # 全局编码

    LOGGER_DIR: str = os.path.join(DIR, 'logs')  # 日志目录
    LOGGER_NAME: str = '{time:YYYY-MM-DD}.logs'  # 日志文件名 (时间格式)
    LOGGER_LEVEL: str = 'DEBUG'  # 日志等级: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "100 MB"  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "1 days"  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]








setting =Setting()
