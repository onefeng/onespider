#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import threading
import csv
from datasource.MysqlClient import MysqlClient
from datasource.MongoClient import MongoDBClient
from datasource.PostgreClient import PostgreClient
from spiders.setings import *
from config.ConfigManager import ConfigManager

lock = threading.Lock()

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DataBaseExport(object):
    config = ConfigManager()
    base_table = config.yaml_setting['base_name']

    def __init__(self):
        """
        获取各数据库连接池
        :param name:
        :param result:
        """
        self.con_pg = PostgreClient() if DATAFLAG['postgre'] else None
        self.con_mysql = MysqlClient() if DATAFLAG['mysql'] else None
        self.con_mongo = MongoDBClient() if DATAFLAG['mongo'] else None

    def output_base(self, name, result):
        """
        不同数据库写入操作
        :param name:
        :param result:
        :return:
        """
        if self.con_pg:
            self.insert_postgre(name, result)
        if self.con_mysql:
            self.insert_mysql(name, result)
        if self.con_mongo:
            self.insert_mongo(name, result)
    def insert_postgre(self,table,datas={}):
        flag = False
        try:
            db = self.con_pg.get_conn()
            cursor = db.cursor()
            keys = ','.join(datas.keys())
            values = ','.join(['%s'] * len(datas))
            table=self.base_table+table
            sql = 'insert into {table}({keys}) values ({values})'.format(table=table, keys=keys, values=values)
            cursor.execute(sql, tuple(datas.values()))
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            print("查询失败->%s" % e)
            db.rollback()
        finally:
            return flag

    def insert_mongo(self, table, result):

        db = self.con_mongo.get_conn()
        collection = db[table]
        collection.insert_one(result)

    def insert_mysql(self, table, datas={}):
        flag = False
        try:
            db = self.con_mysql.get_conn()
            cursor = db.cursor()
            keys = ','.join(datas.keys())
            values = ','.join(['%s'] * len(datas))
            sql = 'insert into {table}({keys}) values ({values})'.format(table=table, keys=keys, values=values)
            cursor.execute(sql, tuple(datas.values()))
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            db.rollback()
            print("执行失败->%s" % e)
        finally:
            return flag

class FileHandler(object):
    def __init__(self,name=None,result=None):

        if DATAFLAG['json']:
            FileHandler.write_json(name, result)
        if DATAFLAG['csv']:
            FileHandler.write_csv(name, result)


    @staticmethod
    def write_txt(table,result):
        path=dir_path+'/spiders/'+table+'.txt'
        with open(path, 'a', encoding='utf-8') as f:
            f.write(str(result)+'\n')
    @staticmethod
    def write_json(table,result):
        lock.acquire()
        path = dir_path + '/spiders/' + table + '.json'
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + ',\n')
        lock.release()

    @staticmethod
    def write_csv(table, result):
        lock.acquire()
        path = dir_path + '/spiders/' + table + '.csv'
        with open(path, 'a', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow(result.values())
        lock.release()


if __name__ == '__main__':
    pass

