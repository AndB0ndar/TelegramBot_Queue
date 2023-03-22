from telebot import TeleBot
from telebot import types
import re
from random import randint
from db import QueueHandler


bot = TeleBot('5516733632:AAEMeOASkrHYkRTtbeFtqDeD_2UPQjNH8y4')


def button_greed(title):
    """
     function that creates buttons
    Options:
        title (str): queue title
    Return value:
        (telebot.types): markup of buttons
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    msg_quit = "Выйти из очереди " + title
    markup.add(types.KeyboardButton(msg_quit))
    msg_add = "Встать в очередь " + title
    markup.add(types.KeyboardButton(msg_add))
    msg_info = "Информация об очереди " + title
    markup.add(types.KeyboardButton(msg_info))
    return markup


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
        (bool or int): failure of create to the queue by title OR key queue
    """
    q = QueueHandler()
    queue_id = q.create_queue(title)
    return queue_id


def connect_by_name(title, user_id):
    """
    A function connecting to queue by title
    Options:
        title (str): queue title
        user_id(int): user identifier
    Return value:
        (bool): success/failure of connecting to the queue by title
    """
    q = QueueHandler()
    return q.connect_by_name(title, user_id)


def connect_by_id(key, user_id):
    """
    A function connecting to queue by title
    Options:
        key (int): key for connect to queue
        user_id(int): user identifier
    Return value:
        (bool): success/failure of connecting to the queue by title
    """
    q = QueueHandler()
    return q.connect_by_id(key, user_id)


def disconnect_by_id(queue_id, user_id):
    """
    Disconnect from queue function
    Options:
        queue_id (int): queue identifier
        user_id (int): user identifier
    Return value:
        (bool): success/failure of disconnect from queue
    """
    q = QueueHandler()
    return q.disconnect_by_id(queue_id, user_id)


def disconnect_by_name(queue_title, user_id):
    """
    Disconnect from queue function
    Options:
        queue_title (int): queue identifier
        user_id (int): user identifier
    Return value:
        (bool): success/failure of disconnect from queue
    """
    q = QueueHandler()
    return q.disconnect_by_name(queue_title, user_id)


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


def info_by_name(q_title, user_id):
    """
    A function giving information about the queue
    Options:
        q_name (str): queue name
        user_id (int): user identifier
    Return value:
        (str): queue information
    """
    q = QueueHandler()
    return q.info_by_name(q_title, user_id)


def info_by_id(q_id, user_id):
    """
    A function giving information about the queue
    Options:
        q_id (str): queue identifier
        user_id (int): user identifier
    Return value:
        (str): queue information
    """
    q = QueueHandler()
    return q.info_by_id(q_id, user_id)

def notification_by_name(q_name):
    q = QueueHandler()
    return q.get_first_two_by_name(q_name)


@bot.message_handler(commands=['start'])
def decorate_info(message):
    """the decorator issuing the starting information"""
    answer = "👋 Привет! Я твой бот-очередь!\n"
    answer += "Я помогу тебе и твоим друзьям организованно выстроиться в очередь\n"
    answer += "\nВведите:\n"
    answer += "/create <название очереди> - чтобы создать очередь\n"
    answer += "/connect <название очереди> - чтобы вступить в очередь\n"
    # answer += "/connect_by_key <ключ очереди> - чтобы вступить в очередь\n"
    # answer += "\n/disconnect - чтобы отключиться от очередь"
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['create'])
def decorate_create(message):
    """the decorator called when a command is given to create the queue"""
    command = re.split(r' ', message.text, 1)
    title = command[1] if len(command) == 2 else generating_title()
    res = create(title)
    if res is False:
        answer = "Имя занято"
    else:
        answer = "Ключ вашей очереди: " + str(res)
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['connect', 'connect_by_key'])
def decorate_connect(message):
    """decorator called when a command is given to connection the queue"""
    command = re.split(r' ', message.text, 1)
    if len(command) == 2:
        title = command[1]
        fl = connect_by_name(command[1], message.from_user.id) if command[0] == "/connect" \
            else connect_by_id(command[1], message.from_user.id)
        if fl:
            answer = "Вы подключились к группе: " + title
        else:
            answer = "Что-то пошло не так, попробуйте повторить позже"
        bot.send_message(message.from_user.id, answer, reply_markup=button_greed(title))
    else:
        answer = "Вы не ввели "
        answer += "имя" if command[0] == "/connect" else "ключ"
        answer += " очереди"
        bot.send_message(message.from_user.id, answer)


# @bot.message_handler(commands=['disconnect'])
# def decorate_disconnect(message):
#     """the decorator called when a command is given to disconnect from the queue"""
#     fl = disconnect()
#     if fl:
#         answer = "Вы отключились от очереди"
#     else:
#         answer = "Что-то пошло не так, попробуйте повторить позже"
#     bot.send_message(message.from_user.id, answer, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def decorate_main(message):
    """the main decorator implementing the main interface"""
    title = None
    if len(re.split(r"^Выйти из очереди ", message.text)) > 1:
        title = re.split(r'^Выйти из очереди ', message.text)[1]
        if re.findall(r"id", message.text):
            fl = disconnect_by_id(re.split(r'id', message.text)[1], message.from_user.id)
        else:
            fl = disconnect_by_name(re.split(r'^Выйти из очереди ', message.text)[1], message.from_user.id)
        if fl:
            answer = "Вы вышли из очереди"
            lst = notification_by_name(re.split(r'^Выйти из очереди ', message.text)[1])[0]
            if lst:
                for user in lst:
                    bot.send_message(user, "ваша очередь")
        else:
            answer = "Что-то пошло не так, попробуйте повторить позже"
    elif len(re.split(r"^Встать в очередь ", message.text)) > 1:
        title = re.split(r'^Встать в очередь ', message.text)[1]
        if re.findall(r"id", message.text):
            fl = connect_by_id(re.split(r'id', message.text)[1], message.from_user.id)
        else:
            fl = connect_by_name(re.split(r'^Встать в очередь ', message.text)[1], message.from_user.id)
        if type(fl) is int:
            answer = "Место " + str(fl)
        else:
            answer = "Что-то пошло не так, попробуйте повторить позже"
    elif len(re.split(r"^Информация об очереди ", message.text)) > 1:
        title = re.split(r'^Информация об очереди ', message.text)[1]
        if re.findall(r"id", message.text):
            fl = info_by_id(re.split(r'id', message.text)[1], message.from_user.id)
        else:
            fl = info_by_name(re.split(r'^Информация об очереди ', message.text)[1], message.from_user.id)
        if type(fl) is int:
            answer = "Место " + str(fl)
        else:
            answer = "Вы не в очереди"
    else:
        bot.reply_to(message, "Я не занаю такой команды!")
        answer = "Попробуй ещё раз"
    if title is None:
        bot.send_message(message.from_user.id, answer)
    else:
        bot.send_message(message.from_user.id, answer, reply_markup=button_greed(title))


if __name__ == "__main__":
    print("bot started")
    bot.polling(none_stop=True, interval=0)
# bot.infinity_polling()
