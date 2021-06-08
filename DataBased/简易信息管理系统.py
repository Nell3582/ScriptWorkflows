# -*- coding:utf-8 -*-
# 账号管理系统v3.0
import os
import json;
import pyperclip;
#定义账号类
class Student:
    #类似java的构造器
    def __init__(self,id,name,age):
        self.id = id
        self.name = name
        self.age = age

    #相当于java的toString()方法
    def __str__(self):
        #msg = "{'id':" + "'"+self.id +"'"+ ",'name':" + "'" +self.name + "'" + ",'age':" + "'" + self.age+"'}"
        msg = "账号ID" + self.id + ",代理人类别：" + self.name + ",已授权时间：" + self.age
        return msg

    #获取id
    def getId(self):
        return self.id
    #获取name
    def getName(self):
        return self.name
    #获取age
    def getAge(self):
        return self.age
    #设置name
    def setName(self,name):
        self.name = name
    #设置age
    def setAge(self,age):
        self.age = age

# 添加账号信息
def addStu(array):
    "添加账号信息"
    id = input("请输入账号手机号：")
    for i in range(len(array)):
        stu2 = array[i]
        if id == stu2.getId():
            print(f'该手机号已存在,账号信息{stu2}')
            return
    name = input("请输入账号代理人代码：")
    age = input("请输入账号授权截至日期：")
    stu = Student(id,name,age)
    array.append(stu)  # 把单个账号添加到总列表中
    print("添加成功:",stu)

# 删除账号信息
def delStu(array):
    "删除账号信息"
    id = input("请输入要删除的账号手机号：")
    for i in range(len(array)):
        stu2 = array[i]
        if id == stu2.getId():
           del array[i]
           return 0
    return 1

# 修改账号信息
def updateStu(array):
    "修改账号信息"
    id = input("请输入要修改的账号手机号：")
    for i in range(len(array)):
        stu2 = array[i]
        if id == stu2.getId():
            name = input("请输入要修改的账号代理人代码：")
            age = input("请输入要修改的账号授权截至日期：")
            stu2.setName(name)
            stu2.setAge(age)
            print("修改成功")
            return
    print("找不到该手机号，没法修改")

# 查询账号信息
def selectStu(array):
    "查询账号信息"
    id = input("请输入要查询的账号手机号：")
    for i in range(len(array)):
        stu2 = array[i]
        if id == stu2.getId():
            print("查询到的账号信息：",stu2)
            return
    print("查询失败，查不到该账号信息")
    return
#打印账号信息
def printStuInfo(array):
    for i in range(len(array)):
        stu = array[i]
        print(stu)

print("=="*30)
print("欢迎使用账号管理系统")
print("1.添加账号信息")
print("2.删除账号信息")
print("3.修改账号信息")
print("4.查询账号信息")
print("5.退出系统")
print("6.生成Json数据")
print("=="*30)
flag = 0
array = [] #定义list用于保存账号信息
dic ={}
filename = 'write_data.txt' #文件名
if not os.path.exists(filename) : # 判断文件是否存在
    file = open(filename, 'w') # 不存在就创建文件
    file.close()
f = open(filename, "r")
content = f.readlines()
# print("文件内容：",content)
array.extend(content)
array_temp = [] # 临时变量
for i in range(len(array)): # 遍历转成账号对象
    print("第"+str(i)+"行:", array[i])
    if isinstance(array[i], str):  # 判断是否为字符串
        strArray = str(array[i]).split(",")
        id = strArray[0]
        name = strArray[1]
        age = strArray[2].replace("\n","")
        utime = name + "@"+ age
        dic[strArray[0]] = utime
        student = Student(id,name,age)#创建账号对象
        array_temp.append(student)
del array

array = array_temp
def getJsonData():
    str_json = json.dumps(dic) 
    # print(str_json) 
    with open('./jsonDataBased.txt','w') as f:
        f.write( json.dumps( dic,ensure_ascii=False,indent=2 ) )

    text = f'''

    let iterable = '{str_json}';
    
    '''
    pyperclip.copy(text)
    print('数据已发送到粘贴板,可直接进行粘贴')


while flag != 1:
    step = input("请输入你的操作：")
    step = int(step)
    if step == 1:
        addStu(array)
        #print("账号信息打印：", array)
    elif step == 2:
        num = delStu(array)
        if num == 0:
            print("删除成功")
        elif num == 1 or num == 2:
            print("删除失败")
        printStuInfo(array)
    elif step == 3:
        updateStu(array)
        printStuInfo(array)
    elif step == 4:
        selectStu(array)
    elif step == 5:
        flag = 1
        with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            for i in range(len(array)):
                if i == len(array)-1 :
                    stu =array[i]
                    f.write(stu.getId() + ","+stu.getName()+","+stu.getAge())
                else:
                    stu = array[i]
                    f.write(stu.getId() + ","+stu.getName()+","+stu.getAge() + "\n")
            f.close()
    elif step == 6:
        getJsonData()
    else:
        print("输入指令错误，请重新输入！！")
print("退出系统成功")