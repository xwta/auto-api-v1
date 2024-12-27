# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-09
# @File   : create_case_file.py

import os
from conf.setting import setting


class CreateCaseFile:

    def __init__(self, directory_name: str, case_name: str):
        """
        :param directory_name: 目录名称
        :param case_name: case文件名称
        """
        self.case_name = case_name
        self.directory_name = directory_name
        if not os.path.exists(setting.CASE_FILE_PATH + self.directory_name):
            os.mkdir(setting.CASE_FILE_PATH + self.directory_name)
        self.case_file_path = setting.CASE_FILE_PATH + self.directory_name + "/" + "test_" + self.case_name + ".py"
        if os.path.exists(self.case_file_path):
            raise Exception(f"{self.directory_name}目录下的{self.case_name}文件已存在！")

    def create_case_file(self):
        case_template = f"""
# coding=utf-8
import pytest
import allure
from utils.handle_yaml_tips.analyse_yaml_data import AnalyseYamlData
from utils.execute_tips.base_requests import BaseRequests


ayd = AnalyseYamlData('{self.directory_name}', '{self.case_name}')
allure_params = ayd.analyse_yaml_data()[0]
case_title = ayd.analyse_yaml_data()[1]
case_list = ayd.analyse_yaml_data()[2]


@allure.epic(allure_params['allureEpic'])
@allure.feature(allure_params['allureFeature'])
@allure.story(allure_params['allureStory'])
@pytest.mark.parametrize("case", case_list, ids=case_title)
def test_{self.case_name}(case):
    br = BaseRequests(case)
    result = br.base_requests()
    if result is None:
        pytest.skip("")
    assert result


if __name__ == '__main__':
    pytest.main(["-s","-q","test_{self.case_name}.py"])       
        
        """
        with open(self.case_file_path, "w", encoding=setting.GLOBAL_ENCODING) as f:
            f.write(case_template)


if __name__ == '__main__':
    ccf = CreateCaseFile('referenceStandards', 'referenceStandards')
    ccf.create_case_file()
