from nonebot import get_driver, on_command, plugin
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from . import config

help_handler = on_command(config.name, aliases={config.aliases}, priority=5, block=True)
default_start = list(get_driver().config.command_start)[0]

@help_handler.handle()
async def _(event: Event, matcher: Matcher, args: Message = CommandArg()):
    arg = args.extract_plain_text()
    at = MessageSegment.at(event.get_user_id())
    result = ''
    subcommands = list(config.subcommands.keys())
    if(arg == ""):
        result = get_plugin_help('help')
    elif(arg == subcommands[1]):
        result = get_all_plugin_help()
    else:
        result = get_plugin_help(arg)
    await matcher.finish(Message(at + "\n" + result))

def get_plugin_help(arg:str) -> str:
    result_plugin = None
    plugin_set = plugin.get_loaded_plugins()
    for temp_plugin in plugin_set:
        if temp_plugin.metadata and temp_plugin.metadata.name == arg:
            result_plugin = temp_plugin
            break
    if not result_plugin:
        result = f'{arg} 指令不存在，请确认输入了正确的指令'
    else:
        if result_plugin.metadata and result_plugin.metadata.name and result_plugin.metadata.usage:
            result = f'指令 {result_plugin.metadata.name}({result_plugin.metadata.extra.get("aliases",result_plugin.metadata.name)}) 的帮助页面:\n{result_plugin.metadata.extra.get("full_description", "")}\n\n{result_plugin.metadata.usage}'
        else:
            result = f'{arg} 无指令帮助，请自己瞎试'
    return result

def get_all_plugin_help() -> str:
    plugin_list = plugin.get_loaded_plugins()
    plugin_helps = []
    for p in plugin_list:
        if(p.metadata and p.metadata.name and p.metadata.description):
            plugin_helps.append(default_start + p.metadata.name + ' ' + p.metadata.description)
    return '\n'.join(plugin_helps)