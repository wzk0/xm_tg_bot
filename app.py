import telebot
from xm_api import search,get_link
import tok
import random

API_TOKEN=tok.token
bot=telebot.TeleBot(API_TOKEN,parse_mode='MARKDOWN')

@bot.message_handler(commands=['help','start'])
def send_welcome(message):
    bot.reply_to(message,'输入歌名或歌手可查找歌曲以获取ID, 输入ID则返回下载链接')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text.isdigit():
        try:
            data=get_link(message.text)
        except:
            bot.reply_to(message,'暂无结果!')
        result=[]
        for d in data:
            result.append('[%s](%s)\n'%(d['quality'],d['url']))
        bot.reply_to(message,'\n'.join(result))
    else:
        try:
            data=search(message.text)
        except:
            bot.reply_to(message,'暂无结果!')
        result=[]
        for d in data['data']:
            result.append('%s. %s\n└─ ID: `%s`\n└─ 标签: %s\n└─ 上传时间: *%s*\n└─ 热度: *%s*\n'%(data['data'].index(d)+1,d['name'],d['song_id'],', '.join(d['tags']),d['upload_time'],d['hot']))
        bot.reply_to(message,'👻已找到%s条结果!\n\n'%data['length']+'\n'.join(result))

bot.infinity_polling()