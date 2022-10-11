# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-08
# @File   : handle_cache_file.py

from conf.setting import setting
from utils.handle_yaml_tips.extract_jsonpath import extract_jsonpath
from typing import Dict


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

    def save_cache_data(self, res, sava_cache: Dict):
        """
        保存缓存数据
        :param res: resquests请求返回对象
        :param sava_cache: yaml文件中配置的save_cache数据
        :return:
        """
        rules = sava_cache.get("rules")
        for rule in rules:
            type_str = rule.get('type')
            jsonpath_rule = rule.get('jsonpath')
            name = rule.get('name')
            if type_str == "response":
                pass



if __name__ == '__main__':
    hcf = HandleCacheFile()
    data = hcf.read_cache_file('${id}')
    print(data)
