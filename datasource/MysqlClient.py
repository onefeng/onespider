#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.ConfigManager import ConfigManager
from DBUtils.PersistentDB import PersistentDB
import pymysql
import logging
class MysqlClient(object):
    config = ConfigManager()
    mysql_account = config.yaml_setting['datasouce']['mysql']

    def __init__(self):
        """
        初始化连接
        """
        try:
            self._pool = PersistentDB(pymysql, maxusage=None, threadlocal=None, closeable=False,
                                **self.mysql_account)
        except Exception as e:
            logging.exception(e)
    def get_conn(self):
        """取数据库连接"""
        return self._pool.connection()

    def insert(self, table, datas={}):
        flag = False
        try:
            db = self.get_conn()
            cursor = db.cursor()
            keys = ','.join(datas.keys())
            values = ','.join(['%s'] * len(datas))
            sql = 'insert into {table}({keys}) values ({values})'.format(table=table, keys=keys, values=values)
            #print(sql)
            cursor.execute(sql, tuple(datas.values()))
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            db.rollback()
            logging.exception(e)
        finally:
            return flag
    def insertmany(self, table, datas=None):
        flag = False
        try:
            db=self.get_conn()
            cursor = db.cursor()
            keys = ','.join(datas[0].keys())
            values = ','.join(['%s'] * len(datas[0]))
            sql = 'insert into {table}({keys}) values ({values})'.format(table=table, keys=keys, values=values)
            # print(sql)
            # print([tuple(data.values()) for data in datas])
            cursor.executemany(sql, [tuple(data.values()) for data in datas])
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            db.rollback()
            logging.exception(e)
        finally:
            return flag

    def query(self, sql):
        """
        数据库查询操作
        :param sql:需要查询的语句
        :return:返回元组
        """
        results = ()
        try:
            db = self.get_conn()
            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            db.rollback()
            logging.exception(e)
        finally:
            return results

    def noquery(self, sql):
        """
        数据库非查询操作,删除，建表，赋权，更新等操作
        :param sql:需要执行的语句
        :return:返回元组
        """
        flag = False
        try:
            db = self.get_conn()
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            db.rollback()
            logging.exception(e)
        finally:
            return flag

