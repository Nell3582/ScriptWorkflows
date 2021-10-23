
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests
import time
import datetime
import json
import os
from nonebot.permission import SUPERUSER


update = on_command("授权", permission=SUPERUSER, priority=5)


def getDiff(date_str):
    now_time = time.localtime(time.time())
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    date1 = datetime.datetime(
        compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
    dayCount = (date1 - date2).days
    return dayCount


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录,创建目录操作函数
        '''
        os.mkdir(path)与os.makedirs(path)的区别是,当父目录不存在的时候os.mkdir(path)不会创建，os.makedirs(path)则会创建父目录
        '''
        # 此处路径最好使用utf-8解码，否则在磁盘中可能会出现乱码的情况
        os.makedirs(path)
        # print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path+' 目录已存在')
        return False

def setFile(filepath, userId):
    mkdir(filepath)
    f = f'./{filepath}/{userId}.json'
    return f


def save_data(account_dic, f):
    with open(f, 'w') as new_f:
        json.dump(account_dic, new_f, sort_keys=True, indent=4)
        print("updata account ")

def load_json(file_path):
    assert file_path.split('.')[-1] == 'json'
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


def formatTimes(userId):
    dic ={}
    f = setFile('inbox', userId)
    if not os.path.exists(f):  # 初始化生成用户数据信息
        todayUsed = 0
        dic['userId'] = userId
        dic['totalUsed'] = 0
        dic['recordtime'] = str(datetime.date.today())
        dic['init_time'] = str(datetime.date.today())
        dic['todayUsed'] = todayUsed
        save_data(dic, f)
        print(f'用户{userId}信息建档成功')
    else:
        data = load_json(f)
        if data['recordtime'] != str(datetime.date.today()):
            data['todayUsed'] = 0
            todayUsed = data['todayUsed']
            print(f'初始化用户 {userId} 本日使用数据')
            data['recordtime'] = str(datetime.date.today())
            print(f'更新用户 {userId} 使用时间为当日')
            save_data(data, f)

# 发送数据获取通知


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

def getData(qq):
    url = "https://gitee.com/Nell3582/Nell9382/raw/master/data/sample.json"  # 等价下面的
    res = requests.get(url).json()
    print(res)
    for dic in res:
        if dic["qmsg"] == qq:
            break
        else:
            dic = False
    return dic

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


def addUser(tel, dlr, deadline, qq_id):
    dic = getData(qq_id)

    if dic:
        dlId = dic["id"]
    else:
        dlId = "999"

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
    msg = f'{start}\n\n新授权账号： {userid} \n授权截至日期: {deadline}\n剩余有效期 {ntime} 天 \n\n{start}'
    f = setFile('inbox', qq_id)
    data = load_json(f)
    data['totalUsed'] += 1
    data['todayUsed'] += 1
    todayUsed = data['todayUsed']
    save_data(data, f)
    content = f'{start}\n新授权账号： {userid} \n授权截至日期: {deadline}\n剩余有效期 {ntime} 天\n代理人ID: {dlId}\n今日第 {todayUsed} 次授权\n\n{start}'
    QYWXNotify(qq_id, content)
    return msg


def updateUser(tel, item_id, deadline, qq_id):
    dic = getData(qq_id)

    if dic:
        dlId = dic["id"]
    else:
        dlId = "999"

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
    msg = f'{start}\n\n续授权账号 {userid} \n截至日期为: {deadline}\n有效期还剩 {ntime} 天 \n\n{start}'
    f = setFile('inbox', qq_id)
    data = load_json(f)
    data['totalUsed'] += 1
    data['todayUsed'] += 1
    todayUsed = data['todayUsed']
    save_data(data, f)
    content = f'{start}\n续授权账号：{userid} \n授权截至日期: {deadline}\n剩余有效期 {ntime} 天\n代理人ID: {dlId}\n今日第 {todayUsed} 次授权\n\n{start}'
    QYWXNotify(qq_id, content)
    return msg


def getFutureDays(d):
    d = int(d)
    time.strftime('%Y-%m-%d')
    now_time = datetime.datetime.now()
    future_time = now_time + datetime.timedelta(d)
    fu = future_time.strftime('%Y-%m-%d')
    return fu

# 修改默认参数处理


@update.args_parser
async def parse(bot: Bot, event: Event, state: T_State):
    print(state["_current_key"], ":", str(event.get_message()))
    state[state["_current_key"]] = str(event.get_message())


@update.handle()
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


@update.got("arg1", prompt="请输你希望授权的账号id：")
async def arg_handle(bot: Bot, event: Event, state: T_State):
    # 在这里对参数进行验证
    id = state["arg1"]


@update.got("arg2", prompt="请输入希望授予的用户时长？")
async def arg_handle(bot: Bot, event: Event, state: T_State):
    days = state["arg2"]
    id = state["arg1"]
    data = isHasUser(id)
    qq_id = event.get_user_id()
    formatTimes(qq_id)
    if data:
        userid = data["title"]
        deadline = data["description"]
        ntime = getDiff(deadline)
        start = 'EasyBath'.center(30, '-')
        # await update.reject("该用户已在授权库中，请检查输入是否正确,重新输入")
        await update.send(f"{start}\n\n用户已在授权库中，信息如下:\n\n账户ID:  {userid}\n授权截至日期:  {deadline}\n剩余可用时间 {ntime} 天\n\n{start}")
        time.sleep(1)
    else:
        deadline = getFutureDays(days)
        dlr = event.get_user_id()
        text = addUser(id, dlr, deadline, qq_id)
        await update.finish(text)


@update.got("choice", prompt="是否更新该用户信息:\n是请输入数字 1 \n否请输入数字 0")
async def arg_handle(bot: Bot, event: Event, state: T_State):
    days = state["arg2"]
    user_id = state["arg1"]
    data = isHasUser(user_id)
    qq_id = event.get_user_id()
    print(state["choice"])
    choic = state["choice"]
    formatTimes(qq_id)
    if choic == "1":
        deadline = data["description"]
        item_id = data['id']
        nCount = getDiff(deadline)
        if nCount > 0:
            addDay = int(days) + int(nCount)
            deadline = getFutureDays(addDay)
        else:
            deadline = getFutureDays(days)
        # await update.send('开始更新用户信息')
        msg = updateUser(user_id, item_id, deadline, qq_id)
        await update.finish(msg)

    elif choic == "0":
        await update.finish('好的,已为您退出授权系统')
    else:
        await update.reject('不合法的输入,请重新输入')
