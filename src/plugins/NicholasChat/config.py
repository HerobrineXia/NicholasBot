# 配置文件
name = "帮帮忙"
descritpion = "询问ChatGPT"
full_description = \
"""
向ChatGPT询问问题
"""
aliases = ("bbm")
subcommands = {
    "<消息>" : "发送指定消息"
}

# ChatGPT设置
gpt3_preset = "以下是与AI助手的对话。助理乐于助人、富有创意、聪明而且非常友好。"
gpt3_max_tokens = 1000
gpt3_model = "gpt-3.5-turbo"
gpt3_proxy = "http://127.0.0.1:7890"

# 私有配置
from . import private
gpt3_key = private.key