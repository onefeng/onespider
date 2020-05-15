#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import yaml

class ConfigManager(object):

    def __init__(self):
        self.yaml_setting = self.get_yaml()

    def get_yaml(self):
        """
        解析 yaml
        :return: s  字典
        """
        #path = os.path.split(os.path.realpath(__file__))[0]+'/config.yaml'
        path = os.path.dirname(__file__)+'/config.yaml'
        try:
            with open(path, 'r', encoding='utf-8') as file:
                config = yaml.load(file, Loader=yaml.Loader)
            return config
        except Exception as error:
            print(error)
        return None

if __name__=='__main__':
    x=ConfigManager()
    y=x.get_yaml()
    print(y['datasouce']['postgresql'])
