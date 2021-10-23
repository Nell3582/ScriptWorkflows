
import time
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

img = on_command('赞赏', priority=1)

group = {'833258227':"1",'783384299':'2',"519036865":'3',"87629913":'4',"908326662":'5'}

@img.handle()
async def _(bot: Bot, event: Event):
    img_path = f'/root/Alice/src/img/zanshang1.jpg'
    msg = f'\n本消息将在60秒后自动撤回,请尽快保存处理哦'
    rely = [
        {
            "type": "image",
            "data": {
                "file": f'file://{img_path}'
            }
        },
        {
            "type": "text",
            "data": {
                "text": msg
            }
        }, ]
    session_id = event.get_session_id().split('_')[2]
    print(session_id)
    if event.group_id == 907442227:
        result = await img.send(message=rely)
        # await img.finish(message=rely)
        message_id = result['message_id']
        time.sleep(60)
        await bot.delete_msg(message_id=message_id)
    else:
        print(event.group_id)
