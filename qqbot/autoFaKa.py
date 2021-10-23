from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
import nonebot.adapters.cqhttp
import requests
import time
import datetime
import json
import re

matcher = on_regex("(\d{11})购买的(趣智|汇优)热水解锁", priority=1)

def getDiff(date_str):
    now_time = time.localtime(time.time())
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    date1 = datetime.datetime(
        compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
    dayCount = (date1 - date2).days
    return dayCount


def QYWXNotify(title, content):
    try:
        text = f'{title}\n\n{content}'
        QYWX_KEY = '5ecd6ec2-2039-4ca0-a9d9-dcaeaa9b4e74'
        url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={QYWX_KEY}'
        body = json.dumps({
            "msgtype": "text",
            "text": {
                "content": f'{text}',
                # "mentioned_list": ["wangqing", "@all"],
                # "mentioned_mobile_list": ["13800001111", "@all"]
            }
        })
        response = requests.post(url, data=body)
        result = response.json()
        print(result)
    except:
        print('消息发送失败')

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


def addUser(tel, dlr, deadline):
    dic = {"3058649832": 1, "2642831696": 2,
           "779544383": 3, "2633188067": 4, "2026501285": 5}
    dlId = dic[dlr]
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {"title": tel, "description": deadline}

    res = requests.post(
        f'http://47.98.173.224:5700/users/{dlId}/items/', headers=headers, data=json.dumps(data))
    data = res.json()
    print(data)
    userid = data["title"]
    deadline = data["description"]
    ntime = getDiff(deadline)
    start = 'EasyBath'.center(26, '-')
    msg = f'{start}\n\n新用户自动授权成功\n授权账号ID：{userid}\n截至日期为: {deadline}\n有效期还剩 {ntime} 天 \n\n{start}'
    return msg


def getFutureDays(d):
    d = int(d)
    time.strftime('%Y-%m-%d')
    now_time = datetime.datetime.now()
    future_time = now_time + datetime.timedelta(d)
    fu = future_time.strftime('%Y-%m-%d')
    return fu


def updateUser(tel, item_id, deadline, qq_id):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {"title": tel, "description": deadline}
    res = requests.put(
        f'http://47.98.173.224:5700/items/{item_id}', headers=headers, data=json.dumps(data))
    data = res.json()
    print(data)
    userid = data["title"]
    deadline = data["description"]
    ntime = getDiff(deadline)
    start = 'EasyBath'.center(30, '-')
    msg = f'{start}\n\n用户自动续授权成功\n续授权账号：{userid}\n截至日期为: {deadline}\n有效期还剩 {ntime} 天 \n\n{start}'
    QYWXNotify(qq_id, msg)
    return msg

@matcher.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    qq = event.get_user_id()
    msg = str(event.get_message())
    bot = nonebot.get_bot()
    print(f'msg:{type(msg)}')
    user_lst = ["2831187603",'779544383','3058649832']
    if qq in user_lst:
        tel = re.search(r'\d{11}', msg)[0]
        data = isHasUser(tel)
        dlr = "3058649832"
        days = "30"
        if data:
            deadline = data["description"]
            item_id = data['id']
            nCount = getDiff(deadline)
            if nCount > 0:
                addDay = int(days) + int(nCount)
                nDay = getFutureDays(addDay)
            else:
                nDay = getFutureDays(days)
            # await update.send('开始更新用户信息')
            msg = updateUser(tel, item_id, nDay, dlr)
        else:
            nDay = getFutureDays(days)
            msg = addUser(tel,dlr,nDay)
        await bot.send_private_msg(user_id=3058649832, message=msg)
        await matcher.finish(msg)
    else:
        await matcher.finish("非授权用户，无相应权限哦")
