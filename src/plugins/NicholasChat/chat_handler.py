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

    # 重置人格
    def reset_preset(self):
        self.preset = config.gpt3_preset

    # 设置人格
    def set_preset(self, msg: str) -> str:
        self.preset = msg.strip()
        self.reset()
        return self.preset

    # 导入用户会话
    def load_user_session(self, msg) -> str:
        import ast
        config = ast.literal_eval(msg)
        self.set_preset(config[0]['content'])
        self.conversation = config[1:]

        return f'导入会话: {len(self.conversation)}条\n' \
               f'导入人格: {self.preset}'

    # 导出用户会话
    def dump_user_session(self):
        return str([{"role": "system", "content": self.preset}] + self.conversation)

    # 会话
    async def get_chat_response(self, reset: bool, msg) -> str:
        if config.gpt3_key == '':
            return f'无API Keys，请在配置文件中配置'

        def check_and_reset() -> bool:
            # 超过一天重置
            from datetime import datetime
            last = datetime.fromtimestamp(self.last_timestamp)
            now = datetime.fromtimestamp(time.time())
            delta = now - last
            if delta.days > 0:
                self.chat_count = 0
                self.reset()
            return False
        
        check_and_reset()

        import tiktoken
        try:
            # 长度超过设置时，清空会话
            encoding = tiktoken.encoding_for_model(config.gpt3_model)
            if self.total_tokens + len(encoding.encode(msg)) > config.gpt3_max_tokens or reset:
                self.reset()
        except Exception:
            self.reset()
            return f'无法获取模型编码，可能网络出错或模型不存在'

        res, ok = await get_chat_response(self.preset,
                                          self.conversation,
                                          msg)
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
async def _(matcher: Matcher, event: Event, arg: Message = CommandArg()):
    session_id = event.get_session_id()
    msg = arg.extract_plain_text().strip()
    if not msg:
        return

    if session_id in user_lock and user_lock[session_id]:
        await matcher.finish("消息太快啦～请稍后", at_sender=True)

    user_lock[session_id] = True
    resp = await get_user_session(session_id).get_chat_response(True, msg)

    # 发送消息
    at = MessageSegment.at(event.get_user_id())
    await matcher.send(Message(at + resp))
    user_lock[session_id] = False
