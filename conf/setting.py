# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-02
# @File   : setting.py

import os
from typing import Dict


class Setting:
    host = "xxxxx:xxxxx"  # ip+port或者域名
    HTTP_TYPE = "http"
    BASE_URL = HTTP_TYPE + "://" + host
    DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_FILE_PATH = DIR + "/data/"  # yaml存放路径
    CASE_FILE_PATH = DIR + "/case/"  # case存放路径
    CACHE_FILE_PATH = DIR + "/cache/"  # cache缓存文件存放路径
    CONF_FILE_PATH = DIR + "/conf/"  # 配置文件存放路径
    CODE_PATH = DIR + "/conf/code/"  # 验证码存放路径
    REPORT_PATH = DIR + "/report"  # 报告存放路径
    DEPS_NAME = "conf.deps"  # 自定义方法的py文件路径

    YAML_CASE_STARTSWITH = "case"  # yaml文件中用例序号默认以case开头格式
    GLOBAL_ENCODING: str = 'utf-8'  # 全局编码

    LOGGER_DIR: str = os.path.join(DIR, 'logs')  # 日志目录
    LOGGER_NAME: str = '{time:YYYY-MM-DD}.logs'  # 日志文件名 (时间格式)
    LOGGER_LEVEL: str = 'DEBUG'  # 日志等级: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "100 MB"  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "1 days"  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]

    DING_ACCESS_TOKEN: str = "xxxxx"  # 钉钉群access_token
    MESSAGE_SWITCH = False  # 发送钉钉或者企业微信、邮件等开关
    CACHE_TYPE: str = "text"  # 缓存存储类型，默认以文本形式存储和读取，改成redis时，以redis存储和读取

    MYSQL_DB: Dict = {"host": "xxxxx", "port": 3306, "database": "xxxxx", "user": "xxxxx", "passwd": "xxxxx",
                      "charset": "utf8"}
    REDIS_DB: Dict = {"host": "xxxxx", "port": 6379, "xxxxx": "xxxxx", "db": 0}


setting = Setting()
