
# coding=utf-8
import pytest
import allure
from utils.handle_yaml_tips.analyse_yaml_data import AnalyseYamlData
from utils.execute_tips.base_requests import BaseRequests


ayd = AnalyseYamlData('login', 'login')
allure_params = ayd.analyse_yaml_data()[0]
case_title = ayd.analyse_yaml_data()[1]
case_list = ayd.analyse_yaml_data()[2]


@allure.epic(allure_params['allureEpic'])
@allure.feature(allure_params['allureFeature'])
@allure.story(allure_params['allureStory'])
@pytest.mark.parametrize("case", case_list, ids=case_title)
def test_login(case):
    br = BaseRequests(case)
    result = br.base_requests()
    # 当结果为None时，跳过该用例不执行
    if result is None:
        pytest.skip("")
    assert result


if __name__ == '__main__':
    pytest.main(["-s","-q","test_login.py"])       
        
        