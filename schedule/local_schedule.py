# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'onefeng'
from multiprocessing import Manager, Queue
from process.down_task import DownProcess
from process.parse_task import ParseProcess
from process.result_task import ResultProcess


class LocalSchedule(object):
    def __init__(self):
        self.request_q = Queue()

    def main(self):
        """
        初始任务并调度各个进程
        :return:
        """
        response_q = Queue()
        result_q = Queue()
        signal=Manager().dict()
        down = DownProcess(self.request_q, response_q, signal)
        parse = ParseProcess(self.request_q, response_q, result_q, signal)
        result = ResultProcess(result_q, signal)
        down.start()
        parse.start()
        result.start()
        down.join()
        parse.join()
        result.join()
