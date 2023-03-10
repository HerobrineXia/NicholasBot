from nonebot import plugin
from nonebot import get_driver
from . import config

default_start = list(get_driver().config.command_start)[0]

__plugin_meta__ = plugin.PluginMetadata(
    name=config.name,
    description=config.descritpion,
    usage= "\n".join(map(lambda var: f'{default_start}{config.name}{"" if var[0].startswith("-") else " "}{var[0]} #{var[1]}', config.subcommands.items())),
    extra={
        "aliases": config.aliases,
        "full_description": config.full_description.strip()
    }
)

from .dice_handler import dice_handler
