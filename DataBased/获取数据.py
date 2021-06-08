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
str_json = json.dumps(dic) 
# print(str_json) 
with open('./jsonDataBased.txt','w') as f:
    f.write( json.dumps( dic,ensure_ascii=False,indent=2 ) )

text = f'''
const jsName = "校园无忧洗";
const $ = new Env(jsName);
const url = $request.url;
var body = $request.body;
const path1 = "upload/data";
let KEY = "f3ff0fa4-f022-4be0-90fa-de0d0f9a903a";

let iterable = '{str_json}';

let IDdatabase = new Map([
  ["A", "3058649832"],
  ["B", "2642831696"],
]);

let telphone = $.getdata("qzxyTel");
let nCount = $.getdata("nCount");
$.log(`${{$.name}} nCount 的值为: ${{nCount}}`);
let uCount = addNum(nCount);
$.log(`${{$.name}} uCount 的值为: ${{uCount}}`);

if (typeof telphone !== "undefined") {{
  $.log(`${{$.name}} 服务器账户查询中,账户ID为: ${{telphone}}`);
  if (iterable.match(telphone)) {{
    let today_time = FormatDate();
    let utime = getJson(telphone).split('@');
    let userType = utime[0];
    var deadline = utime[1];
    var myID = getID(userType);
    var iDays = DateDiff(today_time, deadline);
    $.log(
      `${{$.name}} 账户ID: ${{telphone}}\n截至使用日期:${{deadline}}\n剩余使用时间:${{iDays}}天`
    );
    if (today_time <= deadline) {{
      reWrite();
      notify();
    }}
  }} else {{
    $.log(
      `${{$.name}} 未授权用户，您的账号不具有使用权限，请联系QQ:${{myID}}解锁使用权`
    );
    $.msg(
      $.name,
      `未授权用户,您的账号无使用权限`,
      `请联系QQ:${{myID}}解锁使用权`
    );
  }}
}} else {{
  $.log(`${{$.name}} 数据未获取，请先打开getData获取账户用水数据`);
  $.msg($.name, `账户用水数据未获取`, `请先打开 getData 脚本获取账户用水数据`);
}}

function getJson(key) {{
  let jsonObj = json.parse(iterable);
  for (var item in jsonObj) {{
    if (item == key) {{
      var jValue = jsonObj[item];
      return jValue;
    }}
  }}
}}
function addNum(num) {{
  if (typeof num !== "undefined") {{
    num = num + 1;
  }} else {{
    var num = 1;
  }}
  if (num) $.setdata(num, "nCount");
  return num;
}}

function getID(item) {{
  if (IDdatabase.has(item)) {{
    myID = IDdatabase.get(item);
  }} else {{
    myID = "3058649832";
  }}
  return myID;
}}

function notify() {{
  if (iDays < 3) {{
    $.log(
      `${{$.name}} 您的有效使用时长仅剩${{iDays}}天,为不影响继续使用,请联系申请解锁`
    );
    $.msg(
      $.name,
      `您的有效使用时长仅剩${{iDays}}天`,
      `如需继续使用：请联系QQ:${{myID}} 申请解锁`
    );
  }}
  if (uCount == 2) {{
    $.msg(
      $.name,
      `您的账户ID: ${{telphone}}`,
      `截至使用日期:${{deadline}},剩余使用时间:${{iDays}}天`
    );
  }}
}}

function FormatDate() {{
  var now = new Date();
  var year = now.getFullYear();
  var month = now.getMonth();
  var date = now.getDate();
  month = month + 1;
  if (month < 10) {{
    month = "0" + month;
  }}
  if (date < 10) {{
    date = "0" + date;
  }}
  var time = year + "-" + month + "-" + date;
  return time;
}}

function DateDiff(D1, D2) {{
  var dateStart = new Date(D1);
  var dateEnd = new Date(D2);
  var difValue = Math.abs(dateEnd - dateStart) / (1000 * 60 * 60 * 24);
  return difValue;
}}

function reWrite() {{
  if (url.indexOf(path1) != -1) {{
    if (body.match(telphone)) {{
      $.log(`${{$.name}} 账户二次校验成功,解密算法加载中`);
      let s = body.match(/xfData=\d{{1,14}}/)[0];
      $.log(`${{$.name}} 数据S计算成功:${{s.length}}`);
      let sys = body.match(/phoneSystem=(\w+)/)[1];
      let x = $.getdata("qzxyxfData");
      if (sys == "ios") {{
        $.log(`${{$.name}} 当前的软件环境是:${{sys}}`);
        let m = $.getdata("qzxymoney");
        $.log(`${{$.name}} 数据M计算成功:${{m.length}}`);
        const nData = s + x.slice(21);
        $.log(
          `${{$.name}} 新数据生成: 成功,当前保存的持久化数据: ${{nData.length}} = 91`
        );
        body = body.replace(/xfData=(\w+)/, nData);
        $.log(`${{$.name}} body1数据解密成功`);
        body = body.replace(/upMoney=\d+/, m);
        $.log(`${{$.name}} body2数据解密成功`);
      }} else {{
        $.log(`${{$.name}} 当前的软件环境是:${{sys}}`);
        $.log(`${{$.name}} body1数据解密成功`);
        body = body.replace(/xfData=(\w+)/, x);
        $.log(`${{$.name}} body2数据解密成功`);
      }}
      $.done({{ body }});
    }} else {{
      $.log(
        `${{$.name}} 数据解密失败,原因是本地账户与实际使用账户不符,请打开 getData 脚本重新获取数据`
      );
      $.msg(
        $.name,
        `数据解密失败,原因是本地账户与实际使用账户不符`,
        `请打开 getData 脚本重新获取数据`
      );
    }}
  }}
}}

function BotNotify(text, desp) {{
  return new Promise((resolve) => {{
    var dataString = `{{ "msgtype": "text", "text": {{ "content": "${{text}}\\n\\n${{desp}}"}}}}`;
    const options = {{
      url: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${{KEY}}`,
      body: dataString,
      headers: {{
        "Content-Type": "application/json",
      }},
    }};
    if (KEY) {{
      $.post(options, (err, resp, data) => {{
        try {{
          if (err) {{
            console.log("发送数据清理指令失败！！\n");
            console.log(err);
          }} else {{
            data = JSON.parse(data);
            if (data.errcode === 0) {{
              console.log("发送数据清理指令完成。\n");
            }} else {{
              console.log(`${{data.errmsg}}\n`);
            }}
          }}
        }} catch (e) {{
          $.logErr(e, resp);
        }} finally {{
          resolve(data);
        }}
      }});
    }} else {{
      console.log("取消数据清理\n");
      resolve();
    }}
  }});
}}
'''
print(text)
pyperclip.copy(text)





