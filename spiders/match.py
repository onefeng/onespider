#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'onefeng'
from libs.web_request import WebRequest
from libs.spider import Spider
import re
from pyquery import PyQuery as pq
from spiders.items import MatchItems,DetailItems
from urllib.parse import urljoin

class MatchSpider(Spider):
    start_url = ['http://www.lottery.gov.cn/football/result.jspx']
    params={'f_league_id': 0, 'f_league_name': '全部联赛','startDate':'2020-01-01','endDate': '2020-01-04'}

    def start_request(self):
        """
        加入初始请求队列
        :return:
        """
        for _ in self.start_url:
            yield WebRequest(url=_, callback=self.parse, params=self.params)

    def parse(self, response):
        response.encoding = 'utf-8'
        doc = pq(response.text)
        # 解析本页数据
        trs = doc('table[cellpadding="1"] tr:has(img)').items()
        pattern = re.compile(r'\d{1,9}', re.S)
        for tr in trs:
            datas = MatchItems()
            match_url = tr('td a').attr('href')
            if match_url:
                datas['match_id'] = re.search(pattern, tr('td a').attr('href')).group()
                datas['match_date'] = tr('td:eq(0)').text()
                datas['match_xuhao'] = tr('td:nth-child(2)').text()
                datas['league'] = tr('td:nth-child(3)').text()
                datas['home'] = tr('td span:nth-child(1)').text()
                datas['guest'] = tr('td span:eq(2)').text()
                datas['half_scorce'] = tr('td:nth-child(5)').text()
                datas['all_scorce'] = tr('td:nth-child(6)').text()
            yield datas
        items = doc('td a:has(img)').items()
        for item in items:
            #url = 'http://www.lottery.gov.cn'+str(item.attr('href'))
            url = urljoin(response.url, str(item.attr('href')))
            new_request = WebRequest(url=url, callback=self.parse_detail)
            yield new_request
        next = doc('a:contains("下一页")').attr('href')
        if next:
            #url1 = 'http://www.lottery.gov.cn/football/'+str(next)
            url1=urljoin(response.url, str(next))
            new_request = WebRequest(url=url1, callback=self.parse)
            yield new_request

    def parse_detail(self, response):
        doc = pq(response.text)
        table = doc('.table1')
        data=DetailItems()
        p = re.compile(r'>\((.*?)\)<')
        r = re.search(p, str(table))
        p1=re.compile(r'\d{6}')
        data['match_id']=re.search(p1, response.url).group()
        if r:
            data['rangqiu']=r.group(1)
        yield data
if __name__ == '__main__':

    x = dict()
    print(x.name)
    x['text']='dd'
    print(x)
