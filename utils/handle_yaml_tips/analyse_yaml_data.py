# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-14
# @File   : analyse_yaml_data.py

from utils.handle_yaml_tips.read_yaml_data import ReadYamlData
from conf.setting import setting
from typing import Dict, Text, Union, List, Any
from utils.exceptions import *
from utils.handle_yaml_tips.get_setting_data import get_setting_data
from utils.handle_yaml_tips.call_deps_method import call_deps_method
import re
from utils.handle_cache_tips.handle_cache_file import HandleCacheFile


class AnalyseYamlData(ReadYamlData):

    setting_regular = r"\$\{\w+\}"  # 提取配置文件数据正则
    method_regular = r"\$\{{2}[^$]+\}{2}"  # 提取方法正则

    def __init__(self, directory_name: str, yaml_name: str):
        super().__init__(directory_name, yaml_name)


    @classmethod
    def analyse_params_rules(cls, params: Union[Dict, str]) -> Union[Dict, str]:
        """
        提取传入的参数中的两种类型：
        ${host} ：setting配置文件中参数
        ${{add()}} ：deps文件中的自定义方法
        :param params: yaml文件中对应key的值
        :return:
        """
        if isinstance(params, str):
            setting_re_list = re.findall(cls.setting_regular, params)
            method_re_list = re.findall(cls.method_regular, params)
            ret_params = cls.handle_str_rules(params, setting_re_list, method_re_list)
        elif isinstance(params, dict):
            ret_params = cls.search_dict_rules(params)
        else:
            ret_params = params
        return ret_params

    @classmethod
    def analyse_setting_data(cls, params: str, setting_re_list: List) -> str:
        """
        解析配置文件中的数据
        :param params: yaml文件中对应key的值
        :param setting_re_list: eg：['${host}','${DIR}']
        :return:
        """
        for item in setting_re_list:
            item_value = get_setting_data(item.split('{')[1].split("}")[0])
            # 把原字符串中的${xxx}换成获取配置文件后的值
            params = params.replace(item, item_value)
        return params

    @classmethod
    def analyse_method_data(cls, params: str, method_re_list: List) -> str:
        """
        解析并执行方法得到返回值并替换
        :param params: yaml文件中对应key的值
        :param cacheOrMethod_re_list: eg：['${{add()}}','${{reduce()}}']
        :return:
        """
        for method in method_re_list:
            # 方法名称
            method_name = method.split("{{")[1].split("(")[0]
            # 方法传入的参数,执行报错说明没有参数，并捕获异常
            try:
                # 方法传参
                method_params = method.split("{{")[1].split("(")[1].split(")")[0].split(',')
                method_value = call_deps_method(method_name, method_params)
            except:
                method_value = call_deps_method(method_name)
            params = params.replace(method, str(method_value))
        return params

    @classmethod
    def analyse_cache_data(cls, cache_re_list: List) -> str:
        """
        解析缓存文件名称并得到文件内容后返回
        :param cache_re_list:
        :return:
        """
        cache_file_name = cache_re_list[0]
        hcf = HandleCacheFile()
        data = hcf.read_cache_file(cache_file_name)
        return data

    @classmethod
    def search_dict_rules(cls, params_dict):
        """
        查找传入的dict中key对应的value中含有${host},${{add(1,2)}}执行并替换成执行后的数据，
        注意！！！
          如果value不是字符串，是list或者其他类型中的配置项不会执行和替换
        :param params_dict: yaml文件中配置key对应的value
        :return: 返回执行并替换后的dict
        """
        if not isinstance(params_dict, dict):
            return

        for key, value in params_dict.items():
            if isinstance(value, dict):
                cls.search_dict_rules(value)
            elif isinstance(value, str):
                setting_re_list = re.findall(cls.setting_regular, value)
                method_re_list = re.findall(cls.method_regular, value)
                new_value = cls.handle_str_rules(value, setting_re_list, method_re_list)
                params_dict[key] = new_value

        return params_dict

    @classmethod
    def handle_str_rules(cls, params: str, setting_re_list: List, method_re_list: List) -> str:
        """
        处理字符串中含有的${host},${{add(1,2)}}配置
        :param params:
        :param setting_re:
        :param method_re:
        :return:
        """
        if setting_re_list != [] and method_re_list != []:
            # 解析配置文件中的数据并替换
            ret_params = cls.analyse_setting_data(params, setting_re_list)
            # 判断cacheOrMethod_re中的值是否存在英文(),存在则执行调用方法，否则抛出异常
            if "(" in method_re_list[0] and ")" in method_re_list[0]:
                ret_params = cls.analyse_method_data(ret_params, method_re_list)
            else:
                raise NotAllowCacheError("此项不能使用cache！")
        elif setting_re_list != [] and method_re_list == []:
            ret_params = cls.analyse_setting_data(params, setting_re_list)
        elif setting_re_list == [] and method_re_list != []:
            if "(" in method_re_list[0] and ")" in method_re_list[0]:
                ret_params = cls.analyse_method_data(params, method_re_list)
            else:
                raise NotAllowCacheError("此项不能使用cache配置项读取内容！")
        else:
            ret_params = params
        return ret_params

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
        if key_value is not None:
            url_path = self.analyse_params_rules(key_value)
            url = setting.HTTP_TYPE + "://" + self.get_host(case_id, case_data) + url_path
            return url
        else:
            raise NotCaseKeyError(f"用例{case_id},缺少url关键字key！")

    def get_method(self, case_id: str, case_data: Dict) -> Text:
        """
        获取用例中的请求方式
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("method")
        if key_value is not None:
            if key_value.upper() in ["POST", "GET", "DELETE", "PUT", "HEAD", "OPTIONS"]:
                return key_value.upper()
            else:
                raise NotFoundError(f"{key_value}请求方式填写错误或者不支持该方式")
        else:
            raise NotCaseKeyError(f"用例{case_id},缺少method关键字key！")

    def get_title(self, case_id: str, case_data: Dict) -> Text:
        """
        获取用例中的标题
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("title")
        if key_value is not None:
            return key_value
        else:
            raise NotCaseKeyError(f"用例{case_id},缺少title关键字key！")

    def get_headers(self, case_id: str, case_data: Dict) -> Text:
        """
        获取用例中的请求头
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("headers")
        if key_value is not None:
            return key_value
        else:
            raise NotCaseKeyError(f"用例{case_id},缺少headers关键字key！")

    def get_data(self, case_id: str, case_data: Dict) -> Dict:
        """
        获取用例中的请求参数
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("data")
        if key_value is not None:
            req_type = key_value.get('type')
            if req_type in ["data", "json", "file", "params"]:
                # 请求参数中可以写自定义方法和配置文件中数据
                values = self.analyse_params_rules(key_value.get("values"))
                key_value["values"] = values
                return key_value
            else:
                raise NotFoundError(f"用例{case_id},type类型中不存在:{req_type}")
        else:
            raise NotCaseKeyError(f"用例{case_id},缺少headers关键字key！")

    def get_is_run(self, case_id: str, case_data: Dict) -> Any:
        """
        获取用例中是否执行项
        :param case_id:
        :param case_data:
        :return:
        """
        try:
            key_value = case_data["is_run"]
            return key_value
        except:
            raise NotCaseKeyError(f"用例{case_id},缺少is_run关键字key！")

    def get_save_cache(self, case_id: str, case_data: Dict) -> Any:
        """
        获取用例中设置的保存缓存数据,为开启缓存或者没有此项，返回False
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("sava_cache")
        if key_value is not None:
            is_cache = key_value.get("is_cache")
            if is_cache:
                rules = key_value.get("rules")
                if rules is not None:
                    for rule in rules:
                        if rule.get("type") not in ["response", "headers", "cookies"]:
                            raise NotFoundError(f"用例{case_id},缓存取值类型无:{rule.get('type')}")
                    return rules
                else:
                    raise NotCaseKeyError(f"用例{case_id},已开启保存缓存，但缺少rules关键字key！")
            # 如果未开启保存缓存设置，则返回False
            else:
                return False
        else:
            return False

    def get_dependent_data(self, case_id: str, case_data: Dict) -> Any:
        """
        获取用例中配置的依赖数据
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("dependent_data")
        if key_value is not None:
            is_dependent = key_value.get("is_dependent")
            if is_dependent:
                rules = key_value.get("rules")
                if rules is not None:
                    return rules
                else:
                    raise NotCaseKeyError(f"用例{case_id},已开启依赖配置，但缺少rules关键字key！")
            # 如果未开启依赖数据配置，则返回False
            else:
                return False
        else:
            return False

    def get_asserts(self, case_id: str, case_data: Dict) -> Any:
        """
        获取用例中的断言配置项
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("asserts")
        if key_value is not None:
            return key_value
        else:
            raise NotCaseKeyError(f"用例{case_id},缺少assert关键字key！")

    def get_teardown(self, case_data: Dict) -> Any:
        """
        获取用例中后置操作配置
        :param case_id:
        :param case_data:
        :return:
        """
        key_value = case_data.get("teardown")
        if key_value is not None:
            return key_value
        else:
            return False

    def analyse_yaml_data(self):
        """解析yaml文件中配置内容"""
        yaml_data = self.read_yaml_data()
        allure_params = yaml_data["allure_params"]  # allure基础配置信息
        all_keys = yaml_data.keys()
        case_list = []  # 用例list
        case_title = []  # 用例名称
        for case_id in all_keys:
            # 默认以“case”开头的用例名称才匹配
            if case_id.startswith(setting.YAML_CASE_STARTSWITH):
                case_data = yaml_data[case_id]
                case_info = {
                    "case_id": case_id,
                    "url": self.get_url(case_id, case_data),
                    "method": self.get_method(case_id, case_data),
                    "title": self.get_title(case_id, case_data),
                    "headers": self.get_headers(case_id, case_data),
                    "data": self.get_data(case_id, case_data),
                    "is_run": self.get_is_run(case_id, case_data),
                    "sava_cache": self.get_save_cache(case_id, case_data),
                    "dependent_data": self.get_dependent_data(case_id, case_data),
                    "asserts": self.get_asserts(case_id, case_data),
                    "teardown": self.get_teardown(case_data)
                }
                case_list.append(case_info)
                case_title.append(case_info['title'])
        return allure_params, case_title, case_list


if __name__ == '__main__':
    ayd = AnalyseYamlData('login', 'login')
    # name="/${{add(7,3)}}/xxx/${host},${DEPS_NAME},sad/${{add(2,3)}}"
    data = ayd.analyse_yaml_data()
    print(data[2][0])
