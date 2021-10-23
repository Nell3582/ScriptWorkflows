from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

# weather = on_command("天气", rule=to_me(), priority=5)


# @weather.handle()
# async def handle_first_receive(bot: Bot, event: Event, state: T_State):
#     args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
#     if args:
#         state["user_id"] = args  # 如果用户发送了参数则直接赋值


# @weather.got("user_id", prompt="您希望授权的账号ID为？")
# async def handle_user_id(bot: Bot, event: Event, state: T_State):
#     user_id = state["user_id"]
#     if user_id not in ["上海", "北京"]:
#         await weather.reject("你想查询的城市暂不支持，请重新输入！")
#     user_id_weather = await get_weather(user_id)
#     await weather.pause('请输入您想授权的时长')
#     await weather.finish(user_id_weather)


# async def get_weather(user_id: str):
#     return f"{user_id}的天气是..."


matcher = on_command("test",rule=to_me(), priority=5)

# 修改默认参数处理
@matcher.args_parser
async def parse(bot: Bot, event: Event, state: T_State):
    print(state["_current_key"], ":", str(event.get_message()))
    state[state["_current_key"]] = str(event.get_message())

@matcher.handle()
async def first_receive(bot: Bot, event: Event, state: T_State):
    # 获取用户原始命令，如：/test
    print(state["_prefix"]["raw_command"])
    # 处理用户输入参数，如：/test arg1 arg2
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
        # 将参数存入state以阻止后续再向用户询问参数
        state["arg1"] = arg_list[0]


@matcher.got("arg1", prompt="参数？")
async def arg_handle(bot: Bot, event: Event, state: T_State):
    # 在这里对参数进行验证
    if state["arg1"] not in ["allow", "list"]:
        await matcher.reject("参数不正确！请重新输入")
    # 发送一些信息
    await bot.send(event, "message")
    await matcher.send("message")
    await matcher.finish("message")