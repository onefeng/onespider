#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from redis import StrictRedis, ConnectionPool
from config.ConfigManager import ConfigManager

class RedisClient(object):
    config = ConfigManager()
    redis_account = config.yaml_setting['datasouce']['redis']['url']
    def __init__(self):
        """初始化连接"""
        pool = ConnectionPool.from_url(self.redis_account)
        self._redis = StrictRedis(connection_pool=pool)

    @property
    def get_conn(self):
        """
        :return: 获取连接
        """
        return self._redis

    # def put(self, item):
    #     con = self.get_conn()
    #     con.rpush(self.KEY, item)
    #
    # def get(self,timeout=0):
    #     con = self.get_conn()
    #     data = con.blpop(self.KEY,timeout=timeout)[1]
    #     return data
    #
    # def sadd(self, item):
    #     con = self.get_conn()
    #     con.sadd(self.KEY, item)
    #
    #
    # def empty(self):
    #     con=self.get_conn()
    #     if con.exists(self.KEY):
    #         return False
    #     else:
    #         return True
    #
    # def __getattr__(self, command):
    #     """
    #     方法重载
    #     :param command:
    #     :return:
    #     """
    #     def _(*args):
    #         return getattr(self.get_conn(), command)(*args)  # 重新组装方法调用
    #     return _

if __name__=='__main__':
    s = RedisClient()

    #print(x)





