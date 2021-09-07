import json

text = {"code": 0, "message": "", "data": {"userId": 2561117, "userMobile": "15207163636", "franchiseeId": 18532, "serviceSubjectId": 37810, "serviceSubjectName": "武汉理工大学.马房山校区", "storeName": "西12-3", "storeMobile": "18971250732", "deviceId": "7b9a95dd016b8ddfffaffc5711125711", "deviceNo": "120003", "deviceSn": "0000ED11488800011213090008030000", "subDeviceTypeId": 1, "orderNo": "2021090316343054656", "orderStatus": 10, "hotWaterML": 0, "warmWaterML": 0, "domesticHotML": 0, "hotWaterUnitPrice": 0.18, "warmWaterUnitPrice": 0.18,
                                           "domesticHotPrice": 0.06, "payPrice": 0, "payment": 0, "rechargeAmount": 0, "giftAmount": 0, "coupon": 0, "payFlag": 0, "actualIncome": 0, "errorCode": "", "payType": 1, "duration": 0.02, "orderType": 6, "id": 24702905, "sceneId": 0, "refund": 0, "scene": {"title": "", "waterAmount": 0, "price": 0}, "qrCode": "", "hotWaterSeconds": 0, "waterSeconds": 0, "domesticHotSeconds": 0, "takeWaterMode": 0, "payMode": 4, "isHidePrice": 1, "createdAt": "2021.09.03 16:34:31", "paidAt": "", "updatedAt": "2021.09.03 16:34:31"}}

# body = json.loads(text)
a = text['data']['userId']
print(a)