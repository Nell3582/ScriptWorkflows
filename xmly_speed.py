import requests
import json
import rsa
import base64
import time
from itertools import groupby
import hashlib
from datetime import datetime, timedelta
import os
import re


# 喜马拉雅极速版
# 使用参考 https://github.com/Zero-S1/xmly_speed/blob/master/xmly_speed.md

###################################################
# 账号1 我主账号 2 老妈 3老爸 4我分号 5 lulu 6
# 对应方案2: 下载到本地,需要此处填写
cookies1 = "1&_device=iPhone&6A4CAE27-22EA-4472-A6D5-30443C970A20&2.0.12; 1&_token=27318049&6772E880340CE59A244ABAB26F3F2FA8AC49453B4D883519D9E0396E86D6F41FCF6D22D6D6E062M47A604224B9342B_; NSUP=; XD=rwrhEiKWmS02qwL826Tn5nlPUjemoGw1mxukkaK8xjzHrjvDHwxIzzY258SFlMy2EheLchGg0snMZdq+puNzpg==; XUM=6A4CAE27-22EA-4472-A6D5-30443C970A20; _xmLog=h5&b02a239c-4af4-4e1a-874b-a919667eb968&2.2.12; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone XR; idfa=00000000-0000-0000-0000-000000000000; impl=com.ximalaya.tingLite; ip=2409:8805:2486:fab9:3a:8704:100:0; net-mode=WIFI; res=828%2C1792"
cookies2 = "1&_device=android&1eb7ccd5-4c30-3331-8581-3e02de1d9d99&2.1.3; channel=and-f5.cpd; impl=com.ximalaya.ting.lite; osversion=25; device_model=LIO-AN00; XUM=CAAnrBUL; XIM=310f3cf8dd366; c-oper=%E6%9C%AA%E7%9F%A5; net-mode=WIFI; NSUP=; AID=5CW+A0kLe5Q=; manufacturer=HUAWEI; umid=90c64418ce29b8617dd5e8b93603df8; xm_grade=1000; appVersion=2.1.3.3; yzChannel=and-f5.cpd; _token=null; _xmLog=h5&5fd6b381-914a-41d1-a93b-716e9116cd61&2.2.5; 1&_token=171372239&F1E41130240CABFA768FB15366AD5AF699977B6FDAA7970C54BB927A42B60B5C1B45885A716F85Mb505e2969D339C8_; res=720%2C0; s&e=c02a908bfa3ed515ae320f3c3314e50a; s&a=%1D[Y%02WSC%05%10%0AX%06%0AVJV%1B%0EXU^%09L%04M%5C^W%0BVK%02VZCSBRWWB[CXVS; XD=z3OeA7QMlB3fccilTonxOGFX9ae8UW1gYhdR6gSFv5hyO+lDBSBEL7RY0kaKn7x1iyVWrveShJPV26ESR0fFpNLMWuFQ5kyiR2sXs2ajs9cwBHT/4dUxaGjL3RsBIHKustXi+Yjct8iddx+JZV1tGXxDk0L0+Gh7+IebFFdO+/gGgAzlWpby+ASapSf7yovm"
cookies3 = "1&_device=android&902e11c4-a851-3983-b883-79c51b26e6b4&2.1.3; channel=and-f5; impl=com.ximalaya.ting.lite; osversion=22; device_model=TAS-AN00; XUM=1CWLMHeo; XIM=310f3e04d8ba6; c-oper=%E6%9C%AA%E7%9F%A5; net-mode=WIFI; res=900%2C1552; NSUP=; AID=krM+eC+pnhk=; manufacturer=HUAWEI; umid=6ebdc02a9a836baf48d5e4f52824bca; xm_grade=1000; appVersion=2.1.3.3; yzChannel=and-f5; _token=null; _xmLog=h5&38437bef-69ec-4683-b335-37fb345ffdde&2.2.5; 1&_token=115184991&EE15AB20140C6DCB054EA473627D6B41556E7F4895CE82A802D222E187DC0AD35FA09F1CF2B4139M241895b4FF60DDF_; XD=793RdaTOmscv6/sMdL2dQ7lQcELrXHSvmdAp2aOqd02rZ5BrXoLsl4ACoeGjubIL4L34HvnNAw75cknKYGJPutOcrAxp9c//xH6wbp+aVbVt8v/m0FCkk9N9O9MK/gTeIZu4mNMYSJOkUBW36EK9iFMimYyjw/n5IyLVzdytNPZZuA3biZRRH4LmxVwWVNgl"
cookies4 = '1&_device=iPhone&6A4CAE27-22EA-4472-A6D5-30443C970A20&2.1.3; 1&_token=290180254&A4BDFD00140C83560A66DFB28B00CD6A12FC150D567666D94D756BF4A2A40320A6AD0AE8118429M47A6042461CE612_; NSUP=; XD=rwrhEiKWmS02qwL826Tn5nlPUjemoGw1mxukkaK8xjzR7Kn0t1vuM9GR4GeO37Lg2pxRWnJuhuG2vt3UIzgjHg==; XUM=6A4CAE27-22EA-4472-A6D5-30443C970A20; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone XR; idfa=00000000-0000-0000-0000-000000000000; impl=com.ximalaya.tingLite; ip=2409:8805:249f:77f0:1a:92a:100:0; net-mode=WIFI; res=828%2C1792; _xmLog=h5&8da53c0d-7d81-4eb9-80f6-58547b78a8c2&2.2.5'
cookies5 = '1&_device=iPhone&CF75A3BB-7BAC-4144-A549-1A16D26F4D22&2.1.3; 1&_token=230208053&82B64C70240CE452900815712C42E83177C21A9D5B9B3E4E5C6BE1B485A00FD3C7504C97527238M7BC5A6273417648_; NSUP=; XD=izhvSlPlLvSm5joQ34cX34xWK36+HXfZpRcHqzVrs6YPi1NH2Nf5SaOqOWt9J7/kmJtS0Jpmo1T+9qWeB4QCYQ==; XUM=CF75A3BB-7BAC-4144-A549-1A16D26F4D22; _xmLog=xm_kl7ljk57w3djo3; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone 6s Plus; idfa=CF75A3BB-7BAC-4144-A549-1A16D26F4D22; impl=com.ximalaya.tingLite; ip=10.170.169.18; net-mode=WIFI; res=1242%2C2208'
cookies6 = '1&_device=iPhone&6A4CAE27-22EA-4472-A6D5-30443C970A20&2.1.3; 1&_token=301469339&7BCF5E00340C0E312B52922E03E631ABF37465A2A1EECABC9E960F470E81399D48D80469B260174M47A604243BADB8C_; NSUP=42EBA6E6%2C42090D9D%2C1614038171648; XD=rwrhEiKWmS02qwL826Tn5nlPUjemoGw1mxukkaK8xjyho3tR48MMUlxftvCNZ3XIWMciWnXB37mN/nF/O1UDbQ==; XUM=6A4CAE27-22EA-4472-A6D5-30443C970A20; _xmLog=xm_klj105ja5oaz49; ainr=0; c-oper=%E6%9C%AA%E7%9F%A5; channel=ios-b1; device_model=iPhone XR; idfa=D251418E-A31B-40DC-AF02-4370024169B6; impl=com.ximalaya.tingLite; ip=2408:853d:32a0:4283:92:8505:100:0; net-mode=WIFI; res=828%2C1792; s&e=5f9f88fe4f707147f2b9429d39e55afa'
cookiesList = [cookies1, cookies2, cookies3,
               cookies4, cookies5, cookies6]   # 多账号准备

# 通知服务
BARK = ''                   # bark服务,自行搜索; secrets可填;形如jfjqxDx3xxxxxxxxSaK的字符串
SCKEY = ''                  # Server酱的SCKEY; secrets可填
TG_BOT_TOKEN = ''           # telegram bot token 自行申请
TG_USER_ID = ''             # telegram 用户ID

###################################################
# 对应方案1:  GitHub action自动运行,此处无需填写;
if "XMLY_SPEED_COOKIE" in os.environ:
    """
    判断是否运行自GitHub action,"XMLY_SPEED_COOKIE" 该参数与 repo里的Secrets的名称保持一致
    """
    print("执行自GitHub action")
    xmly_speed_cookie = os.environ["XMLY_SPEED_COOKIE"]
    cookiesList = []  # 重置cookiesList
    for line in xmly_speed_cookie.split('\n'):
        if not line:
            continue
        cookiesList.append(line)
    # GitHub action运行需要填写对应的secrets
    if "BARK" in os.environ and os.environ["BARK"]:
        BARK = os.environ["BARK"]
        print("BARK 推送打开")
    if "SCKEY" in os.environ and os.environ["SCKEY"]:
        BARK = os.environ["SCKEY"]
        print("serverJ 推送打开")
    if "TG_BOT_TOKEN" in os.environ and os.environ["TG_BOT_TOKEN"] and "TG_USER_ID" in os.environ and os.environ["TG_USER_ID"]:
        TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
        TG_USER_ID = os.environ["TG_USER_ID"]
        print("Telegram 推送打开")


###################################################
# 可选项
# 自定义设备命名,非必须 ;devices=["iPhone7P","huawei"];与cookiesList对应
devices = []
notify_time = 19                            # 通知时间,24小时制,默认19
XMLY_ACCUMULATE_TIME = 1                    # 希望刷时长的,此处置1,默认打开;关闭置0
UserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 iting/1.0.12 kdtunion_iting/1.0 iting(main)/1.0.12/ios_1"
# 非iOS设备的需要的自行修改,自己抓包 与cookie形式类似


def str2dict(str_cookie):
    if type(str_cookie) == dict:
        return str_cookie
    tmp = str_cookie.split(";")
    dict_cookie = {}
    try:
        for i in tmp:
            j = i.split("=")
            if not j[0]:
                continue
            dict_cookie[j[0].strip()] = j[1].strip()

        assert dict_cookie["1&_token"].split("&")[0]
        regex = r"&\d\.\d\.\d+"
        appid = "&1.0.12"
        dict_cookie["1&_device"] = re.sub(
            regex, appid, dict_cookie["1&_device"], 0, re.MULTILINE)
        print(dict_cookie["1&_device"])

    except (IndexError, KeyError):
        print("cookie填写出错 ❌,仔细查看说明")
        raise
    return dict_cookie


def get_time():
    mins = int(time.time())
    date_stamp = (mins-57600) % 86400
    utc_dt = datetime.utcnow()  # UTC时间
    bj_dt = utc_dt+timedelta(hours=8)  # 北京时间
    _datatime = bj_dt.strftime("%Y%m%d", )
    notify_time = bj_dt.strftime("%H %M")
    print(f"\n当前时间戳: {mins}")
    print(f"北京时间: {bj_dt}\n\n")
    return mins, date_stamp, _datatime, notify_time


def read(cookies):
    print("\n【阅读】")
    headers = {
        'Host': '51gzdhh.xyz',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    params = (
        ('hid', '233'),
    )
    try:
        response = requests.get(
            'https://51gzdhh.xyz/api/new/newConfig', headers=headers, params=params)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    result = response.json()
    pid = str(result["pid"])
    headers = {
        'Host': '51gzdhh.xyz',
        'content-length': '37',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    uid = get_uid(cookies)
    data = {"pid": str(pid), "mtuserid": uid}
    try:
        response = requests.post(
            'https://51gzdhh.xyz/api/new/hui/complete', headers=headers, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    result = response.json()
    if result["status"] == -2:
        # print("无法阅读,尝试从安卓端手动开启")
        return
    # print(result["completeList"])
    if result["isComplete"] or result["count_finish"] == 9:
        print("今日完成阅读")
        return
    headers = {
        'Host': '51gzdhh.xyz',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    taskIds = set(['242', '239', '241', '240', '238', '236',
                   '237', '235', '234'])-set(result["completeList"])
    params = (
        ('userid', str(uid)),
        ('pid', pid),
        ('taskid', taskIds.pop()),
        ('imei', ''),
    )
    try:
        response = requests.get(
            'https://51gzdhh.xyz/new/userCompleteNew', headers=headers, params=params)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return 0
    result = response.json()
    print(result)


def ans_receive(cookies, paperId, lastTopicId, receiveType):
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    _checkData = f"""lastTopicId={lastTopicId}&numOfAnswers=3&receiveType={receiveType}"""
    checkData = rsa_encrypt(str(_checkData), pubkey_str)
    data = {
        "paperId": paperId,
        "checkData": checkData,
        "lastTopicId": lastTopicId,
        "numOfAnswers": 3,
        "receiveType": receiveType
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/receive',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return 0
    return response.json()


def stage(cookies):
    # 新手任务
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 iting/2.0.9 kdtunion_iting/1.0 iting(main)/2.0.9/ios_1',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/task/stage-rewards-daily', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    data = response.json()["data"]
    if not data:
        return
    stageRewards = data["stageRewards"]
    for k, v in enumerate(stageRewards, 1):
        print(k, v)
        if v["status"] == 1:
            headers = {
                'Host': 'm.ximalaya.com',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'User-Agent': 'ting_v2.0.9_c5(CFNetwork, iOS 14.3, iPhone9,2)',
                'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
            }
            params = (('stage', f'{k}'),)
            try:
                response = requests.get('https://m.ximalaya.com/speed/web-earn/task/stage-reward/receive',
                                        headers=headers, params=params, cookies=cookies)
            except:
                print("网络请求异常,为避免GitHub action报错,直接跳过")
                return
            print(response.text)


def ans_restore(cookies):
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    checkData = rsa_encrypt("restoreType=2", pubkey_str)

    data = {
        "restoreType": 2,
        "checkData": checkData,
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/restore',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return 0
    result = response.json()
    if "errorCode" in result:
        return 0
    return 1


def ans_getTimes(cookies):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/topic/user', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return {"stamina": 0,
                "remainingTimes": 0}
    print(response.text)
    result = response.json()
    stamina = result["data"]["stamina"]
    remainingTimes = result["data"]["remainingTimes"]
    return {"stamina": stamina,
            "remainingTimes": remainingTimes}


def ans_start(cookies):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/topic/start', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return 0, 0, 0
    # print(response.text)
    result = response.json()

    try:
        paperId = result["data"]["paperId"]
        dateStr = result["data"]["dateStr"]
        lastTopicId = result["data"]["topics"][2]["topicId"]
        print(paperId, dateStr, lastTopicId)
        return paperId, dateStr, lastTopicId
    except:
        print("❌1 重新抓包 2 手动答题")
        return 0, 0, 0


def _str2key(s):
    b_str = base64.b64decode(s)
    if len(b_str) < 162:
        return False
    hex_str = ''
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2
    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]
    return modulus, exponent


def rsa_encrypt(s, pubkey_str):
    key = _str2key(pubkey_str)
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    pubkey = rsa.PublicKey(modulus, exponent)
    return base64.b64encode(rsa.encrypt(s.encode(), pubkey)).decode()


pubkey_str = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVhaR3Or7suUlwHUl2Ly36uVmboZ3+HhovogDjLgRE9CbaUokS2eqGaVFfbxAUxFThNDuXq/fBD+SdUgppmcZrIw4HMMP4AtE2qJJQH/KxPWmbXH7Lv+9CisNtPYOlvWJ/GHRqf9x3TBKjjeJ2CjuVxlPBDX63+Ecil2JR9klVawIDAQAB"


def lottery_info(cookies):
    print("\n【幸运大转盘】")
    """
    转盘信息查询
    """
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/inspire/lottery/info', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    result = response.json()
    remainingTimes = result["data"]["remainingTimes"]
    print(f'转盘info: {result["data"]}\n')
    if remainingTimes in [0, 1]:
        print("今日完毕")
        return
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/inspire/lottery/token', headers=headers, cookies=cookies)
    print("token", response.text)
    token = response.json()["data"]["id"]
    data = {
        "token": token,
        "sign": rsa_encrypt(f"token={token}&userId={get_uid(cookies)}", pubkey_str),
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/chance',
                             headers=headers, cookies=cookies, data=json.dumps(data))

    result = response.json()
    print("chance", result)
    data = {
        "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def index_baoxiang_award(cookies):
    print("\n  【首页、宝箱奖励及翻倍】")
    headers = {
        'User-Agent': UserAgent,
        'Host': 'mobile.ximalaya.com',
    }
    uid = cookies["1&_token"].split("&")[0]
    currentTimeMillis = int(time.time()*1000)-2
    try:
        response = requests.post('https://mobile.ximalaya.com/pizza-category/activity/getAward?activtyId=baoxiangAward',
                                 headers=headers, cookies=cookies)
    except:
        return
    result = response.json()
    print("宝箱奖励: ", result)
    if "ret" in result and result["ret"] == 0:
        awardReceiveId = result["awardReceiveId"]
        headers = {
            'Host': 'mobile.ximalaya.com',
            'Accept': '*/*',
            'User-Agent': UserAgent,
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        params = (
            ('activtyId', 'baoxiangAward'),
            ('awardReceiveId', awardReceiveId),
        )
        try:
            response = requests.get('http://mobile.ximalaya.com/pizza-category/activity/awardMultiple',
                                    headers=headers, params=params, cookies=cookies)
        except:
            print("网络请求异常,为避免GitHub action报错,直接跳过")
            return
        print("翻倍 ", response.text)
    uid = get_uid(cookies)
    ###################################
    params = (
        ('activtyId', 'indexSegAward'),
        ('ballKey', str(uid)),
        ('currentTimeMillis', str(currentTimeMillis)),
        ('sawVideoSignature', f'{currentTimeMillis}+{uid}'),
        ('version', '2'),
    )
    try:
        response = requests.get('https://mobile.ximalaya.com/pizza-category/activity/getAward',
                                headers=headers, cookies=cookies, params=params)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    result = response.json()
    print("首页奖励: ", result)
    if "ret" in result and result["ret"] == 0:
        awardReceiveId = result["awardReceiveId"]
        headers = {
            'Host': 'mobile.ximalaya.com',
            'Accept': '*/*',
            'User-Agent': UserAgent,
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        params = (
            ('activtyId', 'indexSegAward'),
            ('awardReceiveId', awardReceiveId),
        )
        try:
            response = requests.get('http://mobile.ximalaya.com/pizza-category/activity/awardMultiple',
                                    headers=headers, params=params, cookies=cookies)
        except:
            print("网络请求异常,为避免GitHub action报错,直接跳过")
            return
        print("翻倍: ", response.text)


def checkin(cookies, _datatime):
    print("\n【连续签到】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('time', f"""{int(time.time()*1000)}"""),
    )
    try:
        response = requests.get('https://m.ximalaya.com/speed/task-center/check-in/record',
                                headers=headers, params=params, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return 0
    result = json.loads(response.text)
    print(result)
    print(f"""连续签到{result["continuousDays"]}/{result["historyDays"]}天""")
    print(result["isTickedToday"])
    if not result["isTickedToday"]:
        print("!!!开始签到")
        # if result["canMakeUp"]:
        #     print("canMakeUp 第30天需要手动")
        #     return
        headers = {
            'User-Agent': UserAgent,
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'm.ximalaya.com',
            'Origin': 'https://m.ximalaya.com',
            'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        }
        uid = get_uid(cookies)
        data = {
            "checkData": rsa_encrypt(f"date={_datatime}&uid={uid}", pubkey_str),
            "makeUp": False
        }

        response = requests.post('https://m.ximalaya.com/speed/task-center/check-in/check',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        print(response.text)
    return result["continuousDays"]


def ad_score(cookies, businessType, taskId):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain ,*/*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/task-center/ad/token', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    result = response.json()
    token = result["id"]
    uid = get_uid(cookies)
    data = {
        "taskId": taskId,
        "businessType": businessType,
        "rsaSign": rsa_encrypt(f"""businessType={businessType}&token={token}&uid={uid}""", pubkey_str),
    }
    try:
        response = requests.post(f'https://m.ximalaya.com/speed/task-center/ad/score',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    print(response.text)
    print("\n")


def bubble(cookies):
    print("\n【bubble】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-open-components/bubble',
    }
    uid = get_uid(cookies)
    data = {"listenTime": "41246", "signature": "2b1cc9e8831cff8874d9c",
            "currentTimeMillis": "1596695606145", "uid": uid, "expire": False}
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/listen/bubbles',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    result = response.json()
    # print(result)

    if not result["data"]["effectiveBubbles"]:
        print("暂无有效气泡")
        return
    for i in result["data"]["effectiveBubbles"]:
        print(i["id"])

        tmp = receive(cookies, i["id"])
        if "errorCode" in tmp:
            print("❌ 每天手动收听一段时间，暂无其他方法")
            return
        time.sleep(1)
        ad_score(cookies, 7, i["id"])
    for i in result["data"]["expiredBubbles"]:
        ad_score(cookies, 6, i["id"])


def receive(cookies, taskId):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-open-components/bubble',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            f'https://m.ximalaya.com/speed/web-earn/listen/receive/{taskId}', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    print("receive: ", response.text)
    return response.json()


def getOmnipotentCard(cookies, mins, date_stamp, _datatime):
    print("\n 【领取万能卡】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    try:
        count = requests.get('https://m.ximalaya.com/speed/web-earn/card/omnipotentCardInfo',
                             headers=headers, cookies=cookies,).json()["data"]["count"]
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    if count == 5:
        print("今日已满")
        return

    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/1',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
    uid = get_uid(cookies)
    data = {
        "listenTime": mins-date_stamp,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/getOmnipotentCard',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    print(response.text)


def cardReportTime(cookies, mins, date_stamp, _datatime):
    print("\n【收听获得抽卡机会】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    listenTime = mins-date_stamp
    uid = get_uid(cookies)
    data = {"listenTime": listenTime,
            "signData": rsa_encrypt(f"{_datatime}{listenTime}{uid}", pubkey_str), }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/reportTime',
                                 headers=headers, cookies=cookies, data=json.dumps(data)).json()
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    try:
        response["data"]["upperLimit"]
        print("今日已达上限")
    except:
        return


def account(cookies):
    print("\n【 打印账号信息】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': UserAgent,
        'Referer': 'https://m.ximalaya.com/speed/web-earn/wallet',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/account/coin', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return '', '', ''
    result = response.json()
    total = result["total"]/10000
    todayTotal = result["todayTotal"]/10000
    historyTotal = result["historyTotal"]/10000
    print(f"""
当前剩余:{total}
今日获得:{todayTotal}
累计获得:{historyTotal}

""")
    return total, todayTotal, historyTotal


def answer(cookies):
    print("\n【答题】")
    ans_times = ans_getTimes(cookies)
    if not ans_times:
        return
    if ans_times["stamina"] == 0:
        print("时间未到")
    for _ in range(ans_times["stamina"]):
        paperId, _, lastTopicId = ans_start(cookies)
        if paperId == 0:
            return
        tmp = ans_receive(cookies, paperId, lastTopicId, 1)
        print(tmp)
        if "errorCode" in tmp:
            print("❌ 每天手动收听一段时间，暂无其他方法")
            return
        time.sleep(1)
        tmp = ans_receive(cookies, paperId, lastTopicId, 2)
        print(tmp)
        if tmp == 0:
            return
        time.sleep(1)

    if ans_times["remainingTimes"] > 0:
        print("[看视频回复体力]")
        if ans_restore(cookies) == 0:
            return
        for _ in range(5):
            paperId, _, lastTopicId = ans_start(cookies)
            if paperId == 0:
                return
            tmp = ans_receive(cookies, paperId, lastTopicId, 1)
            print(tmp)
            if "errorCode" in tmp:
                print("❌ 每天手动收听一段时间，暂无其他方法")
                return
            time.sleep(1)
            tmp = ans_receive(cookies, paperId, lastTopicId, 2)
            print(tmp)
            if tmp == 0:
                return
            time.sleep(1)


def saveListenTime(cookies, date_stamp):
    print("\n【刷时长1】")
    headers = {
        'User-Agent': UserAgent,
        'Host': 'mobile.ximalaya.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    listentime = date_stamp
    print(f"上传本地收听时长1: {listentime//60}分钟")
    currentTimeMillis = int(time.time()*1000)-2
    uid = get_uid(cookies)
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        'activtyId': 'listenAward',
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        'nativeListenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }
    try:
        response = requests.post('http://mobile.ximalaya.com/pizza-category/ball/saveListenTime',
                                 headers=headers, cookies=cookies, data=data)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    print(response.text)


def listenData(cookies, date_stamp):
    print("\n【刷时长2】")
    headers = {
        'User-Agent': 'ting_v1.1.9_c5(CFNetwork, iOS 14.0.1, iPhone9,2)',
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json',
    }
    listentime = date_stamp-1
    print(f"上传本地收听时长2: {listentime//60}分钟")
    currentTimeMillis = int(time.time()*1000)
    uid = get_uid(cookies)
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }
    try:
        response = requests.post('http://m.ximalaya.com/speed/web-earn/listen/client/data',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    print(response.text)


def card_exchangeCoin(cookies, themeId, cardIdList, _datatime):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/3',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
    uid = get_uid(cookies)
    data = {
        "cardIdList": cardIdList,
        "themeId": themeId,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
    }
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCoin',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    print("card_exchangeCoin: ", response.text)


def card_exchangeCard(cookies, toCardAwardId, fromRecordIdList):
    fromRecordIdList = sorted(fromRecordIdList)
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    data = {
        "toCardAwardId": toCardAwardId,
        "fromRecordIdList": fromRecordIdList,
        "exchangeType": 1,
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCard',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    print(response.text)


def draw_5card(cookies, drawRecordIdList):  # 五连抽
    drawRecordIdList = sorted(drawRecordIdList)
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    uid = get_uid(cookies)
    data = {
        "signData": rsa_encrypt(f"{''.join(str(i) for i in drawRecordIdList)}{uid}", pubkey_str),
        "drawRecordIdList": drawRecordIdList,
        "drawType": 2,
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/draw',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    print("五连抽: ", response.text)


def card(cookies, _datatime):
    print("\n【抽卡】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接跳过")
        return
    data = response.json()["data"]
    #######
    # 5连抽
    drawRecordIdList = data["drawRecordIdList"]
    print("抽卡机会: ", drawRecordIdList)
    for _ in range(len(drawRecordIdList)//5):
        tmp = []
        for _ in range(5):
            tmp.append(drawRecordIdList.pop())
        draw_5card(cookies, tmp)
    ########
    # 手牌兑换金币
    # 1 万能卡  10 碎片
    print("检查手牌，卡牌兑金币")
    themeId_id_map = {
        2: [2, 3],
        3: [4, 5, 6, 7],
        4: [8, 9, 10, 11, 12],
        5: [13, 14, 15, 16, 17, 18],
        6: [19, 20, 21, 22],
        7: [23, 24, 25, 26, 27],
        8: [28, 29, 30, 31, 32],
        9: [33, 34, 35, 36, 37]
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    except:
        return
    data = response.json()["data"]
    userCardsList = data["userCardsList"]  # 手牌
    lstg = groupby(userCardsList, key=lambda x: x["themeId"])
    for key, group in lstg:
        if key in [1, 10]:
            continue
        themeId = key
        ids = list(group)
        tmp_recordId = []
        tmp_id = []
        for i in ids:
            if i["id"] in tmp_id:
                continue
            tmp_recordId.append(i["recordId"])
            tmp_id.append(i["id"])
        if len(tmp_recordId) == len(themeId_id_map[key]):
            print("可以兑换")
            card_exchangeCoin(cookies, themeId, tmp_recordId, _datatime)
    ###############
    # 万能卡兑换稀有卡
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    data = response.json()["data"]
    userCardsList = data["userCardsList"]
    omnipotentCard = [i for i in userCardsList if i["id"] == 1]
    cityCardId = [i["id"] for i in userCardsList if i["themeId"] == 9]
    need = set(themeId_id_map[9])-set(cityCardId)

    print("万能卡: ", [i['recordId'] for i in omnipotentCard])
    for _ in range(len(omnipotentCard)//4):
        tmp = []
        for _ in range(4):
            tmp.append(omnipotentCard.pop())
        fromRecordIdList = [i['recordId'] for i in tmp]
        if need:
            print("万能卡兑换稀有卡:")
            card_exchangeCard(cookies, need.pop(), fromRecordIdList)


def get_uid(cookies):
    return cookies["1&_token"].split("&")[0]


def serverJ(title, content):
    print("\n")
    sckey = SCKEY
    if "SCKEY" in os.environ:
        """
        判断是否运行自GitHub action,"SCKEY" 该参数与 repo里的Secrets的名称保持一致
        """
        sckey = os.environ["SCKEY"]

    if not sckey:
        print("server酱服务的SCKEY未设置!!\n取消推送")
        return
    print("serverJ服务启动")
    data = {
        "text": title,
        "desp": content.replace("\n", "\n\n")+"\n\n [打赏作者](https://github.com/Zero-S1/xmly_speed/blob/master/thanks.md)"
    }
    response = requests.post(f"https://sc.ftqq.com/{sckey}.send", data=data)
    print(response.text)


def bark(title, content):
    print("\n")
    bark_token = BARK
    if "BARK" in os.environ:
        bark_token = os.environ["BARK"]
    if not bark_token:
        print("bark服务的bark_token未设置!!\n取消推送")
        return
    print("bark服务启动")
    response = requests.get(
        f"""https://api.day.app/{bark_token}/{title}/{content}""")
    print(response.text)


def telegram_bot(title, content):
    print("\n")
    tg_bot_token = TG_BOT_TOKEN
    tg_user_id = TG_USER_ID
    if "TG_BOT_TOKEN" in os.environ and "TG_USER_ID" in os.environ:
        tg_bot_token = os.environ["TG_BOT_TOKEN"]
        tg_user_id = os.environ["TG_USER_ID"]
    if not tg_bot_token or not tg_user_id:
        print("Telegram推送的tg_bot_token或者tg_user_id未设置!!\n取消推送")
        return
    print("Telegram 推送开始")
    send_data = {"chat_id": tg_user_id, "text": title +
                 '\n\n'+content, "disable_web_page_preview": "true"}
    response = requests.post(
        url='https://api.telegram.org/bot%s/sendMessage' % (tg_bot_token), data=send_data)
    print(response.text)


def run():
    print(f"喜马拉雅极速版 (https://github.com/Zero-S1/xmly_speed/blob/master/xmly_speed.md ) ,欢迎打赏¯\(°_o)/¯")
    mins, date_stamp, _datatime, _notify_time = get_time()
    table = []
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        if XMLY_ACCUMULATE_TIME == 1:
            saveListenTime(cookies, date_stamp)
            listenData(cookies, date_stamp)
        stage(cookies)
        read(cookies)  # 阅读
        bubble(cookies)  # 收金币气泡
        # continue
        continuousDays = checkin(cookies, _datatime)  # 自动签到
        # lottery_info(cookies)  # 大转盘4次
        answer(cookies)      # 答题赚金币
        cardReportTime(cookies, mins, date_stamp, _datatime)  # 卡牌
        getOmnipotentCard(cookies, mins, date_stamp, _datatime)  # 领取万能卡
        card(cookies, _datatime)  # 抽卡
        index_baoxiang_award(cookies)  # 首页、宝箱奖励及翻倍
        total, todayTotal, historyTotal = account(cookies)
        try:
            device = devices[k]
        except IndexError:
            device = cookies['device_model']
        else:
            device = f"设备{k+1}"

        table.append((device, total, todayTotal,
                      historyTotal, continuousDays,))

        print("###"*20)
        print("\n"*4)
    if _notify_time.split()[0] == str(notify_time) and int(_notify_time.split()[1]) > 30:
        # if 1:
        message = ''
        for i in table:
            message += f"[{i[0].replace(' ',''):<9}]: {i[1]:<6.2f} (＋{i[2]:<4.2f}) {i[3]:<7.2f} {i[4]}\\30\n"
        message += "⭕tips:第30天需要手动签到 by zero_s1, (*^_^*)欢迎打赏 "
        if len(table) <= 4:
            message = "【设备】| 当前剩余 | 今天| 历史| 连续签到\n"+message

        bark("⏰ 喜马拉雅极速版", message)
        serverJ("⏰ 喜马拉雅极速版", message)
        telegram_bot("⏰ 喜马拉雅极速版", message)


if __name__ == "__main__":
    run()
