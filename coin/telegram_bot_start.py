import telegram

bot = telegram.Bot(token= '1772750536:AAFHXUrrcXi15DnUyJ99ZEb5WwqOaZIOE6A')

for i in bot.getUpdates():
    print(i)
    print()

bot.send_message('hello')
