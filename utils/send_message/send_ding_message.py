# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-10-27
# @File   : send_ding_message.py

import requests
from conf.setting import setting

def send_ding_message(content: str):
    """
    支持以html、markdown语法的格式发送消息给钉钉群
    :param content: 消息内容
    :return:
    """
    url = f"https://oapi.dingtalk.com/robot/send?access_token={setting.DING_ACCESS_TOKEN}"
    headers = {'Content-Type': 'application/json'}

    data = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": "接口自动化测试报告",
            # 要发送的内容【支持markdown】【！注意：content内容要包含机器人自定义关键字，不然消息不会发送出去，这个案例中是test字段】
            "text": content,
            "btnOrientation": "1",
            "btns": [
                {"title": "查看详情",
                 "actionURL": "https://www.dingtalk.com/"}  # 报告地址，用到时更改
            ]
        },
        "at": {
            # 要@的人
            # "atMobiles": mobile_list,
            # 是否@所有人
            "isAtAll": True
        }
    }

    res = requests.post(url=url, headers=headers, json=data)

    return res
