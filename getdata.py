
import re
import requests
import json
import time


text = '''
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-cn
Connection: keep-alive
Cookie: __jd_ref_cls=JDReact_StartReactModule; mba_muid=16283920902081640557473; mba_sid=1628392090210216317151411118.5; __jda=122270672.16283920902081640557473.1628392090.1628392090.1628392090.1; __jdb=122270672.5.16283920902081640557473|1.1628392090; __jdc=122270672; TrackerID=sfpLkUCR_AojTTSzJkPyYAcMBTp1Pupfexx1bxBuSUirFMJgAYPAu040cXbVhefUjZn7m2e9Ysu6xRkuklkoP9LNBlUhhg8yhdIMW4zYWLYMSBl1C3Vxn5H8z4kJlHIyNiJXbpDDxJZqPPX32r_2yA; pt_key=AAJhD0yOADCLmTTvy_2BUmNXPlYLorsD-GUYvZumttIvvgsEm4n1_If3GWuqsZF7jMgJ3cFzGUg; pt_pin=jd_7c7de935d2d9f; pt_token=78uf8h01; pwdt_id=jd_7c7de935d2d9f; sfstoken=tk01m1b871d4da8sMysxKzIrMngxPXNZzxwuyvdWjzcsTlaAyhPE7qBKp6HlBII7XbG5iy+4XqM6b39mdgy50SPGMHYE; whwswswws=; shshshfpa=c3613392-0f6b-bf3a-0b23-306ff0dde43d-1628392127; shshshfpb=buPTCMuUWd28Tzipb y3Ssw==; jcap_dvzw_fp=G-8F4hRg5yvKkSLJ01Sr09vVMtIcJulW0eFso2bW0tITx-J1SAkE5Xkj4KzQUfhohhZBZA==; 3AB9D23F7A4B3C9B=JST7XPSVC4J2TWYLJX6R3AXLGDOCOUTXQCTG6RBAS6BQ4VCSLKUW5A3N3LRBCF5K2NPFZAZJ7ZNWUAJNSXUKB535EY; shshshfp=210210ff37577e822bfb8b8bd5c7c1e3; shshshsID=7eb48d72feb0ec609f9d4b31e91d046a_2_1628392572980; __jdv=122270672|direct|-|none|-|1628392090209; mobilev=html5
Host: api.m.jd.com
Referer: https://h5.m.jd.com/rn/2E9A2bEeqQqBP9juVgPJvQQq6fJ/index.html
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1
'''
ck = re.findall('pt_key=.+pt_pin=\w+',text)[0]
print(ck)
