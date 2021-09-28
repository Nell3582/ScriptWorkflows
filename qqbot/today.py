import requests
import re
import time
import datetime
from nonebot import on_command, require, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
import nonebot.adapters.cqhttp
import _thread


group = {'1':833258227,'2':783384299,'3':519036865,'4':87629913,'5':908326662}
# 获取所有用户信息
def getAllData():

    headers = {
        'accept': 'application/json',
    }

    res = requests.get(
        'http://47.98.173.224:5700/items/?skip=0&limit=10000', headers=headers)
    data = res.json()
    # print(data)
    return data

def getOwnerID(qq):

    headers = {
        'accept': 'application/json',
    }

    res = requests.get(
        'http://47.98.173.224:5700/users/?skip=0&limit=10000', headers=headers)
    lst = res.json()
    for dic in lst:
        if dic['email'] == str(qq):
            owner_id = dic['id']
            break
        else:
            owner_id = 1
    return owner_id



def getDiff(date_str):
    now_time = time.localtime(time.time())
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    date1 = datetime.datetime(
        compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
    dayCount = (date1 - date2).days
    return dayCount

# 判断用户是否已在数据库中存在，如果存在返回其用户信息，如果不存在返回Flase
def isHasUser(tel):
    headers = {
        'accept': 'application/json',
    }

    res = requests.get(
        'http://47.98.173.224:5700/items/?skip=0&limit=1000', headers=headers)
    data = res.json()
    for dic in data:
        if dic["title"] == tel:
            break
        else:
            dic = False
    return dic


scheduler = require('nonebot_plugin_apscheduler').scheduler
 
@scheduler.scheduled_job('cron', hour=10,minute=00)
async def demo():
    bot = nonebot.get_bot()
    res = getAllData()
    pat = re.compile(r'(\d{3})(\d{4})(\d{4})')
    for dic in res:
        id = pat.sub(r'\1****\3', dic['title'])
        deadline = dic['description']
        owner = str(dic['owner_id'])
        group_id = group[owner]
        nTime = getDiff(deadline)
        start = '授权到期提醒'.center(26, '-')
        if -1 < nTime < 3:
            qmsg = f'{start}\n\n用户{id},您好：\n\n您在本站订购的自助热水服务即将到期,为不影响您的使用,请及时申请下一阶段授权,祝您用水愉快！\n\n您的账户详细使用信息如下:\n\n授权账号ID: {id}\n截至使用日期:{deadline}\n可用时长还剩 {nTime} 天\n\n{start}'
            await bot.send_group_msg(group_id=group_id, message=qmsg)


