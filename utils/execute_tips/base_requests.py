# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-10
# @File   : base_requests.py

import requests
from typing import Dict
from utils.logger import logger
from utils.exceptions import *
from utils.handle_yaml_tips.asserts_result import asserts_result
from utils.handle_cache_tips.handle_cache_file import HandleCacheFile
from utils.handle_yaml_tips.update_dict_data import update_dict_data
from utils.db import MySqlDb
from utils.handle_yaml_tips.analyse_yaml_data import AnalyseYamlData
from conf.setting import setting
from utils.db import RedisDb

class BaseRequests:
    """
    执行用例请求、是否运行、读取缓存、依赖数据，后置操作等
    """

    def __init__(self, case: Dict):
        self.mysql_db = MySqlDb()
        self.redis_db = RedisDb()
        self.case_id = case.get('case_id')
        self.type = case.get('data').get('type')
        self.url = case.get('url')
        self.title = case.get('title')
        self.method = case.get('method')
        self.headers = case.get('headers')
        self.file_path = case.get('data').get('file_path')
        self.is_run = case.get('is_run')
        self.sava_cache = case.get('sava_cache')
        self.asserts = case.get('asserts')
        self.teardown = case.get('teardown')
        self.dependent_data = case.get('dependent_data')
        self.data = case.get('data').get('values')
        # 处理缓存数据
        if self.dependent_data:
            for dep_data in self.dependent_data:
                dep_type = dep_data.get('type')
                dep_key = dep_data.get('key')
                dep_name = dep_data.get('name')
                # 判断缓存使用文件还是redis
                if setting.CACHE_TYPE == "text":
                    cache_value = HandleCacheFile().read_cache_file(dep_name)
                elif setting.CACHE_TYPE == "redis":
                    cache_value = self.redis_db.get(dep_name)
                else:
                    raise NotFoundError(f"不支持该缓存类型:{setting.CACHE_TYPE}")
                # 存入文件或者redis的数据有可能是字典或者其他格式变成字符串需要转换
                try:
                    cache_value = eval(cache_value)
                except:
                    cache_value = cache_value
                if dep_type == "headers":
                    self.headers = update_dict_data(self.headers, dep_key, cache_value)
                elif dep_type == "data":
                    self.data = update_dict_data(self.data, dep_key, cache_value)
                else:
                    raise NotFoundError(f"依赖项中的type类型不支持{dep_type}")

    def post(self):

        if self.type == "data":
            res = requests.post(url=self.url, data=self.data, headers=self.headers)
        elif self.type == "json":
            res = requests.post(url=self.url, json=self.data, headers=self.headers)
        elif self.type == "file":
            res = requests.post(url=self.url, data=self.data, headers=self.headers, files=self.file_path)
        else:
            res = None
        return res

    def get(self):

        if self.type == "params":
            res = requests.get(url=self.url, params=self.data, headers=self.headers)
        else:
            res = None
        return res

    def delete(self):

        res = requests.delete(url=self.url, headers=self.headers)
        return res

    def put(self):

        res = requests.put(url=self.url, data=self.data, headers=self.headers)
        return res

    def head(self):

        res = requests.head(url=self.url, headers=self.headers)
        return res

    def base_requests(self):
        """
        执行用例请求
        :return:
        """
        # 当is_run不是false时，用例才执行
        if self.is_run is not False:
            logger.info("=" * 20 + self.case_id + "=" * 20)
            logger.info(f"用例标题:{self.title}")
            logger.info(f"请求URL:{self.url}")
            logger.info(f"请求方法:{self.method}")
            logger.info(f"请求参数:{self.data}")
            logger.info(f"请求文件参数:{self.file_path}")
            logger.info(f"请求头:{self.headers}")
            res = None
            try:
                if self.method == "POST":
                    res = self.post()
                elif self.method == "GET":
                    res = self.get()
                elif self.method == "PUT":
                    res = self.put()
                elif self.method == "DELETE":
                    res = self.delete()
                elif self.method == "HEAD":
                    res = self.head()
                else:
                    raise NotFoundError(f"暂时不支持该请求方式{self.method}")
            except Exception as e:
                logger.error(f"请求错误，错误原因:{e}")
            logger.info(f"响应状态码:{res.status_code}")
            logger.info(f"响应时间(s):{res.elapsed.total_seconds()}")
            try:
                logger.info(f"响应结果:{res.json()}")
            except:
                logger.info(f"响应结果:{res.text}")
            # 处理缓存信息
            if self.sava_cache:
                hcf = HandleCacheFile()
                hcf.save_cache_data(res, self.sava_cache)
            # 处理后置操作
            if self.teardown:
                sqls = self.teardown.get('sqls')
                tips = self.teardown.get('tips')
                # 执行后置操作sql
                if sqls:
                    for sql in sqls:
                        self.mysql_db.update_data(sql.get('sql'))
                # 执行后置操作方法
                if tips:
                    for tip in tips:
                        AnalyseYamlData.analyse_params_rules(tip.get("tip"))
            # 断言
            assert_result = asserts_result(res.json(), self.asserts)
            return assert_result

        else:
            logger.warning(f"{self.case_id} 跳过不执行")


if __name__ == '__main__':
    ayd = AnalyseYamlData("login", "login")
    case_list = ayd.analyse_yaml_data()[2]
    for case in case_list:
        br = BaseRequests(case)
        br.base_requests()
