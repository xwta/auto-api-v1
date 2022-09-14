# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-14
# @File   : analyse_yaml_data.py

from utils.handle_yaml_tips.read_yaml_data import ReadYamlData
from conf.setting import setting
from typing import Dict, Text, Union
from utils.exceptions import *
from utils.handle_yaml_tips.get_setting_data import get_setting_data
from utils.handle_yaml_tips.call_deps_method import call_deps_method
import re


class AnalyseYamlData(ReadYamlData):

    def __init__(self, directory_name: str, yaml_name: str):
        super().__init__(directory_name, yaml_name)

    def yaml_required_keys(self, case_order, case_keys) -> None:
        """
        判断yaml文件中的用例配置中是否缺少必填项
        :param case_order: 用例序号名称
        :param case_keys: 用例文件中所有的keys
        :return:
        """
        for key in setting.YAML_REQUIRED_KEYS:
            if key not in case_keys:
                raise Exception(f"{self.yaml_file_path},文件中用例{case_order}缺少{key}参数")

    def get_params_rules(self, params: Union[Dict, str]) -> Union[Dict, str]:
        """
        提取传入的参数中的三种类型：
        ${host} ：setting配置文件中参数
        ${{cache}} ：缓存文件名称
        ${{add()}} ：deps文件中的自定义方法
        :param params: yaml文件中对应key的值
        :return:
        """
        global ret_params
        setting_re = re.findall("\$\{[a-z]*\}", params)
        cacheOrMethod_re = re.findall("\$\{\{.*\}$", params)  # 注意一个字符串中只能匹配到一个方法
        if isinstance(params, str):
            if setting_re != [] and cacheOrMethod_re != []:
                # setting_re的值存在多个时，循环替换
                if len(setting_re) > 1:
                    for item in setting_re:
                        item_value=get_setting_data(item.split('{')[1].split("}")[0])
                        # 把原字符串中的${xxx}换成获取配置文件后的值
                        ret_params=params.replace(item,item_value)
                else:
                    setting_value=get_setting_data(setting_re[0].split('{')[1].split("}")[0])
                    ret_params=params.replace(setting_re[0],setting_value)
                # 判断cacheOrMethod_re中的值是否存在英文(),存在则执行调用方法，否则获取cache文件中内容
                if "(" in cacheOrMethod_re[0] and ")" in cacheOrMethod_re[0] :
                    # 方法名称
                    method_name=cacheOrMethod_re[0].split("{{")[1].split("(")[0]
                    # 方法传入的参数,执行报错说明没有参数，并捕获异常
                    try:
                        method_params=cacheOrMethod_re[0].split("{{")[1].split("(")[1].split(")")[0].split(',')
                        cacheOrMethod_value = call_deps_method(method_name,method_params)
                    except:
                        cacheOrMethod_value = call_deps_method(method_name)
                    ret_params=ret_params.replace(cacheOrMethod_re[0],str(cacheOrMethod_value))
            return ret_params


    def analyse_yaml_data(self):
        """解析yaml文件中配置内容"""
        yaml_data = self.read_yaml_data()
        allure_params = yaml_data["allure_params"]  # allure基础配置信息
        all_keys = yaml_data.keys()
        case_list = []  # 用例list
        for case_id in all_keys:
            # 默认以“case”开头的用例名称才匹配
            if case_id.startswith(setting.YAML_CASE_STARTSWITH):
                case_data = yaml_data[case_id]
                # 判断用例中必填的关键内容是否缺失
                self.yaml_required_keys(case_id, case_data.keys())
                case_info = {
                    "url": self.get_host(case_id, case_data)
                }
                print(case_info)

    def get_host(self, case_id: str, case_data: Dict) -> Text:
        """
        获取用例中的host
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("host")
        if key_value is None:
            raise NotCaseKeyError(f"用例{case_id},缺少host关键字key！")
        # 提取配置host的数据
        host = get_setting_data(key_value.split('{')[1].split("}")[0])
        return host

    def get_url(self, case_id: str, case_data: Dict) -> Text:
        """
        获取用例中的url
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("url")
        if key_value is None:
            raise NotCaseKeyError(f"用例{case_id},缺少url关键字key！")


if __name__ == '__main__':
    ayd = AnalyseYamlData('login', 'login')
    data=ayd.get_params_rules("/xxx/xxx/${host},${{add(1,2)}}")
    print(data)
