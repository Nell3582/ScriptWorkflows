from nonebot import on_notice
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Message, GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent
 
welcome = on_notice()
#朋友加群
@welcome.handle()
async def _(bot: Bot, event:GroupIncreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    at_ = "[CQ:at,qq={}]".format(user)
    msg = at_ + '欢迎您的加入！我是机器人晚星，您可以直接在群聊/私聊我来查询自己的授权时长信息，只需对我说 查询+手机号 (示例：查询 12345678901) 即可哦'
    msg = Message(msg)
    await welcome.finish(message=msg)
 
#群友退群
@welcome.handle()
async def _(bot: Bot, event:GroupDecreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    at_ = "[CQ:at,qq={}]".format(user)
    msg = at_ + '\n' + '一位朋友离我们而去！'
    msg = Message(msg)
    await welcome.finish(message=msg)