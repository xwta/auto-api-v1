# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-02
# @File   : read_yaml_data.py

import os
import yaml
from conf.setting import setting

class ReadYamlData:

    def __init__(self,directory_name:str,yaml_name:str):
        """
        :param directory_name: 目录名称
        :param yaml_name: yaml文件名称
        """
        self.yaml_file_path = setting.DATA_FILE_PATH + directory_name + "/" + yaml_name + ".yaml"
        if not os.path.exists(self.yaml_file_path):
            raise Exception(f"{self.yaml_file_path},路径不存在！")

    def read_yaml_data(self):
        with open(self.yaml_file_path,'r',encoding="utf-8") as f:
            yaml_data = f.read()
            data=yaml.load(yaml_data,yaml.SafeLoader)
            print(data)

if __name__ == '__main__':
    ryd=ReadYamlData('login','login')
    ryd.read_yaml_data()
