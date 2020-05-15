#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.ConfigManager import ConfigManager
from pymongo import MongoClient
import logging
class MongoDBClient(object):
    config = ConfigManager()
    mongo_account = config.yaml_setting['datasouce']['mongoBD']['url']
    mongo_database = config.yaml_setting['datasouce']['mongoBD']['database']
    def __init__(self):
        """初始化连接"""
        try:
            client = MongoClient(self.mongo_account)
            self._db = client[self.mongo_database]
        except Exception as e:
            logging.exception(e)

    def get_conn(self):
        return self._db

    def insert(self, table, result):

        db = self.get_conn()
        collection = db[table]
        collection.insert_one(result)

    def __getattr__(self, command):
        """
        方法重载
        :param command:
        :return:
        """
        def _(*args):
            return getattr(self.get_conn(), command)(*args)  # 重新组装方法调用
        return _


if __name__=='__main__':
    x = MongoClient()