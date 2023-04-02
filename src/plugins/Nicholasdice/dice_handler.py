from typing import Tuple
from nonebot import get_driver, on_command, plugin
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from . import config
from . import dice
dice_handler = on_command(config.name, aliases={config.aliases}, priority=5, block=True)

@dice_handler.handle()
async def _(event: Event, matcher: Matcher, args: Message = CommandArg()):
    result_str = ""
    at = MessageSegment.at(event.get_user_id())
    try:
        input_arg = args.extract_plain_text().strip()
        if(input_arg == ""):
            input_arg = "d"
        result = dice.eval_dice_exp(input_arg)
        result_str = input_arg + "=" + str(result[1]) + "=" + str(result[0])
    except Exception as e:
        result_str = str(e)
    await matcher.finish(Message(at + "\n" + result_str))
