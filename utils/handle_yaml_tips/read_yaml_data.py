# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-02
# @File   : read_yaml_data.py

import os
import yaml
from conf.setting import setting


class ReadYamlData:

    def __init__(self, directory_name: str, yaml_name: str):
        """
        :param directory_name: 目录名称
        :param yaml_name: yaml文件名称
        """
        self.yaml_file_path = setting.DATA_FILE_PATH + directory_name + "/" + yaml_name + ".yaml"
        if not os.path.exists(self.yaml_file_path):
            raise Exception(f"{self.yaml_file_path},路径不存在！")

    def read_yaml_data(self):
        """
        读取yaml内容
        :return:
        """
        with open(self.yaml_file_path, 'r', encoding=setting.GLOBAL_ENCODING) as f:
            yaml_data = f.read()
            data = yaml.load(yaml_data, yaml.SafeLoader)
        return data

    def yaml_required_keys(self, case_order, case_keys):
        """
        判断yaml文件中的用例配置中是否缺少必填项
        :param case_order: 用例序号名称
        :param case_keys: 用例文件中所有的keys
        :return:
        """
        for key in setting.YAML_REQUIRED_KEYS:
            if key not in case_keys:
                raise Exception(f"{self.yaml_file_path},文件中用例{case_order}缺少{key}参数")

    def analyse_yaml_data(self):
        """解析yaml文件中配置内容"""
        yaml_data = self.read_yaml_data()
        allure_params = yaml_data["allure_params"]  # allure基础配置信息
        all_keys = yaml_data.keys()
        case_list = []  # 用例list
        for keys in all_keys:
            # 默认以“case”开头的用例名称才匹配
            if keys.startswith(setting.YAML_CASE_STARTSWITH):
                case_data = yaml_data[keys]
                # 判断用例中必填的关键内容是否缺失
                self.yaml_required_keys(keys, case_data.keys())
                for key, value in case_data.items():
                    temp_list = []



if __name__ == '__main__':
    ryd = ReadYamlData('login', 'login')
    data = ryd.analyse_yaml_data()
