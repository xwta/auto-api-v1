# coding=utf-8
import pytest
import allure
import os
import shutil
from utils.handle_yaml_tips.analyse_yaml_data import AnalyseYamlData
from utils.logger import logger

ayd = AnalyseYamlData("login", "login")
allure_params = ayd.analyse_yaml_data()[0]
case_title = ayd.analyse_yaml_data()[1]
case_list = ayd.analyse_yaml_data()[2]


@allure.epic(allure_params['allureEpic'])
@allure.feature(allure_params['allureFeature'])
@allure.story(allure_params['allureStory'])
@pytest.mark.parametrize("case", case_list, ids=case_title)
def test_login(case):
    logger.info(f"测试数据为:{case}")


if __name__ == '__main__':
    # pytest.main(["-s","-q","test_login.py"])
    shutil.rmtree("../../report")
    os.system("pytest -s -q --alluredir ../../report")
    os.system("allure generate ../../report/ -o ../../allure-report --clean")
