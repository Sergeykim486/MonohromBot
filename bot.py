import telebot
from telebot import types
import json
from datetime import datetime, date, time
bot = telebot.TeleBot('5750687344:AAEVWNtI3WGoalFjtuSqWXX1SxxWNmvhNnw')
# Глобальные переменные
uid = 0
ufname = ''
ulname = ''
uphone = ''
ustat = ''
finded = 0
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
a = telebot.types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])

# ====================  С Т А Р Т   Б О Т А  ====================
def send_welcome(message):
    global uid, ufname, ulname, uphone, ustat, finded
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Начать работу')
    bot.send_message(message.chat.id, 'Добро пожаловать в систему.', reply_markup=markup)
    bot.register_next_step_handler(message, start_working)
def start_working(message):
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Начать работу')
    if message.text == 'Начать работу' or message.text == 'Главное меню':
        global uid, ufname, ulname, uphone, ustat
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        usr = open('Users.txt', 'r')
        usrt = usr.read()
        usrj = json.loads(usrt)
        finded = 0
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
                    markup.row('Написать всем участникам')
                    bot.send_message(message.chat.id, 'Выберите действие...', reply_markup=markup)
                    bot.register_next_step_handler(message, main_menu_manager)
                elif ustat == 'Master':
                    markup.row('Список заявок', 'Написать всем участникам')
                    bot.send_message(message.chat.id, 'Выберите действие...', reply_markup=markup)
                    bot.register_next_step_handler(message, main_menu_master)
        if finded == 0:
            markup.row('Зарегистрироваться')
            bot.send_message(message.chat.id, f'Приветствую!\nВы не авторизованы.\nПожалуйста зарегистрируйтесь.', reply_markup=markup)
            bot.register_next_step_handler(message, reg1)
        usr.close()
    else:
        bot.send_message(message.chat.id, 'Команда не распознана!', reply_markup=markup)
        bot.register_next_step_handler(message, start_working)
# ===============================================================

@bot.message_handler(content_types=['text'])

# ==================== ГЛАВНОЕ МЕНЮ ПОЛЬЗОВАТЕЛЯ ====================
def main_menu_manager(Message):
    if Message.text == 'Список заявок':
        now = datetime.now()
        tasksfile = str(now.month) + str(now.year) + '.txt'
        # bot.send_message(Message.chat.id, tasksfile)
        file = open(tasksfile, 'r')
        tasklist = json.loads(file.read())
        for tasks in tasklist['response']['tasks']:
            tnum = tasks['task_id']
            tdate = tasks['task_add_date']
            ttime = tasks['task_add_time']
            tfrom = tasks['task_from']
            tmaster = tasks['master_name']
            tmanagerc = tasks['manager_name_c']
            tstatus = tasks['task_status']
            if tstatus == 1:
                taskmes = '🔵' + str(tdate) + ' ' + str(ttime) + ' - ' + str(tfrom)
            elif tstatus == 2:
                taskmes = '🟡' + str(tdate) + ' ' + str(ttime) + ' - ' + str(tfrom) + ' (' + str(tmaster) + ')'
            elif tstatus == 3:
                taskmes = '🟢' + str(tdate) + ' ' + str(ttime) + ' - ' + str(tfrom) + ' (' + str(tmaster) + ')'
            elif tstatus == 4:
                taskmes = '🔴' + str(tdate) + ' ' + str(ttime) + ' - ' + str(tfrom) + ' (' + str(tmanagerc) + ')'
            bot.send_message(Message.chat.id, taskmes)
        bot.register_next_step_handler(Message, main_menu_manager)
    elif Message.text == 'Написать всем участникам':
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Отмена')
        bot.send_message(Message.chat.id, 'Что вы хотите написать?', reply_markup=markup)
        bot.register_next_step_handler(Message, chat)
    else:
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Список заявок', 'Добавить заявку')
        markup.row('Написать всем участникам')
        bot.send_message(Message.chat.id, 'команда не опознана.', reply_markup=markup)
        bot.register_next_step_handler(Message, main_menu_manager)
def main_menu_master(Message):
    if Message.text == 'Список заявок':
        now = datetime.now()
        tasksfile = str(now.month) + str(now.year) + '.txt'
        # bot.send_message(Message.chat.id, tasksfile)
        file = open(tasksfile, 'r')
        tasklist = json.loads(file.read())
        for tasks in tasklist['response']['tasks']:
            tnum = tasks['task_id']
            tdate = tasks['task_add_date']
            ttime = tasks['task_add_time']
            tfrom = tasks['task_from']
            tmaster = tasks['master_name']
            tmanagerc = tasks['manager_name_c']
            tstatus = tasks['task_status']
            if tstatus == 1:
                taskmes = '🔵' + str(tdate) + ' ' + str(ttime) + ' - ' + str(tfrom)
            elif tstatus == 2:
                taskmes = '🟡' + str(tdate) + ' ' + str(ttime) + ' - ' + str(tfrom) + ' (' + str(tmaster) + ')'
            elif tstatus == 3:
                taskmes = '🟢' + str(tdate) + ' ' + str(ttime) + ' - ' + str(tfrom) + ' (' + str(tmaster) + ')'
            elif tstatus == 4:
                taskmes = '🔴' + str(tdate) + ' ' + str(ttime) + ' - ' + str(tfrom) + ' (' + str(tmanagerc) + ')'
            bot.send_message(Message.chat.id, taskmes)
        bot.register_next_step_handler(Message, main_menu_master)
    elif Message.text == 'Написать всем участникам':
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Отмена')
        bot.send_message(Message.chat.id, 'Что вы хотите написать?', reply_markup=markup)
        bot.register_next_step_handler(Message, chat)
    else:
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Список заявок', 'Написать всем участникам')
        bot.send_message(Message.chat.id, 'команда не опознана.', reply_markup=markup)
        bot.register_next_step_handler(Message, main_menu_master)
# ===================================================================

# ==================== отправка сообщения всем ====================
def chat(message):
    if message.text != 'Отмена':
        sfname = ''
        slname = ''
        usr = open('Users.txt', 'r')
        usrt = usr.read()
        usrj = json.loads(usrt)
        for users in usrj['response']['users']:
            if int(message.chat.id) == int(users['user_id']):
                sfname = users['user_f_name']
                slname = users['user_l_name']
        for users in usrj['response']['users']:
            if int(message.chat.id) != int(users['user_id']):
                bot.send_message(users['user_id'], f"‼️ сообщение ‼️ \n от {slname} {sfname} ‼️\n\n{message.text}")
        usr.close()
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Главное меню')
        bot.send_message(message.chat.id, 'Ваше сообщение отправлено', reply_markup=markup)
        bot.register_next_step_handler(message, start_working)
    else:
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Главное меню')
        bot.send_message(message.chat.id, 'Возврат в главное меню.', reply_markup=markup)
        bot.register_next_step_handler(message, start_working)
# =================================================================

# ==================== РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ ====================
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
            json_data = {
                'user_id': uid,
                'user_f_name': ufname,
                'user_l_name': ulname,
                'user_phone_num': uphone,
                'user_status': ustat
                }
            usrj['response']['users'].append(json_data)
            for users in usrj['response']['users']:
                bot.send_message(message.chat.id, users['user_f_name'])
                bot.send_message(message.chat.id, users['user_l_name'])
            usr.close()
            nusr = open('Users.txt', 'w')
            nusr.write(json.dumps(usrj, indent=2))
            nusr.close()
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
# =========================================================================
            
bot.polling(none_stop=True, interval=0)