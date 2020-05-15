# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__='onefeng'

"""
程序入口
"""
from spiders.area import AreaSpider
from spiders.match import MatchSpider
import time
from utils.log_handler import LogHandler
log=LogHandler('alldata')
def timer(f):
    """
    计时器
    :param f:
    :return:
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        f(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time)
        log.info("运行时间{}秒".format(execution_time))
    return wrapper

@timer
def run():
    """
    程序入口
    :return:
    """
    spider_list={
        #'AreaSpider': AreaSpider(),
        'MatchSpider': MatchSpider(),
    }
    for k,v in spider_list.items():
        print('开始'+k)
        v.run()

if __name__ == '__main__':
    run()
