#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'onefeng'
from libs.web_request import WebRequest
from libs.spider import Spider
import re
from pyquery import PyQuery as pq
from spiders.items import AreaItems

class AreaSpider(Spider):
    start_url=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/51/07/510703.html',
               'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/51/07/510703.html']
    #start_url = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html']

    def start_request(self):
        """
        加入初始请求队列
        :return:
        """
        for _ in self.start_url:
            yield WebRequest(url=_, callback=self.parse)

    def parse_datail(self, response):
        response.encoding = 'gb2312'
        doc = pq(response.text)
        province = doc('.provincetr')
        city = doc('.citytr')
        county = doc('.countytr')
        town = doc('.towntr')
        village = doc('.villagetr')
        if province:
            items = doc('td > a[href]').items()
            for item in items:
                data = AreaItems()
                pattern = re.compile(r'\d{2}', re.S)
                data['area'] = item.text()
                areaid = re.search(pattern, item.attr('href'))
                if areaid:
                    data['area_id'] = areaid.group(0) + '0' * 10
                data['area_level'] = '1'
                data['class_code'] = ''
                yield data
        elif city:
            items = doc('tr.citytr').items()
            for item in items:
                data = AreaItems()
                data['area'] = item('td:eq(1)').text()
                data['area_id'] = item('td:eq(0)').text()
                data['area_level'] = '2'
                data['class_code'] = ''
                yield data
        elif county:
            items = doc('tr.countytr').items()
            for item in items:
                data = AreaItems()
                data['area'] = item('td:eq(1)').text()
                data['area_id'] = item('td:eq(0)').text()
                data['area_level'] = '3'
                data['class_code'] = ''
                yield data
        elif town:
            items = doc('tr.towntr').items()
            for item in items:
                data = AreaItems()
                data['area'] = item('td:eq(1)').text()
                data['area_id'] = item('td:eq(0)').text()
                data['area_level'] = '4'
                data['class_code'] = ''
                yield data
        elif village:
            items = doc('tr.villagetr').items()
            for item in items:
                data = AreaItems()
                data['area'] = item('td:eq(2)').text()
                data['area_id'] = item('td:eq(0)').text()
                data['area_level'] = '5'
                data['class_code'] = item('td:eq(1)').text()
                yield data
    def parse(self, response):
        response.encoding = 'gb2312'
        doc = pq(response.text)
        province = doc('.provincetr')
        detail = self.parse_datail(response)
        for _ in detail:
            yield _
        items_a = doc("a[href$='.html']")
        items = doc("a[href$='.html']:odd")
        if items or items_a:
            if province:
                a = re.sub(r'/[^/]*?\.html$', '/', response.url)
                for item in items_a.items():
                    b = item.attr('href')
                    now_url = a + b
                    new_request = WebRequest(url=now_url, callback=self.parse)
                    yield new_request
            else:
                a = re.sub(r'/[^/]*?\.html$', '/', response.url)
                for item in items.items():
                    b = item.attr('href')
                    now_url = a + b
                    new_request = WebRequest(url=now_url, callback=self.parse)
                    yield new_request




