import mysql.connector
import telebot
from telebot import types
import os
import random
import aiogram
from config import token


import geocoder

api_key = '...' #гугл апи ключ


user_data = {} #создаем словарь, который используем при регистрации юзера /reg
                #записываем в начале ту


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="...",
    port="3306",
    database="mydatabase"
)
print(db)


cursor = db.cursor()
#cursor.execute("CREATE DATABASE mydatabase")
#cursor.execute("SHOW DATABASES")

#for x in cursor:
#  print(x)

#cursor.execute("CREATE TABLE users (first_name VARCHAR(255), second_name VARCHAR(255))")

#cursor.execute("SHOW TABLES")

#for x in cursor:
#  print(x)

#cursor.execute("ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE)")

#sql = "INSERT INTO users (first_name, second_name, user_id) VALUES (%s, %s, %s)"
#val = ("Kostya", "Dudar", 777)
#cursor.execute(sql, val)
#db.commit()

#print(cursor.rowcount, "Одна запись добавлена")

class User:
    def __init__(self, first_name):
        user_id = int
        self.first_name = first_name
        self.second_name = ""
        self.user_wlt_digit_uah=""
        #self.user_role_sorting = False #роль юзера "Сортировщик".
        #self.user_role_monitoring_location = False #роль юзера, который сообщает координаты свалки с мусором
        #self.user_role_monitoring_util_location = False

    # возвращает имя юзера
    def get_user_first_name(self):
        return self.first_name
    #возвращает фамилию юзера
    def get_user_second_name(self):
        return self.second_name
    def set_user_role_sorting_true(self):
        self.user_role_sorting = True
        print("Статус юзера изменен на Сортировку")
    #def set_user_role_monitoring_locatin_True(self):
    #    self.set_user_monitoring_locatin = True
    #    print("Статус юзера изменен на Мониторинг свалок")
    #def set_user_role_monitoring_util_location_true(self):
    #    self.user_monitoring_util_location = True
    #    print("Статус юзера изменен на Фото пункта приема")
    #def get_user_role_sorting(self):
    #    return self.user_role_sorting
    #def get_user_role_monitoring_location(self):
     #   return self.user_role_monitoring_location
    #def get_user_role_monitoring_util_location(self):
     #   return self.user_monitoring_util_location

bot = telebot.TeleBot(token)
print(bot.get_me())

#TODO написать инструкцию, мануал для команды хэлп
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Ожидайте, помощь в дороге!")

#TODO отправлять кнопку старт, чтобы сразу можно было вызвать меню.
@bot.message_handler(commands=['stop'])
def handle_stop(message):
	bot.send_message(message.from_user.id, "Чтобы вернуть меню нажмите /start", reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands=['photo'])
def send_welcome(message):
    #bot.send_message(message.from_user.id, "Какой вид фото?", reply_markup=telebot.types.ReplyKeyboardRemove())

    #keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    #photo_category_sorting = telebot.types.KeyboardButton(text="Фото сортировки")
    #photo_category_monitoring_location = telebot.types.KeyboardButton(text="Фото свалки")
    #photo_category_monitoring_util_location = telebot.types.KeyboardButton(text="Фото пункта приема")
    #keyboard.add(photo_category_sorting, photo_category_monitoring_location, photo_category_monitoring_util_location)
    #bot.send_message(message.chat.id, "Выберите категорию фото", reply_markup=keyboard)
    bot.reply_to(message, "Пришлите мне ваше фото и я прикреплю к вашей заявке.\nНе забудьте после этого отправить геолокацию командой - /geo\nПодпишите фото, сделайте комментарий перед отправкой.")

#TODO прописать, чтобы включал юзер перед отправгой гео геолокацию на своем телефоне. или же отправил ее в ручном режиме
@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение. "
                                      "\nНе забудь включить перед этим геолокацию на своем телефоне.", reply_markup=keyboard)

#welcome start
@bot.message_handler(commands=['start'])
def send_welcome(message):

    userid = int(message.from_user.id)
    usrinfo = bot.get_chat_member(userid, userid).user

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    #клавиатура
    #user_markup.row('Фото сортировки', 'Фото свалки', 'Фото пункта приема')
    user_markup.row('О конкурсе', 'О токене', 'О проекте')
    user_markup.row('/start', '/stop', '/geo')
    bot.send_message(userid, "Привет, " + usrinfo.first_name + "!\nЯ бот и буду помогать тебе.\n" +
                     'Учавствовать в конкурсе фотографий - /photo\n' + 'Чтобы получить информацию и помощь - /help\n' +
                     'Скрыть клавиатуру нажмите /stop, \nчтобы вернуть нажмите /start\n' +
                     'Отправить боту ваше местоположение, нажмите /geo\n' +
                     'Зарегистрироваться, нажмите /reg', reply_markup=user_markup)

    print(message.from_user.id)
    print(usrinfo)
    print(str(usrinfo.username))
    print(str(usrinfo.first_name))

#проверять, зарегистрирован ли пользователь уже. если да, то выдать данные о его регистрации.
#2 step registration user first name and second name Не работает.
"""@bot.message_handler(commands=['reg'])
def send_welcome(message):

    #if user_data[message.from_user.id] == message.from_user.id:
    #    bot.send_message(message.from_user.id, "Вы уже зарегистрированы.")
    #else:

    user_id = int(message.from_user.id)
    cursor.execute("SELECT first_name FROM mydatabase.users WHERE user_id = user_id;")


    #usrdt = user_data.get(message.from_user.id)
    #print("usrdt = user_data.get(message.from_user.id) = "+str(usrdt))
    #for x in user_data:
    #    print(x)

    msg = bot.send_message(message.from_user.id, "Для регистрации введите ваше имя. \nБудьте внимательны, только имя.")
    bot.register_next_step_handler(msg, process_first_step_name)

def process_first_step_name(message):

    try:
        user_id = message.from_user.id
        first_name = message.text
        user = User(first_name)#создаем юзера по имени
        user_data[user_id] = user#записываем юзера по его ID в uset_data{}
        #user_data_first_name = user_data(message.from_user.id).get(first_name)

        print(user_data[user_id])
        print('user.first_name=' + user.first_name)
        #print(str(user_data_first_name))
        print(user_data.get(user_id))
        msg = bot.send_message(message.from_user.id, "Теперь введите вашу фамилию или псевдоним")
        bot.register_next_step_handler(msg, process_second_name_step)


    except Exception as e:
        bot.reply_to(message, 'oooops')
def process_second_name_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.second_name = message.text
        #print(user_data)
        #print(user_data[user_id])
        print('user.second_name=' + user.second_name)
        print(user_data)

        sql = "INSERT INTO users (first_name, second_name, user_id) VALUES (%s, %s, %s)"
        val = (user.first_name, user.second_name, user_id)
        cursor.execute(sql, val)
        db.commit()

        print(cursor.rowcount, "Одна запись добавлена")

        bot.send_message(message.from_user.id, "Вы успешно зарегистрированы")

    except Exception as e:
        bot.reply_to(message, 'Ошибка, или вы уже зарегистрированы.')
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers()
# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
"""

@bot.message_handler(commands=['reg'])
def send_welcome(message):
    msg = bot.send_message(message.from_user.id, "Для регистрации введите ваше имя")
    bot.register_next_step_handler(msg, process_first_step_name)


def process_first_step_name(message):

    try:
        user_id = message.from_user.id
        first_name = message.text
        user = User(first_name)
        user_data[user_id] = user
        print(user_data)
        print(user_data[user_id])
        print('user.first_name=' + user.first_name)

        msg = bot.send_message(message.from_user.id, "Введите фамилию")
        bot.register_next_step_handler(msg, process_second_name_step)


    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_second_name_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.second_name = message.text
        print(user_data)
        print(user_data[user_id])
        print('user.second_name=' + user.second_name)
        msg = bot.send_message(message.from_user.id, "Вы успешно зарегистрированы")

    except Exception as e:
        bot.reply_to(message, 'oooops')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()


#TODO передавать в чат адрес по координатам места.
@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        print (place_from_coordinats([message.location.latitude, message.location.longitude]))

        userid = int(message.from_user.id)
        usrinfo = bot.get_chat_member(userid, userid).user
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # клавиатура
        # user_markup.row('Фото сортировки', 'Фото свалки', 'Фото пункта приема')
        user_markup.row('О конкурсе', 'О токене', 'О проекте')
        user_markup.row('/start', '/stop', '/geo')
        #TODO убрать везде команду локации. она должна вызываться только после определения категории фото.
        bot.send_message(userid, "Поздравляю, " + usrinfo.first_name + "!\nВы успешно отправили фото, категорию и локацию.\n", reply_markup=user_markup)

        chat_ecomaner_photos_id = -1001161418865
        coordinates_str = str(place_from_coordinats([message.location.latitude, message.location.longitude]))
        bot.send_message(chat_ecomaner_photos_id, "Координаты фото прислал: " + str(message.from_user.id) + "\n"
                                                    + coordinates_str +
                                                        "\n" + str(message.location))

#TODO сделать обратную связь. чтобы приходящие сообщения от пользователя логировались
#Текстовые команды
@bot.message_handler(content_types='text')
def handle_text(message):

    user_id = str(message.from_user.id)

    if message.text == "Фото сортировки":
        chat_ecomaner_photos_id = -1001161418865
        bot.send_message(chat_ecomaner_photos_id, "Фото сортировки прислал: " + user_id)
        start_after_photo_category(message, message.text)

    if message.text == "Фото свалки":
        chat_ecomaner_photos_id = -1001161418865
        bot.send_message(chat_ecomaner_photos_id, "Фото свалки прислал: " + user_id)
        start_after_photo_category(message, message.text)

    if message.text == "Фото пункта приема":
        chat_ecomaner_photos_id = -1001161418865
        bot.send_message(chat_ecomaner_photos_id, "Фото пункта приема прислал: " + user_id)
        start_after_photo_category(message, message.text)

    if message.text == "О конкурсе":
        bot.send_message(message.from_user.id, "Сочиняю.")
    if message.text == "О токене":
        bot.send_message(message.from_user.id, "Сочиняю.")
    if message.text == "О проекте":
        bot.send_message(message.from_user.id, "Сочиняю.")

    #get photo

#TODO
#save photo from user
@bot.message_handler(content_types=['photo'])
def photo(message):
    photo_category = "пусто"
    user_location = message.location
    print('user_location= ' + str(user_location))
    name = message.from_user.first_name
    user_id = message.from_user.id
    print ('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_message(user_id, "Сохранил! Не останавливайся на достигнутом!"+
                              "\nНе забудь после серии фото, отправить геолокацию.")
    print('Photo saved ' + 'chat_id- ' + str(user_id) + 'User first name- ' + str(message.from_user.first_name))
    which_category_foto_recived(message)#узнаем категорию
    print("photo_category" + photo_category)
    idphoto = message.photo[0].file_id
    caption_photo = str(message.caption) + '\n user_id = ' + str(user_id) + ' user_name = ' + str(name) + ' user_location = ' + str(user_location)

    chat_ecomaner_photos_id = -1001161418865
    bot.send_photo(chat_ecomaner_photos_id, idphoto, caption=caption_photo)
    description_photo = message.caption
    if description_photo != None:
        print('description_photo = ' + description_photo)

    save_photo_in_user_folder(message)

#save_photo_in_user_folder
def save_photo_in_user_folder(message):

    user_id = message.from_user.id
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    print("File is laded")
    print("Текущая деректория:", os.getcwd())
    if os.path.isdir(str(user_id)):
        os.chdir(str(user_id))
        print('Change folder= ' + str(user_id))
        print("Текущая деректория:", os.getcwd())
    else:

       print("Текущая деректория:", os.getcwd())
       os.mkdir(str(user_id))
       print('Create new folder= ' + str(user_id))
       print("Текущая деректория:", os.getcwd())
       os.chdir(str(user_id))
       #print('Change folder= ' + str(user_id))
       #print("Текущая деректория:", os.getcwd())
    rand = str(random.randint(0, 9999))
    description_photo = message.caption
    new_photos_name = str(description_photo) + " " + rand + " " + str(message.from_user.first_name) + ".jpg"

    with open(new_photos_name, 'wb') as new_file:
        new_file.write(downloaded_file)
        print('File saved ' + str(user_id))
        print("Текущая деректория:", os.getcwd())
        os.chdir('C:\\Users\\Константин\\untitled1')
        print("Текущая деректория:", os.getcwd())
        #print('Change folder= ' + str(user_id))

#определяем, какой категории отправили фото
def which_category_foto_recived(message):
    #keyboard = telebot.types.InlineKeyboardMarkup()
    #callback_data = ""
    #photo_category_sorting = telebot.types.InlineKeyboardButton(text="Фото сортировки")
    #photo_category_monitoring_location = telebot.types.InlineKeyboardButton(text="Фото свалки")
    #photo_category_monitoring_util_location = telebot.types.InlineKeyboardButton(text="Фото пункта приема")
    #keyboard.row(photo_category_sorting, photo_category_monitoring_location, photo_category_monitoring_util_location)
    #bot.send_message(message.chat.id, "Выберите категорию фото", reply_markup=keyboard)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Фото сортировки', 'Фото свалки', 'Фото пункта приема')
    bot.send_message(message.from_user.id, "Выберите категорию отправленного фото:", reply_markup=user_markup)

def start_after_photo_category(message, category):
    userid = int(message.from_user.id)
    usrinfo = bot.get_chat_member(userid, userid).user

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False) # клавиатура
    user_markup.row( '/geo')
    bot.send_message(userid, "Поздравляем, " + usrinfo.first_name + "!\nВаша фотография принята в категорию - " + str(category) +
                     "\nОсталось отправить местоположение, нажмите /geo\n"+
                     "Отправить можно только со смарфона,\nдля Telegram Desktop не работает." , reply_markup=user_markup)
#TODO дописать.
def start_after_geo_locatin_point(message, category):
    userid = int(message.from_user.id)
    usrinfo = bot.get_chat_member(userid, userid).user

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    # клавиатура
    # user_markup.row('Фото сортировки', 'Фото свалки', 'Фото пункта приема')
    #user_markup.row('О конкурсе', 'О токене', 'О проекте')
    user_markup.row( '/geo')
    bot.send_message(userid, "Поздравляем, " + usrinfo.first_name + "!\nВаша геолокация принята. ", reply_markup=user_markup)

#получаем название из координат. принимает массив с двумя данными place_from_coordinats([00.848919, 00.811503])
def place_from_coordinats(coordinats):

    g = geocoder.google(coordinats, method='reverse', key=api_key)

    print(str(g.ok))#False возвращает.

    city = str(g.city)
    print("city = " + city)
    state = str(g.state)
    print("state = " + state)
    state_long = str(g.state_long)
    country = str(g.country)
    print("country = " + country)
    country_long = str(g.country_long)
    print("country_long = " + country_long)

    housenumber = str(g.housenumber)
    print("housenumber = " + housenumber)
    postal = g.postal
    print("postal = " + postal)
    street = str(g.street)
    print("street = " + street)
    street_long = g.street_long
    print("street_long = " + str(street_long))
    latlng = g.latlng
    print("latlng = " + str(latlng))

    return country + " " + postal + " " + state + " " + city + " " + street_long + " " + housenumber


#DataBase
#bot.enable_save_next_step_handlers(delay=2)
#bot.load_next_step_handlers()
if __name__ == '__main__':
    bot.polling(none_stop=True)
