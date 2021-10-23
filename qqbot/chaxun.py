from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests
import datetime
import time
import re

weather = on_command("查询")
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


@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["user_id"] = args  # 如果用户发送了参数则直接赋值


@weather.got("user_id", prompt="您希望查询的账号ID为？")
async def handle_user_id(bot: Bot, event: Event, state: T_State):
    try:
        user_id = state["user_id"]
        if not isHasUser(user_id):
            await weather.reject("暂未查询到该用户的授权信息，请确认您是否是已授权用户或检查您的输入是否正确！")
        user_id_weather = await get_weather(user_id)
        # await weather.pause('请输入您想授权的时长')
        await weather.finish(user_id_weather)
    except:
        # await weather.finish("抱歉，出错了，已为您退出本次会话，请您稍后在试")
        pass


async def get_weather(user_id: str):
    pat = re.compile(r'(\d{3})(\d{4})(\d{4})')
    id = pat.sub(r'\1****\3', user_id)
    dic = isHasUser(user_id)
    deadline = dic['description']
    nTime = getDiff(deadline)
    text = f'---------用户信息详情----------\n\n账户ID：{id}\n授权截至日期: {deadline}\n有效期还剩 {nTime} 天\n\n-------------End--------------'
    return text
