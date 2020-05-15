#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from process.down_task import RemoteDownProcess
from process.parse_task import RemoteParseProcess
from process.result_task import ResultProcess
from multiprocessing import Manager, Queue

class RemoteSchedule(object):

    def main(self):
        """
        :return:
        """
        response_q = Queue()
        result_q = Queue()
        signal = Manager().dict()
        down = RemoteDownProcess(response_q, signal)
        parse = RemoteParseProcess(response_q, result_q, signal)
        result = ResultProcess(result_q, signal)
        down.start()
        parse.start()
        result.start()
        down.join()
        parse.join()
        result.join()
