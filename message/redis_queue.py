# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datasource.RedisClient import RedisClient
class RedisQueue(RedisClient):
    key = 'request'
    def put(self, item):
        con = self.get_conn
        con.rpush(self.key, item)

    def get(self, timeout=0):
        con = self.get_conn
        data = con.blpop(self.key, timeout=timeout)[1]
        return data

    def sadd(self, item):
        con = self.get_conn
        con.sadd(self.key, item)

    def empty(self):
        con = self.get_conn
        if con.exists(self.key):
            return False
        else:
            return True
class RedisSet(RedisClient):
    key = 'request_set'
    def add(self,value):
        flag = self.get_conn.sadd(self.key,value)
        return flag
# redis队列
request_q = RedisQueue()
# 去重集合
request_set = RedisSet()