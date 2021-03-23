from telethon import TelegramClient, events, sync

import httpx
# import yaml
import time
import json
import os
import re
import asyncio
import logging
from typing import Final

# pip3 install telethon pysocks httpx 或者 py -3 -m pip install telethon pysocks httpx
# path: Final = "D:/1.ScriptsWorkSpace/jdDailyTask"

JD_COOKIE = [
  'pt_key=AAJgK-BMADDxtsnTZPrpnN4YZgWiocJRTsFOz1nKn8qnAPMm5SrkXXUkl1js4cWjSY_CjYEMAH4; pt_pin=jd_7c7de935d2d9f;',
  'pt_key=AAJgK-FfADA3Rih0l6-W9WA_acoX3sdfdp4dWFMvqLFgA7wwloPa1iPKEzNbHMjGmhFf0yXRaBg; pt_pin=jd_JVMksbPCFjSo;',
  'pt_key=AAJgK1WdADAqZWH2rcIJRXfTsfODjVgVSptackCWFoEu2ibGGJQNskJ3I7WwDbyeJebVWjcs9Ic; pt_pin=jd_73cf2b923c7ec;',
  'pt_key=AAJgK1rtADBVFTd3jq0K0yQ5fxaaKks-s_6hQvls1Cd_lbOXu-wt-d3AZDy5a1oPmuhQOfpF0QU; pt_pin=jd_5f8b29cd69ac9;'
]


# def get_ck() -> str:
#     with open(os.path.join(path, "serverless.yml"), "r") as f:
#         data: dict = yaml.load(f, Loader=yaml.CLoader)
#     env: dict = data["inputs"]["environment"]["variables"]
#     return "&".join(env["JD_COOKIE"])


# cookies中间用&分开
cks: Final = "&".join(JD_COOKIE)

# url1 = 'https://api.m.jd.com/client.action?functionId=liveDrawLotteryV842&body={"lotteryId":666351,"liveId":3656131}&uuid=8888888&client=apple&clientVersion=9.4.1&st=1615429563038&sign=17c699f8504b22f3e0bf961f7a7d941e&sv=121'


async def send_live(cks, url):
    if len(cks) > 0:
        str_ck = cks.split("&")
        for i in range(1, len(str_ck) + 1):
            if len(str_ck[i - 1]) > 0:
                # print(str_ck[i-1])
                # header
                header = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
                    "Cookie": str_ck[i - 1],
                }
                # 访问url
                async with httpx.AsyncClient() as client:
                    r = await client.get(url=url, headers=header)
                # r = await httpx.get(url=url, headers=header)
                logging.debug(type(r.text))
                logging.info(r.text)
                await asyncio.sleep(0.5)


# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
# 必须填写 api_id api_hash proxy
api_id = "3379205"
api_hash = "2c74bacfec830be90a3f3620e8b81679"
# 使用代理proxy
client = TelegramClient("test", api_id, api_hash, proxy=("socks5", "127.0.0.1", "7890"))
# 不使用代理
# client = TelegramClient('test', api_id, api_hash)

p1: Final = re.compile(r"[(](.*?)[)]", re.S)


@client.on(events.NewMessage(incoming=True, chats="🍉&🐱&🥔", from_users="直播间京豆📢"))
async def my_event_handler(event):
    if "跳转直播间抽奖" in event.raw_text and "抽奖直达" in event.raw_text:
        logging.debug(event.message)
        # if event.message.sender_id == '1663824060':
        sec = re.findall(p1, event.message.text)
        if sec != None and len(sec) == 2:
            await send_live(cks, sec[1])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with client:
        # client.loop.run_until_complete(main())
        client.loop.run_forever()