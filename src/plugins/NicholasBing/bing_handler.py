from nonebot import on_command
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from . import config
from EdgeGPT import Chatbot, ConversationStyle

bing_handler = on_command(config.name, aliases={config.aliases}, priority=5, block=True)

@bing_handler.handle()
async def _(event: Event, matcher: Matcher, args: Message = CommandArg()):
    result_str = ""
    at = MessageSegment.at(event.get_user_id())
    input_arg = args.extract_plain_text().strip()
    if(input_arg == ""):
        await matcher.finish(Message(at + "\n" + "请输入想要询问的问题"))
    try:
        bot = await Chatbot.create(proxy=config.bing_proxy, cookie_path='./src/plugins/NicholasBing/cookies.json')
        res = await bot.ask(prompt=input_arg, conversation_style=ConversationStyle.balanced, wss_link="wss://sydney.bing.com/sydney/ChatHub")
        result_str = res["item"]["messages"][1]["text"]
        await bot.close()
    except Exception as e:
        result_str = str(e)
    await matcher.finish(Message(at + "\n" + result_str))