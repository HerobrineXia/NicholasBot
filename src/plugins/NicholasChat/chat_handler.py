from . import config
from .openai import get_chat_response
from nonebot import get_driver, on_command, plugin
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from typing import Dict
import time

class Session:
    chat_count: int = 1
    last_timestamp: int = 0

    def __init__(self, _id):
        self.session_id = _id
        self.preset = config.gpt3_preset
        self.temperature = config.gpt3_temperature
        self.conversation = []
        self.reset()
        self.token_record = []
        self.total_tokens = 0

    # 重置会话
    def reset(self):
        self.conversation = []
        self.token_record = []
        self.total_tokens = 0
        self.chat_count = 1

    # 设置随机值
    def set_temperature(self, value: float):
        self.temperature = value
    
    # 重置人格
    def reset_preset(self):
        self.preset = config.gpt3_preset

    # 设置人格
    def set_preset(self, msg: str) -> str:
        self.preset = msg.strip()
        self.reset()
        return self.preset

    # 会话
    async def get_chat_response(self, reset: bool, msg) -> str:
        if config.gpt3_key == '':
            return f'无API Keys，请在配置文件中配置'

        def date_reset():
            # 超过一天重置
            from datetime import datetime
            last = datetime.fromtimestamp(self.last_timestamp)
            now = datetime.fromtimestamp(time.time())
            delta = now - last
            if delta.days > 0:
                self.reset()
        
        date_reset()

        import tiktoken
        require_token = 0
        try:
            # 长度超过设置时，清空会话
            encoding = tiktoken.encoding_for_model(config.gpt3_model)
            input_token = len(encoding.encode(self.preset + msg))
            if input_token + self.total_tokens > config.gpt3_max_tokens or reset:
                self.reset()
            require_token = config.gpt3_max_tokens - input_token - self.total_tokens
        except Exception as e:
            self.reset()
            return f'无法获取模型编码，可能网络出错或模型不存在'

        res, ok = await get_chat_response(self.preset,
                                          self.conversation,
                                          msg, require_token, self.temperature)
        if ok:
            self.chat_count += 1
            self.last_timestamp = int(time.time())
            # 输入token数
            self.token_record.append(res['usage']['prompt_tokens'] - self.total_tokens)
            # 回答token数
            self.token_record.append(res['usage']['completion_tokens'])
            # 总token数
            self.total_tokens = res['usage']['total_tokens']
            return self.conversation[-1]['content']
        else:
            # 出现错误自动重置
            self.reset()
            return res

user_session: Dict[str, Session] = {}
user_lock = {}

def get_user_session(user_id) -> Session:
    if user_id not in user_session:
        user_session[user_id] = Session(user_id)
    return user_session[user_id]

chat_handler = on_command(config.name, aliases={config.aliases}, priority=5, block=True)

@chat_handler.handle()
async def _(matcher: Matcher, event: Event, args: Message = CommandArg()):
    session_id = event.get_session_id()
    arg = args.extract_plain_text().strip()
    at = MessageSegment.at(event.get_user_id())
    msg = ""
    subcommands = [cmd.split(" ")[0] for cmd in config.subcommands.keys()]
    reset = True
    if(arg.startswith(subcommands[0])):
        arg = arg[arg.find(subcommands[0]) + len(subcommands[0]):].strip()
        if(arg == ""):
            await matcher.finish(Message(at + "你的GPT预设是：" + get_user_session(session_id).preset))
        else:
            get_user_session(session_id).set_preset(arg)
            await matcher.finish(Message(at + "已设置GPT预设：" + arg))
    elif(arg.startswith(subcommands[1])):
        msg = arg[arg.find(subcommands[1]) + len(subcommands[1]):].strip()
        reset = False
    elif(arg.startswith(subcommands[2])):
        get_user_session(session_id).set_preset(config.gpt3_preset)
        await matcher.finish(Message(at + "已恢复初始GPT预设：" + config.gpt3_preset))
    elif(arg.startswith(subcommands[3])):
        arg = arg[arg.find(subcommands[3]) + len(subcommands[3]):].strip()
        try:
            num = float(arg)
        except Exception:
            num = -1
        if(num < 0 or num > 1):
            await matcher.finish(Message(at + "请输入0-1中的有效的数字"))
        get_user_session(session_id).set_temperature(num)
        await matcher.finish(Message(at + "已设置GPT随机度：" + str(num)))
    else:
        msg = arg
    if not msg:
        return
    if session_id in user_lock and user_lock[session_id]:
        await matcher.finish(Message(at + "消息太快啦～请稍后"))

    user_lock[session_id] = True
    resp = await get_user_session(session_id).get_chat_response(reset, msg)

    # 发送消息
    user_lock[session_id] = False
    await matcher.finish(Message(at + resp))
