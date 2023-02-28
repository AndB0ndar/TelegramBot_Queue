import telebot
from telebot import types

bot = telebot.TeleBot('5516733632:AAEMeOASkrHYkRTtbeFtqDeD_2UPQjNH8y4')

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-очередь!\nЯ помогу тебе и твоим друзьям организованно выстроиться в очередь", reply_markup=markup)

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть