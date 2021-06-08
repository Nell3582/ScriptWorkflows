import os;
import json;
import pyperclip;

array = [] #定义list用于保存账号信息
filename = 'write_data.txt' #文件名
if not os.path.exists(filename) : # 判断文件是否存在
    file = open(filename, 'w') # 不存在就创建文件
    file.close()
f = open(filename, "r")
content = f.readlines()
dic ={}
# print("文件内容：",content)
array.extend(content)
array_temp = [] # 临时变量
for i in range(len(array)): # 遍历转成账号对象
    # print("第"+str(i)+"行:", array[i])
    if isinstance(array[i], str):  # 判断是否为字符串
        strArray = str(array[i]).split(",")
        id = strArray[0]
        name = strArray[1]
        age = strArray[2].replace("\n","")
        utime = name + "@"+ age
        dic[strArray[0]] = utime
del array
print(dic)
def getJsonData(dic):
    str_json = json.dumps(dic) 
    # print(str_json) 
    with open('./jsonDataBased.txt','w') as f:
        f.write( json.dumps( dic,ensure_ascii=False,indent=2 ) )

    text = f'''
    let iterable = '{str_json}';
    '''
    print(text)
    pyperclip.copy(text)

getJsonData(dic)





