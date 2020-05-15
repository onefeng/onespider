#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pickle import dumps
from message.redis_queue import *
from schedule.local_schedule import LocalSchedule
from schedule.remote_schedule import RemoteSchedule
from spiders.setings import *
from utils.log_handler import LogHandler
log=LogHandler('alldata')
class Spider(object):
    start_url = []

    def start_request(self):
        """
        构造初始请求
        :return:
        """
        return []
    def local_run(self):
        """
        开始调度
        :return:
        """
        local = LocalSchedule()
        local_set = set()
        start_requests = self.start_request()
        for r in start_requests:
            if dumps(r) not in local_set:
                local_set.add(dumps(r))
                local.request_q.put(dumps(r))
        log.info('加入初始请求')
        local.main()

    def remove_run(self):
        """
        redis远程队列
        :return:
        """
        start_requests = self.start_request()
        for r in start_requests:
            if request_set.add(dumps(r)):
                request_q.put(dumps(r))
        log.info('加入初始请求')
        test = RemoteSchedule()
        test.main()

    def run(self):
        """
        运行程序
        :return:
        """
        if request_queue == 1:
            log.info('调度本地请求')
            self.local_run()

        elif request_queue == 2:
            log.info('调度远程请求')
            self.remove_run()
        else:
            log.info('参数配置错误')
