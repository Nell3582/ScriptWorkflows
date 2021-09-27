import requests
import json


# 获取所有用户信息
def getAllData():

    headers = {
        'accept': 'application/json',
    }

    res = requests.get(
        'http://47.98.173.224:5700/items/?skip=0&limit=1000', headers=headers)
    data = res.json()
    # print(data)
    return data


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

# tel = '15207163636'
# dic = isHasUser(tel)
# if dic:
#     deadline = dic['description']
#     if getDiff(deadline)

# a = isHasUser('15207163637')

# if a:
#     print("111")
# else:
#     print('b')


def addUser(tel, dlr, deadline):
    dic = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    dlId = dic[dlr]
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {"title": tel, "description": deadline}

    res = requests.post(
        f'http://47.98.173.224:5700/users/{dlId}/items/', headers=headers, data=json.dumps(data))
    data = res.json()
    # if data["owner_id"] == tel:
    #     QYWXNotify('新增授权提醒', f'用户{tel}添加成功')
    print(data)
    return data


def getUser(id):
    url = "https://gitee.com/Nell3582/Nell9382/raw/master/Task/zqkd/JsonData.json"  # 等价下面的
    res = requests.get(url).json()
    if (id in res):
        # type = res[id].split('@')[0]
        deadline = res[id].split('@')[1]
    else:
        deadline = '2021-01-01'
    return deadline


def main():
    url = "https://gitee.com/Nell3582/Nell9382/raw/master/Task/zqkd/JsonData.json"  # 等价下面的
    res = requests.get(url).json()
    for k, v in res.items():
        dlr = v.split('@')[0]
        deadline = v.split('@')[1]
        tel = k
        a = isHasUser(tel)
        if not a:
            addUser(tel, dlr, deadline)


if __name__ == '__main__':
    main()
