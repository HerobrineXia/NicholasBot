# 配置文件
name = "help"
descritpion = "获取指令帮助"
full_description = \
"""
获取指令帮助
"""
aliases = ("?")
subcommands = {
    "" : "获取此帮助",
    "-l" : "获取指令列表",
    "<指令>" : "获取指定指令帮助"
}