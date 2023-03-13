from nonebot import get_driver, on_command, plugin
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from . import config
from .private import jrrp
from random import randint

rp_handler = on_command(config.name, aliases={config.aliases}, priority=5, block=True)

def numToIdentity(id: int) -> str:
    result = str(hex(id))[2:].upper()
    result = (16 - len(result)) * "0" + result
    result = result[0:4] + "-" + result[4:8] + "-" + result[8:12] + "-" + result[12:16]
    return result

def getRPIdentity(target_rp: int) -> str:
    numIdentity = randint(0, 16 ** 16 - 1)
    change = 1 if numIdentity < 16 ** 16 / 2 else -1 
    Identity = numToIdentity(numIdentity)
    rp = jrrp(Identity)
    while rp != target_rp:
        numIdentity += change
        Identity = numToIdentity(numIdentity)
        rp = jrrp(Identity)
    return Identity

@rp_handler.handle()
async def _(event: Event, matcher: Matcher, args: Message = CommandArg()):
    at = MessageSegment.at(event.get_user_id())
    arg = args.extract_plain_text()
    subcommands = list(config.subcommands.keys())
    target_rp = 0
    if(arg == ""):
        target_rp = 100
    else:
        try:
            target_rp = int(arg)
            if(target_rp < 0 or target_rp > 100):
                raise Exception
        except Exception as e:
            await matcher.finish(f"{subcommands[1]} 参数错误!")
    identity = getRPIdentity(target_rp)
    await matcher.finish(Message(at + "获得了识别码：" + identity))