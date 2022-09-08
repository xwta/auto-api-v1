# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-08
# @File   : logger.py
import os
from loguru import logger
from conf.setting import setting


def logger_file() -> str:
    """日志文件路径"""
    return os.path.join(setting.LOGGER_DIR, setting.LOGGER_NAME)

logger.add(
    logger_file(),
    encoding=setting.GLOBAL_ENCODING,
    level=setting.LOGGER_LEVEL,
    rotation=setting.LOGGER_ROTATION,
    retention=setting.LOGGER_RETENTION,
    enqueue=True
)

