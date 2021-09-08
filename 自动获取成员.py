import json
import requests

def postwechat(corpid, corpsecret, url='https://www.coachoutlet.com/'):
    HEADERS = {"Content-Type": "application/json ;charset=utf-8"}
    # 图片地址，自行替换
    p = requests.get('https://ley.best/picapi/').text
    # 获取token
    r = requests.get(
        f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}').text
    js = json.loads(r)
    token = js['access_token']
    # data 中agentid 按应用实际id更换
    data = {
        "touser": "@all",
        "msgtype": "news",
        "agentid": 1000002,
        "news": {
            "articles": [
                {
                    "title": "Elune 的小卖铺",
                    "description": "无忧热水服务",
                    "url": url,
                    "picurl": p
                }
            ]
        },
        "at": {
            "atMobiles": [
                ""
            ],
            "isAtAll": "true"
        }
    }
    String_textMsg = json.dumps(data)
    # 企业微信应用地址
    wechaturl = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}'
    res = requests.post(wechaturl, data=String_textMsg, headers=HEADERS)
    print(res.text)


# 企业id
CORPID = 'ww82e647299f8ccc9b'
# 应用secret
COPRSECRET = 'dzJNMu-oexza2qYHpUJQzMQPh9Z-q-pHSWpRuKS-0Lw'
# 点击跳转的url
URL = 'http://my.freebath.me'

# 推送
# postwechat(CORPID, COPRSECRET, URL)


def find_ID():
    corpid = 'ww82e647299f8ccc9b'
    corpsecret = 'dzJNMu-oexza2qYHpUJQzMQPh9Z-q-pHSWpRuKS-0Lw'
    r = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}').text
    js = json.loads(r)
    token = js['access_token']
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist'
    params = {'access_token': token, 
    'fetch_child': 'FETCH_CHILD', 
    'department_id': 1}
    res = requests.get(url, params).json()
    lst = res['userlist']
    print(lst)
find_ID()
