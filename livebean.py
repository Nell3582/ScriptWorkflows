
#不过滤信息，但只打印抽奖相关信息，需要可自行过滤
#没有代理设置，需要请自行添加

from telethon import TelegramClient, events, sync
import httpx
import json
import re
import asyncio
import os
import requests
import socket  
import socks  
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7890)  
socket.socket = socks.socksocket 

#账号cookie的格式替换xxx，1️⃣2️⃣3️⃣处的字符可以自行替换，前后的0不要动多账号自行增加额外的行
cookies = [
        ['pt_key=AAJgK-BMADDxtsnTZPrpnN4YZgWiocJRTsFOz1nKn8qnAPMm5SrkXXUkl1js4cWjSY_CjYEMAH4; pt_pin=jd_7c7de935d2d9f;', 0, " 1️⃣ ", 0],
        ['pt_key=AAJgK-FfADA3Rih0l6-W9WA_acoX3sdfdp4dWFMvqLFgA7wwloPa1iPKEzNbHMjGmhFf0yXRaBg; pt_pin=jd_JVMksbPCFjSo;', 0, " 2️⃣ ", 0],
        ['pt_key=AAJgK1WdADAqZWH2rcIJRXfTsfODjVgVSptackCWFoEu2ibGGJQNskJ3I7WwDbyeJebVWjcs9Ic; pt_pin=jd_73cf2b923c7ec;', 0, " 3️⃣ ", 0],
        ['pt_key=AAJgK1rtADBVFTd3jq0K0yQ5fxaaKks-s_6hQvls1Cd_lbOXu-wt-d3AZDy5a1oPmuhQOfpF0QU; pt_pin=jd_5f8b29cd69ac9;', 0, " 4️⃣ ", 0]
]

#TGBOT推送
tg_bot_token = '1572513125:AAHDokotZU8dQquPPeg1BJH27oeap0hhDCw'
tg_user_id = '995328749' 

#API信息填写
api_id = "3379205"
api_hash = "2c74bacfec830be90a3f3620e8b81679"

headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
        "Cookie": "",
        }

p1 = re.compile(r"(https.+)\)", re.M)
p2 = re.compile(r'^.+;pt_pin=(.+);$')
p3 = re.compile(r'^([0-9]+)京豆')

count = 0

def get_bean(url):
    z = 0
    totalCouponinfo = ""
    accountNum = 0
    for cookie in cookies:
        headers["Cookie"] = cookie[0]
        res = requests.get(url, headers=headers).json()
        cookiename = re.findall(p2, cookie[0])[0]
        accountinfo = "【账号" +  str(cookie[2]) + "】" +  cookiename 
        if int(res['code']) != 0:
            print("cookie无效")
        else:
            if "恭喜" in res['data']['awardTitle']:
                print(res['data']['awardTitle'], res['data']['couponQuota'])
                if "京豆" in res['data']['couponQuota'] and len(tg_bot_token) != 0: 
                    cookie[1] += 1
                    couponQuotaNum = int(re.findall(p3, res['data']['couponQuota'])[0])
                    cookie[3] += couponQuotaNum
                    couponinfo = "【获得奖品】" + res['data']['couponQuota'] + " 🎉 "
                    winRatio = '【中奖概率】{:.2f}%'.format(cookie[1]/count*100) + " (" + str(cookie[1]) + "/" + str(count) + ")"
                    totalCouponQuotaNum = "【累计获得】" + str(cookie[3]) + "京豆"
                    totalCouponinfo += "\n" + accountinfo + "\n" + couponinfo + "\n" + winRatio + "\n" + totalCouponQuotaNum + "\n"
                    z = 1 
                else:
                    couponinfo = "【获得奖品】" + res['data']['couponQuota'] + " 🙁 "
                    winRatio = '【中奖概率】{:.2f}%'.format(cookie[1]/count*100) + " (" + str(cookie[1]) + "/" + str(count) + ")"
                    totalCouponQuotaNum = "【累计获得】" + str(cookie[3]) + "京豆"
                    totalCouponinfo += "\n" + accountinfo + "\n" + couponinfo + "\n" + winRatio + "\n" + totalCouponQuotaNum + "\n"
            else:
                couponinfo = "【获得奖品】" + res['data']['awardTitle'] + " 🙁 "
                winRatio = '【中奖概率】{:.2f}%'.format(cookie[1]/count*100) + " (" + str(cookie[1]) + "/" + str(count) + ")"
                totalCouponQuotaNum = "【累计获得】" + str(cookie[3]) + "京豆"
                totalCouponinfo += "\n" + accountinfo + "\n" + couponinfo + "\n" + winRatio + "\n" + totalCouponQuotaNum + "\n"
                print(res['data']['awardTitle'])
    if z == 1:
        maintitle = drawTitle[0].split(' ')[0] + "(" + drawTitle[0].split(' ')[1] + ")"
        tgNotify(maintitle, totalCouponinfo)


def tgNotify(title, content):
    boturl=f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'chat_id': str(tg_user_id), 'text': f'{title}\n{content}', 'disable_web_page_preview': 'true'}
    response = requests.post(url=boturl, headers=headers, params=payload).json()
    if response['ok']:
        print('推送成功！')
    else:
        print('推送失败！')

# client = TelegramClient("test", api_id, api_hash, proxy=("socks5", "127.0.0.1", "7890"))
client = TelegramClient('test', api_id, api_hash)
client.start()


@client.on(events.NewMessage)
async def my_event_handler(event):
    global drawTitle
    global count
    if "抽奖直达" in event.raw_text:
        count += 1
        drawTitle = event.raw_text.splitlines()
        print('\n'+drawTitle[0])
        #print(event.message.text)
        sec = re.findall(p1, event.message.text)
        if sec!=None and len(sec)==2:
            get_bean(sec[1])

with client:
    client.loop.run_forever()

