#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'onefeng'
from multiprocessing import Process

import threading
import time
from utils.log_handler import LogHandler
from pickle import dumps, loads
from requests import Session
from message.redis_queue import *

class DownProcess(Process):
    log = LogHandler('alldata')
    session = Session()
    def __init__(self, request_q,response_q, signal):
        super(DownProcess, self).__init__()
        self.request_q = request_q
        self.response_q = response_q
        self.signal = signal

        # 会话对象更新headers与cookies
        #self.session.headers=''
    def retry(self, new_request):
        """
        错误处理
        :param new_request: 请求失败后才切换代理，这里我设置为False方便测试
        :return:
        """

        new_request.need_proxy = False
        new_request.fail_time = new_request.fail_time + 1
        self.log.error('数据处理失败'+str(new_request.fail_time)+ '次'+new_request.url)
        if new_request.fail_time < 10:
            self.request_q.put(dumps(new_request))
            self.log.info('加入请求队列重试')

    def down_request(self,new_request):
        """
        下载请求的方法
        :param args:
        :param kwargs:
        :return:
        """
        try:
            if new_request.need_proxy:
                proxy = new_request.random_proxy
                if proxy:
                    proxies = {
                        'http': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
                    prepped = self.session.prepare_request(new_request)
                    return self.session.send(prepped, timeout=8, allow_redirects=False, proxies=proxies)
                else:
                    self.log.debug('未获取到代理ip')
            prepped = self.session.prepare_request(new_request)
            r = self.session.send(prepped, timeout=8, allow_redirects=False)
            return r
        except Exception:
            self.log.error('请求失败', exc_info=True)
            return False
    def down_process(self):
        """
        任务处理将从请求队列接收请求并下载为响应，
        加入到响应队列，请求失败则重新加入到请求队列
        :return:
        """
        while True:
            try:
                new_request = loads(self.request_q.get(timeout=10))
            except Exception:
                self.log.info('目前请求队列为空')
                break
            response = self.down_request(new_request)

            if response and response.status_code in [200]:
                new_response={
                    'response':response,
                    'callback':new_request.callback,
                    'fail_time':0
                }
                self.response_q.put(dumps(new_response))
            else:
                self.retry(new_request)

    def run(self, max=10):
        """
        进程运行方法
        :param max:
        :return:
        """
        threads = []
        while True:
            if self.request_q.empty():
                self.log.info('等待一段时间检查队列')
                time.sleep(20)
                if self.request_q.empty(): break
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < max:
                thread = threading.Thread(target=self.down_process)
                thread.start()
                threads.append(thread)
            #self.log.info('线程数量'+str(threading.activeCount()))
            time.sleep(1)
        #进程结束标志
        self.log.info('下载器结束')
        self.signal['down'] = True
class RemoteDownProcess(DownProcess):
    def __init__(self, response_q, signal):
        super(DownProcess, self).__init__()
        self.response_q = response_q
        self.signal = signal

        # 会话对象更新headers与cookies
        #self.session.headers=''
    def retry(self, new_request):
        """
        错误处理
        :param new_request: 请求失败后才切换代理，这里我设置为False方便测试
        :return:
        """

        new_request.need_proxy = False
        new_request.fail_time = new_request.fail_time + 1
        self.log.error('数据处理失败'+str(new_request.fail_time)+ '次'+new_request.url)
        if new_request.fail_time < 10:
            request_q.put(dumps(new_request))
            self.log.info('加入请求队列重试')
    def down_process(self):
        """
        任务处理将从请求队列接收请求并下载为响应，
        加入到响应队列，请求失败则重新加入到请求队列
        :return:
        """
        while True:
            try:
                new_request = loads(request_q.get(timeout=10))
            except Exception:
                self.log.info('目前请求队列为空')
                break
            response = self.down_request(new_request)

            if response and response.status_code in [200]:
                new_response={
                    'response':response,
                    'callback':new_request.callback,
                    'fail_time':0
                }
                self.response_q.put(dumps(new_response))
            else:
                self.retry(new_request)

    def run(self, max=10):
        """
        进程运行方法
        :param max:
        :return:
        """
        threads = []
        while True:
            if request_q.empty():
                self.log.info('等待一段时间检查队列')
                time.sleep(20)
                if request_q.empty() : break
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < max:
                thread = threading.Thread(target=self.down_process)
                self.log.info('这边启动了一个下载线程')
                thread.start()
                threads.append(thread)
            self.log.info('线程数量', threading.activeCount())
            time.sleep(1)
        #进程结束标志
        self.log.info('下载器结束')
        self.signal['down'] = True




