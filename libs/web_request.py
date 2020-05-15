# !/usr/bin/python
# -*- coding: UTF-8 -*-

from requests import Request
import random
import requests
from spiders.setings import proxy_url,cokies_url
class WebRequest(Request):
    def __init__(self, method='GET',callback=None, need_proxy=False, fail_time=0,*args, **kwargs):
        Request.__init__(self, method, *args, **kwargs)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
    @property
    def user_agent(self):
        """
        return an User-Agent at random
        :return:
        """
        user_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        return random.choice(user_list)

    @property
    def random_header(self):
        """
        basic header
        :return:
        """
        return {'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.8'
                ''}
    @property
    def random_cookies(self):
        jar=requests.cookies.RequestsCookieJar()
        cookies_list = [
            'BIDUPSID=213ACD701B3EC9DCDD72FBA8F78A1C16; PSTM=1562745779; BAIDUID=8EFF220C44943FC9951C80B2AF456106:FG=1; bdshare_firstime=1564455793261; BDUSS=p-LVlyY282WjQ0TkEweWdydlR3NXI3WGNPVnlUdjlER0VnSHloWjZLSUd-N0JkRVFBQUFBJCQAAAAAAAAAAAEAAACIX1CBenjI58j0s~W8-wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZyiV0GcoldZW; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_pvi=2938783744; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=7; H_PS_PSSID=1421_21111_20697_29522_29721_29568_29220_26350; BDSFRCVID=IJusJeCCxG3JggRwZuXva0MZQ0FOeQZRddMu3J; H_BDCLCKID_SF=tR30WJbHMTrDHJTg5DTjhPrMyt6tbMT-027OKKOF5b3CfUcGWbjHDMul0H3lW-QIyHrb0p6athF0HPonHjDaDTQB3J; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1568858068,1569288651,1569312703,1569638650; bdindexid=9nha022850qcs8k80ihjh1vf06; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1569638658',
            #'BAIDUID=7E44519D5AFA576AF3AB84E299C51F69:FG=1; BIDUPSID=7E44519D5AFA576AF3AB84E299C51F69; PSTM=1560574842; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=1; H_PS_PSSID=; BDUSS=BYc0NuNzJmU3BhTnFxaWFldVhOOUZpYldDYWRLTFlMTVFHNGRKWDlwa0lGc2xlRVFBQUFBJCQAAAAAAAAAAAEAAAAAs3z05Ozk7MLkwuTA5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAiJoV4IiaFeeH; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1585725806,1585795580,1587384512,1587644856; bdindexid=ta525t37ldr8k6d6b9nrfp9804; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1587644866; RT="z=1&dm=baidu.com&si=ktfy45e5c5&ss=k9cqr45d&sl=4&tt=6xe&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=eul"',
            #'BAIDUID=7E44519D5AFA576AF3AB84E299C51F69:FG=1; BIDUPSID=7E44519D5AFA576AF3AB84E299C51F69; PSTM=1560574842; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=1; H_PS_PSSID=; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; bdindexid=ta525t37ldr8k6d6b9nrfp9804; BDUSS=lBaaDVERGNrWk5tYllVNnA5c3o4NG50a2VQNERCRmZ4NDNGSlF5QWlXRXlHTWxlRVFBQUFBJCQAAAAAAAAAAAEAAABCi1c2yLzH6bvwyK0wOQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADKLoV4yi6FeV; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1585795580,1587384512,1587644856,1587645239; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1587645244; '
        ]
        cookies=random.choice(cookies_list)
        for cookie in cookies.split(';'):
            key,value=cookie.split('=',1)
            jar.set(key,value)
        return jar
    @property
    def random_proxy(self):
        """
        从代理池获取代理
        :return:
        """
        try:
            response = requests.get(proxy_url)
            if response.status_code == 200:
                return response.text
            return None
        except requests.ConnectionError:
            return None