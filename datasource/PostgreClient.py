#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
postgre数据库连接池
"""
import pg8000
from DBUtils.PersistentDB import PersistentDB
from config.ConfigManager import ConfigManager
import logging
class PostgreClient(object):
    config = ConfigManager()
    postgre_account = config.yaml_setting['datasouce']['postgresql']

    def __init__(self):
        """
        初始化连接
        """
        try:
            self._pool = PersistentDB(creator=pg8000, maxusage=None, threadlocal=None,
                                setsession=[], ping=0, closeable=False, **self.postgre_account)
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
            cursor.execute(sql, tuple(datas.values()))
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            logging.exception(e)
            db.rollback()
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
            logging.exception(e)
            db.rollback()
        finally:
            return results
    def split_sql(self,sql):
        sqllist = sql.split(';')
        return sqllist[0:-1]

    def noquery(self, sqls):
        """
        数据库非查询操作,删除，建表，赋权，更新等操作
        :param sql:需要执行的语句,可支持多条以";"为分隔的事务操作，每一句sql必须加";" ！！！
        :return:返回逻辑值
        """
        flag = False
        try:
            db = self.get_conn()
            cursor = db.cursor()
            #cursor.execute(sql)
            for sql in self.split_sql(sqls):
                cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            logging.exception(e)
            db.rollback()
        finally:
            return flag


if __name__=='__main__':
    y=PostgreClient()
    sql='''
    select '农产品优势网商（全网）' var0,'201912S' var1,'盐源苹果' var2 ,'' var3,x.shop_name,x."type",x.money,x.first_addr,x.second_addr,x.third_addr,'凉山 ' var4,'5134' var5,'全网'var6
            from(
            select shop_name,"type",first_addr,second_addr,third_addr,
            sum(
            COALESCE(month_money_01,0)+COALESCE(month_money_02,0)+COALESCE(month_money_03,0)
            +COALESCE(month_money_04,0)+COALESCE(month_money_05,0)+COALESCE(month_money_06,0)
            +COALESCE(month_money_07,0)+COALESCE(month_money_08,0)+COALESCE(month_money_09,0)
            +COALESCE(month_money_10,0)+COALESCE(month_money_11,0)+COALESCE(month_money_12,0)
            ) as money
            FROM gather_taobao.ir_taobao_product_trade_china_2019 a
            WHERE first_addr not in ('台湾','香港','澳门') and
            (prod_name~'苹果'and prod_name~'盐源'and(prod_name~'四川|凉山' or substr(cast(prod_detail_factory_addrid as varchar) ,1,4)='5134' or produce_second_addr~'凉山') and (agri_firstcat notnull or first_cat~'食品保健'))
            group by  1,2,3,4,5
            order by money desc
            limit 20) x
    '''
    print(y.query(sql))