from fastapi import FastAPI
from pydantic import BaseModel

import json

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    content: str
    friends: list

# save data to json file
def store(data):
    with open('data.json', 'w') as fw:
        # 将字典转化为字符串
        # json_str = json.dumps(data)
        # fw.write(json_str)
        # 上面两句等同于下面这句
        json.dump(data,fw)
# load json data from file

def load():
    with open('data.json','r') as f:
        data = json.load(f)
        return data

@app.get("/")
def index():
    return {"admin": "welcome to FastAPI"}
 
 
@app.get("/users/id={user_id}")
def read_user(user_id: str, deadline: str = None):
    data = load()
    if user_id in data:
        deadline = data[user_id].split("@")[1]
    else:
        deadline = '2021-01-01'
    return {"user_id": user_id, "deadline": deadline}
 
 
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    return {"user_name": user.name, "user_id": user_id}

# @app.post('/users/{user_id}@{content}')
# def upload_user(user_id:str,content: User):
#     data = load()
#     if user_id in data:
#         pass
#     else:
#         data[user_id] = content
#     store(data)
#     return  {"user_id": user_id, "content": content}


