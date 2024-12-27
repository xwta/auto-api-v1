# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-11
# @File   : run.py

import os
import shutil
from conf.setting import setting
"""
总执行用例文件
"""
if os.path.exists(setting.REPORT_PATH):
    shutil.rmtree("./report")
os.system("pytest -s -q --alluredir ./report")
os.system("allure generate ./report/ -o ./allure-report --clean")
