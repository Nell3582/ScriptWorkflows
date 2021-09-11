# import time
# import datetime
import json
import requests


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


url = "https://yjsxx.whut.edu.cn/wx/./monitorRegister"

body = "{\"diagnosisName\":\"\",\"relationWithOwn\":\"\",\"currentAddress\":\"\u6c5f\u82cf\u7701\u5f90\u5dde\u5e02\u90b3\u5dde\u5e02\",\"remark\":\"\",\"healthInfo\":\"\u6b63\u5e38\",\"isDiagnosis\":0,\"isFever\":0,\"isInSchool\":0,\"isLeaveChengdu\":1,\"isSymptom\":0,\"temperature\":\"36\\\"C~36.5\u00b0C\",\"noonTemperature\":\"36.5\u00b0C~36.9\u00b0C\",\"eveningTemperature\":\"36.5\u00b0C~36.9\u00b0C\",\"province\":\"\u6c5f\u82cf\u7701\",\"city\":\"\u5f90\u5dde\u5e02\",\"county\":\"\u90b3\u5dde\u5e02\"}"

headers = {
    "Cookie": "JSESSIONID=0c963631-a7f5-44f4-8352-914cf8b9bed3",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "X-Tag": "flyio",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.17(0x1700112a) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wx225eb50c34f6f98e/6/page-frame.html",
    "Content-Length": "380",
    "Accept-Language": "zh-cn"
}
myjson = json.loads(body)  # data是向 api请求的响应数据，data必须是字符串类型的
newjson = json.dumps(myjson, ensure_ascii=False)
res = requests.post(url, data=newjson.encode(), headers=headers)
print(res.text)

