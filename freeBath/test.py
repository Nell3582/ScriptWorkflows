import json

import requests

# save data to json file


def store(data):
    with open('data.json', 'w') as fw:
        # 将字典转化为字符串
        # json_str = json.dumps(data)
        # fw.write(json_str)
        # 上面两句等同于下面这句
        json.dump(data, fw)
# load json data from file


def load():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    data = load()
    for k, v in data.items():
        tel = k
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        title = v.split('@')[0]
        str = v.split('@')[1]
        data = { "title": title, "description": str }

        response = requests.post(f'http://47.98.173.224:5700/users/{tel}/items/', headers=headers, data=json.dumps(data))
        print(response.text)
    # json_data = '{"login":[{"username":"aa","password":"001"},{"username":"bb","password":"002"}],"register":[{"username":"cc","password":"003"},{"username":"dd","password":"004"}]}'
    # # 函数是将json格式数据转换为字典
    # data = json.loads(json_data)
    # store(data)





