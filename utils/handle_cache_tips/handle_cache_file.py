# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-08
# @File   : handle_cache_file.py

from conf.setting import setting
from utils.handle_yaml_tips.extract_jsonpath import extract_jsonpath
from typing import Dict
from utils.exceptions import *
from utils.logger import logger
from utils.db import RedisDb

class HandleCacheFile:
    """处理缓存文件数据"""

    def read_cache_file(self, file_name: str):
        with open(setting.CACHE_FILE_PATH + file_name, "r", encoding=setting.GLOBAL_ENCODING) as f:
            data = f.read()
        return data

    def write_cache_file(self, file_name: str, content: str):
        """
        创建缓存文件并写入内容
        :param content: 文件内容
        :return:
        """
        with open(setting.CACHE_FILE_PATH + file_name, "w", encoding=setting.GLOBAL_ENCODING) as f:
            f.write(content)

    def save_cache_data(self, res, rules: Dict):
        """
        保存缓存数据
        :param res: resquests请求返回对象
        :param rules: yaml文件中配置的rules数据
        :return:
        """
        logger.info("=" * 10)
        for rule in rules:
            type_str = rule.get('type')
            jsonpath_rule = rule.get('jsonpath')
            name = rule.get('name')
            if type_str == "response":
                result = extract_jsonpath(res.json(), jsonpath_rule)
            elif type_str == "headers":
                result = extract_jsonpath(dict(res.request.headers), jsonpath_rule)
            elif type_str == "cookies":
                result = extract_jsonpath(res.cookies, jsonpath_rule)
            else:
                raise NotFoundError(f"暂不支持此type类型{type_str}")
            if result:
                if setting.CACHE_TYPE == "text":
                    self.write_cache_file(name, str(result))
                    logger.info(f"缓存文件名称:{name},保存值为:{result}")
                elif setting.CACHE_TYPE == "redis":
                    db = RedisDb()
                    db.set(name,str(result))
                    logger.info(f"redis key:{name},value:{result}")
                else:
                    raise NotFoundError(f"不支持该缓存类型:{setting.CACHE_TYPE}")



if __name__ == '__main__':
    hcf = HandleCacheFile()
    hcf.write_cache_file('${{code}}', "3")
