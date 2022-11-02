# coding=utf-8
# @Author : 梗小旭
# @Time   : 2022-11-01
# @File   : db.py

import pymysql
from utils.logger import logger
from conf.setting import setting
import redis
from typing import Dict, List


class MySqlDb:

    def __init__(self, host=setting.MYSQL_DB['host'],
                 port=setting.MYSQL_DB['port'],
                 database=setting.MYSQL_DB['database'],
                 user=setting.MYSQL_DB['user'],
                 passwd=setting.MYSQL_DB['passwd'],
                 charset=setting.MYSQL_DB['charset']):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.passwd = passwd
        self.charset = charset

    def db_connect(self):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            passwd=self.passwd,
            charset=self.charset
        )
        return conn

    def get_all_data(self, sql):
        """
        获取执行sql所有数据
        :param sql:
        :return:
        """
        conn = self.db_connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                data = cursor.fetchall()
                return data
        except Exception as e:
            logger.error(f"查询sql异常:{e}")
        finally:
            conn.close()

    def update_data(self, sql):
        """
        添加、修改、删除等操作
        :param sql:
        :return:
        """
        conn = self.db_connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"更改操作异常:{e}")
        finally:
            conn.close()


class RedisDb:

    def __init__(self, host=setting.REDIS_DB["host"],
                 port=setting.REDIS_DB["port"],
                 password=setting.REDIS_DB["password"],
                 db=setting.REDIS_DB["db"]):
        self.host = host
        self.port = port
        self.password = password
        self.db = db

    def redis_conn(self):
        # 设置decode_responses=True，读取出的数据由原来的byte类型转换成str
        redis_pool = redis.ConnectionPool(host=self.host, port=self.port,
                                          password=self.password, db=self.db, decode_responses=True)
        redis_conn = redis.Redis(connection_pool=redis_pool)

        return redis_conn

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        设置值
        :param name: key值
        :param value: value值
        :param ex: 过期时间（秒），时间到了后redis会自动删除
        :param px: 过期时间（毫秒），时间到了后redis会自动删除。ex、px二选一即可
        :param nx: 如果设置为True，则只有name不存在时，当前set操作才执行
        :param xx: 如果设置为True，则只有name存在时，当前set操作才执行
        :return:
        """
        conn = self.redis_conn()
        conn.set(name=name, value=value, ex=ex, px=px, nx=nx, xx=xx)

    def mset(self, data: Dict):
        """
        设置多个key-value
        :param data:
        :return:
        """
        conn = self.redis_conn()
        conn.mset(data)

    def get(self, name):
        """
        获取某个name对应的value
        :param name:
        :return:
        """
        conn = self.redis_conn()
        value = conn.get(name)
        return value

    def mget(self, data: List):
        """
        获取多个key对应的value值
        :param data:
        :return:
        """
        conn = self.redis_conn()
        value_list = conn.mget(data)
        return value_list

    def hset(self, name: str, mapping: Dict):
        """
        存储字典格式数据
        :param name:
        :param mapping:
        :return:
        """
        conn = self.redis_conn()
        conn.hset(name=name, mapping=mapping)

    def hgetall(self, name: str):
        """
        获取该key的所有key-value数据
        :param name:
        :return:
        """
        conn = self.redis_conn()
        data = conn.hgetall(name)
        return data

    def delete(self, name):
        """
        删除某个key
        :param name:
        :return:
        """
        conn = self.redis_conn()
        conn.delete(name)


if __name__ == '__main__':
    # db = RedisDb()
    # data = db.get("${{code}}")
    # print(data)
    db = MySqlDb()
    db.update_data("update user set username='yxy111' where username='yxy'")

