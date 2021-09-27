
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests
import time
import datetime
import json
from nonebot.permission import SUPERUSER


matcher = on_command("授权", permission=SUPERUSER, priority=5)


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
    start = 'EasyBath'.center(30, '-')
    msg = f'{start}\n\n授权账号: {userid}\n截至日期为: {deadline}\n有效期还剩 {ntime} 天 \n\n{start}'
    return msg


def getFutureDays(d):
    d = int(d)
    time.strftime('%Y-%m-%d')
    now_time = datetime.datetime.now()
    future_time = now_time + datetime.timedelta(d)
    fu = future_time.strftime('%Y-%m-%d')
    return fu

# 修改默认参数处理


@matcher.args_parser
async def parse(bot: Bot, event: Event, state: T_State):
    print(state["_current_key"], ":", str(event.get_message()))
    state[state["_current_key"]] = str(event.get_message())


@matcher.handle()
async def first_receive(bot: Bot, event: Event, state: T_State):
    # 获取用户原始命令，如：/test
    print(state["_prefix"]["raw_command"])
    # 处理用户输入参数，如：/test arg1 arg2
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
        # 将参数存入state以阻止后续再向用户询问参数
        state["arg1"] = arg_list[0]
        state["arg2"] = arg_list[1]


@matcher.got("arg1", prompt="好的,请输你希望授权的账号id：")
async def arg_handle(bot: Bot, event: Event, state: T_State):
    # 在这里对参数进行验证
    id = state["arg1"]
    data = isHasUser(id)
    if data:
        userid = data["title"]
        deadline = data["description"]
        ntime = getDiff(deadline)
        start = 'EasyBath'.center(26, '-')
        # await matcher.reject("该用户已在授权库中，请检查输入是否正确,重新输入")
        await matcher.finish(f"{start}\n\n该用户已在授权库中，用户信息如下:\n\n 账户ID:{userid}\n授权截至日期:{deadline}\n剩余可用时间 {ntime} 天\n\n 已为您关闭本次会话,如果需要更新该用户信息请使用 \更新 命令\n\n{start}")


@matcher.got("arg2", prompt="请输入希望授予的用户时长？")
async def arg_handle(bot: Bot, event: Event, state: T_State):
    days = state["arg2"]
    id = state["arg1"]
    deadline = getFutureDays(days)
    dlr = event.get_user_id()
    text = addUser(id, dlr, deadline)
    await matcher.finish(text)
