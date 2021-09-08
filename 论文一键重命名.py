import os
import json
import requests
import re
import html
from urllib import parse

GOOGLE_TRANSLATE_URL = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'


# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)


# 获取文件夹大小
def getFileSize(path):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        print(err)


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize, 2)

def translate(text, to_language="auto", text_language="auto"):

    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text, to_language, text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""

    return html.unescape(result[0])


def getlst():
    n = 1
    # path = input('请输入文件路径(结尾加上/)：')
    path = r'D:\数据汇交\第一标注(精选) - 副本'

    # 获取该目录下所有文件，存入列表中
    fileList = os.listdir(path)
    lst = []
    for i in fileList:

        name = "-".join(i.split("-")[2:])[:-4]
        qk = i.split('-')[1]
        # bh = i.split('-')[0]
        # tgt = translate(name, "zh-CN", "en")
        # print(tgt)
        oldname = path + os.sep + i
        # fsize = getDocSize(oldname)
        fsize = get_FileSize(oldname)
        text = f'参照本项目对电池体系中电极反应过程、SEI 膜的形成以及容量衰减机制针对开发原位表征技术，本论文通过原位技术探测了电输运、 晶体结构、表观形貌、电子结构和界面反应演化规律，揭示电极材料的储能机制、容量衰减因素的影响，各数据项于2020年5月至2021年6月期间、在武汉理工大学新材所和材料学院的仪器设备共享服务平台获得；通过SEM、ICP、XPS、ESR、UV-vis-NIR、XRD、Raman、BET、TEM和电化学性能以及理论计算等表征、测试和计算手段等多种表征手段，获得了形貌结构、元素含量和组分比表面积、首次库伦效率、比容量、电压、倍率性能和循环性能等电池材料的物化特性和电化学性能，通过原位表征手段揭示了其储能机制和内在机理，本论文包括 1 个文件，共 {fsize}M'
        print(text)
        bh = "{:0>2d}".format(n)

        # newname = path + os.sep + f'{bh}-{qk}-{tgt}.pdf'
        # print(oldname,newname)
        # os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
        # print(oldname, '======>', newname)

        # merge = f'{name}#{tgt}'
        lst.append(text)
        n += 1
    return lst


if __name__ == '__main__':
    # getlst()
    lst = getlst()
    str = '\n'
    f = open("mergedata-精选集.txt", "w")
    f.write(str.join(lst))
    f.close()
    print('all is ok')
