import telebot
from telebot import types
import json
bot = telebot.TeleBot('5750687344:AAEVWNtI3WGoalFjtuSqWXX1SxxWNmvhNnw')

uid = 0
ufname = ''
ulname = ''
uphone = ''
ustat = ''
finded = 0

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
a = telebot.types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])

def send_welcome(message):
    global uid, ufname, ulname, uphone, ustat, finded
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Начать работу.')
    bot.send_message(message.chat.id, 'Добро пожаловать в систему.', reply_markup=markup)
    bot.register_next_step_handler(message, start_working)
def start_working(message):
    global uid, ufname, ulname, uphone, ustat
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    usr = open('Users.txt', 'r')
    usrt = usr.read()
    usrj = json.loads(usrt)
    for users in usrj['response']['users']:
        if int(message.chat.id) == int(users['user_id']):
            finded = 1
            uid = users['user_id']
            ufname = users['user_f_name']
            ulname = users['user_l_name']
            uphone = users['user_phone_num']
            ustat = users['user_status']
            bot.send_message(message.chat.id, f'Приветствую {ufname}!\nВы авторизованы как {ustat}.')
            if ustat == 'Manager':
                markup.row('Список заявок', 'Добавить заявку')
                bot.send_message(message.chat.id, 'Выберите действие...', reply_markup=markup)
                bot.register_next_step_handler(message, main_menu_manager)
            elif ustat == 'Master':
                markup.row('Список заявок')
                bot.send_message(message.chat.id, 'Выберите действие...', reply_markup=markup)
                bot.register_next_step_handler(message, main_menu_master)
    if finded == 0:
        markup.row('Зарегистрироваться')
        bot.send_message(message.chat.id, f'Приветствую!\nВы не авторизованы.\nПожалуйста зарегистрируйтесь.', reply_markup=markup)
        bot.register_next_step_handler(message, reg1)
    usr.close()

@bot.message_handler(content_types=['text'])

def main_menu_manager(Message):
    bot.send_message(Message.chat.id, '🟦🟨приступим', reply_markup=a)

def main_menu_master(Message):
    bot.send_message(Message.chat.id, '🟦🟨🟩🟥приступим', reply_markup=a)

# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
def reg1(Message):
    markup = types.ReplyKeyboardRemove()
    if Message.chat.type == 'private':
        if Message.text == 'Зарегистрироваться':
            bot.send_message(Message.chat.id, 'Напишите Ваше имя.', reply_markup=a)
            bot.register_next_step_handler(Message, reg2)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('Зарегистрироваться')
            bot.send_message(Message.chat.id, f'не верный ввод', reply_markup=markup)
            bot.register_next_step_handler(Message, reg1)
def reg2(message):
    global uid, ufname, ulname, uphone, ustat
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Напишите Вашу Фамилию.', reply_markup=a)
    if message.chat.type == 'private':
        ufname = message.text
        bot.register_next_step_handler(message, reg3)
def reg3(message):
    global uid, ufname, ulname, uphone, ustat
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Напишите Ваш номер телефона.\nв формате +99897 XXX XX XX', reply_markup=a)
    if message.chat.type == 'private':
        ulname = message.text
        bot.register_next_step_handler(message, reg4)
def reg4(message):
    global uid, ufname, ulname, uphone, ustat
    markup = types.ReplyKeyboardRemove()
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Менеджер', 'Мастер')
        bot.send_message(message.chat.id, 'Выберите тип аккаунта.', reply_markup=markup)
        uphone = message.text
        bot.register_next_step_handler(message, reg5)
def reg5(message):
    global uid, ufname, ulname, uphone, ustat
    markup = types.ReplyKeyboardRemove()
    if message.chat.type == 'private':
        if message.text == 'Менеджер':
            ustat = 'Manager'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('Да', 'Нет')
            bot.send_message(message.chat.id, f'Пожалуйста подтвердите введенные данные.\n\n'
                            f'Имя: {ufname}\n'
                            f'Фамилия: {ulname}\n'
                            f'Номер телефона: {uphone}\n'
                            f'Статус: {ustat}\n\n'
                            f'Все верно?', reply_markup=markup)
            bot.register_next_step_handler(message, reg6)
        elif message.text == 'Мастер':
            ustat = 'Master'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('Да', 'Нет')
            bot.send_message(message.chat.id, f'Пожалуйста подтвердите введенные данные.\n\n'
                            f'Имя: {ufname}\n'
                            f'Фамилия: {ulname}\n'
                            f'Номер телефона: {uphone}\n'
                            f'Статус: {ustat}\n\n'
                            f'Все верно?', reply_markup=markup)
            bot.register_next_step_handler(message, reg6)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('Менеджер', 'Мастер')
            bot.send_message(message.chat.id, 'Выберите тип аккаунта.', reply_markup=markup)
            bot.register_next_step_handler(message, reg5)
def reg6(message):
    global uid, ufname, ulname, uphone, ustat
    markup = types.ReplyKeyboardRemove()
    uid = message.chat.id
    if message.chat.type == 'private':
        if message.text == 'Да':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('Главное меню')
            # Сохранение в файл нового пользователя
            usr = open('Users.txt', 'r')
            usrt = usr.read()
            usrj = json.loads(usrt)
            usrj['response']['users'] = {'user_id': uid, 'user_f_name': ufname, 'user_l_name': ulname, 'user_phone_num': uphone, 'user_status': ustat}
            # for users in usrj['response']['users']:
            #     bot.send_message(message.chat.id, type(users))
            # usr.close()
            # usr = open('Users.txt', 'w')
            # ======================================
            bot.send_message(message.chat.id, 'Данные сохранены.', reply_markup=markup)
            bot.register_next_step_handler(message, start_working)
        elif message.text == 'Нет':
            bot.send_message(message.chat.id, 'Введите данные снова.')
            bot.send_message(message.chat.id, 'Напишите Ваше имя.', reply_markup=a)
            bot.register_next_step_handler(message, reg2)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id, 'Вы не подтвердили данные.')
            markup.row('Да', 'Нет')
            bot.send_message(message.chat.id, f'Пожалуйста подтвердите введенные данные.\n\n'
                            f'Имя: {ufname}\n'
                            f'Фамилия: {ulname}\n'
                            f'Номер телефона: {uphone}\n'
                            f'Статус: {ustat}\n\n'
                            f'Все верно?', reply_markup=markup)
            bot.register_next_step_handler(message, reg6)
# ========================
            
bot.polling(none_stop=True, interval=0)