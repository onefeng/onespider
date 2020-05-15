#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'onefeng'

from multiprocessing import Process
import threading
import time
from utils.log_handler import LogHandler
from pickle import dumps, loads
from libs.web_request import WebRequest
from message.redis_queue import *

class ParseProcess(Process):
    log = LogHandler('alldata')
    def __init__(self, request_q,response_q, result_q, signal):
        super(ParseProcess, self).__init__()
        self.request_q = request_q
        self.response_q = response_q
        self.result_q = result_q
        self.signal = signal
        self.request_set=set()


    def retry(self, new_response):
        """
        错误处理
        :param new_request: 请求失败后才切换代理，这里我设置为False方便测试
        :return:
        """
        new_response['fail_time'] = new_response['fail_time'] + 1
        self.log.error('数据处理失败'+str(new_response['fail_time'])+ '次'+new_response['response'].url)
        if new_response['fail_time'] < 10:
            x = WebRequest(url=new_response['response'].url, callback=new_response['callback'], need_proxy=False)
            self.request_q.put(dumps(x))
            self.log.info('加入请求队列重试')
    def parse_process(self):
        """
        从响应队列解析出内容，将内容加入结果队列，
        将解析出新的请求加入请求队列
        :return:
        """
        while True:
            try:
                response1 = loads(self.response_q.get(timeout=10))
                response = response1['response']
            except Exception:
                self.log.debug('目前响应队列为空')
                break
            response.encoding = 'gb2312'
            #print(response.url,response.status_code,response.text)
            back = response1['callback']

            results = list(back(response))
            # results什么也没解析出来要重新构造请求
            if results:
                for result in results:
                    if isinstance(result, dict):
                        self.result_q.put(result)
                    else:
                        # 这里需要对已有的请求去重
                        if dumps(result) not in self.request_set:
                            self.request_set.add(dumps(result))
                            self.request_q.put(dumps(result))
            else:
                #为做测试代理设置为False
                self.retry(response1)
                self.log.info('解析失败')
    def run(self, max=2):
        """
        多进程从响应队列中取出响应
        :param max:
        :return:
        """
        processes = []
        while True:
            if self.response_q.empty():
                #print('响应队列为空',self.signal.get('down'))
                if self.signal.get('down'):
                    self.signal['parse'] = True
                    self.log.info('解析器已结束')
                    break
                time.sleep(1)
            for process in processes:
                if not process.is_alive():
                    processes.remove(process)
            while len(processes) < max:
                process = Process(target=self.parse_process)
                process.start()
                processes.append(process)
            time.sleep(1)

class RemoteParseProcess(ParseProcess):

    def __init__(self, response_q, result_q, signal):
        super(ParseProcess, self).__init__()
        self.response_q = response_q
        self.result_q = result_q
        self.signal = signal
    def retry(self, new_response):
        """
        错误处理
        :param new_request: 请求失败后才切换代理，这里我设置为False方便测试
        :return:
        """
        new_response['fail_time'] = new_response['fail_time'] + 1
        self.log.error('数据处理失败'+str(new_response['fail_time'])+ '次'+new_response['response'].url)
        if new_response['fail_time'] < 10:
            x = WebRequest(url=new_response['response'].url, callback=new_response['callback'], need_proxy=False)
            request_q.put(dumps(x))
            self.log.info('加入请求队列重试')
    def parse_process(self):
        """
        从响应队列解析出内容，将内容加入结果队列，
        将解析出新的请求加入请求队列
        :return:
        """
        while True:
            try:
                response1 = loads(self.response_q.get(timeout=10))
                response = response1['response']
            except Exception:
                self.log.debug('目前响应队列为空')
                break
            response.encoding = 'gb2312'
            #print(response.url,response.status_code,response.text)
            back = response1['callback']

            results = list(back(response))
            # results什么也没解析出来要重新构造请求
            if results:
                for result in results:
                    if isinstance(result, dict):
                        self.result_q.put(result)
                    else:
                        flag = request_set.add(dumps(result))
                        if flag:
                            request_q.put(dumps(result))
            else:
                #为做测试代理设置为False
                self.retry(response1)
                self.log.info('解析失败了')

