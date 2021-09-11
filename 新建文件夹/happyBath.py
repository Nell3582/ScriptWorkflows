# -*- coding:utf-8 -*-
import sys
sys.path.append('c:\\python39\\lib\\site-packages')
sys.path.append('c:\\users\\pc\\appdata\\roaming\\python\\python39\\site-packages')
from mitmproxy.http import flow
# import json
# import re
# import requests
def response(flow: flow):
    path1 = 'getWallet'
    path2 = "addPreConsume"
    path3 = "addWaterConsume"
    if  path1 in flow.request.url:
        # body =flow.response.get_text()
        # taobao_js = taobao_js.replace('!function(){function','!function (){Object.defineProperties(navigator,{webdriver: {get: () => false}})function')
        body = "FRaS30PNLKXMbP7UuTvxCuWcPBrTadtmLhRGGPSEwo1Zf0nrVw6+6q27FaopoHEUo7+kECO5vo9hvtABs9K6k11acivPFIPyzZ/jz4n2Bz1yi0sgn5rUAT8jHvimuu/EauvLduHQjl36uZ6r2+3EaShrQHr5L323Y1F9KI44GBBTPTzn67pouZe8oIF0k76yKBb73iAm898siyYJeQO2XWG+0AGz0rqTXVpyK88Ug/LNn+PPifYHPdKDhMSKZBd8lsFehRFNsk/W0vOuTRWIWRsi79SnscBP9k9LjQARPjU="
        flow.response.set_text(body)
        print('已修改金额')

    if path2 in flow.request.url:
        body = "FRaS30PNLKXMbP7UuTvxCuWcPBrTadtmLhRGGPSEwo1Z72kWFgAPnhze+KfishWCiaOaT0+ZG5rlyvZAZaMxpAc++M+Kwut+ck3Q6TdXf3GTwO/kUTOLlt6YnVhrNenHDLZtauEmdjQJa5qPIE2kHzNzMYj568MgW5eKYx8A8yub1RUWZqfRvZ3x1sVrKAfZczINJV3KHjuI9Cvii90hJrHGUdbMLpx5j3AKqDvQ8PYTL8LSmjC4wi291Phqi0QC"
        flow.response.set_text(body)
        print('已修改预充值金额')


    if path3 in flow.request.url:
        body = "FRaS30PNLKXMbP7UuTvxCl8nXoIX75vY05qERbdxRwy2yh1bMSBqnf65WbfUZC/L"
        flow.response.set_text(body)
        print('已完成结算')


# def getRemoteData():
#     ctrl = True
#     while (ctrl):
#         url = "https://gitee.com/Nell3582/Nell9382/raw/master/Task/zqkd/write_data.txt"  # 等价下面的
#         res = requests.get(url).text
#         if '无法显示' not in res:
#             ctrl = False
#     return res