# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datasource.RedisClient import RedisClient

def clear():
    pool=RedisClient()
    conn=pool.get_conn
    conn.delete('request')
    conn.delete('request_set')

if __name__ == '__main__':
    clear()