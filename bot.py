# -*- coding: utf-8 -*-

# AIOGRAM
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, reply_keyboard
from aiogram.utils import executor
import aiogram.utils
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# DB models
from models import db_session
from models.users import User

db_session.global_init('database.db')

bot_token = '1956084820:AAG2RArJWL1_ukR2JtQyRCwE7qbzVXwraDQ' # @VitaxiBot

bot = Bot(token=bot_token)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class States(Helper):
    mode = HelperMode.snake_case

    STATE_0 = ListItem()

# считаем для статистики
users = 0 # юзеры

# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	global users
	#
	iduser = message.from_user.id
	session = db_session.create_session()
	#
	user_all = session.query(User).all()
	T = True
	for all in user_all:
		if all.id == iduser:
			T = False

	if T == True:
		# добавить нового юзера
		session = db_session.create_session()
		name = message.from_user.first_name
		url = message.from_user.username
		iduser = message.from_user.id
		user = User(
			id=iduser,
			name=name,
			ref='',
			refs='',
			test='',
			score=0
		)
		users += 1
		session.add(user)
		session.commit()
		# Клавиатура
		yes_bt = KeyboardButton('Участвую')
		main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
		main_kb.add(yes_bt)
		await bot.send_message(message.chat.id, '''Уважаемые коллеги, если хотите участвовать в конкурсе,
то нажмите на кнопку "Участвую", а затем напишите боту ваш позывной и агрегатор, в котором вы работаете.

<code>*Если вы не помните свой позывной, то вы можете позвонить к нам в тех.поддержку 8 495 256 11 44 или написать к нам на WhatsApp  8 999 555 55 35 и мы вам его подскажем.</code>

<b>Правила:</b>



1) Вы должны быть подписаны на наш Telegram-канал (https://t.me/joinchat/z2BBGkQLuLYyNjAy) 
3) Приглашенный водитель должен выполнить НЕ МЕНЕЕ 10 ПОЕЗДОК в любом агрегаторе через наш парк (можно по несколько поездок в разных агрегаторах)


<b>Как пригласить водителя?</b>

1) Зайдите на <a href="https://vi.taxi/">сайт</a> или <a href="https://play.google.com/store/apps/details?id=taxi.sss.app&hl=ru&gl=US">приложение</a> по выводу средств в свой личный кабинет
2) Нажмите на кнопку "Пригласить"
3) Впишите имя водителя и номер телефона, с которого он будет работать

❗️ВАЖНО❗️

Пишите именно тот номер, с которого будет работать водитель, иначе он за вами не закрепится!
''', parse_mode="HTML")
		await bot.send_message(message.chat.id, 'Для участия подпишитесь на <a href="https://t.me/joinchat/z2BBGkQLuLYyNjAy">канал</a>', reply_markup=main_kb, parse_mode="HTML")
	else:
		# юзер есть
		test = ''
		session = db_session.create_session()
		user_all = session.query(User).all()
		for user in user_all:
			if user.id == message.from_user.id:
				test = user.test

		session.commit()
		if test:
			keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
			helpe = types.KeyboardButton(text='🆘 Тех.поддержка')
			keyboard.add(helpe)
			await bot.send_message(message.chat.id, '🙋Здравствуйте!', reply_markup=keyboard)
		else:
			yes_bt = KeyboardButton('Участвую')
			main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
			main_kb.add(yes_bt)
			await bot.send_message(message.chat.id, 'Вы не подписались на <a href="https://t.me/joinchat/z2BBGkQLuLYyNjAy">канал</a>!', reply_markup=main_kb, parse_mode="HTML")

@dp.message_handler(content_types=["text"])
async def check(message: types.Message):
	try:
		if message.text == 'Участвую':
			ch = await bot.get_chat_member(chat_id='@Vitaxi_news', user_id=message.from_user.id)
			if ch.status != 'left':
				test = ''
				session = db_session.create_session()
				user_all = session.query(User).all()
				for user in user_all:
					if user.id == message.from_user.id:
						user.test = '+'

				session.commit()
				keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
				helpe = types.KeyboardButton(text='🆘 Тех.поддержка')
				keyboard.add(helpe)
				await bot.send_message(message.chat.id, '🙋Отлично, вы подписаны на канал!', reply_markup=keyboard)
				await bot.send_message(message.chat.id, '''1) Зайдите на <a href="https://vi.taxi/">сайт</a> или <a href="https://play.google.com/store/apps/details?id=taxi.sss.app&hl=ru&gl=US">приложение</a> по выводу средств в свой личный кабинет
2) Нажмите на кнопку "Пригласить"
3) Впишите имя водителя и номер телефона, с которого он будет работать''', parse_mode="HTML")
			else:
				yes_bt = KeyboardButton('Участвую')
				main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
				main_kb.add(yes_bt)
				await bot.send_message(message.chat.id, 'Вы не подписались на <a href="https://t.me/joinchat/z2BBGkQLuLYyNjAy">канал</a>!', reply_markup=main_kb, parse_mode="HTML")
		elif message.text == "🆘 Тех.поддержка":
			keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
			back = types.KeyboardButton(text='◀️ Назад')
			keyboard.add(back)
			await bot.send_message(message.chat.id, 'Следующее ваше сообщение будет отправлено админам!', reply_markup=keyboard)
			state = dp.current_state(user=message.from_user.id)
			await state.set_state(States.all()[0])
		elif message.text == "◀️ Назад":
			keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
			helpe = types.KeyboardButton(text='🆘 Тех.поддержка')
			keyboard.add(helpe)
			await bot.send_message(message.chat.id, '📚 Главное меню', reply_markup=keyboard)
		else:
			keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
			helpe = types.KeyboardButton(text='🆘 Тех.поддержка')
			keyboard.add(helpe)
			await bot.send_message(message.chat.id, '🤕 Я не понял вас, используйте клавиатуру!', reply_markup=keyboard)
	except BaseException as e:
		await bot.send_message(1218845111, 'В системе ошибка...\n<code>' + str(e) + '</code>', parse_mode='html')
		await bot.send_message(message.chat.id, 'Упс, ошибка...')

@dp.message_handler(state=States.STATE_0)
async def state_case_met1(message: types.Message):
	await bot.send_message(665623884, 'Вам сообщение от @' + message.from_user.username + ':\n\n' + message.text)
	await bot.send_message(message.chat.id, 'Отправлено, ожидайте ответа!')

	state = dp.current_state(user=message.from_user.id)
	await state.reset_state()
#
if __name__ == "__main__":
	executor.start_polling(dp)
