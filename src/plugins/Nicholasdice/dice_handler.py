from nonebot import get_driver, on_command, plugin
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from . import config

dice_handler = on_command(config.name, aliases={config.aliases}, priority=5, block=True)

@dice_handler.handle()
async def _(matcher: Matcher):
    await matcher.send("没写完！")