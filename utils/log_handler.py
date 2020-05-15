#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from logging.handlers import TimedRotatingFileHandler
import logging
import os

class LogHandler(logging.Logger):
    """
    LogHandler
    """
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, name, level=logging.DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.set_stream()
        if file:
            self.set_file()


    def set_file(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """
        file_name = self.dir_path+'/log/'+'{name}.log'.format(name=self.name)
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15,encoding='utf-8')
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(pathname)s[line:%(lineno)d] %(levelname)s %(message)s')

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def set_stream(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(pathname)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def reset_name(self, name):
        """
        reset name
        :param name:
        :return:
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.set_file()


if __name__ == '__main__':
    log = LogHandler('hhh')
    x=5
    log.info('this is a test msg'+str(x))

