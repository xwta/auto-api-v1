# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-09-08
# @File   : handle_cache_file.py

from conf.setting import setting


class HandleCacheFile:
    """处理缓存文件数据"""

    def __init__(self, file_name: str):
        self.file_name = file_name

    def read_cache_file(self):
        with open(setting.CACHE_FILE_PATH + self.file_name, "r", encoding=setting.GLOBAL_ENCODING) as f:
            data = f.read()
        return data

    def write_cache_file(self, content:str):
        """
        创建缓存文件并写入内容
        :param content: 文件内容
        :return:
        """
        with open(setting.CACHE_FILE_PATH + self.file_name, "w", encoding=setting.GLOBAL_ENCODING) as f:
            f.write(content)


if __name__ == '__main__':
    hcf = HandleCacheFile('${id}')
    data = hcf.read_cache_file()
    print(data)
