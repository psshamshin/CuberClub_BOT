import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

bot = telebot.TeleBot("")  # Замените на свой токен!
DB_URL = ''

user_dict = {}

class User:
    def __init__(self, tgid):
        self.tgid = tgid
        self.fio_name = ''
        self.fac = ''

@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    #print(user_id_tg)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('✏️ | Заполнить заявку', '📗 | О нас')
    msg = bot.send_message(message.chat.id, 'Привет!👋🏾 Выбери нужный тебе пункт меню! ⬇️⬇️⬇️', reply_markup=markup)
    #print(msg.chat.username)
    bot.register_next_step_handler(msg, markup_handler)

def markup_handler(message):
  if message.text == '✏️ | Заполнить заявку':
    msg = bot.send_message(message.chat.id, 'Как тебя зовут?©️')
    bot.register_next_step_handler(msg, fio_handler)
  elif message.text == '📗 | О нас':
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('⬅️ | Вернуться')
    bot.register_next_step_handler(message, send_welcome)
    msg = bot.send_message(message.chat.id,
    'Привет! 🤟🏿 Я первый киберспортивный 🤖бот-помощник,\n'
          'который проведет тебя в мир игр! 👾\n'
          'С моей помощью ты сможешь найти новых друзей,🤝\n'
          'научить или научиться чему-то новому!\n'
          'Преодолеть все границы и стать настоящим победителем! 🏆\n\n'

          'С уважением, команда ODIN⚡️', reply_markup=markup)

def handle_return(message):
  send_welcome(message)
  bot.register_next_step_handler(message, markup_handler)

def fio_handler(message):
  user_info = {
        'tg_id': message.from_user.id, 
        'username' : message.chat.username,
        'fio' : message.text
  }
  msg = bot.send_message(message.chat.id, 'На каком факультете ты обучаешься?💎')
  bot.register_next_step_handler(msg, faculty_handler, user_info)

def faculty_handler(message, user_info):
  user_info['faculty'] = message.text
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
  markup.add('CS2','Dota 2', 'LoL', 'Valorant')
  msg = bot.send_message(message.chat.id, 'В какой дисциплине ты хочешь принимать участие?⚖️',reply_markup=markup)
  bot.register_next_step_handler(msg, disciplines_handler, user_info)

def disciplines_handler(message, user_info):
  user_info['disc'] = message.text
  msg = bot.send_message(message.chat.id, 'Кратко расскажи о своих достижениях 📝')
  bot.register_next_step_handler(msg, achievements_handler, user_info)

def achievements_handler(message, user_info):
  user_info['achi'] = message.text
  print(user_info)
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add('⬅️ | Вернуться')
  bot.send_message(message.chat.id, 'Спасибо! Твой запрос обработан и скоро будет рассмотрен!🔔',reply_markup=markup)
  bot.register_next_step_handler(message,send_welcome)
  save_to_database(user_info)

def save_to_database(user_info):
  if not firebase_admin._apps:
    cred = credentials.Certificate('admin.json')
    firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})
    
  # Запись данных о пользователе в Realtime Database
  write_user_data(user_info)

# Функция для записи данных о пользователе в Realtime Database
def write_user_data(user_info):
  ref = db.reference('Telegram/' + str(user_info['tg_id']))
  ref.set({
    '6 - достижения': user_info['achi'],
    '5 - дисциплины': user_info['disc'],
    '4 - факультет': user_info['faculty'],
    '3 - ФИО': user_info['fio'],
    '2 - Nickname': "@" + user_info['username'],
    '1 - TelegramID': user_info['tg_id']
  })
  #716578611
  #428571723
  send_notific(999999999, user_info)

def send_notific(ADMIN_ID, user_info):
  text = 'Пользователь ['+user_info['fio']+'](https://t.me/'+user_info['username']+') оставил\(а\) заявку:\nфакультет: '+user_info['faculty']+'\nдисциплины: '+user_info['disc']+'\nдостижения: '+user_info['achi']
  bot.send_message(ADMIN_ID, text, parse_mode='MarkdownV2')

bot.polling()