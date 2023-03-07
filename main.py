from telebot import TeleBot
from telebot import types


bot = TeleBot('5516733632:AAEMeOASkrHYkRTtbeFtqDeD_2UPQjNH8y4')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
msg_quit = "Выйти из очереди"
markup.add(types.KeyboardButton(msg_quit))
msg_add = "Встать в очередь"
markup.add(types.KeyboardButton(msg_add))
msg_info = "Информация об очереди"
markup.add(types.KeyboardButton(msg_info))

def create_queue():
    pass

def connect():
    return True, "ГРУППА"

def disconnect():
    return True

def quit():
    return True

def add():
    return True

def info():
    return "INFO"

@bot.message_handler(commands=['start'])
def decorate_info(message):
    answer = "👋 Привет! Я твой бот-очередь!\n"
    answer += "Я помогу тебе и твоим друзьям организованно выстроиться в очередь\n"
    answer += "\nВведите:\n"
    answer += "\create <название очереди> - чтобы создать очередь\n"
    answer += "\connect <название очереди> - чтобы вступить в очередь\n"
    answer += "\n\disconnect - чтобы отключиться от очередь"
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['create'])
def decorate_create(message):
    answer = "Ключ вашей очереди: " + str(create_queue())
    bot.send_message(message.from_user.id, answer, reply_markup=markup)


@bot.message_handler(commands=['connect'])
def decorate_connect(message):
    fl, title = connect()
    if fl:
        answer = "Вы подключились к группе: " + title
    else:
        answer = "Что-то пошло не так, попробуйте повторить позже"
    bot.send_message(message.from_user.id, answer, reply_markup=markup)


@bot.message_handler(commands=['disconnect'])
def decorate_disconnect(message):
    fl = disconnect()
    if fl:
        answer = "Вы отключились от очереди"
    else:
        answer = "Что-то пошло не так, попробуйте повторить позже"
    bot.send_message(message.from_user.id, answer, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def decorate_main(message):
    if message.text == msg_quit:
        fl = quit()
        if fl:
            answer = "Вы вышли из очереди"
        else:
            answer = "Что-то пошло не так, попробуйте повторить позже"
    elif message.text == msg_add:
        fl = add()
        if fl:
            answer = "Вы добавлены в очередь"
        else:
            answer = "Что-то пошло не так, попробуйте повторить позже"
    elif message.text == msg_info:
        answer = info()
    else:
        bot.reply_to(message, "Я не занаю такой команды!")
        answer = "Попробуй ещё раз"
    bot.send_message(message.from_user.id, answer, reply_markup=markup)


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
# bot.infinity_polling()
