# 配置文件
name = "roll"
descritpion = "丢骰子"
full_description = \
"""
丢骰子捏
骰子例子:
d: 丢默认骰子
2d20: 丢2个20面骰子
3d8+6: 丢3个8面骰子并加6
3#d20+5: 丢3次3个20面骰子加5,最后取平均值
d20min2: 丢1个20面骰子，每个骰子取3次中的最小值
d20max2: 丢1个20面骰子，每个骰子取取3次中的最大值
d20优势2劣势2: 等效丢1个20面骰子
3d20优势: 丢3个20面骰子，每个骰子取2次中的最大值
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