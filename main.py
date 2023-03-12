from telebot import TeleBot
from telebot import types
import re
from random import randint


bot = TeleBot('5516733632:AAEMeOASkrHYkRTtbeFtqDeD_2UPQjNH8y4')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
msg_quit = "Выйти из очереди"
markup.add(types.KeyboardButton(msg_quit))
msg_add = "Встать в очередь"
markup.add(types.KeyboardButton(msg_add))
msg_info = "Информация об очереди"
markup.add(types.KeyboardButton(msg_info))


def generating_title():
    """
    A function to generate the name of the queue if it has not been entered by the user
    Options:
        None
    Return value:
        (str): generated name
    """
    return "queue_" + str(randint(10 ** 5, 10 ** 10))


def create(title):
    """
    Queue creation function
    Options:
        title (str): queue title
    Return value:
        None
    """
    pass


def connect(title):
    """
    A function connecting to queue by title
    Options:
        title (str): queue title
    Return value:
        (bool): success/failure of connecting to the queue by title
    """
    return True


def connect_by_key(key):
    """
    A function connecting to queue by key
    Options:
        key (str): queue key
    Return value:
        (bool): success/failure of connecting to the queue by key
        (str): title queue
    """
    return True, "ГРУППА"


def disconnect():
    """
    Disconnect from queue function
    Options:
    Return value:
        (bool): success/failure of disconnect from queue
    """
    return True


def quite():
    """
    Dequeue function
    Options:
    Return value:
        (bool): success/failure of dequeuing
    """
    return True


def add():
    """
    Add to queue function
    Options:
    Return value:
        (bool): success/failure of adding to the queue
    """
    return True


def info():
    """
    A function giving information about the queue
    Options:
        None
    Return value:
        (str): queue information
    """
    return "INFO"


@bot.message_handler(commands=['start'])
def decorate_info(message):
    """the decorator issuing the starting information"""
    answer = "👋 Привет! Я твой бот-очередь!\n"
    answer += "Я помогу тебе и твоим друзьям организованно выстроиться в очередь\n"
    answer += "\nВведите:\n"
    answer += "/create <название очереди> - чтобы создать очередь\n"
    answer += "/connect <название очереди> - чтобы вступить в очередь\n"
    answer += "/connect_by_key <ключ очереди> - чтобы вступить в очередь\n"
    answer += "\n/disconnect - чтобы отключиться от очередь"
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['create'])
def decorate_create(message):
    """the decorator called when a command is given to create the queue"""
    command = re.split(r' ', message.text, 1)
    title = command[1] if len(command) == 2 else generating_title()
    answer = "Ключ вашей очереди: " + str(create(title))
    bot.send_message(message.from_user.id, answer, reply_markup=markup)


@bot.message_handler(commands=['connect', 'connect_by_key'])
def decorate_connect(message):
    """decorator called when a command is given to connection the queue"""
    command = re.split(r' ', message.text, 1)
    if len(command) == 2:
        fl, title = connect(command[1]), command[1] if command[0] == "/connect" else connect_by_key(command[1])
        if fl:
            answer = "Вы подключились к группе: " + title
        else:
            answer = "Что-то пошло не так, попробуйте повторить позже"
        bot.send_message(message.from_user.id, answer, reply_markup=markup)
    else:
        answer = "Вы не ввели "
        answer += "имя" if command[0] == "/connect" else "ключ"
        answer += " очереди"
        bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['disconnect'])
def decorate_disconnect(message):
    """the decorator called when a command is given to disconnect from the queue"""
    fl = disconnect()
    if fl:
        answer = "Вы отключились от очереди"
    else:
        answer = "Что-то пошло не так, попробуйте повторить позже"
    bot.send_message(message.from_user.id, answer, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def decorate_main(message):
    """the main decorator implementing the main interface"""
    if message.text == msg_quit:
        fl = quite()
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


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
# bot.infinity_polling()
