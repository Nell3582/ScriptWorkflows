#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串，自动提现需要自己抓包
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可
# 分享一篇文章，找到 put.json 的请求，拷贝请求体，放入对应参数
# 主号中青
cookies1 = {
    'YOUTH_HEADER': {
        'Host': 'kd.youth.cn',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 7.1.2; LIO-AN00 Build/LIO-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36',
        'Referer':
        'https://kd.youth.cn/html/income/index.html?access=WIFI&app-version=2.8.8&app_version=2.8.8&carrier=CMCC&channel=c1008&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejlq-bsWSxzZtthoyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWuEon7dsKmuapqGcXY&cookie_id=cc7b690bd439feb3f285c18f5fd7c748&device_brand=HUAWEI&device_id=50457564&device_model=LIO-AN00&device_platform=android&device_type=android&inner_version=202102011723&mi=0&openudid=e425be03490b7b94&os_api=25&os_version=LIO-AN00-user+7.1.2+LIO-AN00+700210126+release-keys&request_time=1613622086&resolution=720x1280&sim=1&sm_device_id=20210212183314acc8b702bc06105566bf382c250a81ee015cf93ece20105f&subv=1.2.2&szlm_ddid=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&uid=46366889&version_code=56&version_name=%E4%B8%AD%E9%9D%92%E7%9C%8B%E7%82%B9&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejlq-bsWSxzZtthoyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWuEon7dsKmuapqGcXY&zqkey_id=cc7b690bd439feb3f285c18f5fd7c748',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'cn.youth.news',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775': '1613358452',
        'sensorsdata2019jssdkcross':
        '%7B%22distinct_id%22%3A%2246366889%22%2C%22%24device_id%22%3A%22177a13490d9323-062ed5f412673a-7b620b3f-360000-177a13490da1b1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177a13490d9323-062ed5f412673a-7b620b3f-360000-177a13490da1b1%22%7D',
        'Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775': '1613621791',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775': '1613358452',
    },
    'YOUTH_READBODY':
    'p=FCWwRj3eGxCw=OY4T2_YuUneXLcIAyCm5MyBnXREtv7Q8FmTJj7tJw-inOhtnPcqM14AtjO4SKiJL-JIILiTKmvZRRQm6KLrsfgKO732J6ZKoWu8MZJAaI_TrS6MvvhjYzyYmI7SCTM2qyxbK0Dsz0KSiJQI5uqG0d5i6aB6uXynH47ZlrtJtQrVLtJSXWDhYSS6W24hkCiT-uNLdN6NY2R0lCai1C6oW7FNLEpDBXtcpy2phY4UXqrLE78Nx6CF0c3vmSA50BuDEj8kbcKAnNxzKsPviyxDsTSixQ7M-6C6hlRf3XZk51PTyg-_40birPk1RT5ft1sEo0bMUS8WdRfFelJ3UBJLxowWZxvwaBbGef4Qe7PaUSRBuByD_F8Hp54c4W-iUkR1at2vZqUyoAAZjsv96H4bqQGT7I6ommyfxxHrkdPZ6t0QoitOAf1susE8nZ-uApogfrhHg9ISLTFzKu2FNmMGrjW1uVXZrb4Hiqpt3Hbi3ADNS0IpNNOTzvf42fcBTq0_EYxM3BKRAMenzAiNesb5tGTgStBAY2EHl_FIwjsyHYuovlrrYZVK_cTv7iyPkZPKwT59u-DgPKBGik0KPselWT_QaDZuaTwy01o44oDVE4H1SSNkTEAOk0SRLv1lMZ4pcFtjmwgdBvTE35cEq2m8ei9sLbJwkHnFRBvy9Pk7USnhpBa2eUekj9N5t8eKgf8TDKFNZhE19zFCKQdBCPLJUPSOV7RayrqrwpsJF3bPx9-cG3pR1tqfDfyYyuZS-eVFPGA0AYbhGrNNqMBPz7GvU3WSSUN3msLY-j8FHP-_C4BC9Kxpo4C0mas2VKIiKLmHfTztQId3bUpCfSaV23T3t51Ktw6ugU2PoE4KC2R_Q8chN2fNRCfOdHXcMyaRucQZAr1zz9FBJ0iYIKLdpJDHZaeeUjh7MdMMh53s7eykhlXSAPrAPYbvfvUjk8xApgXhkBUJcyokTbd_onj00-2P-ujDK1_zY6sMo5aultx5KfgxqFLW6zcIkZZuLY-0OoGvrinzGg0z4WiwicgQBkdFQc_52DqTXRSK2LcGg9PKzvCmId6mtZhS9-4dbcFav4XVfexQyiJ7BkDAtqpSPbVW-ELijgGvhDw7AOp-LuF9M9G3lbRIFFi9KItblGVHyAGdeTrS1yraLWCpoO45aUG4eUHPe-nu4QRb2AAiIKHRQa4XmisZfbRZ_yrNCzaypxXQ6DsFz7B6b9sET9BjRQWbm27DVePO1ZbXfGuDuNUXOc5Zt6KYpAfzEVLV9Mq7HtGnXBQQkzyGPFF1YuyNOXcFIWrKraJbYKehsu-Z8ssQ408nvrw3jDPv_06PcW9Iun60xyh5xC2BrySksV7BjbzbYf2W_UFVwfmEXrePfRhGUji1AoZuQRWAd_MOVst7rQXu1bZcOW-O_OcR-mcgf_L68hDgsQTnqxaq6',
    'YOUTH_REDBODY':
    'p=9NwGV8Ov71o%3DgW5NEpb6rjazbBlBp4-3VBqIE6FTR2KhfyLVi7Pl1_m0wwPJgXu-Fmh7S-5HqV6o2kNNfxbTBdHNeGGUACeILyWR3zMN6Iw3IXfZs4Lu-yb9ynQmQje6lCx_IwxRVvI2SNym5MJ3oH5lFqmbtpdkJfwhB1sUJEdEgJ5iEwGnEtnWJDQPgSUh_43T95feCdA6znUBf7UdpUNuu05JsguiVtt7K_tT2UIuuVvof9Ue3GPhbcYOf2RkxK2Lm3EvI0o599EHSz8GOjyzbxSObMbWvZZwgkKHFQXVOzyoQTTWHFLADZSIgWXcViAEHw4v7N4JP82BlQXsKGgv4dNrEf1VdrUKNKxG3N6KDEB01P3CPua6FvVkUbard09CVB7EtXnTKT1tA6PN2ZnC18_44WENRdSnyX0OKFBy1isFDpep83gNvhCLoDvpAGgSJruf8zQD9GhS2XykfsYutxKDLen8fktWSwT5_OwekSn69xKRkyefjQBVGav9W0hJUtOL-MwuerrWpJXzjmMZiz-A-24K-bYLjCnU43GD3wnCYmVhLpAMqSoqxdkeIXTOz98GDS7xJhsXNsGWnl9noOZVMHcgiZGmuELMwt_kepT26mvBWj2mY8XEkYfGZB_l7BGgBKJj3rZwVZm-yEHoO7ZCEZo6LKP9p4m69bTYtUPXC7Ekp78_MKieZRMKyu_BeaURSSJmGPsVirO9onrMGwr1s7qZlr2Qr0QUsXEMd0mB-g4VO-hVocAezEqoQ1oYy48nNMBkKoSPpYSDZ_o6cMBfTpdLvkU6dy5xhbRWyrtSZB94xt0PjsuNWvU7KjiZNfij52VwKkAGVal0qPPtlfZVKXRrbA%3D%3D',
    'YOUTH_READTIMEBODY':
    'p=fUJybc31G2V0%3DUiVImOW0Nxh7QEGyJ8vYw_KPR8bYDMiyXYzgyLW7CQVEtVQ2tSZumTRkWl8FTp0_VQsgecGEt40x2ZBwFzDZA-PTFWSQj3JR48qKNawZTq2yFOV3sKtKq9njRjPn-W9OPUhqsyna3X-hPRGxheptn-q2BtbDEpqFgG-s3en_18yuXlxId1znME7Np-f3I9lz_H0RmmbPCEC7RDeM5mO3qJ5MFPRc5moXInLAIcZQLnSaitrGxSgp1dLVJs3MGgaCRdny0kWXWAijRU0LBNexMru-kP_EUiEbhCTx_yOWJauzaXkZJtk5E6iV4vJBYs5TCYfegxGht5iNp2KagYln3M5aR2yHg1a1EEwzLv8Vl55pbsXGGdmd-6IvOJ5oc2EV3w7IMxZajdX8DIV_WFOS_1r5RH1obUJwfSNIXbcVlhtzk1s1pt0Eqgppwd66l97Fr4Fjbr6GpP_TvvAfjK_ORNB0nPdYnURNsb787mowBN97Pdf6ym10BnyHgLBion8nBxJJ6cq4htSY1RNCMFUBGoJ_Rn_49PlF0OejpQv_NjIPl-XQ-LDMeNT14NavJk7LHsU9v3qbk2s1F67THC1JqDHVsBxnZg_vk7FnRulvSFkvimnmx0CI63Z5FsxNEscEp2Dstt2UTfCVlMT2vLCJa2RI8L3kHt7F_Z_IQRDXX-nuAtzVUnWwwD6yHYcnAgdOQC2FkFFd_9JdvcezaJSnKQsLd1ZJG2yU6Sp6ir94snft6dTRBWRTGsUEO0pZhi8eNP8IBsr-Jk95Bu29v9YOMq7yBNZGAgidZJPLOS0bOXkpW620LD41SJdluRAFlucpXGe7oNFGYvdYP-Oyxd_nxOQTwwzJsyWa6jLFIPcz9sd08KbwV6Yb_6fpbRaX_T-XTFKeA_PSM8gATp2KJz57EOeO9yONTHIlKZPW9kj1G1OJnRHWCQryoHLMMXyvOxv0BfTO748HiweLV51QBjtOcjixq9ynW39kMYkhzRV7cgSDJV1G3kVWfR3sePtIK4mOK4mvtHpDOED-Krair4X02-iGgPDWKQhYLqPv_ymsIECB4RXniy1eP0eZ-5BpBFVQsc7OYQuWCBHxzPaQAytz_RZkNvQ0H2AWzu-QMwA2F8l3gHaxudKPGaMxX4NgezlBFXJ1NVizSIx0WijFkKpQls0aDIXgN7wc-I9pF9_xIKhBZ3-JYHR4dBYCPDSBmvCOpc0iH7VUZDWqiUr2trACQXK9rOJ7AdQkNgjefHSm9dZKnLB9XDhQ3As93JGLWgz3dsIZIDmTboC5KPHpOFTeaz-k5sSbF-cFUK2rvyDf-b0jfIvFPMcGgBgyUnYiGDUq2rgHU0ETP3edLnFmWojzaTgt4VaCg7VwD8w2WpJJLnM5BYYwdy8cLVhZlwq6M8q4P7JEMkboP5xnmAug56d_Rg%3D%3DpY',
    'YOUTH_WITHDRAWBODY':
    "",
    'YOUTH_SHAREBODY':
    'access=WIFI&androidid=e425be03490b7b94&app-version=2.8.8&app_name=zqkd_app&app_version=2.8.8&article_id=36351129&carrier=CMCC&channel=c1008&device_brand=HUAWEI&device_id=50457564&device_model=LIO-AN00&device_platform=android&device_type=android&dpi=240&fp=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&from=4&imei=863064275407718&inner_version=202102011723&language=zh-CN&memory=2&mi=0&mobile_type=1&net_type=1&network_type=WIFI&openudid=e425be03490b7b94&os_api=25&os_version=LIO-AN00-user%207.1.2%20LIO-AN00%20700210126%20release-keys&request_time=1613624135&resolution=720x1280&rom_version=LIO-AN00-user%207.1.2%20LIO-AN00%20700210126%20release-keys&sim=1&sm_device_id=20210212183314acc8b702bc06105566bf382c250a81ee015cf93ece20105f&storage=61.39&stype=wx&subv=1.2.2&szlm_ddid=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&token=6c0bac017af58bcb8088c447816d0206&uid=46366889&version_code=56&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejlq-bsWSxzZtthoyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWuEon7dsKmuapqGcXY&zqkey_id=cc7b690bd439feb3f285c18f5fd7c748'
}
# 2路路中青
cookies2 = {
    'YOUTH_HEADER': {
        'Host':
        'kd.youth.cn',
        'Accept':
        'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Accept-Language':
        'zh-cn',
        'Referer':
        'https://kd.youth.cn/html/income/index.html?uuid=72c368f1c842c7ee64dd935cef8e2cef&sign=db4b7c3699924995e45fc0d3f8f813a3&channel_code=80000000&uid=47181455&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=05c9b620a626e6daf683cf5e161b4f17&openudid=72c368f1c842c7ee64dd935cef8e2cef&device_type=1&device_brand=iphone&sm_device_id=20210117174702dc03d4fe2a3786e8c335094d6a1a1f930154097f25a73432&device_id=49053187&version_code=200&os_version=14.3&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWKx3XlthIyGl6-4qmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfr9_MZoGfm2uEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWKx3XlthIyGl6-4qmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfr9_MZoGfm2uEY2Ft&cookie_id=05c9b620a626e6daf683cf5e161b4f17',
        'sensorsdata2019jssdkcross':
        '%7B%22distinct_id%22%3A%2247181455%22%2C%22%24device_id%22%3A%2217787873f35464-00b12bff56c75-754c1451-370944-17787873f3610c4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217787873f35464-00b12bff56c75-754c1451-370944-17787873f3610c4%22%7D',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775':
        '1613623511,1613623528,1613624407,1613625711',
        'Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c':
        '1612932298,1612932454,1613374152,1613378558',
    },
    'YOUTH_READBODY': {
        'p':
        '9NwGV8Ov71o=gW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTciNAWzGZJgJdfAqVOR2rEWFCGKAHFjWBumwH5DPAodOA6UXlAMzMOzYzL6b3pvrMRIE_8i0W-uriLapFiFThIpApPw95cReMgVQKjWQzEdrApYPZ60yzGMNIQBUsgrYWdqzRuSGtU_yBfEicH4jnfpSGUILzCiL3yMwUthryt7qG-rjZ7OItlADm6mu3mtohlyol3ovaXVC8DAS9n5MsVPUoeekSGFewJJuPxFqjiY4w1O7Wf2CpKFUGttYZpLKwgz-eZF4ESvS6IM4QIvjJ_P-sxOWP64j3OmbjA9JsenRXu4aeSaGGaY2NtgeiuaPs_cgO9foGmb0DprJdteQoyRHTl9TakMuRt7CBolZvsLOCoFeg4gJsVIEdQGXmindTkTqvt0C1iQgmdWdmvqwzcT8cLn4DT1KfSdyEJgDX_fm3rrp0FelWAJCp_qWUkR8V-HQAZAqd5gEOiot-Id-oPxQIJ2IVFEu4vE3XT3hrq4LxTx35gzgUrcTFVc9hN7p22QBKeyuKdsNBI83Df2vkNr9V_gox-tFV3fVFjiyrYMBrnALOUqyyUXlK7ZOWqiQ0LuGvxoBLcs2TVfIEcpEL2UNr5F4KC7mhMGEg16ChxK6pOxTrhT0dyECaWvs_tXwZwrpSVyPLe9pOPw9iPKzNhPWfiRnALVG7pPxL4ETcNhqA%3D%3D'
    },
    'YOUTH_REDBODY':
    '',
    'YOUTH_READTIMEBODY': {
        'p':
        '9NwGV8Ov71o=gW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTciNAWzGZJgJdfAqVOR2rEWFCGKAHFjWBumwH5DPAodOA6UXlAMzMOzYzL6b3pvrMRIE_8i0W-uriLapFiFThIpApPw95cReMgFS_hgaCNPkfBIgjzNMm5cgpIypUTfrWGIDYahJqBtmfw2JuGLE1SWL25bqJu7gSjdpWeq70co_2NcAxHQrSkXttTA6M35CukrLbu9vH1n4S70Omxo2FGQTnaIYhFw_-5umZ6bLqweeZZjIr21gLgUT4U3P0rSo46D7RR5hOfdBwLvpkSJJlsyNXwOu3gXSMmMdYb8JolJoZnFTrPEieGK10aOo4aPnXu9davL32gg2UO6xyzymz5FDvsE-irBYBTivJoeuiBdt1O3KGSBJAnj3l13u4u4gsTyNHpxnJWG3-cDkWiZqIO0i6Q6Iopt9j7EmXSUa_gAuXHuwQWgBj7kxjgwRb4YSX6L970GJozJGIF8HzIKN1tdeOaAkIXl4dokksve8K6N-5GUmKXR2CkDrMTIiVaWHwdffkN18P_yEztgCXOAy4edKUw4QzY_6UZQMJ1P5qv7XQ5dPcTOw5RKrvnk6RLS3xfjYfXMwdYs28xtZcxdImLMvMaCjXi1OO3j3jhRbileC5XSNfPnulGxQoubQjKhka7NuVJ7kMEJm8CVXgNC91F6nBEk4HycOsA='
    },
    'YOUTH_WITHDRAWBODY':
    '',
    'YOUTH_SHAREBODY':
    'access=WIFI&app_version=2.0.0&article_id=36352852&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.0&device_brand=iphone&device_id=49053187&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=72c368f1c842c7ee64dd935cef8e2cef&os_version=14.3&phone_code=72c368f1c842c7ee64dd935cef8e2cef&phone_network=WIFI&platform=3&request_time=1613625717&resolution=828x1792&sign=27a216058b749ba9f3c6540679a32e0c&sm_device_id=20210117174702dc03d4fe2a3786e8c335094d6a1a1f930154097f25a73432&stype=WEIXIN&szlm_ddid=D2LfGNHTZs/E3Os5C7W9nbhv5ObXnFjQFVt6UZzFTN47wX29&time=1613625717&uid=47181455&uuid=72c368f1c842c7ee64dd935cef8e2cef',
}
# 3老爸中青
cookies3 = {
    'YOUTH_HEADER': {
        'Host': 'kd.youth.cn',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 7.1.2; LIO-AN00 Build/LIO-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36',
        'Referer':
        'https://kd.youth.cn/html/income/index.html?access=WIFI&app-version=2.8.8&app_version=2.8.8&carrier=CMCC&channel=c1008&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66rpWKxzX2whIyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWuEspzgrs-mapqGcXY&cookie_id=38f61df818ab7d9182f17f0738eaef4c&device_brand=HUAWEI&device_id=50457564&device_model=LIO-AN00&device_platform=android&device_type=android&inner_version=202102011723&mi=0&openudid=e425be03490b7b94&os_api=25&os_version=LIO-AN00-user+7.1.2+LIO-AN00+700210126+release-keys&request_time=1613652199&resolution=720x1280&sim=1&sm_device_id=20210212183314acc8b702bc06105566bf382c250a81ee015cf93ece20105f&subv=1.2.2&szlm_ddid=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&uid=53046201&version_code=56&version_name=%E4%B8%AD%E9%9D%92%E7%9C%8B%E7%82%B9&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66rpWKxzX2whIyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWuEspzgrs-mapqGcXY&zqkey_id=38f61df818ab7d9182f17f0738eaef4c',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'cn.youth.news',
    },
    'YOUTH_READBODY':
    'p=VYFg4QJ5A6eY%3DVpUK7bR_CQ5nIaBgbEjpU7HmIYEc8D0tK2gn78lvm17nXwgU7hbtHSAkqZ8Sb2FqLTXM1SgycX4OsiGUAZ50M6CiFMLuFv1xLVubLt4xk5ZVquRPuvqzBWuh1PPco3mwv5EgOgO21ic5ygG_jjtEctTNg_yAKGyGIMgs2PqXzwjT0DzdQcWagnzR4smUO18FcwXlnamuLR-UqiWebc-6Ai68XH84yJr1OPWecwyWp8Gf-NF3tomKiZLZEePzWAgb4U6WLyutZXrd798KKpeXeJmS-jqfcWvzB5TEq9HPSBYeiHUBhVLWDarJ88WPwMxRP43vEncei2aVR7cH42_rU4PTl8S1WnSFERD7uyA23EJqMQV3QxphiijWsd9X0TikigTVTcN0risGmspv-tzqDsBQuss_KC4jGzYIIZs2JmuANii8aQojQX7JIF7l3qPlTD-Mpy8PM_dcANLRQSZPevj4QgGODwlEJ42NYwgSWcT3KUJYKQPgJw4wEMcvu15pnJ9vjqsKweSAeFvhL3cLeUvm2TyIZHYkc8MWbC9WFtGOYIBYMPApAo_tOVk4R5NdEOLFB7QeCPa2VfgLRFDQNwNlKin4DWMpCMeV_fzj34J3r1sdWwvJ-fljXZdU0upyYCw3NRIYejOmJ4ZUxKo6sHNJu2PAdBZ7ln3jkfxL-VYSWq4VAqIOpUPxyDSR4UGuVbSIkpVovFhUHVpGIX_qIQLRSfGDaa1csROebweX4PF7lYYcM8VTKV7Iy4yZNvun4gs32ue_ocXQyjnxvOSnQkhrYK-fhm7Z7iWNtSHsc4-c9SKXJ0ubImH4Am_frvGb7C10Y1-Xc3WbKD4Xcf6nr9xI_JWnFUrEMU0HlBa14vnnwXUXfivgc3T47rdj5FFPsXcjucD7XOiscdVB37bLHDbl7VpusANs8KJ2VtptUKA5dmAJutwO0RKaRg9pYvZQLaSW6n0wVXTI17-70bcHMQJxCrN1euKKfW1WqVC-hF3joTWXZv0CstKpGLxDpzqAfzoTpwRoN_XOWxjW435-KEmkXegLycQsh2qPFNlC15TWvhhWGlO8R9VC7wMLFf-EQDMvrGMufuFCXBqClsI2lChU5xtQAwgcs2Ng8jFJioXLbZKQMN2i2b9YPZsKnzRL13iVrPK_1FcJgEyiyxaINeYq3sZ3I773hgAs3C_o6QPbOHM-BuOFMoJO8ZaiI9BeO4YEpYzObGZo3H4iedy_cIcjle2btLQCRt998q1shQsZ3vm8-jxNrVGPinzteN0JYHfh6DjZxnKxOxvrH8l3CHujb8cRdE6JlNKz6uARBQXBPVPUPT9NwBoW-oxcsy4-6U8YeQQ4OFrbkLcX7ufS5yhWJM12zsEWRtQvzx5oWWFgno79QJgAG8xEZnAa9GHyUUuGj8OCmrTAkVW6h1dVk0aHdTi0bzxD',
    'YOUTH_REDBODY':
    '',
    'YOUTH_READTIMEBODY':
    'p=vYdVi_XPUOzA%3D7ioCfKCMWbI3qgFlRoq41CA_tf3qtclczrmKMWLoy-23fGlXOoPpM4V5GxbkWf4UKQM96Dbz61gCBSv3b6YYnlfGlJLiqcOyrN5BSpN0drQ6YpRo13oYz_Mqhuti2ETDiwNOoCXsB6RajX3d_PBGBpkJxcusvQtMBSJmawoqZzb_AhPtASq2t8bDnGWjxECdfv--EIzt-rJCkHXR84KHWVMwEEHTDB_wiK2OFZ5tPx41NnIz0pjyXg3yfCeNKEr7BuKBidN99LrrXlCrCRJUnGdEbAb9Yop_FSTwsQNqNEary9MC_jSiNI9umzlppqsHYYlXMcofliOHv__afO9lNxijVGolspK1Ku7bqJtwHUNJiE1iPsu0FIcNOJaep3tqkp2mAmCQxWwe6hghztN6u_eEZKO2Q5lfHsJGFtzYgP26Vod-0A3VL_04FFVcauLgMO5Wlx8gLukrZPJ9ySMEf8xUlmhNfz75SEGyIacAOIFU9xQWMZ0FUPMoo6dwH1myqd9y9VNDT-92Qplgsdt6lJ4Gb2vsDs4H729tBIUk1gDwk0HwdF_PM6b8pCyCMbYYBg8pzhhIbgxYgznS196KZMth5iz-coOdZPJ-fgpE572hdeSjgu7xd2bwqds9Jj4n7mYxuBIUErIRWg_boVrb5I-sHdivMTyWavVrs76O50jCkMLtJRmBpJZ8057klTUuX6KipWoGPGeUMAjy49jQm197v8maAwNXF6__n9o94fcb_GSzzoPiv5pcAOEHB7fZDEVFip__MbIBdqMQyAksrK8yXiRZ2vVAjATPZJgKF0A2tL6zcZrcqFDG0NFU6nDt4gFhE59KfC_pma1fm39Z8psGdvcRMDE7trZuiiKnJLZK_tWL1BRUlN6wjiul6VIVq-F312OA5wdNYrHqgBTUsnkhL1Kkbva41mcHV9zVSRJuJut-sX9unpiJns8dbj1wzAjL9SFovfUvYvNd3DVTpi2uh4C_arfwRDDsrl0PcneAJqi9W0RH0VuZtIOgZBSst1JqGpFPIY3uDg3RGdq71iiLblekJdjtr6NGhQKvgbbJCZqVjfHRlZaW4wmUgabAiBKSgKx0fpW1NOZe4E0WYU5cUGJC68YEDCCOiJCTizdoyDxadu875VHJidH2u6VfOgjjineU99_V_2tDZ6PcBYjGTtQsGTwee8-FEsMszFgBiTIWr5h72G6CpGa4zrf6bxfO3c--vHEJMH8RGXBkXhsvK-YvXRecZIAQcTOooHEnoBbvbB9ebLTh7Uk8xFRozFh18Zo4edYMTe8Ksx80YZxrghSfqhp2DfQR9eJy1QWf2oELD9F5HB0FcI_WByblT0nCXktCOKWNV7WCI464HVSndEamFuQ4gJPdZf_7suETGsQbwZ8-3pXn5g3_vK4QUYPNXgXtCSRUCNinrANiUA%3D%3D9G',
    'YOUTH_WITHDRAWBODY':
    '',
    'YOUTH_SHAREBODY':
    'access=WIFI&androidid=e425be03490b7b94&app-version=2.8.8&app_name=zqkd_app&app_version=2.8.8&article_id=36314269&carrier=CMCC&channel=c1008&device_brand=HUAWEI&device_id=50457564&device_model=LIO-AN00&device_platform=android&device_type=android&dpi=240&fp=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&from=4&imei=863064275407718&inner_version=202102011723&language=zh-CN&memory=2&mi=0&mobile_type=1&net_type=1&network_type=WIFI&openudid=e425be03490b7b94&os_api=25&os_version=LIO-AN00-user%207.1.2%20LIO-AN00%20700210126%20release-keys&request_time=1613652565&resolution=720x1280&rom_version=LIO-AN00-user%207.1.2%20LIO-AN00%20700210126%20release-keys&sim=1&sm_device_id=20210212183314acc8b702bc06105566bf382c250a81ee015cf93ece20105f&storage=61.39&stype=wx&subv=1.2.2&szlm_ddid=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&token=99bb162173e2e131a5778f4f57008bda&uid=53046201&version_code=56&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66rpWKxzX2whIyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWuEspzgrs-mapqGcXY&zqkey_id=38f61df818ab7d9182f17f0738eaef4c'
}
# 4老妈中青
cookies4 = {
    'YOUTH_HEADER': {
        'Host': 'kd.youth.cn',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 7.1.2; LIO-AN00 Build/LIO-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36',
        'Referer':
        'https://kd.youth.cn/html/income/index.html?access=WIFI&app-version=2.8.8&app_version=2.8.8&carrier=CMCC&channel=c1008&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66rpWKxzZtrhaKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWyEspzgsLnIapqGcXY&cookie_id=a6bb8a3aacfad23eb31e5506d9ac2e79&device_brand=HUAWEI&device_id=50457564&device_model=LIO-AN00&device_platform=android&device_type=android&inner_version=202102011723&mi=0&openudid=e425be03490b7b94&os_api=25&os_version=LIO-AN00-user+7.1.2+LIO-AN00+700210126+release-keys&request_time=1613740570&resolution=720x1280&sim=1&sm_device_id=20210212183314acc8b702bc06105566bf382c250a81ee015cf93ece20105f&subv=1.2.2&szlm_ddid=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&uid=53046866&version_code=56&version_name=%E4%B8%AD%E9%9D%92%E7%9C%8B%E7%82%B9&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66rpWKxzZtrhaKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWyEspzgsLnIapqGcXY&zqkey_id=a6bb8a3aacfad23eb31e5506d9ac2e79',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'cn.youth.news',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775': '1613358452',
        'sensorsdata2019jssdkcross':
        '%7B%22distinct_id%22%3A%2253046866%22%2C%22%24device_id%22%3A%22177a13490d9323-062ed5f412673a-7b620b3f-360000-177a13490da1b1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177a13490d9323-062ed5f412673a-7b620b3f-360000-177a13490da1b1%22%7D',
        'Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775': '1613740570',
    },
    'YOUTH_READBODY': {
        'p':
        'MFbVGOYyXwIo=PsKtOYIB3RcgcFvZScHlPVx6DHyfS_6C5Kh5jeYTRl09xmXi6yfVUb5o-k2E3YRy0eSoEQ6nJZHZ4VJxBpgmCyL7hhHCYSaHF_za7apDa25BipXd3PRDP_I1w9BhzCesH79OWBDSlohyJPixwPLhSls5aLArGD3i717LwQOZsPlV_o01bInX-4qK7JuuqyX6Xf5XvfViHObjjp6cnAU-zhFTq7cHDkGYIyg3X07ivKBcnMl8QtQkOEdiyw62ICY6j6PNFa7Jtg6_WzthALX8MMDpmkQuRMYZicxk4DgRdrmN4IbsIGb4S9dKLhaMduGEU1fkGXNXZ-_bo8kf_mOHhUUAWNhQyN6VO8b6VKZkt0QpS8LN66SjU7hsfGORgBIXxJ3wZkoaInkRUEmika9om8DDK3epKkQRXNnYmTq09zry4nRH72Mn9hOQwT1Nfq5p8SUmDEF-Kevqc7SbxH5P6DCq2BOoox5LSrYu73-8FJ_YjMlxIjCgPKE-CMOLQ_FHHkugyhgOcdsgEcRJuwTRgvRjJa5DXRw4uYiuY4qwrl8ug4aYx-HwewPNY5HPifRm0-9PWln-OfpNxgbfGPgmvM5tRsW8NakBbfummOMAPZJoOd_k-TwDQAehSiQ94WJLiboBTHfrRQ4CtZhqN3EBnr272Tu9EhJt6Ti538eqJCGtDBXlxWki8jmeraJ4srZcMD7w3mhMJft-kbhwMzX70YEJ3NidudL_kw6sOBzPbazfAqYvAE4j8rchvoeOhPVuSXv_lAgj9eVJt8rLUIWfyuNMP6LfXh9NDslOhmPDBdlyPKv6nDT7unHcsZT9PovWx6Jr54cE-XmD4BJqvWobtPFnVoReZ7BG3VyT4PqLFdrYMKJFW6wxVs-7Pboi8IHHCNyz9e8LKjYjBXntQavF4MYTHBzTr_94EWZSXL8GNn2oQ6Vp4YdjIaHN9uEO_OGtu3O2ysQ2P3LZ-Ky-fI3Rxv5NaWy6OV7y3nOvfUDXlgOoFueZmCcQ8xeB_1gD0_tevue40Igi63z4SSpVQVKMl-AlvPwFROhW9Dg7BoWNaeRSLzvSeFgHQMwY4qEuMFv2hfW2ZptWVbNhZoyP3x-o19osAO73IhiDzNgU7ztEd7zG9xlTa7hmlea5f8AYXdZSJeHpSG_cT0rbKTE300EqWMkT8fA2FziCIWa6keKxuF2YWjomRRjU0ggTeeYC6XoIhFb6KqtNlM44yndaMqNx2qAhBinWOjZTb_evI_kMHGTSNqmHt77MLM7NlPV0ovnh78NUjZD_IaevCEMfO_OQOrgntaO8WZ3RzASp8a4qZ7WDxYAtR1LZZgJHaxF5TUn3K4z59M-T0ZZVmrQ4_ELVIURN56JePMBfb6VnsDcuuCWhM3SiNJFl7QaqLVHrH8bwNWLXJrIwPxVgy-GiIbMRe04H7wz4rGtzF'
    },
    'YOUTH_REDBODY':
    '',
    'YOUTH_READTIMEBODY': {
        'p':
        'tYFg4QJ5A6eY=VpUK7bR_CQ5nIaBgbEjpU7HmIYEc8D0tK2gn78lvm17nXwgU7hbtHSAkqZ8Sb2FqLTXM1SgycX4OsiGUAZ50M6CiFMLuFv1xLVubLt4xk5ZVquRPuvqzBWuh1PPco3mwv5EgOgO21ic5ygG_jjtEctTNg_yAKGyGIMgs2PqXzwjT0DzdQcWagnzR4smUO18FcwXlnamuLR-UqiWebc-6Ai68XH84yJr1OPWecwyWp8Gf-NF3tomKiZLZEePzWAgb4U6WLyutZXrd798KKpeXeJmS-jqfcWvzB5TEq9HPSBYeiHUBhVLWDarJ88WPwMxRP43vEncei2aVR7cH42_rU4PTl8S1WnSFERD7uyA23EJqMQV3QxphiijWsd9X0TikigTVTcN0risnZTmUVtmwXvPhMBxPQk8Xh3FXEBDyA4XfQxebmed82_QXeyKi0cHtAi9WVegSXa8OtUdsEgzznMMAwdHY-5uihhMHA1m8DPjOgL8YaJ2v6KLB3_Hh9U6qOA25OHsS7fVUTXCk_ejNA8vskYImby-QJ2g2MhqkEc9SETOLQkVf84w2gVYEsP2IHdzYmNNGQR3vrqUSwoMtlwkk4LIDvLlMVQ8HJ2lpAeMw0FVhSwPqwNzBV_LLfgzgkD51a4EvUHI4bAKeFb4qGzDu35eI1SfbnE69n85k1DkFFOUsMSFtRjDoU_nrjDjc5Rr_IjsbeuNdXh1wmm6cAT72UbNVekCX1nGRpvKef4DZhy2xgJNIcAbxXtkfbM5zU6EIAhQpHi2Yn58T8j7DrPo4oQvTnecRegkyuE6E5Cc0WOWBn5SJ9eqAcD0Xq0g8olH0KNLVk6_e4NXpt3k3jfsSCbXixoC3UfQVV0pYDGyR-8E8RiPFtMpcILuv1tTvNqLCiN_Or0BzM-ATcpS_xqksMIgekaQbZR8yh1n_85Vs_N0nS9G2jQ-4maX5_bD9T1XraNHIiea4nFXWqMSuwIxtANucnCJxUek5rreH5hgU9Eet0GC9xFIk35KiV6mdgV7aajW8bni4bB14H4WZWsk136zvM3sP4Wpv4ilc-wDfbCgZCRi25hLI3owhhUK26vt1zKPsJjRDNYDObvxlOPZe4j2J2rLhPrkNX3Em3b2GXBuTSa7K1B2d4JpltXeSXo6xH8qAH2ZeyNqGjbo8UCe7n84Zyjw-Y5plKn9Yg7lIJQ4JmatvcLeqOyOBNMyy8B2xyUle49KpkwqlNwZa8LbGa22tZdWnY0UUQvDx6x8F-6NEWlVs0NE7t4zK4kDw1nK2E_aKso8RR0Q8Y0J6bpkBFpta4OAZmD7g2pJAkV7khg2qO04YE-Si0JhshH5D0Rx7CrSKQWgc9U6v66Mytax69q9uTi4Fl_RwSSM-x1-lQEu9n2jrSLdDgKgEvgJJtCYYbEtacN-56sU54XjlnA=='
    },
    'YOUTH_WITHDRAWBODY':
    'p=dCWwRj3eGxCw%3DOY4T2_YuUneXLcIAyCm5MyBnXREtv7Q8FmTJj7tJw-inOhtnPcqM14AtjO4SKiJL-JIILiTKmvZRRQm6KLrsfgKO732J6ZKoWu8MZJAaI_TrS6MvvhjYzyYmI7SCTM2qyxbK0Dsz0KSiJQI5uqG0d5i6aB6uXynH47ZlrtJtQrVLtJSXWDhYSS6W24hkCiT-uNLdN6NY2R0lCai1C6oW7FNLEpDBXtcpy2phY4UXqrLE78Nx6CF0c3vmSA50BuDEj8kbcKAnNxzKsPviyxDsTSixQ7M-6C6hlRf3XZk51PTyg-_40birPk1RT5ft1sEo0bMUS8WdRfFelJ3UBJLxowWZxvwaBbGef4Qe7PaUSRBuByD_F8Hp54c4W-iUkR1at2vZqUyoAAbDdmghTrLTOG0epBkUsoQdCpn9xJ2z5N9__Ze2LtkI1IEMXZ6HVeEipISHgo1D2qOWHgwiMp9OyHNvqiYJ5wiWOADZ0mAcR28A8qzcqzT9EcuEgWzFgRJUKpVJfhQjKzIvOzA-xCI4V5s7pSrD7dVHzhfDqBBSR6Ak43H-Xfvav5p3ckGIJvSJLQLg2QusVsd6_xRBjKKWRYnF5jtZMy78ECks8TGDRChurIJhwq3-JcU61Z3lzv5HveXa02MF0vb0JbDujonQIi4ZPdpSTJmq0DV3eDT4kzksliaCMib5gsjtMcWMT7m53BQ2JehcVH1ZU0_vmCo2LEoOS1p0xPAJnTvR8IjQGbqrEsrQLA-07hVZK0INPp-bUAVQ8OH0zhmBMglaaBKKkFWAFZKySILvz6X8WHyoG48FEhdENroS1wuiuUoJ51_itFMoXjiy117_Fsax0GAf0HgY_bKL5J7WyUJyQTu-sM6DvUtzFkWxiJR5hWLm0ljAunJMquHMWhSi5uCAYoenXZsju7BZEmxu9yDn711TF4l2lpbSroDQ5N5sbYp5_rhjrLJcOFPIlVOH6IDSMk-AXB1OUDoaYX9Zron4qEIiF8lvn4yGded3i1KpMYyX48Mo3inCCmzvvObUX3qAcCH7kQHfLZ02BobjLWtYlxs_3jGkVFH76PAnTiCmR3uw3WzxTwu9TGNhUwfjDayz5RogGWDvdQRVMfFqrjgXTYcDmUG5wTp60H5MdchOuT4r3XYEb1iVkwjrt48cBOnjG5VEXBVHY0ErBddBo1YKADtd-ZAIqXjsw_GcPvetCB1hl8rTJJlmtvQknC918h8O3iGzLHLoe95CJ7B_8QKagfejLaC2SuDgUcBA56PTpvVOzDQ1RryTOKbkgnQvNZMG8ghlf8ZwNf_0jVMZtClajhQ5nuff_S5qLuP0ZWGXw9MYEbNPhLHz1SN1BJyX1Vru7F0IjtpMmSqPfQa2JCdAj4qj3Jcsy1eWudnEsfqvAgUGvfM2c6iLPn2-jg_CVVlMG-SKYvSm-lxnxi53',
    'YOUTH_SHAREBODY':
    'access=WIFI&androidid=e425be03490b7b94&app-version=2.8.8&app_name=zqkd_app&app_version=2.8.8&article_id=36378187&carrier=CMCC&channel=c1008&device_brand=HUAWEI&device_id=50457564&device_model=LIO-AN00&device_platform=android&device_type=android&dpi=240&fp=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&from=4&imei=863064275407718&inner_version=202102011723&language=zh-CN&memory=2&mi=0&mobile_type=1&net_type=1&network_type=WIFI&openudid=e425be03490b7b94&os_api=25&os_version=LIO-AN00-user%207.1.2%20LIO-AN00%20700210126%20release-keys&request_time=1613806280&resolution=720x1280&rom_version=LIO-AN00-user%207.1.2%20LIO-AN00%20700210126%20release-keys&sim=1&sm_device_id=20210212183314acc8b702bc06105566bf382c250a81ee015cf93ece20105f&storage=61.39&stype=wx&subv=1.2.2&szlm_ddid=DuSypxlqjcilx6T9S7kwrEnD09AGXsVBNqd369NPEj%2BwnpBRXX7Vm61hqpFNFl3ue2RhU3ywqx6O9TrvFhLmC%2BcA&token=dd71bb6afe5de995d0490c3a2d26dbf5&uid=53046866&version_code=56&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl66rpWKxzZtrhaKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3gWyFfHqZsLm6apqGcXY&zqkey_id=bd26d98ae95c1dfd2820b29273515a89'
}
# 5 小号中青
cookies5 = {
    'YOUTH_HEADER': {
        'Host':
        'kd.youth.cn',
        'Accept':
        'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Accept-Language':
        'zh-cn',
        'Referer':
        'https://kd.youth.cn/html/income/index.html?uuid=72c368f1c842c7ee64dd935cef8e2cef&sign=cb9b8c4491b92424701b370b49ca9aae&channel_code=80000000&uid=53941358&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=b33e352ecc94a9b973f01c7518b923bb&openudid=72c368f1c842c7ee64dd935cef8e2cef&device_type=1&device_brand=iphone&sm_device_id=20210117174702dc03d4fe2a3786e8c335094d6a1a1f930154097f25a73432&device_id=49053187&version_code=200&os_version=14.3&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3Z9phIyCl7CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWrrmuZoJ5m26EY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3Z9phIyCl7CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWrrmuZoJ5m26EY2Ft&cookie_id=b33e352ecc94a9b973f01c7518b923bb',
        'sensorsdata2019jssdkcross':
        '%7B%22distinct_id%22%3A%2253941358%22%2C%22%24device_id%22%3A%22177c05beeb14b7-01a4f05f113f0b-754c1451-370944-177c05beeb26df%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177c05beeb14b7-01a4f05f113f0b-754c1451-370944-177c05beeb26df%22%7D',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775':
        '1613988964,1613989010,1614073359,1614137531',
        'Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c':
        '1612932454,1613374152,1613378558,1613906358',
        'sensorsdata2015jssdkcross':
        '%7B%22distinct_id%22%3A%2246366889%22%2C%22%24device_id%22%3A%22177c05c43044c0-0a3c8ee4c7c43-754c1451-370944-177c05c4305afa%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177c05c43044c0-0a3c8ee4c7c43-754c1451-370944-177c05c4305afa%22%7D',
    },
    'YOUTH_READBODY':
    "p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTciNAWzGZJgJdfAqVOR2rEWFCGKAHFjWBumwH5DPAodOA6UXlAMzMOzYzL6b3pvrMRIE_8i0W-uriLapFiFThIpApPw95cReMgVQKjWQzEdrJ5yxPZ_Fec_6_GFoMUTIRLffKxXT8JBf-wNkGSwFfSZW1kGzYNf5iQDlQNhqyiO-f0MSFFNNRrPZxo9XW_rbiAZhysij-Ooza9-X5Y_2xgDqM7nDrbMLgWSgSVWcJG8XmrWLI9YtuKEHyK4U9cVzTdmwTXEm0RTKMEC12CqVdaTFwrCnqEeb66HYBhQk7DB2n0wD6p44bpx3PQj3ZcKbtJvi4As1pKlp3t2RiofPPIsNl2xV-kWqQOGUUZSxbvWHeHniBmcDzP1E6rPj5Uyvvw_SmvWHHVMDEo54LYwQs0mIV0Miek4Xh2xV78owcrbJsdQVv3Qhn2sdffMWmjhPdqCQNlualcr78H9LHwHlP_jGslQNekikDFOVH97tjMYLySRJEB7trxsjjeTqYwTbUjtkTr00Va4UC5XsQg7tZ3hBSH4ZpYEeZFBJb0rd-9kKtvMp9XlTJId4_ryf3gGwC-xr8x_cXaiXjCbPyqRzTme3FoBGJ46y_Osy5nOtdjem2vF2afyierYACYGiaKxgdpYkfUS05GVD-pZdWkQrzgX-jvskVfmnkFrOWQq34dRIQ%3D%3D",
    'YOUTH_REDBODY':
    'p=9NwGV8Ov71o%3DgW5NEpb6rjazbBlBp4-3VBqIE6FTR2KhfyLVi7Pl1_m0wwPJgXu-Fmh7S-5HqV6o2kNNfxbTBdHNeGGUACeILyWR3zMN6Iw3IXfZs4Lu-yb9ynQmQje6lCx_IwxRVvI2SNym5MJ3oH5lFqmbtpdkJfwhB1sUJEdEgJ5iEwGnEtnWJDQPgSUh_43T95feCdA6znUBf7UdpUNuu05JsguiVtt7K_tT2UIuuVvof9Ue3GPhbcYOf2RkxK2Lm3EvI0o599EHSz8GOjyzbxSObMbWvZZwgkKHFQXVOzyoQTTWHFLADZSIgWXcViAEHw4v7N4JP82BlQXsKGgv4dNrEf1VdrUKNKxG3N6KDEB01P3CPua6FvVkUbard09CVB7EtXnTKT1tA6PN2ZnC18_44WENRdSnyX0OKFBy1isFDpep83gNvhCLoDvpAGgSJruf8zQD9GhS2XykfsYutxKDLen8fktWSwT5_OwekSn69xKRkyefjQBVGav9W0hJUtOL-MwuerrWpJXzjmMZiz-A-24K-bYLjCnU43GD3wnCYmVhLpAMqSoqxdkeIXTOz98GDS7xJhsXNsGWnl9noOZVMHcgiZGmuELMwt_kepT26mvBWj2mY8XEkYfGZB_l7BGgBKJj3rZwVZm-yEHoO7ZCEZo6LKP9p4m69bTYtUPXC7Ekp78_MKieZRMKyu_BeaURSSJmGPsVirO9onrMGwr1s7qZlr2Qr0QUsXEMd0mB-g4VO-hVocAezEqoQ1oYy48nNMBkKoSPpYSDZ_o6cMBfTpdLvkU6dy5xhbRWyrtSZB94xt0PjsuNWvU7KjiZNfij52VwKkAGVal0qPPtlfZVKXRrbA%3D%3D',
    'YOUTH_READTIMEBODY':
    "p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTciNAWzGZJgJdfAqVOR2rEWFCGKAHFjWBumwH5DPAodOA6UXlAMzMOzYzL6b3pvrMRIE_8i0W-uriLapFiFThIpApPw95cReMgFS_hgaCNPkfBIgjzNMm5cgpIypUTfrWGIDYahJqBtmfw2JuGLE1SWL25bqJu7gSjdpWeq70co_2NcAxHQrSkXttTA6M35CukrLbu9vH1n4S70Omxo2FGQTnaIYhFw_-5umZ6bLqweeZZjIr21gLgUT4U3P0rSo46D7RR5hOfdBwLvpkSJJlsyNXwOu3gXSMmMdYb8JolJoZnFTrPEieGK10aOo4aPnXu9davL32gg2UO6xyzymz5Ft7pW81iR2Ltql9yEHG_ozwtXEFSt96wy3DiP2RZihifHPPueAhU7Z4xk713WxASroWlwbPFOej-lKbLNgpLB-s206n4h2G5pjhvAsQ_0D-W7L9qn1zhjSdDlSJSI21JaasEThwB_7TmlAVwXBfKqc4pR3UDEpuxorBnVKJLryDgV7QP-tn8EPrb5xDS7u_WLdS6khd6RS67s2imi8ihaeGispQYbbLP_OcDdlDHgVdPXosi_G7cPCwCx74xroCkMiDuQ9hGuB_Zndj9yErtpXGKL64Psmg0fFCkUFPuZ8OZen3DPDktqe9wboPrBkdhrFCN7rWtswK0%3D",
    'YOUTH_WITHDRAWBODY':
    "p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTciNAWzGZJgJdfAqVOR2rEWFCGKAHFjWBumwH5DPAodOA6UXlAMzMOzYzL6b3pvrMRIE_8i0W-uriLapFiFThIpApPw95cReMgFS_hgaCNPkfBIgjzNMm5cgpIypUTfrWGjOj6s3hT40AUP-nkzarqtJyaq7SWl8ZMBPfdBXDhkARMHSp-zPuXcJYGdh2j2qa8ii6DpYz0hGriRGy1We0qPdaK-53oZAp1-XkMFN7XOZ4KDqlJWHcfBCHEp-Nnji5lJ8MGFqqQoBqTKzTnk9Awq9jUZRwSmxLlVDAudLxc4tpHOdMNXlaK-DY35_VycR1HBICk50IZi-gRYQPkOycWoihXpqgk-VWG7HrdFRmoLPdua5zLHraV-sb8CAR2UkRcv8W4UT2r60xoRDr1FLvzNgnkRnmnUbSm8MFhJx405kynQWRbZYZM_tIdVAeNxElo79gCoPZKpfxMQAJRRtE87-xGTTydOgLlw3rCUhpGhfeeMnTwaGBLQerO7JO5rE5muB9SH2128rPlHPlpYU9d6gm97Jiqb0ew7jSoQnE7gSQk1wEvyFDhh4K_GWjTF5AMYQik0fIVLTL7AIwwJnHvCQHqTypdtN89esXlRqhE8yfgjOlfF5khVmf8YS3qFgMyhthcvIg5U52_ZBzu8VvvrvxfNuHq7wO0%3D",
    'YOUTH_SHAREBODY':
    "access=WIFI&app_version=2.0.0&article_id=36424327&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.0&device_brand=iphone&device_id=49053187&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=72c368f1c842c7ee64dd935cef8e2cef&os_version=14.3&phone_code=72c368f1c842c7ee64dd935cef8e2cef&phone_network=WIFI&platform=3&request_time=1614138292&resolution=828x1792&sign=a5c15f083c62a02ecf7d82048f5670a4&sm_device_id=20210117174702dc03d4fe2a3786e8c335094d6a1a1f930154097f25a73432&stype=WEIXIN&szlm_ddid=D2LfGNHTZs/E3Os5C7W9nbhv5ObXnFjQFVt6UZzFTN47wX29&time=1614138292&uid=53941358&uuid=72c368f1c842c7ee64dd935cef8e2cef"
}
# 中青 for ZC
cookies6 = {'YOUTH_HEADER': {
    'Host': 'kd.youth.cn',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; TAS-AN00 Build/TAS-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36',
    'Referer': 'https://kd.youth.cn/html/income/index.html?access=WIFI&app-version=2.8.8&app_version=2.8.8&carrier=CMCC&channel=c4081&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691pWaw3YGyhIyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3hWqGjH7frqm2apqGcXY&cookie_id=7b5bfdea76bbd3d2755554ea67e31380&device_brand=HUAWEI&device_id=50759328&device_model=TAS-AN00&device_platform=android&device_type=android&inner_version=202102011723&mi=0&openudid=13c9ac78d3f49cc8&os_api=25&os_version=TAS-AN00-user+7.1.2+TAS-AN00+700210126+release-keys&request_time=1614663424&resolution=720x1280&sim=1&sm_device_id=20210228102005ffbc4a4674f7e3b22bddf8e3c422fb37014e413713a7c18e&subv=1.2.2&szlm_ddid=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&uid=54083321&version_code=56&version_name=%E4%B8%AD%E9%9D%92%E7%9C%8B%E7%82%B9&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691pWaw3YGyhIyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3hWqGjH7frqm2apqGcXY&zqkey_id=7b5bfdea76bbd3d2755554ea67e31380',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2254083321%22%2C%22%24device_id%22%3A%22177ec40bd481ff-0733d8e500622f-6f7e132f-230400-177ec40bd491af%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177ec40bd481ff-0733d8e500622f-6f7e132f-230400-177ec40bd491af%22%7D',
    'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775': '1614569279,1614576444',
    'Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775': '1614592356',
    'sensorsdata2019jssdkcross': '%7B%22distinct_id%22%3A%2254083321%22%2C%22%24device_id%22%3A%22177ebea7ea4326-06cdd1d9f435ec-6f7e132f-230400-177ebea7ea53dd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177ebea7ea4326-06cdd1d9f435ec-6f7e132f-230400-177ebea7ea53dd%22%7D',
},
    'YOUTH_READBODY':
    "p=2CWwRj3eGxCw%3DOY4T2_YuUnclGqUwWSR1eXc0jUYvk6blxRyQrEE9ibu3L5KQHpqrQtdo4QJgOOxV2I6SHPdEgF7a2hNrQ219wjUbQoy7gaiSgqkjBlOWOSyHKFt-2uJ66ujVTaRj-wjh2wOAZjMobOF-8Kkniu4-s3djP2UH5cUZIbW1HVRmeV9HKiYxgi1VEYCeIl-Z-cOFHL1FeU_R1RlwRcYmBFV0_A5RyYD8dW5_vSLlhay6EvDYQvgO5t1JKk69DFsioeOTerSU5aYwmpQWuhzjDu3zgo9-KLPX4wezgYnZffluFJt87Q51-dbB3BHEbaIB5WWBLTI0N3gbPUwA7zViSO9GrgvUXFkj7f2302bVxXkwamCRtMWn7vgp4Vl5Pz2eoy2lf22xkbyTPZrifIFt2bNjeS_anFEnPE8vKUZpmqEsM9AObyu18AGkYZAyTDitrjXCPRYoHsqcgn1Sq8N0DgVIrYvlBmbYEhhZ0CEvtBqiZxTuwX4W_J6BEozPPnVLHrDWZxASsRLMyoPB6VRTiPSEaRIBRlmM2LLlxEgNWyuLtQ7GFM39WFJoYXWrQDHzVzMxwqqlnmxthiAGVVSPI1mp9foDFS8x6dxDx39tdOkahS2hsV3boK57Svh_FLGVEeKO69ho6ovkeDQUbTAIBd8_u-uAQnE2DcLJGuVax-yBVvKhQyaGBwRM0gDOGQH3vkTlaZ-dGtpAHhynF0buNAU3rveZL3RLK0e82BAemfo2urIGHRMQ-Di7ptPuAr_i6s2YmTnLXuSO7u9TQoUsKFyRK4GulK0JXNuIupn3fsJpLACM6TdY27xxNZRRklbW2tdsbUowyQjvwYHEBxhgDaFmZQdMQ-WZEqlFyAGGW1pjP3mwdtNp6iLAoDS9Se8lcoTMKwmCcMjAyRdwjIvphUbGEM2oT-Cfa7z6iwoK-LynutSGgrHeR2aUnGfQno6fls0geY-h1pTIkerws0vxOOXr113TL1Xv1ieRdOLC681Sf3XdnK9OEGhI99aWwZ34gYmCHUWLp0YMc6fQ1Spve7KG2GP3dY8EHM8yMqEz7QBpl8KKq4QZOFQEsZWhjCoC7JDfevl8d2HfdfexAQvWnEPg01VMIPJXkWHNRb1N9aAnBMzWV4-No7k-Cxom6SeibrOmau4ZyQCxGFd3ZGzhArVLtnMfibIDin89_4R6bPPl8Lc4mBLma4_XGqbEYaZqQ8Esfce7UwrTUyXLkZPRAu52tLpD0UAtoJA7N_P3BL70-vRlwmA7ighvKsmKeLakrX9DuNSzzeHFClRHwYmNUTQ4fzXq_mCcXDZ0bQEuonUzd7ny5IKVZCrEz-6zGjH9ILLz7uZSJl44Y_D4VL_LA4-GAYi-5elbeDnMAhdKGZiMu4Vtm4fuPPbzDmd9fFLHCmHzf2u0-K4LQuFc49a4gdGkkp3JEtZ1cTrW",
    'YOUTH_REDBODY':
    'p=9NwGV8Ov71o%3DgW5NEpb6rjazbBlBp4-3VBqIE6FTR2KhfyLVi7Pl1_m0wwPJgXu-Fmh7S-5HqV6o2kNNfxbTBdHNeGGUACeILyWR3zMN6Iw3IXfZs4Lu-yb9ynQmQje6lCx_IwxRVvI2SNym5MJ3oH5lFqmbtpdkJfwhB1sUJEdEgJ5iEwGnEtnWJDQPgSUh_43T95feCdA6znUBf7UdpUNuu05JsguiVtt7K_tT2UIuuVvof9Ue3GPhbcYOf2RkxK2Lm3EvI0o599EHSz8GOjyzbxSObMbWvZZwgkKHFQXVOzyoQTTWHFLADZSIgWXcViAEHw4v7N4JP82BlQXsKGgv4dNrEf1VdrUKNKxG3N6KDEB01P3CPua6FvVkUbard09CVB7EtXnTKT1tA6PN2ZnC18_44WENRdSnyX0OKFBy1isFDpep83gNvhCLoDvpAGgSJruf8zQD9GhS2XykfsYutxKDLen8fktWSwT5_OwekSn69xKRkyefjQBVGav9W0hJUtOL-MwuerrWpJXzjmMZiz-A-24K-bYLjCnU43GD3wnCYmVhLpAMqSoqxdkeIXTOz98GDS7xJhsXNsGWnl9noOZVMHcgiZGmuELMwt_kepT26mvBWj2mY8XEkYfGZB_l7BGgBKJj3rZwVZm-yEHoO7ZCEZo6LKP9p4m69bTYtUPXC7Ekp78_MKieZRMKyu_BeaURSSJmGPsVirO9onrMGwr1s7qZlr2Qr0QUsXEMd0mB-g4VO-hVocAezEqoQ1oYy48nNMBkKoSPpYSDZ_o6cMBfTpdLvkU6dy5xhbRWyrtSZB94xt0PjsuNWvU7KjiZNfij52VwKkAGVal0qPPtlfZVKXRrbA%3D%3D',
    'YOUTH_READTIMEBODY':
    "p=ecTMBiVxDAfc=eYMRZIJw4FHLsVlB9JQKGp44DiOI4f3Pv_oBxQzNAz9jtQ3i8_QUfSjeo9kfKyBlfhCcMUg67yNhSO44S63a8_AD30uQ46AVltnY6b_5FNsbyRjjeYZCIK0HeM2-jPQpi-2tCTlJeVzqfaldkXXvrmxSR5iltTfM2N5QeOmnkS3tvQsG7SphsTTBIy4t1Swomrj7phY8XWh47R1b-YPRh-iEuKDoQRa-YLyeFn1gle54mmcrtnCXyGXQRqIXTg-cxq5GOkPtt6Rgmin1s7z0vKExUie9lg6_klLGGbzi5WRS97_MI4FBjwbYEBIWWHgzU2Zta7sP32Fpxw0pqEGlgYucUO4lQxOVsj1BCNBdtLu_QEj9PJig3QElMU_8I7cCnHi8kabv3Gerh5xMkKSfvdrD8qJjhtC9vT0brsG-SNTRy8ipBN3BimSeliqRexjB97K5CS_5t4eZ_9Vqtf3h9u2BtcHzvtboIjKTLaIsdiAmKKZYwIgFsiEo7BC3_gBoc-6f5Q66ygrjN8EO4BtUye-ahgSGOgVm6jBfxiGemGi2RwlWSnZN-wd9BrnNdplrBuf3Y35OdqIqSYHUORXnwkKd7oy-f6rbV7ZHaFnD-LABft0Gvv7Tb4sVumLnEkx4tcE7vedFEKqAWQY1kvWxoAGElIWF9DWVTmM2eXT-GcONA9X1r6gJ7CXo5uXpmGbud0zZaIh0kvhinyftnmvIYqwhiMqJqiOPZT8fKOc9L45lWF-5Opy_KwOrcccmPOUojI0JlJaivosHlVpPScrP2P-HIxPGLZ0iK9I0Ap7txX3IdvXpNIXDOBALUP38aWoTATTa6euucG-MIlRPrsKPZKwCbi1vyEj7AoKqz5RPSm03cPVjUnEHMJXlOAe1Qpf8kr_LJd-lVKxJLlbSNidRh_RdQV31ndEBZj_qSKiWr_9rm6-JcnkSklpD9eg7LLns7ngyUB4rHt_mO43Gnr2zROWhLP8h7EM5-BVVB0XTkzmQGUNeL-RTYkXqMGSHnn70p4VVBBgetLNc0r1EMy7i7FIrkDDNbnhOf8B5LdnyCvxcDALOKW7GuRXbd1UK7K2Ezmp5bC3nZgYuZtO3aOem05HgXqV-jr84fCyEDkTndRJooutqyzEJhYVmVGuURNMpT4ngE5mBI7ceKfq48xz59sN0VCy6qGJGwY-9rAtKIupFeYah-Q5Gl0UjqXicl6l7W-o-nO0T-wLPTJW1_Gd-wVo-ZxIJ59QmET5tCySWckCZf3vL7GBYbWgkHY_7yef9S23J5hsJVsNdSYawaJW5tIsR2a610uVUCvryVsamfQ_w7dqYi7GYOqWZVDejvsnezVt8jub7XfvuZwWUjEdT9VtVBmzDyjbBFniNZy9kFeGWvT5pQVeqCtenExBrnSHwJ2q_Sd0eJ4YkSrxT28al8w==B",
    'YOUTH_WITHDRAWBODY':
    "p=kFbVGOYyXwIo%3DPsKtOYIB3RfdNtXTZAKxD06yUzQMnrlzvnn5d94Egr0arxNsE-5LRWyaB6VDKGrwrlz7zcCuWyk1g9GnYjGQ0FxhI2VD7ldnoqCnf37vBK-LDUlXIXVzkNnA79HAeAOM2MYeVRLOgYeniUBbBc1jQoBOaFecmglc-fZRQUqj9FURogB44XuHkztk47-ACcTrM4posUhHbU-jbacfL1nClxL4MESyqNCVs5FO6WRWP6NyU0Jyu9PbYQycVYpG_AAJveqzxOeoSSbp0405SbgY26Lqf-CXUlPTufJKN4kuhN2ryr_3KJqR7TWDxO5TRxpiOe-XVv_2GK7wBq2VzAS3Z9D1F7pe1om_J5Q03SGPDzF5sArV3mf80CEGUjb1CEYs-jceqTmRvvudz8QBFIlwf0sjsZYR59jfpyJvvXhVHQQnpQ1nkVLvuytaxbrzmLl1HoS5PekvfrzWM7VZ3S4-e5UiEW6zqVbKjOKK_eiZQrPYvqkSffnhBLY0uLyOvcEtZ6qf1URLkCFQRz5X5LZO6f43uAZZS-Cxgv6xR5smUbWOxc4zALWlatkkC2MoCrbe-q6gZ3VDT8r3maRvfmq7xRohpSUoIgLs_hFJB4XVeYzXONvT6j29ajjHvvwLkdNJQSAlhfFV_5b2gnZ6UyKfyH3I6rdzmimy6PkAUh6S3PvLlgnIOhkeAGz5Xjw4RDHSPq8SSfg2ogAJK4raine1iQkfdTtbCRcCBYe_QKMV25mfur_kSXkDRHJsj_47cSyw-84Ip0RkKf9G7x17YvpEGLpP0bh5ddgof_Otjvs2cRwpVst8vaa3FWU945k6qvzBdUWbsE2Uw0WSv4Erd-5n-4qrm_mfmjSsj5RaIt-RVUS5VH0st-2P9vl9Jq5D9WQjHwMhiFnLaOj80xjdMv_kQpDMz9hu3BmDiE8SSQ3_qKroJ0VHjiQM6PNSRWuNJI8YdAfchVOfOn7QOQ5JScSKln5nH4Cl1ATMnShPq8I1OEU9sLx-BBWPCJIJAHMqdYGtd94G9Z-EuMiASyR7Ajm9-ACALx9kB3cFDEO2S28ZPTT0n3oyEE6ckIOHq1dc2TR-BCIg5PqvE7tfyq08IFzN8rv_3hc-G1gCjgqvOs25Bsigic5eOzvT3uXw5-_mZZ1v1yjbPJ4nCbzc7e4jfSFANyjkBklgD0McUlLKy0ZVRAghRXH4ydNzPt9XDfMXub8DDx2SlRJQx5tjzVM5K27CocKClEMl9Ont8ULmRXWFAKHAfeQoJq91PtFLQmtXJWkHGvm8vuM5G1Nw_91J6FIdjnk0jPCIqxyqiUmgVaJSuoSGrogj_Xmiz7KN5vZoj5jBdnDzao2gfA74JJXjxMW5KBrOcdgjeYCzA3Eeu0su6Tsnq4pffMTg3BdD6fkFG6lFHbQ_sV6R0402ZcRuYgPjqtoYu6FvhnLqqLD07rBBCw0%3DD",
    'YOUTH_SHAREBODY':
    "access=WIFI&androidid=13c9ac78d3f49cc8&app-version=2.8.8&app_name=zqkd_app&app_version=2.8.8&article_id=36552476&carrier=CMCC&channel=c4081&device_brand=HUAWEI&device_id=50759328&device_model=TAS-AN00&device_platform=android&device_type=android&dpi=240&fp=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&from=4&imei=863064168372912&inner_version=202102011723&language=zh-CN&memory=3&mi=0&mobile_type=1&net_type=1&network_type=WIFI&openudid=13c9ac78d3f49cc8&os_api=25&os_version=TAS-AN00-user%207.1.2%20TAS-AN00%20700210126%20release-keys&request_time=1614664298&resolution=720x1280&rom_version=TAS-AN00-user%207.1.2%20TAS-AN00%20700210126%20release-keys&sim=1&sm_device_id=20210228102005ffbc4a4674f7e3b22bddf8e3c422fb37014e413713a7c18e&storage=61.39&stype=wx&subv=1.2.2&szlm_ddid=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&token=93a14cb187aa3642c88c4afbbff4fcd2&uid=54083321&version_code=56&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691pWaw3YGyhIyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3hWqGjH7frqm2apqGcXY&zqkey_id=7b5bfdea76bbd3d2755554ea67e31380"
}
# 提现和阅读时长信息没有抓到
cookies7 = {
    'YOUTH_HEADER':  {
        'Host': 'kd.youth.cn',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; TAS-AN00 Build/TAS-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36',
        'Referer': 'https://kd.youth.cn/html/income/index.html?access=WIFI&app-version=2.8.8&app_version=2.8.8&carrier=CMCC&channel=c4081&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691qayxt5eyhKKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3hWyFfHrgrt-2apqGcXY&cookie_id=80c9edd0d034857f4e183d80f77a3e09&device_brand=HUAWEI&device_id=50759328&device_model=TAS-AN00&device_platform=android&device_type=android&inner_version=202102011723&mi=0&openudid=13c9ac78d3f49cc8&os_api=25&os_version=TAS-AN00-user+7.1.2+TAS-AN00+700210126+release-keys&request_time=1614747675&resolution=720x1280&sim=1&sm_device_id=20210228102005ffbc4a4674f7e3b22bddf8e3c422fb37014e413713a7c18e&subv=1.2.2&szlm_ddid=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&uid=54135722&version_code=56&version_name=%E4%B8%AD%E9%9D%92%E7%9C%8B%E7%82%B9&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691qayxt5eyhKKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3hWyFfHrgrt-2apqGcXY&zqkey_id=80c9edd0d034857f4e183d80f77a3e09',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'cn.youth.news',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775': '1614569279,1614576444',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2254135722%22%2C%22%24device_id%22%3A%22177ec40bd481ff-0733d8e500622f-6f7e132f-230400-177ec40bd491af%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177ec40bd481ff-0733d8e500622f-6f7e132f-230400-177ec40bd491af%22%7D',
        'sensorsdata2019jssdkcross': '%7B%22distinct_id%22%3A%2254135722%22%2C%22%24device_id%22%3A%22177ebea7ea4326-06cdd1d9f435ec-6f7e132f-230400-177ebea7ea53dd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177ebea7ea4326-06cdd1d9f435ec-6f7e132f-230400-177ebea7ea53dd%22%7D',
        'Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775': '1614747661',
    },
    'YOUTH_READBODY':
    "p=ycTMBiVxDAfc=eYMRZIJw4FHLsVlB9JQKGp44DiOI4f3Pv_oBxQzNAz9jtQ3i8_QUfSjeo9kfKyBlfhCcMUg67yNhSO44S63a8_AD30uQ46AVltnY6b_5FNsbyRjjeYZCIK0HeM2-jPQpi-2tCTlJeVzqfaldkXXvrmxSR5iltTfM2N5QeOmnkS3tvQsG7SphsTTBIy4t1Swomrj7phY8XWh47R1b-YPRh-iEuKDoQRa-YLyeFn1gle54mmcrtnCXyGXQRqIXTg-cxq5GOkPtt6Rgmin1s7z0vKExUie9lg6_klLGGbzi5WRS97_MI4FBjwbYEBIWWHgzU2Zta7sP32Fpxw0pqEGlgYucUO4lQxOVsj1BCNBdtLu_QEj9PJig3QElMU_8I7cCnHi8kabv3GdcpX-cSo348j4X5unpKh2EaCvFPXp79lulV5BYgOFquvkStCpAhW-T_554ZD9c2YYDhMefCeUIs-hklpQPmmZt5R4-xjFP20HNaIZZFNbAgWeMQEQcnsdDdzZvZtEPTwMYRJj7ab-GVLz7O42v8SW58E81-LZK4apEzZpB3-QnjWqCLbWRKGzHRqWaf4E2jEv-yg69c9CJWBHKeEEI-lKyIPnrLEjVoEKHb7_Uh3xl1t1G_Qj9F9kBRlI4qGOCwaKGsV-i08em58annoIYSLm31BRnGJnbshr2V6kq5DgvZ4zOD0IIIUn32W5ZqDvdNcLPhXXnNqOb3Ui6Csw9JAOK7jremXKIzMGATGxD7xqhzlOmUM0rcLxoIPeWui7FECT1-y7uyusCEhIZu2PsxStLzjkIKT03clW1ZlXyj1OAM0NXGkTe2qxa9e_PdWZ_V91ctUDxkrFkmuknhzwSxuu3FesURuwz55ccWRlccUzTpW8-FN5ARJTJyVsvL-SUPW86BfkO0Nxxlujx2Is6EMDpsFCRhBQauIV7veQgCNiT6--DUyIEObrJ9zZd9WtMfFO-C3A6wlsu4BX7CXoHsFO_k8SXMI3yE4c_CbZbR_q3todWkjQx8KiyC5fmMF82bv7FnRTvPpL7qQINMOEsmvJ5TgPJN8NocLL6nRqjRG96V0GFKCB7Zu2cB7Ueh6WJoc5Mwk8gtIoJ6sakOtFn0yPKfqXhG4638tYrBTktgofRHXbJOqo7z9s2hJy_jTRbVkDBr5N4jWQtJqfoU4hf-qXKDHFTbHYLCY_T6Kmu-Hl4XZtqKz8xyewUhE7KGcZocpSLRlD0OFgmqW1zFCmE-_Lu_YuT4ZIhtxeEWNhdGJa1NgngKXd90XyAfyVQtTiB_d9qtL-2-kQMfDOH3qAQAhQooIcOhc97GQ3IGhRy75m8G_bqvP8fY95R5nDpex08G-CbTHPcZ9HWRgtxObvOsj6U9gYCZqWr3FJ3iYygNOZRwuq5s8x-bDV1KSj_IhiAUfhOAO7Ip77PIn2wU6nq_D0Aa",
    'YOUTH_REDBODY':
    "p=9NwGV8Ov71o=gW5NEpb6rjazbBlBp4-3VBqIE6FTR2KhfyLVi7Pl1_m0wwPJgXu-Fmh7S-5HqV6o2kNNfxbTBdHNeGGUACeILyWR3zMN6Iw3IXfZs4Lu-yb9ynQmQje6lCx_IwxRVvI2SNym5MJ3oH5lFqmbtpdkJfwhB1sUJEdEgJ5iEwGnEtnWJDQPgSUh_43T95feCdA6znUBf7UdpUNuu05JsguiVtt7K_tT2UIuuVvof9Ue3GPhbcYOf2RkxK2Lm3EvI0o599EHSz8GOjyzbxSObMbWvZZwgkKHFQXVOzyoQTTWHFLADZSIgWXcViAEHw4v7N4JP82BlQXsKGgv4dNrEf1VdrUKNKxG3N6KDEB01P3CPua6FvVkUbard09CVB7EtXnTKT1tA6PN2ZnC18_44WENRdSnyX0OKFBy1isFDpep83gNvhCLoDvpAGgSJruf8zQD9GhS2XykfsYutxKDLen8fktWSwT5_OwekSn69xKRkyefjQBVGav9W0hJUtOL-MwuerrWpJXzjmMZiz-A-24K-bYLjCnU43GD3wnCYmVhLpAMqSoqxdkeIXTOz98GDS7xJhsXNsGWnl9noOZVMHcgiZGmuELMwt_kepT26mvBWj2mY8XEkYfGZB_l7BGgBKJj3rZwVZm-yEHoO7ZCEZo6LKP9p4m69bTYtUPXC7Ekp78_MKieZRMKyu_BeaURSSJmGPsVirO9onrMGwr1s7qZlr2Qr0QUsXEMd0mB-g4VO-hVocAezEqoQ1oYy48nNMBkKoSPpYSDZ_o6cMBfTpdLvkU6dy5xhbRWyrtSZB94xt0PjsuNWvU7KjiZNfij52VwKkAGVal0qPPtlfZVKXRrbA%3D%3D",
    'YOUTH_READTIMEBODY':
    "p=XYdVi_XPUOzA=7ioCfKCMWbKZ8BDqt18ZclD65zMt4knVbpLxufIJdHkTcSpTdqKK6vnaWO5Cfsm4o7Z5yipAjOFS8GWQATdVwfpP8iJKRVSvmdl4iISxqzXgkMOygF4j-C5mxggftKzWNRa15E-5B4mx2OzOI7x6LJREjD5sSQJem5e6HuXChwVJXeQ8nu9fXLrgMeBkFOkK794H8MYo4kRql_rUJw12fLXhsjcIAueV7u-5jKJG1xnK5fvbHJyCtpLYJnQwo0UiZT2i03dO5qh2VOw_Ep0pKV4BoZAWEd3ZHTyQ1UgZk_rCQJaa2HgZziO_dAolg3IViEeYfGXLl_Mt3thnyhrryOBXPFqkSZ_FiPtDxsdJhJItKpOdMuljNxA617GISfD0JR7kqtZRXGcdh0BU-qlrPV9wRuERIswqn9CbfNm-9Y_639kzSsid_E9O1659FsavHs7CAj1aPZEGvHzvSxbBCMaLz_UGYZ5ixUP2xAiRDwI0GLO_nXNxFhlsqypgaKGv2C_q_K45xz5ItibIqzkYJBnvRhR201gJfo1N1nztIJsF1XzO-SeRjfTiycQpShAWCCaueMrqdYIuy6b78iuNs-_432wNefTjsABGM559IMF07pp0zucj0bpit_DnLgRQrc6IrxZWV7JF1BdeUNFVRRZPGLph3zi_Qz6E0uQ79xSmTJ-GEJ8CGTWdptMNEwl_qcFmOmQgf4qnJhChjtCC1ONSElPK3bfyi3cef6aaZ26R7fZETneEf4uzJBOw6kHXsQaIR6Oi1rf1qTx9NJY5xzCsnSk74WuWwoXJlRfvSi5679MEHpaoOa8ZXGDcE7w_UmJQb4c_skCaoOAfslmW7k3yqheVZPtlnKtuzd_W7F8Qa3n_UejmUZJPxc9lVl-9gl6jZAslKiCbTpeAWsT_2UjZNKo6SnEZVcbxydad4NvHSaHyv0kZtR5xkp_IOJDNlHpOUYQfQT6TXDtfl4VIXDcuDMckqwDdiUWhVy1QMzzmsPJKogzUs2_9jtRgz20EgXC3y9vdn5Ykx2w55NswDBMclVy5kgsd_-yiubKtYvve_5_UnhHOoao8zvJhwWqtZ9OZFcNvsblIgpW7hmXpFWOmd6i9z1UKzokNYZY1gR6laE-ac9mlsDp16t8nyrIseXT2SA-Qto2uEv0YOS3EMsoBsi1Ryr00bZn03qb1KQxCycusfaQon8W2YtmHC_zuny7Q6pJiTjVIJ5b_QgQ-M00UCyUokw4-EJoeWBUGZPmCe7n8RkoqQqqjtka9O9Xfr9La2M3I7Q9PeC7Hya5bkKt_xbsDOVhAZjzXilWIH61TfR1lDXbyWpj-0Tz4fAwNkk8HISU8TYl74KblvwY9Nxg69mNdVoz-xybJQQSQO2HdN4064aZ2TpfJMJtTjuh9GS6TdTn6OtOjdwA56BrkTA==GN",
    'YOUTH_WITHDRAWBODY':
    "p=kFbVGOYyXwIo%3DPsKtOYIB3RfdNtXTZAKxD06yUzQMnrlzvnn5d94Egr0arxNsE-5LRWyaB6VDKGrwrlz7zcCuWyk1g9GnYjGQ0FxhI2VD7ldnoqCnf37vBK-LDUlXIXVzkNnA79HAeAOM2MYeVRLOgYeniUBbBc1jQoBOaFecmglc-fZRQUqj9FURogB44XuHkztk47-ACcTrM4posUhHbU-jbacfL1nClxL4MESyqNCVs5FO6WRWP6NyU0Jyu9PbYQycVYpG_AAJveqzxOeoSSbp0405SbgY26Lqf-CXUlPTufJKN4kuhN2ryr_3KJqR7TWDxO5TRxpiOe-XVv_2GK7wBq2VzAS3Z9D1F7pe1om_J5Q03SGPDzF5sArV3mf80CEGUjb1CEYs-jceqTmRvvudz8QBFIlwf0sjsZYR59jfpyJvvXhVHQQnpQ1nkVLvuytaxbrzmLl1HoS5PekvfrzWM7VZ3S4-e5UiEW6zqVbKjOKK_eiZQrPYvqkSffnhBLY0uLyOvcEtZ6qf1URLkCFQRz5X5LZO6f43uAZZS-Cxgv6xR5smUbWOxc4zALWlatkkC2MoCrbe-q6gZ3VDT8r3maRvfmq7xRohpSUoIgLs_hFJB4XVeYzXONvT6j29ajjHvvwLkdNJQSAlhfFV_5b2gnZ6UyKfyH3I6rdzmimy6PkAUh6S3PvLlgnIOhkeAGz5Xjw4RDHSPq8SSfg2ogAJK4raine1iQkfdTtbCRcCBYe_QKMV25mfur_kSXkDRHJsj_47cSyw-84Ip0RkKf9G7x17YvpEGLpP0bh5ddgof_Otjvs2cRwpVst8vaa3FWU945k6qvzBdUWbsE2Uw0WSv4Erd-5n-4qrm_mfmjSsj5RaIt-RVUS5VH0st-2P9vl9Jq5D9WQjHwMhiFnLaOj80xjdMv_kQpDMz9hu3BmDiE8SSQ3_qKroJ0VHjiQM6PNSRWuNJI8YdAfchVOfOn7QOQ5JScSKln5nH4Cl1ATMnShPq8I1OEU9sLx-BBWPCJIJAHMqdYGtd94G9Z-EuMiASyR7Ajm9-ACALx9kB3cFDEO2S28ZPTT0n3oyEE6ckIOHq1dc2TR-BCIg5PqvE7tfyq08IFzN8rv_3hc-G1gCjgqvOs25Bsigic5eOzvT3uXw5-_mZZ1v1yjbPJ4nCbzc7e4jfSFANyjkBklgD0McUlLKy0ZVRAghRXH4ydNzPt9XDfMXub8DDx2SlRJQx5tjzVM5K27CocKClEMl9Ont8ULmRXWFAKHAfeQoJq91PtFLQmtXJWkHGvm8vuM5G1Nw_91J6FIdjnk0jPCIqxyqiUmgVaJSuoSGrogj_Xmiz7KN5vZoj5jBdnDzao2gfA74JJXjxMW5KBrOcdgjeYCzA3Eeu0su6Tsnq4pffMTg3BdD6fkFG6lFHbQ_sV6R0402ZcRuYgPjqtoYu6FvhnLqqLD07rBBCw0%3DD",
    'YOUTH_SHAREBODY':
    "access=WIFI&androidid=13c9ac78d3f49cc8&app-version=2.8.8&app_name=zqkd_app&app_version=2.8.8&article_id=36584071&carrier=CMCC&channel=c4081&device_brand=HUAWEI&device_id=50759328&device_model=TAS-AN00&device_platform=android&device_type=android&dpi=240&fp=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&from=4&imei=863064168372912&inner_version=202102011723&language=zh-CN&memory=3&mi=0&mobile_type=1&net_type=1&network_type=WIFI&openudid=13c9ac78d3f49cc8&os_api=25&os_version=TAS-AN00-user%207.1.2%20TAS-AN00%20700210126%20release-keys&request_time=1614779161&resolution=720x1280&rom_version=TAS-AN00-user%207.1.2%20TAS-AN00%20700210126%20release-keys&sim=1&sm_device_id=20210228102005ffbc4a4674f7e3b22bddf8e3c422fb37014e413713a7c18e&storage=61.39&stype=wx&subv=1.2.2&szlm_ddid=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&token=21db1cdd31cbabc18329ff4a11d57c14&uid=54135722&version_code=56&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691qayxt5eyhKKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3hWyFsoqZr7mmapqGcXY&zqkey_id=9c92ca22fffaf09e6becedc1b47ca8fc"
}

cookies8 = {
    'YOUTH_HEADER':  {
        'Host': 'kd.youth.cn',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; TAS-AN00 Build/TAS-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36',
        'Referer': 'https://kd.youth.cn/html/income/index.html?access=WIFI&app-version=2.8.8&app_version=2.8.8&carrier=CMCC&channel=c4081&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691rWWyt5tuhbKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3ibKEjHabr6mmapqGcXY&cookie_id=ab338feba11fa06a79d2b9e4771f0e3c&device_brand=HUAWEI&device_id=50759328&device_model=TAS-AN00&device_platform=android&device_type=android&inner_version=202102011723&mi=0&openudid=13c9ac78d3f49cc8&os_api=25&os_version=TAS-AN00-user+7.1.2+TAS-AN00+700210126+release-keys&request_time=1615299178&resolution=720x1280&sim=1&sm_device_id=20210228102005ffbc4a4674f7e3b22bddf8e3c422fb37014e413713a7c18e&subv=1.2.2&szlm_ddid=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&uid=54279897&version_code=56&version_name=%E4%B8%AD%E9%9D%92%E7%9C%8B%E7%82%B9&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691rWWyt5tuhbKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3ibKEjHabr6mmapqGcXY&zqkey_id=ab338feba11fa06a79d2b9e4771f0e3c',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'cn.youth.news',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775': '1614569279,1614576444',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2254135722%22%2C%22%24device_id%22%3A%22177ec40bd481ff-0733d8e500622f-6f7e132f-230400-177ec40bd491af%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177ec40bd481ff-0733d8e500622f-6f7e132f-230400-177ec40bd491af%22%7D',
        'sensorsdata2019jssdkcross': '%7B%22distinct_id%22%3A%2254279897%22%2C%22%24device_id%22%3A%22177ebea7ea4326-06cdd1d9f435ec-6f7e132f-230400-177ebea7ea53dd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177ebea7ea4326-06cdd1d9f435ec-6f7e132f-230400-177ebea7ea53dd%22%7D',
        'Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775': '1615299072',
    },
    'YOUTH_READBODY': "p=c2JgR8oZr6IU=3jJeRBx8_Tpz442V0PZl57K_4wSG7H3DXE8V3cvfxdgG4G7kAOSou9Yr72QO9aFKWC26DS8bN2IJm69nizUFJ3fgipcFW3i_rSjwlyCGUtel_MadHaRSJz22b-ZyzviTpoQU4HiI1wg1FQBqt2O4gYY2VNNU_-_tt4yXMps7InZ102N8YnBrq34ntYkJG8xb_quePdbOBJQvtdrmDlYbI6eKKmH59l1jhRdLOFSTwa9TCWmTW-pvdfDkKgAoU-Yvqv_S1dO2hNZLzE2kQsj3jSKS081wOugz8EykNJA1ATsOCnNM3_N5Z8Z3mbvflmyif2ji_lE7zkObm_TVKLWs1HRD-wXbAmLhEQAaJi0K-SqW4XEolImquIbpMUIZwQPpV8ybwsxGc7OZ_GJyyBBWUBN8a2UXrPKOIKgK3v9bPAYiTbXyHnNZXRs0FpcDoE_n_Q4vT3jD2U3G-yiTkZ7tjV6BCqylJl2CCTdOIWY_VoQoELv5SoqOtmXXNQQbnaWEffrN7dX547BKYa7_x3i28oetDZZL7f65_FIwlyswOKvqqXDpV6V2vCehdfVHLz8z7hm9IXPhPuG-5CmrW7aIOIu9GqhdpjkC8hfKq5Yny-dlEjtCsRCAutjlzlyLt9cHCsCKvA76yFL7VDL8NrfgrtsGoQqr80Ys0l2pzbVzK0snTiM0T7p7-fArCFPLvRdGkLjGHwhltMeB0XfqoujXqiRsPfMO_Ank1PED_pgUk5dmjJBvaKLneH0SC-Om3oMlzutsg8ismpAQG_l5fAngZKXiFQJQEzmKQxKAl0MH0fnP8hxwtKdsln7EFuEuKpIb45Yna_I34dRYW6eFffGf6VbwukxzvwYvbiOy7b7E-07mfIZ91G272sGqkkBj56LBnw0_QHY9wTP3QqOgsNlUoe244ZCwQjHfIyT63H38CTSf0jwrQSht7uR8RCE8kkHpCe8AICLisZmrZVGamcg5zlnqRGWarnXYSMcqgc0LyrhNaKvVAufAZMwZOUrTPP_N1dgVKbwJ9Oxt92aS5ErmxxnzY-m1Q4-x1Moi0nqhOWYgfqrfUhPck7HdE6uxwvo1zOIb3LlwgXRmKgkcmprvp61hwXij7dmJjBwP9d_VM9Emga9CKTPaWK83Aky3mxXQ39_nAkgIUxmFlQrGvtbRd5411TmKRQk7NkVDkfbt3upcP1Cb5cdU72D-irXhki9jBWZWknQEMNiHk-0ZH3TeOszHjdpKM-95YWMm-Z7L0ULbUoVZp6WXk4-WCnKdvZge3P5vME1vFb7g7PhAP5ccG0Poppl8BVWNoARaaE239Qrpx3FYo8HqHh6wdKpxlgS-1zLZlwoUMlnj8XKe4FhqmhgfOJlSh5hQdvrh_QJm-m09oIL0Y9blm75NchOWbgxbD0gLbmh5oK-rvoRe1kTN32hOJ1MPh6uA",
    'YOUTH_REDBODY':
    "p=jYFg4QJ5A6eY=fvHMutpdSzxiZkUGzaUqhfYzb47FFCgEbgAFx-QNQ9auJXDo5D6g4NeiFmGz-mODbuy_JVne7pmweCm9K6yIqkB6C-zT3OJxIohlZ6OOovLjer2W2bunzugabBJt7cpoPr10H0OwnXvRluvc2Re7-VfWb6E_CASJZaVo89J-lHRKG91bNC0D2I1ZTdIctkWbUMkqlEke36_Ww_59hlFT2AL-0Ka9jt0BpIDKnJPLib-FozCiVDwkESGtYzf79Wv9qPBlSskmbiB_-YWr3tzhIVvsw-przT3KtJaTAtlYkR5Z0tkn4aA9sa8NqiQIKLoqdwDiNUPBGsJzx7bQODh-9s-Vk2BANqnvp8Y84nw1iNz3YQ_lLRsUZxxkf61yQpiGgeLqR6_Ccwh5fDuWo9veFe2TS3015-1NVh6nCGrlgbpnKCK-bkrBVH53LHUbv8JCC5S3wtk5DF_5e2lYyTQfs7RBnodI9XOND3UHI1v_9ZWexffidVeGrHLWzs-tjDhGaeg_JSEqniKGjjUjVFtWGaz2P16XKVtnEdCk8U-KdDzYPmGzzkrDkgtYOCmTTxp6PX6ZUUcRot_FRrIeUIy34fOjE6kgCghZBEITxgdeIPQE_-D2_cUuU6EQWIFRLdr04eGkvEM1W01tZeHeX_Yghz31MwzhqibeKFfZNmUtAvWWrmSLJLSDdg_nn9GCt8VtmqkY4QLowJ-ai5yeTDjzwFb5re4nUYgfOJmWJV9G_Tau483K7DfQ05GQcQXyu0vpay4P7NjAK3gYIdnPnyGfX5_ykr4sa2NZ0HEZHLwDgB6OT4-bFzh2sE5Y5oSx0HE_bMswsqvL0mTIXS4JOWTPWNYJT1zPXoO2_h_RhoC5PJljRAesqgmdyh5JBSOby5cwImEcUIAnncFNY97-IKyHCBXPOP6wSrpSs_xeol0nVnh-m5x8u_uTBUQyGP5tDpPfj5KnmSk-8-mTItKyYu9qKG5oF8UWVK3Sjhk3vqmoxSylaCg8E5UgkQ97NOzPa4Oc6MZooO-nB-RTZI3TekUbrJrLkqCCkpFp7u1ZEmYQR4klRb5cWO9GCbjGoHGSGp_KdwD-V4unAcXB7qsAP2z8E_lEWKOTI6f-AhmTUn8rzKHkzHsPEiMmSqcRFPC8KEPl_iNnEhs__2iZMtNDuzF8bH0iQrHZjqqotOT9ULv5M_6aw3IaxW5_drX3x_LU37L2_qvi-qbxmQ5GZ1RroP4jo3mACbMLihl3lD3bEaFxP116EKekDE6Uhq11ER7mNoCWOH1ISCz83X14GCp-cVBz2ON-l6IKLjP6urcs2DNjONRB_MXsvNTfoIMyWF9-f7calZGnALAgOXsrs29yVq6e6OaryP-hhKkDCRgOnL3WY6yuwgKzi8SYxAXOsGi0XqPHL0v3rI0_wvSVnmZz8Tagu5nCVJuC_zuacrXIPemoUMKFenA2Jtkat6uP_ltYE2Te",
    'YOUTH_READTIMEBODY':
    "p=12JgR8oZr6IU=3jJeRBx8_Tpz442V0PZl57K_4wSG7H3DXE8V3cvfxdgG4G7kAOSou9Yr72QO9aFKWC26DS8bN2IJm69nizUFJ3fgipcFW3i_rSjwlyCGUtel_MadHaRSJz22b-ZyzviTpoQU4HiI1wg1FQBqt2O4gYY2VNNU_-_tt4yXMps7InZ102N8YnBrq34ntYkJG8xb_quePdbOBJQvtdrmDlYbI6eKKmH59l1jhRdLOFSTwa9TCWmTW-pvdfDkKgAoU-Yvqv_S1dO2hNZLzE2kQsj3jSKS081wOugz8EykNJA1ATsOCnNM3_N5Z8Z3mbvflmyif2ji_lE7zkObm_TVKLWs1HRD-wXbAmLhEQAaJi0K-SqW4XEolImquIbpMUIZwQPpV8ybwsxGc7NzRIshOZBWbY7RZWyGEme2D_ekNeuZkGRLUPG9OvhWGbSiumujxgieq57RQueSe4PMeS6Lc2RWTXoq9T7G0APVVUB4JhGD2E5ImCxqDb2LrInrWsRe14N_QRk8fyP5fOBfuv4DqaCArV_zTV_yGRbhvFdirAjdU8H6_FyS97iUKrY2XZMd7MTbYcIHRHITjJajxGn_HaeA4FYP9_qSNY_gTJfALqbcjLk1mFAUGsojnoF3QaHfgZI9DRshTwRMS61WFqCqy1kLmVDtZHPR6bEKQl3pgNprrXFmxO68YT4LtRh9iFuKeTr1DYU2nAwKK47EsVJZGmOlmueYc1WYaiSiW4SpAA0BfEIgU5mKjYSRbi3U_uKqJ4M_BIdGIMUfO3_m-GNHvUJ9_M9SAwOxlpm6R7JOmh_hcAjJ__nUuwvyT37frF0xeE7ztoE0GPkmmRN24E5WZ3LriTav3A0C-81JiZBbBLMtuG4E3HtEMVzjejiWoY8eWH4sFdTR8zXdGAzdfzJJ47_fuFb06dhOu_iQ0Sg6InebcsZpQ8fEXJ2MbunogdYz5g_tMvAvPOZOu6_-EqJpWw8nCuZxFG_wNimd0_Ki3j1V_XEbJQOjuJcZeR35galPMbfVQPUiffwitdyA5Lzi1eJXULeltrvJQfUiKMtjsqL_6QQGQWPbhNMY9p9xxYyXB1Vh2W4VzAVHXR6vAbeXUbvmLSBC9Kj11d3dYETwcrEJS_-9Z_KLWIQ-OGejl9Zjt4Y1Orop6y1wsE6noaKTNHSsowZXSQWMIkWZuSy8lXHUuvoyKamirKDVzEyqQprKXZAMaKWxgv0ljqB6YiNUIkiqG-c63nMHp7_m-sroRq3Vl0OJdPY2U4hMO7S39f2U7AvdEBRObWmC1CczVBaF8KrhfZCu2I9a8ZjnrwVAgsdsL4pcRHCSbsoyFJh4JNmrTghJJQVYbhCF9QpYJTy6jqaPdroFvtBbmQOWXwtb85kYQ7nGbD6ZHD9Kcpq84mfufeIkzz_JhLfkKsl9_RhTGlMqqQ==",
    'YOUTH_WITHDRAWBODY':
    "p=CFbVGOYyXwIo=PsKtOYIB3RfdNtXTZAKxD06yUzQMnrlzvnn5d94Egr0arxNsE-5LRWyaB6VDKGrwrlz7zcCuWyk1g9GnYjGQ0FxhI2VD7ldnoqCnf37vBK-LDUlXIXVzkNnA79HAeAOM2MYeVRLOgYeniUBbBc1jQoBOaFecmglc-fZRQUqj9FURogB44XuHkztk47-ACcTrM4posUhHbU-jbacfL1nClxL4MESyqNCVs5FO6WRWP6NyU0Jyu9PbYQycVYpG_AAJveqzxOeoSSbp0405SbgY26Lqf-CXUlPTufJKN4kuhN2ryr_3KJqR7TWDxO5TRxpiOe-XVv_2GK7wBq2VzAS3Z9D1F7pe1om_J5Q03SGPDzF5sArV3mf80CEGUjb1CEYs-jceqTmRvvudz8QBFIlwf0sjsZYR59jfpyJvvXhVHQQnpQ1nkVLvuytaxbrzmLl1HoS5PekvfrzWM7VZ3S4-e5UiEW6zqVbKjOKK_eiZQrPYvqkSffnhBLY0uLyOvcEtZ6qf1URLkCHmD-RbFugVV9fOHjP5wJ8kNlFsOK_I_RPb0rXbHBnAmhoxrNqKNQSHk2GPDnX0eEHlyiqoPDoh23qC4pz5epAMQ7AABtSSrkkXvuusod6jT0rAj6eJpBOAahbMGNfAnFDpYvxCpZXAtaa29uyg5EMcxjXqZsiqlz9M8V0cwBJrLTliVREJu3UZnFSLRCNIR8nU5ycwLgydBcRKJAkemUSQoC58HxnKu8f8dCXHCkZQTo0LKkbe1FfCnROlEeeenaDr82584CYvEP00Laspn4Vt2oNnIt_jZRNCmrKM_KnBcTegabrOjclZsNezgwDCiUq1iE-X7bWq6IfOtUO_JrwnXwgZhWobnInodGECty5gBpQukrZHQAtB7ncjNhqILiwrSu9P5YRY7e7SGTs8Tyg6e0oYQ8E1bphx-wHQcFLWd7C8Rmc0FgT0wVA4010gIlh-U6krVWpbzGGnFw5ceRCBPvxhdThsy72pnYB3VgQYJ-hTvp7SVZq5wY9I0SimFx_HELYdyN6X6YzjUUEtmYXuz0bvqoqUAjMcF4vWCqYmAuFOsCBHwH9TmzQuLeYLk9xVcw7FW6uLBRoxzPafffdkVpM-Jy7Kdu1WMIR9OSdXE05Dw57gs5xTD8P3Mmkc0H0bw0Br8G16xMtZKwdThosQ0ld7aKKPS423vF_GjWmQNQnYlZxN1hHm5ddMqXNUx_fGEGX0d6vGyk_a0ChSzNeI5dLE4JbeO-vrEv_q2KUqkl87z-TQVG4LPb-pp3lp_NVgPtvcNsDFiMHlXCwfHBYNoOQuXeH7_yo1Zh8DlykR8MqouzEo94HLCNsN5GG4GlfW6mRGQawbhfI0RwuFw2HChL8vXsfd0KoS9vsRw5ss8rczI78Kd1HYsSX1zGfypp6StrRC-ZWaakN77G8VmM6BRg-gh20JhzY=p",
    'YOUTH_SHAREBODY':
    "access=WIFI&androidid=13c9ac78d3f49cc8&app-version=2.8.8&app_name=zqkd_app&app_version=2.8.8&article_id=36721302&carrier=CMCC&channel=c4081&device_brand=HUAWEI&device_id=50759328&device_model=TAS-AN00&device_platform=android&device_type=android&dpi=240&fp=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&from=4&imei=863064168372912&inner_version=202102011723&language=zh-CN&memory=3&mi=0&mobile_type=1&net_type=1&network_type=WIFI&openudid=13c9ac78d3f49cc8&os_api=25&os_version=TAS-AN00-user%207.1.2%20TAS-AN00%20700210126%20release-keys&request_time=1615299195&resolution=720x1280&rom_version=TAS-AN00-user%207.1.2%20TAS-AN00%20700210126%20release-keys&sim=1&sm_device_id=20210228102005ffbc4a4674f7e3b22bddf8e3c422fb37014e413713a7c18e&storage=61.39&stype=wx&subv=1.2.2&szlm_ddid=DuQipKRR8wtNQzYU8AIPYcOfpX2MWQl594q8P%2BJyNJiwhpzlpkT4Srm7vl%2B5ZHzSDkqDPQ7M9PToe9A56DI%2Fnz6Q&token=6f4229aca6498d92736c51f48d88438b&uid=54279897&version_code=56&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691rWWyt5tuhbKp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3ibKEjHabr6mmapqGcXY&zqkey_id=ab338feba11fa06a79d2b9e4771f0e3c"
}
COOKIELIST = [cookies1, cookies2]
# COOKIELIST = [cookies8]

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
    COOKIELIST = []
    for i in range(5):
        headerVar = f'YOUTH_HEADER{str(i+1)}'
        readBodyVar = f'YOUTH_READBODY{str(i+1)}'
        redBodyVar = f'YOUTH_REDBODY{str(i+1)}'
        readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
        withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
        shareBodyVar = f'YOUTH_SHAREBODY{str(i+1)}'
        if headerVar in os.environ and os.environ[
                headerVar] and readBodyVar in os.environ and os.environ[
                    readBodyVar] and redBodyVar in os.environ and os.environ[
                        redBodyVar] and readTimeBodyVar in os.environ and os.environ[
                            readTimeBodyVar]:
            globals()['cookies' + str(i + 1)]["YOUTH_HEADER"] = json.loads(
                os.environ[headerVar])
            globals()['cookies' +
                      str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
            globals()['cookies' +
                      str(i + 1)]["YOUTH_REDBODY"] = os.environ[redBodyVar]
            globals()[
                'cookies' +
                str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
            globals()[
                'cookies' +
                str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
            globals()['cookies' +
                      str(i + 1)]["YOUTH_SHAREBODY"] = os.environ[shareBodyVar]
            COOKIELIST.append(globals()['cookies' + str(i + 1)])
    print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"


def get_standard_time():
    """
  获取utc时间和北京时间
  :return:
  """
    # <class 'datetime.datetime'>
    utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
    beijing_datetime = utc_datetime.astimezone(timezone(
        timedelta(hours=8)))  # 北京时间
    return beijing_datetime


def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))


def sign(headers):
    """
  签到
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = 'https://kd.youth.cn/TaskCenter/sign'
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           timeout=30).json()
        print('签到')
        print(response)
        if response['status'] == 1:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def signInfo(headers):
    """
  签到详情
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = 'https://kd.youth.cn/TaskCenter/getSign'
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           timeout=30).json()
        print('签到详情')
        print(response)
        if response['status'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def punchCard(headers):
    """
  打卡报名
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}PunchCard/signUp'
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           timeout=30).json()
        print('打卡报名')
        print(response)
        if response['code'] == 1:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def doCard(headers):
    """
  早起打卡
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}PunchCard/doCard'
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           timeout=30).json()
        print('早起打卡')
        print(response)
        if response['code'] == 1:
            shareCard(headers=headers)
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def shareCard(headers):
    """
  打卡分享
  :param headers:
  :return:
  """
    time.sleep(0.3)
    startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
    endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
    try:
        response = requests_session().post(url=startUrl,
                                           headers=headers,
                                           timeout=30).json()
        print('打卡分享')
        print(response)
        if response['code'] == 1:
            time.sleep(0.3)
            responseEnd = requests_session().post(url=endUrl,
                                                  headers=headers,
                                                  timeout=30).json()
            if responseEnd['code'] == 1:
                return responseEnd
        else:
            return
    except:
        print(traceback.format_exc())
        return


def luckDraw(headers):
    """
  打卡分享
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}PunchCard/luckdraw'
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           timeout=30).json()
        print('七日签到')
        print(response)
        if response['code'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def timePacket(headers):
    """
  计时红包
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}TimePacket/getReward'
    try:
        response = requests_session().post(
            url=url,
            data=f'{headers["Referer"].split("?")[1]}',
            headers=headers,
            timeout=30).json()
        print('计时红包')
        print(response)
        return
    except:
        print(traceback.format_exc())
        return


def watchWelfareVideo(headers):
    """
  观看福利视频
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}NewTaskIos/recordNum?{headers["Referer"].split("?")[1]}'
    try:
        response = requests_session().get(url=url, headers=headers,
                                          timeout=30).json()
        print('观看福利视频')
        print(response)
        return
    except:
        print(traceback.format_exc())
        return


def shareArticle(headers, body):
    """
  分享文章
  :param headers:
  :return:
  """
    url = 'https://ios.baertt.com/v2/article/share/put.json'
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('分享文章')
        print(response)
        return
    except:
        print(traceback.format_exc())
        return


def threeShare(headers, action):
    """
  三餐分享
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}ShareNew/execExtractTask'
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
    body = f'{headers["Referer"].split("?")[1]}&action={action}'
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('三餐分享')
        print(response)
        return
    except:
        print(traceback.format_exc())
        return


def openBox(headers):
    """
  开启宝箱
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}invite/openHourRed'
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           timeout=30).json()
        print('开启宝箱')
        print(response)
        if response['code'] == 1:
            share_box_res = shareBox(headers=headers)
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def shareBox(headers):
    """
  宝箱分享
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}invite/shareEnd'
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           timeout=30).json()
        print('宝箱分享')
        print(response)
        if response['code'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def friendList(headers):
    """
  好友列表
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
    try:
        response = requests_session().get(url=url, headers=headers,
                                          timeout=30).json()
        print('好友列表')
        print(response)
        if response['error_code'] == '0':
            if len(response['data']['active_list']) > 0:
                for friend in response['data']['active_list']:
                    if friend['button'] == 1:
                        time.sleep(1)
                        friendSign(headers=headers, uid=friend['uid'])
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def friendSign(headers, uid):
    """
  好友签到
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
    try:
        response = requests_session().get(url=url, headers=headers,
                                          timeout=30).json()
        print('好友签到')
        print(response)
        if response['error_code'] == '0':
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def sendTwentyScore(headers, action):
    """
  每日任务
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
    try:
        response = requests_session().get(url=url, headers=headers,
                                          timeout=30).json()
        print(f'每日任务 {action}')
        print(response)
        if response['status'] == 1:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def watchAdVideo(headers):
    """
  看广告视频
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
    try:
        response = requests_session().post(url=url,
                                           data="type=taskCenter",
                                           headers=headers,
                                           timeout=30).json()
        print('看广告视频')
        print(response)
        if response['status'] == 1:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def watchGameVideo(body):
    """
  激励视频
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           data=body,
                                           timeout=30).json()
        print('激励视频')
        print(response)
        if response['success'] == True:
            return response['items']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def visitReward(body):
    """
  回访奖励
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/mission/msgRed.json'
    headers = {
        'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('回访奖励')
        print(response)
        if response['success'] == True:
            return response['items']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def articleRed(body):
    """
  惊喜红包
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/article/red_packet.json'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('惊喜红包')
        print(response)
        if response['success'] == True:
            return response['items']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def readTime(body):
    """
  阅读时长
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/user/stay.json'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('阅读时长')
        print(response)
        if response['error_code'] == '0':
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def rotary(headers, body):
    """
  转盘任务
  :param headers:
  :return:
  """
    time.sleep(0.3)
    currentTime = time.time()
    url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('转盘任务')
        print(response)
        return response
    except:
        print(traceback.format_exc())
        return


def rotaryChestReward(headers, body):
    """
  转盘宝箱
  :param headers:
  :return:
  """
    time.sleep(0.3)
    currentTime = time.time()
    url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('转盘宝箱')
        print(response)
        if response['status'] == 1:
            i = 0
            while (i <= 3):
                chest = response['data']['chestOpen'][i]
                if response['data']['opened'] >= int(
                        chest['times']) and chest['received'] != 1:
                    time.sleep(1)
                    runRotary(headers=headers, body=f'{body}&num={i+1}')
                i += 1
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def runRotary(headers, body):
    """
  转盘宝箱
  :param headers:
  :return:
  """
    time.sleep(0.3)
    currentTime = time.time()
    url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('领取宝箱')
        print(response)
        if response['status'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def doubleRotary(headers, body):
    """
  转盘双倍
  :param headers:
  :return:
  """
    time.sleep(0.3)
    currentTime = time.time()
    url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
    try:
        response = requests_session().post(url=url,
                                           data=body,
                                           headers=headers,
                                           timeout=30).json()
        print('转盘双倍')
        print(response)
        if response['status'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def incomeStat(headers):
    """
  收益统计
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
    try:
        response = requests_session().get(url=url, headers=headers,
                                          timeout=50).json()
        print('收益统计')
        print(response)
        if response['status'] == 0:
            return response
        else:
            return
    except:
        print(traceback.format_exc())
        return


def withdraw(body):
    """
  自动提现
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
    headers = {
        'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           data=body,
                                           timeout=30).json()
        print('自动提现')
        print(response)
        if response['success'] == True:
            return response['items']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def bereadRed(headers):
    """
  时段红包
  :param headers:
  :return:
  """
    time.sleep(0.3)
    url = f'{YOUTH_HOST}Task/receiveBereadRed'
    try:
        response = requests_session().post(url=url,
                                           headers=headers,
                                           timeout=30).json()
        print('时段红包')
        print(response)
        if response['code'] == 1:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def run():
    title = f'📚中青看点'
    content = ''
    result = ''
    beijing_datetime = get_standard_time()
    print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
    hour = beijing_datetime.hour
    for i, account in enumerate(COOKIELIST):
        headers = account['YOUTH_HEADER']
        readBody = account['YOUTH_READBODY']
        redBody = account['YOUTH_REDBODY']
        readTimeBody = account['YOUTH_READTIMEBODY']
        withdrawBody = account['YOUTH_WITHDRAWBODY']
        shareBody = account['YOUTH_SHAREBODY']
        rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'
        sign_res = sign(headers=headers)
        if sign_res and sign_res['status'] == 1:
            content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
        elif sign_res and sign_res['status'] == 2:
            send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
            continue

        sign_info = signInfo(headers=headers)
        if sign_info:
            content += f'\n【账号】：{sign_info["user"]["nickname"]}'
            content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
            result += f'【账号】: {sign_info["user"]["nickname"]}'
        friendList(headers=headers)
        if hour > 12:
            punch_card_res = punchCard(headers=headers)
            if punch_card_res:
                content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
        if hour >= 5 and hour <= 8:
            do_card_res = doCard(headers=headers)
            if do_card_res:
                content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
        luck_draw_res = luckDraw(headers=headers)
        if luck_draw_res:
            content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
        visit_reward_res = visitReward(body=readBody)
        if visit_reward_res:
            content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
        shareArticle(headers=headers, body=shareBody)
        for action in [
                'beread_extra_reward_one', 'beread_extra_reward_two',
                'beread_extra_reward_three'
        ]:
            time.sleep(5)
            threeShare(headers=headers, action=action)
        open_box_res = openBox(headers=headers)
        if open_box_res:
            content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
        watch_ad_video_res = watchAdVideo(headers=headers)
        if watch_ad_video_res:
            content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
        watch_game_video_res = watchGameVideo(body=readBody)
        if watch_game_video_res:
            content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
        # article_red_res = articleRed(body=redBody)
        # if article_red_res:
        #   content += f'\n【惊喜红包】：+{article_red_res["score"]}个青豆'
        read_time_res = readTime(body=readTimeBody)
        if read_time_res:
            content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
        if (hour >= 6 and hour <= 8) or (hour >= 11
                                         and hour <= 13) or (hour >= 19
                                                             and hour <= 21):
            beread_red_res = bereadRed(headers=headers)
            if beread_red_res:
                content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
        for i in range(0, 5):
            time.sleep(5)
            rotary_res = rotary(headers=headers, body=rotaryBody)
            if rotary_res:
                if rotary_res['status'] == 0:
                    break
                elif rotary_res['status'] == 1:
                    content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
                    if rotary_res['data']['doubleNum'] != 0 and rotary_res[
                            'data']['score'] > 0:
                        double_rotary_res = doubleRotary(headers=headers,
                                                         body=rotaryBody)
                        if double_rotary_res:
                            content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

        rotaryChestReward(headers=headers, body=rotaryBody)
        for i in range(5):
            watchWelfareVideo(headers=headers)
        timePacket(headers=headers)
        for action in [
                'watch_article_reward', 'watch_video_reward',
                'read_time_two_minutes', 'read_time_sixty_minutes',
                'new_fresh_five_video_reward', 'first_share_article'
        ]:
            time.sleep(5)
            sendTwentyScore(headers=headers, action=action)
        stat_res = incomeStat(headers=headers)
        if stat_res['status'] == 0:
            for group in stat_res['history'][0]['group']:
                content += f'\n【{group["name"]}】：+{group["money"]}青豆'
            today_score = int(stat_res["user"]["today_score"])
            score = int(stat_res["user"]["score"])
            total_score = int(stat_res["user"]["total_score"])

            if score >= 300000 and withdrawBody:
                with_draw_res = withdraw(body=withdrawBody)
                if with_draw_res:
                    result += f'\n【自动提现】：发起提现30元成功'
                    content += f'\n【自动提现】：发起提现30元成功'
                    send(title=title,
                         content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

            result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
            content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
            result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
            content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
            result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
            content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

    print(content)

    # 每天 23:00 发送消息推送
    if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 5:
        send(title=title, content=result)
    elif not beijing_datetime.hour == 23:
        print('未进行消息推送，原因：没到对应的推送时间点\n')
    else:
        print('未在规定的时间范围内\n')


if __name__ == '__main__':
    run()
