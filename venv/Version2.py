import telebot
import logging
from telebot import types
import requests
import json
from datetime import datetime
from googletrans import Translator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(filename='bot-debug.log', level=logging.DEBUG)

bot = telebot.TeleBot("1781090040:AAGayK-XU80ZLIvsRBKajUdygMjescgzcNQ")
url = "https://api.thecatapi.com/v1/images/search"

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markups = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Выйти")

    markups.add(item)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "хочу знать про тебя всё!".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markups)
    bot.send_message(message.chat.id, message.from_user.first_name + " , ты помылся?", reply_markup=gen_markup())

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="cb_yes"),
               InlineKeyboardButton("Нет", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.send_message(call.from_user.id, "Красучик! Чисто сработано!")
        bot.send_message(call.from_user.id, "Как дела?", reply_markup=butons())

    # bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.send_message(call.from_user.id, "фу! Пора идти!")
        bot.send_message(call.from_user.id, "Как дела?", reply_markup=butons())

    elif call.data == "c_yes":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=None, text="И у меня всё хорошо")
        bot.send_message(call.from_user.id, "Хочешь киску?", reply_markup=mem_markup())
    elif call.data == "b_no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=None, text="И у меня всё плохо")
        bot.send_message(call.from_user.id, "Хочешь киску?", reply_markup=mem_markup())
    elif call.data == "mem_yes":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=None, text="Держи киску:")
        after_kiska(call)
    elif call.data == "mem_no":
        bot.send_message(call.from_user.id, "Хочешь погоду?")
        bot.send_message(call.from_user.id, "Хочешь рассвет?")
        # тут еще добавил обнуление это счетчика, можешь убрать если хочешь
        count_cats[call.from_user.id] = 0
    elif call.data == "kiska_more":
        after_kiska(call)

count_cats = {}
def after_kiska(call):
    # тут если что мы достаем из dict count_cats по call.from_user.id, но если такого ключа еще нет, то нам вернется 0,
    # потому что я вторым аргументом передаю 0(второй аргумент это default, то есть вернется такое значение, если нет такого ключа)
    count = count_cats.get(call.from_user.id, 0)
    # это когда количество 5, тогда мы не будем выводить киску для этого можно pass навернео лучше
    if count >= 5:
        bot.send_message(call.from_user.id, 'Лимит котиков на сегодня исчерпан')
    else:
        # если меньше 5 то увеличиваем на 1
        count = count + 1
        count_cats[call.from_user.id] = count
        bot.send_message(call.from_user.id, "У тебя осталось " + str(5 - count) + " котика на сегодня")
        response = requests.get(url)
        obj = json.loads(response.text)
        url_photo = obj[0]['url']
        response_photo = requests.request("GET", url_photo)
        bot.send_photo(call.from_user.id, response_photo.content, reply_markup=more())
    bot.send_message(call.from_user.id, "Хочешь погоду?")
    bot.send_message(call.from_user.id, "Хочешь рассвет?")



@bot.message_handler(content_types=['text'])
def test_message(message):
    if message.text.lower() == "да":
        bot.send_message(message.from_user.id,text="Введи город по-английски")
        bot.register_next_step_handler(message, city)

    elif message.text.lower() == "нет":
        bot.reply_to(message, "Ну и ладно")
# bot.register_next_step_handler(msg, callback_how)
@bot.message_handler(content_types=['text'])

def city(message):
    url = "http://api.openweathermap.org/data/2.5/weather"
    city = message
    appid = '9ee3c7f0f13cdf0cd12c5bd180210c5d'
    inits = 'metric'
    try:
        response = requests.get(url, params={'q': city, 'appid': appid, 'units': inits})
    # print(response.text)
        obj = json.loads(response.text)
        main = obj['main']
        temp = main['temp']
        sys = obj['sys']
        sunrise = sys['sunrise']
        dt_object = datetime.fromtimestamp(sunrise)

        bot.send_message(message.from_user.id, "Температура в " + city + ": " + str(temp) + "\nРассвет будет в {:d}:{:02d}".format(dt_object.hour, dt_object.minute) )
    except:
        bot.send_message(message.from_user.id, "Город не найден")


def more():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Хочу еще киску!", callback_data="kiska_more"))
    return markup

def mem_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="mem_yes"),
               InlineKeyboardButton("Нет", callback_data="mem_no"))
    return markup

def butons():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Хорошо", callback_data="c_yes"),
               InlineKeyboardButton("Не очень", callback_data="b_no"))
    return markup


bot.polling(none_stop=True)
