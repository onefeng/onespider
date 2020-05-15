#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'onefeng'
from multiprocessing import Process
import threading
import time
from utils.log_handler import LogHandler
from utils.export_handler import FileHandler,DataBaseExport

class ResultProcess(Process):

    log = LogHandler('alldata')
    base_pool = DataBaseExport()
    def __init__(self, result_q, signal):
        super(ResultProcess, self).__init__()
        self.result_q = result_q
        self.signal = signal
    def result_process(self):
        """
        结果写入
        :return:
        """
        while True:
            try:
                result = self.result_q.get(timeout=10)
            except Exception:
                self.log.debug('目前结果队列为空')
                break
            FileHandler(result.table_name, result)
            self.base_pool.output_base(result.table_name, result)

    # def retry(self,flag, results):
    #     times = 0
    #     while not flag:
    #         times += 1
    #         flag = self.con.insertmany(self.table, results)
    #         # print('数据写入失败，正在重新写入')
    #         self.log.info('数据写入失败，正在重新写入')
    #         if times > 3:
    #             self.log.info('数据写入失败超过3次')
    #             break
    # def result_process1(self):
    #     """
    #     结果写入
    #     :return:
    #     """
    #     n = 1
    #     result_list = []
    #     while True:
    #         try:
    #             result = self.result_q.get(timeout=10)
    #             # 需要完善写入失败重试的规则
    #             # 批量写入，减少网络消耗
    #             result_list.append(result)
    #             if n % 100 == 0 or self.result_q.empty():
    #                 n = 1
    #                 print('结果数据长度为', len(result_list))
    #                 flag = self.con.insertmany(self.table, result_list)
    #                 self.retry(flag,result_list)
    #                 result_list = []
    #             else:
    #                 n += 1
    #         except Exception:
    #             self.log.debug('目前结果队列为空')
    #             if result_list:
    #                 #print(result_list)
    #                 flag=self.con.insertmany(self.table, result_list)
    #                 self.retry(flag, result_list)
    #             break

    def run(self, max = 5):
        """
        多线程结果写入
        :return:
        """
        threads = []
        while True:
            if self.result_q.empty():
                if self.signal.get('parse'):
                    self.signal['result'] = True
                    self.log.info('结果处理器已结束')
                    break
                time.sleep(1)
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < max:
                thread = threading.Thread(target=self.result_process)
                thread.start()
                threads.append(thread)
            #self.log.info('线程数量'+str(threading.activeCount()))
            time.sleep(1)
        # 进程结束标志
        #self.signal['result'] = True

if __name__ == '__main__':
    pass
    # data = {
    #     'mysql': MysqlClient(),
    #     'mysql1': MysqlClient()
    # }
    # print(data)
    # for k,v in data.items():
    #     x=v.query('select * from area_base_2019_test limit 10')
    #     print(x)

