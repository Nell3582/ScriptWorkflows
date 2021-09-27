
import requests
import json
import time
import datetime



# 发送数据获取通知
def QYWXNotify(title, content):
    try:
        text = f'{title}\n\n{content}'
        QYWX_KEY = 'ac8e4b2f-e383-4265-a186-7859ccb90ab5'
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


def getDiff(date_str):
    now_time = time.localtime(time.time())
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    date1 = datetime.datetime(
        compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
    dayCount = (date1 - date2).days
    return dayCount


def getRemoteData():
    url = "https://gitee.com/Nell3582/Nell9382/raw/master/Task/zqkd/JsonData.json"  # 等价下面的
    # url = "https://gitee.com/Nell3582/Nell9382/raw/master/Task/zqkd/JsonData_test.json"  # 等价下面的
    res = requests.get(url).json()
    return res


def notify():
    d = getRemoteData()
    for k, v in d.items():
        usertype = v.split('@')[0]
        deadline = v.split("@")[1]
        nTime = getDiff(deadline)
        if k[0] == "1":
            print("趣智用户")
        else:
            print("旺达水宝")
            if usertype == 'A':
                type = '旺达单人版'
            else:
                type = '旺达宿舍版'
                
        if -1 < nTime < 3:
            # text = f'用户{k}\n类别{type}\n使用权限仅剩{nTime}天\n请提醒及时续费'
            QYWXNotify('授权失效提醒', f'用户{k}\n类别{type}\n使用权限仅剩{nTime}天\n请提醒及时续费')

            # qmsg = f'----------账户信息提醒----------\n\nDear Friends:\n您在本站订购的自助热水服务即将到期,如需继续使用本站服务,请在授权结束后及时申请下一阶段授权,您的账户详细使用信息如下:\n\n授权账号识别码: {k}\n截至使用日期:{deadline}\n可用时长还剩 {nTime} 天\n\n---------------------------\n本提醒由信息通知系统自动发送,仅在授权到期前三日触发,旨在提醒您的使用时长权限即将到期,如需继续使用,请注意及时申请下一阶段授权'
            # url = f"http://127.0.0.1:6666/send_private_msg?"
            # params = {'user_id': '779544383', 'message': qmsg}
            # res = requests.get(url, params).text
            # print(res)


if __name__ == "__main__":
    notify()
