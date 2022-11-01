# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-02
# @File   : create_yaml_file.py

import os
from conf.setting import setting


class CreateYamlFile:
    """创建yaml文件模板"""

    def __init__(self,directory_name:str,yaml_name:str):
        """
        :param directory_name: 目录名称
        :param yaml_name: yaml文件名称
        """
        if not os.path.exists(setting.DATA_FILE_PATH + directory_name):
            os.mkdir(setting.DATA_FILE_PATH + directory_name)
        self.yaml_file_path=setting.DATA_FILE_PATH + directory_name + "/" + yaml_name + ".yaml"
        if os.path.exists(self.yaml_file_path):
            raise Exception(f"{directory_name}目录下的{yaml_name}文件已存在！")

    def create_yaml_file(self):
        yaml_content="""
#allure基础信息配置
allure_params:
  allureEpic: "项目名称描述"
  allureFeature: "功能点描述（模块名称）"
  allureStory: "接口名称"

#用例序号默认以case开头，可以在配置文件中更改，xxx为自定义名称
case_xxx_01:
  #${xxx}表示从配置文件中获取值，${{xxx()}}表示从deps文件中调用方法，${{xxx}}表示缓存存取文件名
  host: ${host}
  url: /xxxx/xxx/xxx
  method: POST
  title: 验证XXXX成功
  headers:
    content-type: application/json
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36
  #请求参数分为4种类型，values根据类型传入不同的参数
  data:
    type: data | json | file | params
    values: {"name":"zwx"}
    file_path: ../data/1.png  #可能存在同时需要上传参数和文件的情况
  #空、true、None默认执行，false不执行该用例
  is_run:
  #是否在接口返回值存入缓存中，type: redis | text ，放入配置文件中，总的来控制是使用文本还是redis存缓存数据
  sava_cache:
    is_cache: true #如果不写此项、为空、false，则认为不开启
    #可能存在多个需要存的值
    rules:
      - type: response | headers | cookies
        jsonpath: $.code  # 采用jsonpath提取值
        name: ${{code}}
      - type: response | headers | cookies
        jsonpath: $.code  # 采用jsonpath提取值
        name: ${{code}}
  #是否需要依赖数据
  dependent_data:
    is_dependent: true #如果不写此项、为空、false，则认为不需要
    rules:
      - type: data | headers  #修改依赖数据的位置
        key: code   #需要修改的值对应的key
        name: ${{code}}    #缓存文件名称
  #断言，可以存在多个
  asserts:
    is_full_assert: false  #是否全量断言，只有写了此关键字并设置true才开启，其他默认不开启走具体返回值断言
    rules:
      - jsonpath: $.code
        type: == | >= | <= | != | in | not in  #注意pyyaml因版本问题不兼容!=,需要加引号'!='
        value: 200   #预期结果
      - jsonpath: $.code
        type: == | >= | <= | != | in | not in 
        value: 200   #预期结果
  #用例执行完、后置清理数据操作
  teardown:
    sqls:
      - sql: xxxxxx
      - sql: xxxxxx
    tips:
      - tip: ${{xxx()}}
      - tip: ${{xxx()}}
"""

        with open(self.yaml_file_path,"w",encoding=setting.GLOBAL_ENCODING) as f:
            f.write(yaml_content)


if __name__ == '__main__':
    cyf=CreateYamlFile('login','login')
    cyf.create_yaml_file()





