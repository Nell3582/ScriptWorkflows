import calendar
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests
import datetime
import time
import calendar

from nonebot.permission import SUPERUSER



myuser = on_command("用户", permission=SUPERUSER, priority=6)


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


def getFirstAndLastDay():
    # 获取当前年份
    year = datetime.date.today().year
    # 获取当前月份
    month = datetime.date.today().month
    # 获取当前月的第一天的星期和当月总天数
    weekDay, monthCountDay = calendar.monthrange(year, month)
    # 获取当前月份第一天
    firstDay = datetime.date(year, month, day=1).strftime('%Y-%m-%d')
    # 获取当前月份最后一天
    lastDay = datetime.date(
        year, month, day=monthCountDay).strftime('%Y-%m-%d')
    # 返回第一天和最后一天
    return firstDay, lastDay

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


def getDiff(date_str):
    now_time = time.localtime(time.time())
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    date1 = datetime.datetime(
        compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
    dayCount = (date1 - date2).days
    return dayCount


def getNextMonthEndDay():
    today = datetime.date.today().strftime('%Y-%m-%d')
    time = datetime.datetime.strptime(today, '%Y-%m-%d')
    first_day = datetime.date(time.year, time.month, 1)
    days_num = calendar.monthrange(first_day.year, first_day.month)[
        1]  # 获取一个月有多少天
    end_day_of_next_month = first_day + \
        datetime.timedelta(days=days_num+30)  # 当月的最后一天只需要days_num-1即可
    print(end_day_of_next_month.strftime('%Y-%m-%d'))
    return end_day_of_next_month.strftime('%Y-%m-%d')


@myuser.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["choice"] = args  # 如果用户发送了参数则直接赋值


@myuser.got("choice", prompt=('查询所有推广用户信息请输入 1\n查询本月有效推广用户信息请输入 2'))
async def handle_user_id(bot: Bot, event: Event, state: T_State):
    choice = state['choice']
    qq_id = event.get_user_id()
    try:
        owner_id = getOwnerID(qq_id)
        res = requests.get(
            f"http://47.98.173.224:5700/users/{owner_id}").json()
        items_lst = res['items']
        n = 1
        lst = []
        if choice == "1":
            for dic in items_lst:
                user_id = dic['title']
                deadline = dic['description']
                num = "{:0>2d}".format(n)
                user_id = dic['title'][-6:]
                deadline = dic['description']
                str = f'{num}  |  {user_id}  |  {deadline}'
                lst.append(str)
                n += 1
            table = "\n".join(lst)
            await myuser.finish(table)
        elif choice == "2":
            end = getFirstAndLastDay()[1]
            for dic in items_lst:
                user_id = dic['title']
                deadline = dic['description']
                if deadline >= end:
                    num = "{:0>2d}".format(n)
                    user_id = dic['title'][-4:]
                    deadline = dic['description']
                    str = f'{num}  |  {user_id}  |  {deadline}'
                    lst.append(str)
                    n += 1
            table = "\n".join(lst)
            await myuser.finish(table)
        else:
            await myuser.reject("不合法的数据输入，请重新输入\n查询所有推广用户信息请输入 1\n查询本月有效推广用户信息请输入 2")
    except:
        await myuser.finish('信息获取完毕，已自动为你退出回话')



