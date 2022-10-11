# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-11
# @File   : asserts_result.py

from typing import Dict
from utils.logger import logger
from utils.handle_yaml_tips.extract_jsonpath import extract_jsonpath
from utils.exceptions import *

def asserts_result(data: Dict,asserts: Dict):
    """
    断言多个接口返回值
    :param asserts: yaml文件提取出来asserts对象
    :return:
    """
    rules = asserts.get("rules")
    if rules is not None:
        for rule in rules:
            jsonpath_rule = rule.get('jsonpath')
            type_str = rule.get('type')
            value = rule.get('value') # 预期结果值
            inter_ret_value = extract_jsonpath(data,jsonpath_rule) # 接口返回提取值
            logger.info("="*10)
            logger.info(f"预期结果值:{value}")
            logger.info(f"断言方式:{type_str}")
            logger.info(f"提取表达式:{jsonpath_rule},接口返回提取值:{inter_ret_value}")
            if type_str == "==":
                result = value == inter_ret_value
            elif type_str == ">=":
                result = value >= inter_ret_value
            elif type_str == "<=":
                result = value <= inter_ret_value
            elif type_str == "!=":
                result = value != inter_ret_value
            elif type_str == "in":
                result = value in inter_ret_value
            elif type_str == "not in":
                result = value not in inter_ret_value
            else:
                raise NotFoundError(f"暂不支持:{type_str}该类型断言方式")
            logger.info(f"断言结果:{result}")
            if result is False:
                return False
        return True
    else:
        raise NotCaseKeyError("断言数据中无rules规则数据")

# asserts = {'is_full_assert': False, 'rules': [{'jsonpath': '$.code', 'type': '==', 'value': 200}, {'jsonpath': '$.code', 'type': '!=', 'value': 201}]}
# data = {"code":200,"name":"zwx"}
# res = asserts_result(data,asserts)



