# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-27
# @File   : conftest.py


import pytest
from utils.send_message.send_ding_message import send_ding_message
import time
from utils.logger import logger
from conf.setting import setting


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    收集测试报告信息钩子函数，并发送消息给钉钉群
    :param terminalreporter:
    :param exitstatus:
    :param config:
    :return:
    """

    total = terminalreporter._numcollected
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    success_rate = round(passed / total) * 100
    duration = time.time() - terminalreporter._sessionstarttime
    logger.info(f"=" * 20 + "测试报告" + "=" * 20)
    logger.info(f"用例总数：{total}")
    logger.info(f"成功数：{passed}")
    logger.info(f"失败数：{failed}")
    logger.info(f"错误数：{error}")
    logger.info(f"跳过数：{skipped}")
    logger.info(f"成功率：▓▓▓▓▓▓▓▓▓▓▓ {success_rate} %")
    logger.info(f"执行时间：{round(duration, 2)} s")
    logger.info(f"=" * 44)
    content = f"""
### ✨接口自动化报告✨
- <font color="#444444">用例总数：{total}</font>
- <font color="#66FF66">成功数：{passed}</font>
- <font color="#FF5511">失败数：{failed}</font>
- <font color="#FF0000">错误数：{error}</font>
- <font color="#FFFF33">跳过数：{skipped}</font>
- <font color="#444444">成功率：▓▓▓▓▓▓▓▓▓▓▓ {success_rate} %</font>
- <font color="#444444">执行时间：{round(duration, 2)} s</font>
    """
    # 判断消息发送是否开启
    if setting.MESSAGE_SWITCH:
        send_ding_message(content)
