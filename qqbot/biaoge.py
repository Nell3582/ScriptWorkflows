#!/usr/bin/python
# **coding:utf-8**
import calendar
import datetime
import sys
import prettytable as pt
import requests
import time
import datetime
import arrow
import datetime  # 提供操作日期和时间的类
# from datetime import datetime,timedelta
# from prettytable import PrettyTable
# reload(sys)
# sys.setdefaultencoding('utf8')

table = pt.PrettyTable(['编号', '账号ID', '截至时间'])
# table.add_row(['1','server01','服务器01','172.16.0.1'])
# table.add_row(['2','server02','服务器02','172.16.0.2'])
# table.add_row(['3','server03','服务器03','172.16.0.3'])
# table.add_row(['4','server04','服务器04','172.16.0.4'])
# table.add_row(['5','server05','服务器05','172.16.0.5'])
# table.add_row(['6','server06','服务器06','172.16.0.6'])
# table.add_row(['7','server07','服务器07','172.16.0.7'])
# table.add_row(['8','server08','服务器08','172.16.0.8'])
# table.add_row(['9','server09','服务器09','172.16.0.9'])
# # print(table)
owner_id = 4
res = requests.get(f"http://47.98.173.224:5700/users/{owner_id}").json()
items_lst = res['items']
n = 1
for dic in items_lst:
    num = "{:0>2d}".format(n)
    user_id = dic['title'][-4:]
    deadline = dic['description']
    table.add_row([num, user_id, deadline])
    n += 1

# str = '\n'.join(lst)
print(type(table))


def getDiff(date_str):
    now_time = time.localtime(time.time())
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    date1 = datetime.datetime(
        compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
    dayCount = (date1 - date2).days
    return dayCount


def getFutureDays(d):
    d = int(d)
    time.strftime('%Y-%m-%d')
    now_time = datetime.datetime.now()
    future_time = now_time + datetime.timedelta(d)
    fu = future_time.strftime('%Y-%m-%d')
    return fu



