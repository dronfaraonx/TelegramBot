import telebot
import logging
from telebot import types
import requests
import json
from datetime import datetime
# from googletrans import Translator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


logging.basicConfig(filename='bot-debug.log', level=logging.DEBUG)

bot = telebot.TeleBot("1781090040:AAGayK-XU80ZLIvsRBKajUdygMjescgzcNQ")
url = "https://api.thecatapi.com/v1/images/search"

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('venv/static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nМеня зовут <b>{1.first_name}</b>, "
                                      "и я хочу сделать твой день лучше!".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=keyboard())

    bot.send_message(message.chat.id, "Если хочешь...\nпройти тест - нажми '/quiz'\nпосмотреть на милых животных "
                                      "- нажми '/animals'\nузнать погоду - нажми '/weather'")
    # bot.register_next_step_handler(message, commands)
"""MAIN COMMANDS """
#------------------------------------------------
@bot.message_handler(commands=['return'])
def main_menu(call):
    bot.send_message(call.from_user.id, "Если хочешь...\nпройти тест - нажми '/quiz'\nпосмотреть на милых животных "
                                      "- нажми '/animals'\nузнать погоду - нажми '/weather'")
@bot.message_handler(commands=['weather'])
def weather_command(message):
    weather(message)
@bot.message_handler(commands=['quiz'])
def quiz_command(message):
    bot.send_message(message.chat.id, "{0.first_name}, хочешь пройти тест?".format(message.from_user),
                     parse_mode='html', reply_markup=gen_quiz_markup())
@bot.message_handler(commands=['animals'])
def animals_command(message):
    bot.send_message(message.chat.id, "Киски или собачки?", parse_mode='html', reply_markup=cats_and_dogs())
#------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def commands(message):
    if message.text == "Погода":
        weather(message)
    if message.text == "Quiz":
        bot.send_message(message.chat.id, "{0.first_name}, хочешь пройти тест?".format(message.from_user),
                         parse_mode='html', reply_markup=gen_quiz_markup())
    if message.text == "Animals":
        bot.send_message(message.chat.id, "Киски или собачки?", parse_mode='html', reply_markup=cats_and_dogs())
        # catdog(message)
        # after_kiska(message)
    # else:
        # bot.send_message(message.chat.id, message.from_user.first_name + " , ты помылся?", reply_markup=gen_markup())
# @bot.enable_save_next_step_handlers(delay=2)

#weather button
@bot.message_handler(commands = ["weather"])
def weather(message):
    # if message.text == "Погода":
    bot.send_message(message.from_user.id, text="Введи город по-английски")
    bot.register_next_step_handler(message, city)


@bot.message_handler(commands = ["weather"])
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



#Quiz
@bot.message_handler(commands=['quiz'])
def quiz(message):
    # if message.text == "Quiz":
    # print("quiz")
    bot.send_message(message.chat.id, "{0.first_name}, хочешь пройти тест?".format(message.from_user),
                        parse_mode='html', reply_markup=gen_quiz_markup())

@bot.callback_query_handler(func=lambda call: True)
def catdog(call):
    if call.data == 'mem_dog':
        bot.send_message(call.from_user.id, 'Лимит собачек на сегодня исчерпан')
    elif call.data == 'mem_cat':
        after_kiska(call)
    elif call.data == "kiska_more":
        after_kiska(call)
    elif call.data == "kiska_enough":
        main_menu(call)

    elif call.data == "quiz_yes":
        bot.send_message(call.from_user.id, "Who created Python?\nA: Guido van Rossum\nB: Elon Mask\nC: Bill Gates\nD: Zuckerburg")
        # bot.register_next_step_handler(message_quiz, answer1)
    elif call.data =="quiz_no":
        main_menu(call)
# def first(bot)
#     if call.data == "cb_yes":
#         bot.send_message(call.from_user.id, "Красучик! Чисто сработано!")
#         bot.send_message(call.from_user.id, "Как дела?", reply_markup=butons())
#
#     # bot.answer_callback_query(call.id, "Answer is Yes")
#     elif call.data == "cb_no":
#         bot.send_message(call.from_user.id, "фу! Пора идти!")
#         bot.send_message(call.from_user.id, "Как дела?", reply_markup=butons())

    # elif call.data == "c_yes":
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                           reply_markup=None, text="И у меня всё хорошо")
    #     bot.send_message(call.from_user.id, "Хочешь киску?", reply_markup=mem_markup())
    # elif call.data == "b_no":
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                           reply_markup=None, text="И у меня всё плохо")
    #     bot.send_message(call.from_user.id, "Хочешь киску?", reply_markup=mem_markup())
    # elif call.data == "mem_yes":
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                           reply_markup=None, text="Держи киску:")
    #     after_kiska(call)
    # elif call.data == "mem_no":
    #     message = bot.send_message(call.from_user.id, "Хочешь погоду?")
    #     # bot.send_message(call.from_user.id, "Хочешь рассвет?")
    #     # тут еще добавил обнуление это счетчика, можешь убрать если хочешь
    #     count_cats[call.from_user.id] = 0
    #     bot.register_next_step_handler(message, test_message)
    # elif call.data == "kiska_more":
    #     after_kiska(call)

#
# @bot.message_handler(content_types=['text'])
# def answer1(message):
#     guesses[message.chat.id] = list()
#     correct_guesses(message.chat.id, message.text.upper())
#     # guesses.update(message.chat.id, message.text.upper())
#     if message.text.lower() == "a":
#         bot.send_message(message.chat.id, "CORRECT!")
#         #Сделать проверку на другие буквы
#     # elif message.text.lower() != "c" or "b" or "d":
#     #     bot.send_message(message.chat.id, "Choose A, B, C or D")
#     #     return callback_query(ess)
#     else:
#         bot.send_message(message.chat.id, "WRONG!")
#
#     bot.send_message(message.chat.id, "What year was Python created?\nA: 1989\nB: 1991\nC: 2000\nD: 2016")
#     bot.register_next_step_handler(message, question2)
#     # print(guesses)
#
# def question2(message):
#     if message.text.lower() == "b":
#         bot.send_message(message.chat.id, "CORRECT!")
#     else:
#         bot.send_message(message.chat.id, "WRONG!")
#     correct_guesses(message.chat.id, message.text.upper())
#     bot.send_message(message.chat.id, "Python is tributed to which comedy group?\nA: Lonely Island\nB: Smosh\nC: Monthy Python\nD: SNL")
#     bot.register_next_step_handler(message, question3)
#     # print(guesses)
#
# def question3(message):
#     if message.text.lower() == "c":
#         bot.send_message(message.chat.id, "CORRECT!")
#     else:
#         bot.send_message(message.chat.id, "WRONG!")
#     correct_guesses(message.chat.id, message.text.upper())
#     bot.register_next_step_handler(message, test_message)
#     bot.send_message(message.chat.id,
#                      "Is the Earth round?\nA: True\nB: False\nC: Sometimes\nD: What's the Earth?")
#     bot.register_next_step_handler(message, question4)
#     # print(guesses)
#
# def question4(message):
#     if message.text.lower() == "a":
#         bot.send_message(message.chat.id, "CORRECT!")
#     else:
#         bot.send_message(message.chat.id, "WRONG!")
#     correct_guesses(message.chat.id, message.text.upper())
#     list_of_answers = " ".join(guesses[message.chat.id])
#     x = guesses[message.chat.id]
#     y = [*questions.values()]
#     # print(guesses)
#     bot.send_message(message.chat.id, "Result:\nAnswers:\n" + str(correct_answers)
#                      + "\nGuesses:\n" + str(list_of_answers))
#     score = int(len([i for i, j in zip(x, y) if i == j])/4*100)
#     bot.send_message(message.chat.id, "Your score is " + str(score)+ "%")
#
# questions = {"Who created Python?: ": "A",
#              "What year was Python created?: ": "B",
#              "Python is tributed to which comedy group?: ": "C",
#              "Is the Earth round?: ": "A"
#              }
# correct_answers = str()
# for i in questions:
#     correct_answers = correct_answers + questions.get(i) + " "
#     # print(questions.get(i), end="")
#
# guesses = {}
# def correct_guesses(key, value):
#     if key not in guesses:
#         # guess =[value]
#         guesses[key] = list()
#     guesses[key].append(value)

# @bot.callback_query_handler(func=lambda call: True)
# def catdog(call):
#     if call.data == 'mem_dog':
#         bot.send_message(call.from_user.id, 'Лимит собачек на сегодня исчерпан')
#     elif call.data == 'mem_cat':
#         after_kiska(call)
#     elif call.data == "kiska_more":
#         after_kiska(call)
#     elif call.data == "kiska_enough":
#         main_menu(call)

#     after_kiska(call)

count_cats = {}
def after_kiska(call):
    # тут если что мы достаем из dict count_cats по call.from_user.id, но если такого ключа еще нет, то нам вернется 0,
    # потому что я вторым аргументом передаю 0(второй аргумент это default, то есть вернется такое значение, если нет такого ключа)
    count = count_cats.get(call.from_user.id, 0)
    # это когда количество 5, тогда мы не будем выводить киску для этого можно pass навернео лучше

    if count >= 5:
        bot.send_message(call.from_user.id, 'Лимит котиков на сегодня исчерпан')
    else:
        if count == 0:
            bot.send_message(call.from_user.id, "Ты можешь посмотреть только 5 котиков в день. Потребляй контент в "
                                                "разумных пределах")
        # если меньше 5 то увеличиваем на 1
        count = count + 1
        count_cats[call.from_user.id] = count
        bot.send_message(call.from_user.id, "У тебя осталось " + str(5 - count) + " котика на сегодня")
        response = requests.get(url)
        obj = json.loads(response.text)
        url_photo = obj[0]['url']
        response_photo = requests.request("GET", url_photo)
        bot.send_photo(call.from_user.id, response_photo.content, reply_markup=more())
    # bot.send_message(call.from_user.id, "Хочешь погоду?")
    # bot.send_message(call.from_user.id, "Хочешь рассвет?")



# @bot.message_handler(content_types=['text'])
# def test_message(message):
#     if message.text.lower() == "да":
#         bot.send_message(message.from_user.id,text="Введи город по-английски")
#         bot.register_next_step_handler(message, city)
#
#     elif message.text.lower() == "нет":
#         bot.reply_to(message, "Ну и ладно")
    # bot.register_next_step_handler(city)

# @bot.message_handler(content_types=['text'])
# def city(message):
#     url = "http://api.openweathermap.org/data/2.5/weather"
#     city = message
#     appid = '9ee3c7f0f13cdf0cd12c5bd180210c5d'
#     inits = 'metric'
#     try:
#         response = requests.get(url, params={'q': city, 'appid': appid, 'units': inits})
#     # print(response.text)
#         obj = json.loads(response.text)
#         main = obj['main']
#         temp = main['temp']
#         sys = obj['sys']
#         sunrise = sys['sunrise']
#         dt_object = datetime.fromtimestamp(sunrise)
#
#         bot.send_message(message.from_user.id, "Температура в " + city + ": " + str(temp) + "\nРассвет будет в {:d}:{:02d}".format(dt_object.hour, dt_object.minute) )
#     except:
#         bot.send_message(message.from_user.id, "Город не найден")
#

#Ты помылся? - buttons
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="cb_yes"),
               InlineKeyboardButton("Нет", callback_data="cb_no"))
    return markup


def more():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Хочу еще киску!😽", callback_data="kiska_more"),
               InlineKeyboardButton("Удовлетворён 🤩", callback_data="kiska_enough"))
    return markup


def mem_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Да", callback_data="mem_yes"),
               InlineKeyboardButton("Нет", callback_data="mem_no"))
    return markup

def butons():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Хорошо", callback_data="c_yes"),
               InlineKeyboardButton("Не очень", callback_data="b_no"))
    return markup

# quiz buttons
def gen_quiz_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Конечно", callback_data="quiz_yes"),
               InlineKeyboardButton("Нет", callback_data="quiz_no"))
    return markup

#Dogs or cats buttons
def cats_and_dogs():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("🐶", callback_data="mem_dog"),
               InlineKeyboardButton("😼", callback_data="mem_cat"))
    return markup

# Start buttons
def keyboard():
    markups = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Quiz")
    item2 = types.KeyboardButton("Погода")
    item3 = types.KeyboardButton("Animals")
    markups.add(item, item2, item3)
    return markups

bot.polling(none_stop=True)