# 配置文件
name = "roll"
descritpion = "丢骰子"
full_description = \
"""
丢骰子捏
"""
aliases = ("r")
subcommands = {
    "" : "丢默认骰子",
    "<骰子>" : "丢指定骰子"
}
# 配置
default_dice = 20
max_repeat = 5
max_dice = 100
max_dice_size = 1000000
max_dice_select = 100