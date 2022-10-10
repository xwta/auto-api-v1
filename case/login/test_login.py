#coding=utf-8
import pytest
import allure
import os
from utils.handle_yaml_tips.analyse_yaml_data import AnalyseYamlData

ayd=AnalyseYamlData("login","login")
allure_params=ayd.analyse_yaml_data()[0]
case_list=ayd.analyse_yaml_data()[1]
@allure.epic(allure_params['allureEpic'])
@allure.feature(allure_params['allureFeature'])
@allure.story(allure_params['allureStory'])
@pytest.mark.parametrize("case",case_list,ids=["ces1","ces2"])
def test_login(case):
    print("="*30)
    print(case)





if __name__ == '__main__':
    # pytest.main(["-s","-q","test_login.py"])
    os.system("pytest -s -q --alluredir ../../report")
    os.system("allure generate ../../report/ -o ../../allure-report --clean")