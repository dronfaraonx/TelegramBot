import telebot
import logging

logging.basicConfig(filename='bot-debug.log', level=logging.DEBUG)

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bot = telebot.TeleBot("1722410502:AAEnCdc8z1VWd-RF9-k127GDAN6cZZoShlw")

stateStorage = {}



def gen_markup():
	markup = InlineKeyboardMarkup()
	markup.row_width = 2
	markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
			   InlineKeyboardButton("No", callback_data="cb_no"))
	return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	print(call)
	if call.data == "cb_yes":
		bot.send_message(call.from_user.id, "Красучик! Чисто сработано!")
		bot.answer_callback_query(call.id, "Answer is Yes")
	elif call.data == "cb_no":
		bot.answer_callback_query(call.id, "Answer is No")
		bot.send_message(call.from_user.id, "фу! Пора идти!")


@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('static/AnimatedSticker.tgs', 'rb')
	bot.send_sticker(message.chat.id, sti)
	bot.send_message(message.chat.id, message.from_user.first_name + " , ты помылся?", reply_markup=gen_markup())



	stateStorage[message.from_user.id] = 'Answer question about shower'
	# print(message)
	bot.register_next_step_handler(message, answer_shower_message)

# @bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == 'Answer question about shower', content_types=['text'])
@bot.message_handler(content_types=['text'])
def answer_shower_message(message):
	print(message.text)
	if message.text.lower() == "да" or message.text.lower() == "конечно":
		bot.reply_to(message, "Красучик! Чисто сработано!")

	elif message.text.lower() == "нет":
		bot.reply_to(message, "фу! Пора идти!")
	bot.reply_to(message, "Как дела?")
	# stateStorage[message.from_user.id] = 'Answer how u doing'
	bot.register_next_step_handler(message, test_message)


# @bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == 'Answer how u doing',
# 					 content_types=['text'])
@bot.message_handler(content_types=['text'])
def test_message(message):
	print(message.text)
	if message.text.lower() == "хорошо":
		bot.reply_to(message, "Отлично! У меня тоже дела ок")

	elif message.text.lower() == "плохо":
		bot.reply_to(message, "Че ты разнылся")

	stateStorage[message.from_user.id] = ''

def get_current_state(user_id):
	try:
		return stateStorage[user_id]
	except Exception:
		return ''

while True:
	try:
		bot.polling(none_stop=True, interval=0, timeout=20)
	except Exception as e:
		logging.debug('Error: ' + e)
