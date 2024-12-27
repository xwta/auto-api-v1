# -*- coding: utf-8 -*-
# @Time    : 2024/5/21 16:04
# @Author  : 梗小旭
# @File    : common.py

import ddddocr
import requests
import base64
from PIL import Image
from io import BytesIO
import random
from conf.setting import setting


def get_size():
    """获取验证码图片数据"""
    url = setting.BASE_URL + "/nbcio-boot/sys/randomImage/1716172800254"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
    }
    res = requests.get(url=url, headers=headers)
    return res.json()["result"]


def convert_base64_to_image(base64_data, save_path):
    # 从base64数据中提取图像数据部分
    image_data = base64_data.split(';base64,')[1]

    # 将base64数据解码为图像二进制数据
    image_binary = base64.b64decode(image_data)

    # 使用PIL库打开二进制数据作为图像
    image = Image.open(BytesIO(image_binary))

    # 保存图像为JPG文件
    image.save(save_path, 'JPEG')


def recognize(path):
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(path, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)

    return res


def main():
    data = get_size()
    sava_path = setting.CODE_PATH + str(random.choice(range(100000))) + ".jpg"
    convert_base64_to_image(data, sava_path)
    imgSize = recognize(sava_path)
    return imgSize


if __name__ == '__main__':
    data_list = [{'case_rs_01': [{'url': 'http://192.168.31.246:8080/nbcio-boot/baseDataPreserve/referenceStandardSave', 'method': 'POST', 'title': '验证新增参考标准成功', 'headers': {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36', 'X-Access-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYzNDc0MTUsInVzZXJuYW1lIjoiYWRtaW4ifQ.5W57_TNc44rNRaoauexRR0UdI0lf61dKocM2iLhGoBY'}, 'data': {'type': 'json', 'values': {'content': '111', 'referenceStandardCode': 'GB123', 'standardName': '执行标准'}}, 'is_run': None, 'sava_cache': False, 'dependent_data': False, 'asserts': {'rules': [{'jsonpath': '$.success', 'type': '==', 'value': True}]}, 'teardown': False}, {'url': 'http://192.168.31.246:8080/nbcio-boot/baseDataPreserve/referenceStandardSave', 'method': 'POST', 'title': '验证新增参考标准成功', 'headers': {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36', 'X-Access-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYzNDc0MTUsInVzZXJuYW1lIjoiYWRtaW4ifQ.5W57_TNc44rNRaoauexRR0UdI0lf61dKocM2iLhGoBY'}, 'data': {'type': 'json', 'values': {'content': '111', 'referenceStandardCode': 'GB123', 'standardName': '执行标准'}}, 'is_run': None, 'sava_cache': False, 'dependent_data': False, 'asserts': {'rules': [{'jsonpath': '$.success', 'type': '==', 'value': True}]}, 'teardown': False}]}, {'case_rs_02': [{'url': 'http://192.168.31.246:8080/nbcio-boot/baseDataPreserve/referenceStandardSave', 'method': 'POST', 'title': '验证新增参考标准成功', 'headers': {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36', 'X-Access-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYzNDc0MTUsInVzZXJuYW1lIjoiYWRtaW4ifQ.5W57_TNc44rNRaoauexRR0UdI0lf61dKocM2iLhGoBY'}, 'data': {'type': 'json', 'values': {'content': '111', 'referenceStandardCode': 'GB123', 'standardName': '执行标准'}}, 'is_run': None, 'sava_cache': False, 'dependent_data': False, 'asserts': {'rules': [{'jsonpath': '$.success', 'type': '==', 'value': True}]}, 'teardown': False}, {'url': 'http://192.168.31.246:8080/nbcio-boot/baseDataPreserve/referenceStandardSave', 'method': 'POST', 'title': '验证新增参考标准成功', 'headers': {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36', 'X-Access-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYzNDc0MTUsInVzZXJuYW1lIjoiYWRtaW4ifQ.5W57_TNc44rNRaoauexRR0UdI0lf61dKocM2iLhGoBY'}, 'data': {'type': 'json', 'values': {'content': '111', 'referenceStandardCode': 'GB123', 'standardName': '执行标准'}}, 'is_run': None, 'sava_cache': False, 'dependent_data': False, 'asserts': {'rules': [{'jsonpath': '$.success', 'type': '==', 'value': True}]}, 'teardown': False}]}]
    for data in data_list:
        for x,y in data.items():
            for c in y:
                print(c)
                print("="*20)

