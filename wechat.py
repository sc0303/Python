# Write on 2017/10/12 by Chuan.Sun
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot()
print(bot.friends().search('Alance'))
my_friend = bot.friends().search('文件传输助手')[0]
# 发送文本给好友
my_friend.send('Hello WeChat!')

