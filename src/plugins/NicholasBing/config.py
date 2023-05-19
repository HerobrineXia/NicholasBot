# 配置文件
name = "bing"
descritpion = "询问Bing"
full_description = \
"""
向Bing询问问题
"""
aliases = ("bing")
subcommands = {
    "<消息>" : "发送指定消息",
}

# Bing设置
bing_proxy = "http://127.0.0.1:7890"