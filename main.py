import logging
from telegram import (InputMedia, InputMediaPhoto, Update,
                      ReplyKeyboardMarkup,
                      InlineKeyboardMarkup,
                      InlineKeyboardButton,
                      ChatAction
                       )
from telegram.ext import (Updater,
                          CallbackContext,
                          Filters,
                          CommandHandler,
                          MessageHandler,
                          ConversationHandler,
                          Filters,
                          CallbackQueryHandler)
from mysql import connector
import sqlite3

logging.basicConfig(level=logging.DEBUG)
 
# moviebot
updater = Updater(token="5166424476:AAEw0P90VO6BmVBhybktPQUVQjNZ_cT2P1c")


# config = {
    
#     'user': 'mirabror',
#     'password': "devmir1998@@",
#     'host':"127.0.0.1",
#     'database': "uzmoviebotdb",
#     'raise_on_warnings':True
# }
# connection = connector.connect(**config)
# cursor = connection.cursor()

connection = sqlite3.connect('uzmoviebotdb.db',  check_same_thread=False)
cursor = connection.cursor()

# banner tags
tags =  '<a href="http://uzmovi.com/tarjima-kinolar">Tarjima kinolar </a>'\
        '<a href="http://uzmovi.com/jangari">Jangari </a>'\
        '<a href="http://uzmovi.com/fantastika">Fantastika </a>'\
        '<a href="http://uzmovi.com/treyler">Treyler </a>'

#year buttons   
YEAR_BTN = ReplyKeyboardMarkup([ 
   ["2022","2021","2020","2019"],              
   ["2018","2017","2016","2015"],
   ["2014","2013","2012","2011"],
   ["2010"],
   ["⬅️ Orqaga"]            
])


#main menu 
MENU = ReplyKeyboardMarkup([
    ['🎬 Premyera'],
    ['🎥 Kinolar', '📽 Janr', '🎞 Serial'],
    ['📅 Yil', '🔊 Konsert', '⌛️ Treyler'],
    ['🔔 Bildirishnomalar', '🆘 Yordam', '📝 Biz haqimizda']
], resize_keyboard=True)

# kinolar
MOV_BTN = ReplyKeyboardMarkup([
    ['🎬 Premyera', 'Multfilm'],
    ["O'zbek kinolar", "Hind kinolar"],
    ["⬅️ Orqaga"]
], resize_keyboard=True)

# genre buttons
GENRES_BTN = ReplyKeyboardMarkup([
     
    ["Qo'rqinchli", 'Komediya', 'Jangari'],
    ['Fantastika', 'Melodramma', 'Sarguzasht'],
    ['Drama', 'Tarixiy', 'Klassika'],
    ['Hayotiy'],
    ['⬅️ Orqaga'] 
     
], resize_keyboard=True)

# notification menu
BUTTON1 = ReplyKeyboardMarkup([ 
    ['👌 Ha', '😶 Yo\'q'] ,
    ['⬅️ Orqaga']   
], resize_keyboard=True) 


CURRENT_MOVIE_LIST = []
id_owner = 640077553

def inline_button_generator(current_trailer_num: int, genre_id: int, genre: str):
    
    if current_trailer_num == 0:
        return InlineKeyboardMarkup([[
                InlineKeyboardButton(text="Keyingi", callback_data=f"{genre_id},{current_trailer_num+1},{genre}")
            ]])
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Oldingi", callback_data=f"{genre_id},{current_trailer_num-1},{genre}"),
            InlineKeyboardButton(text="Keyingi", callback_data=f"{genre_id},{current_trailer_num+1},{genre}"),
        ]
    ])

    
def start_handler(update: Update, context: CallbackContext):
    
    tuple1 =(int(update.effective_user.id), str(update.effective_user.first_name), str(update.effective_user.last_name))
    query = "INSERT INTO users(telegram_id, first_name, last_name) VALUES(%s, %s, %s )"
    
    try:
        list1 = []
        cursor.execute("SELECT * FROM users;")
        for id in cursor:
            list1.append(id[0])
        
        if (update.effective_user.id) not in list1:
            cursor.execute(query, tuple1)

        connection.commit()
    except Exception as e:
        print(e)
    update.message.reply_text("Quyidagida menyulardan birini tanlang yoki "
                              "film qidirish uchun so'rovni kiriting 👇",
                              reply_markup=MENU)
    
def say_hello(update: Update, context: CallbackContext):
    
    if update.effective_user.id == id_owner:
        cursor.execute("SELECT * FROM users")
        users_string = ""
        count = 0
        for user in cursor:
            count+=1
            users_string += f"{count}.id-{user[0]} Ismi:{user[1]} Familiya:{user[2]}\n"
        update.message.reply_text(users_string)
    else:
        update.message.reply_text(f"Salom, {update.effective_user.first_name}")
        
        


                           


def sort_year(update: Update, context: CallbackContext):
    
    update.effective_chat.send_chat_action(action = "typing")
    update.message.reply_text("Kerakli yilni tanlang:👇", reply_markup=YEAR_BTN)
 

def get_genres(update:Update, context:CallbackContext):
    
    # update.effective_chat.send_chat_action(action = "typing")
    if update.message.text == '📽 Janr':
        update.message.reply_text('Iltimos kerakli janrni tanlang', reply_markup=GENRES_BTN)
    else:
        if update.message.text == "🎥 Kinolar":
            update.message.reply_text('Iltimos kerakli ruknni tanlang', reply_markup=MOV_BTN)


def movie_handler(update: Update, context: CallbackContext):
     
    update.effective_chat.send_chat_action(action="upload_photo") 
    if  update.message.text == "🎞 Serial":
        cursor.execute("SELECT * FROM movies WHERE category_id = 6  ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "🔊 Konsert":
        cursor.execute("SELECT * FROM movies WHERE category_id = 4   ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "🎬 Premyera":
        cursor.execute("SELECT * FROM movies WHERE category_id = 3  ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "⌛️ Treyler":
        cursor.execute("SELECT * FROM movies WHERE category_id = 5  ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "Jangari":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 1  ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "Drama":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 2 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "Komediya":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 3 ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "Melodramma":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 4  ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "Sarguzasht":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 5 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "Qo'rqinchli":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 6 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "Tarixiy": 
        cursor.execute("SELECT * FROM movies WHERE genre_id = 7  ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "Klassika":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 8 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "Fantastika":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 9  ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "Hayotiy":
        cursor.execute("SELECT * FROM movies WHERE genre_id = 10 ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "Hind kinolar":
        cursor.execute("SELECT * FROM movies WHERE category_id = 9  ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "O'zbek kinolar":
        cursor.execute("""SELECT * FROM movies WHERE category_id = 7 ORDER BY id DESC LIMIT 1;""")
    elif update.message.text == "Multfilm":
        cursor.execute("SELECT * FROM movies WHERE category_id = 8 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "2010":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2010 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "2011":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2011 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "2012":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2012 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "2013":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2013 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "2014":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2014  ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "2015":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2015 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "2016":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2016 ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "2017":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2017 ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "2018":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2018 ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "2019":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2019 ORDER BY id DESC LIMIT 1;")
    elif update.message.text == "2020":
        cursor.execute("""SELECT * FROM movies WHERE released_year = 2020 ORDER BY id DESC LIMIT 1;""")
    elif update.message.text == "2021":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2021 ORDER BY id DESC  LIMIT 1;")
    elif update.message.text == "2022":
        cursor.execute("SELECT * FROM movies WHERE released_year = 2022  ORDER BY id DESC LIMIT 1;")
    else:
        pass
     
    for row in cursor:
        data = row 
    # update.effective_chat.send_message(f"{data}, {type(data)}")
    if update.message.text in ["🎞 Serial", "🔊 Konsert", "🎬 Premyera", "Multfilm", "⌛️ Treyler", "O'zbek kinolar", "Hind kinolar"]:
        genre_id = data[9]
        print(genre_id,"\n\n\n\n\n\n\n\n\n\n\n\n\n")
        genre = "kinolar"
    elif update.message.text in ["Drama", "Komediya", "Melodramma", "Sarguzasht", "Qo'rqinchli", "Tarixiy", "Klassika", "Fantastika", "Hayotiy", "Jangari"]:
        genre_id = data[10]
        genre = "janrlar"
    elif update.message.text in ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021","2022"]:
        genre_id = data[3]   
        genre = "yil" 
    else:
        pass
    print(data, "\n\n\n\n\n\n\n")
    text1 = tags
    text1 +=f"\n\n<b> Nomi</b>: {data[1]}\n\n"
    text1+=f"<b>🏳️Davlati</b>: {data[2]}\n"
    text1+=f"<b>🗓Yili</b>: {data[3]}\n"
    text1+=f"<b>📢Tili</b>: {data[4]}\n"
    text1+=f"<b>⌛️Davomiyligi</b>: {data[5]}\n"
    # text1+=f"<b>📜Janr: </b>{data[11].capitalize()}\n"
    text1+=f"<b>👀Ko'rildi</b>: {data[6]}\n"
    text1+=f"\n<b>📺 Onlayn ko'rish va Yuklab olish 👇</b>:\n{data[7]}"
    text1+=f"{genre_id} "
    update.message.reply_photo(
        photo=data[7],
        caption=text1,
        parse_mode='HTML',
        reply_markup=inline_button_generator(0, genre_id, genre)    # update.effective_chat.send_photo( 
      )
    

def callback_handler(update: Update, context: CallbackContext):
    # update.effective_chat.send_message(update.inline_query.data)
    # update.effective_chat.send_chat_action(action="upload_photo") 
    part=[]
    k = (update.callback_query.data).split(",")
    # update.effective_chat.send_message(f"{k}, {type(k)}, {[type(a) for a in k]}")
    if k[2] == "janrlar":
        cursor.execute(f"SELECT * FROM movies WHERE genre_id = {int(k[0])} ORDER BY id DESC")
    elif k[2] == "yil":
        cursor.execute(f"SELECT * FROM movies WHERE released_year = {int(k[0])} ORDER BY id DESC")
    elif k[2] == "kinolar":
        cursor.execute(f"SELECT * FROM movies WHERE category_id = {int(k[0])} ORDER BY id DESC")
    else:
        pass

    for  cur in cursor:
        part.append(cur)
    # update.effective_chat.send_message(f"{part[:3]}")
    current_genre_list = part[int(k[1])]
    text1 = tags
    text1 +=f"\n\n<b> Nomi</b>: {current_genre_list[1]}\n"
    text1+=f"<b>🏳️Davlati</b>: {current_genre_list[2]}\n"
    text1+=f"<b>🗓Yili</b>: {current_genre_list[3]}\n"
    text1+=f"<b>📢Tili</b>: {current_genre_list[4]}\n"
    text1+=f"<b>⌛️Davomiyligi</b>: {current_genre_list[5]}\n"
    # text1+=f"<b>📜 Janr:</b> {current_genre_list[11].capitalize()}\n"
    text1+=f"<b>👀Ko'rildi</b>: {current_genre_list[6]}\n"
    text1+=f"\n<b>📺 Onlayn ko'rish va Yuklab olish 👇</b>\n{current_genre_list[7]}"
    update.callback_query.message.edit_media(media=InputMediaPhoto(media=current_genre_list[7],caption=text1,parse_mode='HTML'),reply_markup=inline_button_generator(int(k[1]),int(k[0]),k[2]))
    # update.effective_message.edit_media(media=InputMediaPhoto(media=part[2],caption=text1,parse_mode='HTML'),reply_markup=inline_button_generator(int(update.callback_query.data)))
 

def switch_notification(update: Update, context: CallbackContext):
    update.effective_chat.send_chat_action(action = "typing")
    if update.message.text == "🔔 Bildirishnomalar":
        update.message.reply_text("Saytimiz yangiliklaridan doimiy xabardor bo'lib turishni xohlaysizmi?",reply_markup=BUTTON1)
    elif update.message.text == "👌 Ha":
        update.message.reply_text("Bildirishnomalar yoqildi 🔔")
    else:
        if update.message.text == "😶 Yo'q":
            update.message.reply_text("Bildirishnomalar o'chirildi 🔕")
            
def get_sos(update: Update, context: CallbackContext):
    update.effective_chat.send_chat_action(action = "typing")
    msg = f"Ushbu bot orqali siz <a href='https://uzmovi.com'>UZMOVI</a> saytidan o'zingizni qiziqtirgan filmlarni izlashingiz va tomosha qilishingiz mumkin."\
           "\nShuningdek bot sozlamalaridan «🔔 Bildirishnomalar»ni yoqish orqali saytimizning doimiy yangiliklaridan xabardor bo\'lib turishingiz mumkin."
    update.message.reply_html(msg, disable_web_page_preview=True)

def aboutus_handler(update: Update, context: CallbackContext):
    update.effective_chat.send_chat_action(action = "typing")
    text = "🌐 Bizning veb sayt: <a href='http://uzmovi.com/'>WWW.UZMOVI.COM </a>\n"
    text+= "👥 Telegram guruhimiz: <a href='https://t.me/+Y7UTPUhzpbkzN2Ji'>Muhokama</a>\n"
    text+= "------------------------\n"
    text+= "👨‍⚖️ Administrator: <a href='http://t.me/mirabror_fayzullayev'>Mirabror Fayzullayev</a>\n"
    text+= "🧑‍💻 Dasturchi: Mirabror Fayzullayev"
    update.message.reply_html(text,disable_web_page_preview=True )

genres = ["🎞 Serial", "🔊 Konsert", "🎬 Premyera", "Multfilm", "⌛️ Treyler", "Jangari", "O'zbek kinolar", "Hind kinolar",
          "Drama", "Komediya", "Melodramma", "Sarguzasht", "Qo'rqinchli", "Tarixiy", "Klassika", "Fantastika", "Hayotiy",
          "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021","2022"
]

updater.dispatcher.add_handler(CommandHandler('start', start_handler))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text("📝 Biz haqimizda"), callback=aboutus_handler))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text(genres), callback=movie_handler))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text(["🔔 Bildirishnomalar", "👌 Ha", "😶 Yo'q"]), callback=switch_notification))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text("📽 Janr"), callback=get_genres))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text("🎥 Kinolar"), callback=get_genres))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text("📅 Yil"), callback=sort_year))
updater.dispatcher.add_handler(CallbackQueryHandler(callback=callback_handler))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text("⬅️ Orqaga"), callback=start_handler))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text("🆘 Yordam"), callback=get_sos))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text("show_users"), callback=say_hello))
                                 

         
updater.start_polling()
updater.idle()








































































































































































# import logging
# from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import Updater, CallbackContext,\
#         CommandHandler, MessageHandler, Filters, CallbackQueryHandler
# # 
# logging.basicConfig(level=logging.DEBUG)

# updater = Updater(token="5234535719:AAHgiZ-tHWbTE0ixZEZ6NWcRqJd7TyIiYrg")
# dispatcher = updater.dispatcher


# MENU = ReplyKeyboardMarkup([
#     ['🎬 Premyera'],
#     ['🎥 Kinolar', '📽 Janr', '🎞 Serial'],
#     ['📅 Yil', '🔊 Konsert','⌛️ Treyler'],
#     ['🔔 Bildirishnomalar', '🆘 Yordam', '📝 Biz haqimizda']
# ])

# NEXT = InlineKeyboardMarkup([
#     [InlineKeyboardButton(text="Keyingi", callback_data="2")]
# ])

# PREV_NEXT = InlineKeyboardMarkup([
#     [
#         InlineKeyboardButton(text="Oldingi", callback_data="1"),
#         InlineKeyboardButton(text="Keyingi", callback_data="3"),
#     ]
# ])

# def inline_button_generator(current_trailer_num):
#     if current_trailer_num == 1:
#         return InlineKeyboardMarkup([[
#                 InlineKeyboardButton(text="Keyingi", callback_data=f"{current_trailer_num+1}")
#             ]])
#     return InlineKeyboardMarkup([
#         [
#             InlineKeyboardButton(text="Oldingi", callback_data=f"{current_trailer_num-1}"),
#             InlineKeyboardButton(text="Keyingi", callback_data=f"{current_trailer_num+1}"),
#         ]
#     ])


# def start_handler(update: Update, context: CallbackContext):
#     update.message.reply_text("Quyidagida menyulardan birini tanlang yoki "
#                               "film qidirish uchun so'rovni kiriting 👇",
#                               reply_markup=MENU)


# def aboutus_handler(update, context):
#     update.message.reply_text("🌐 Bizning veb sayt: WWW.UZMOVI.COM (http://uzmovi.com/)"
#                               "👥 Telegram guruhimiz: https://t.me/+Y7UTPUhzpbkzN2Ji"
#                               "------------------------"
#                               "👨‍⚖️ Administrator: Po'latov Shohabbos (http://t.me/uzmovicom)"
#                               "🧑‍💻 Dasturchi: Manuchehr Usmonov"
#                             )


# def trailers_handler(update: Update, context):
#     image_as_bytes = open("qora-adam.jpg", "rb")
#     text = """
#             <a href="http://uzmovi.com/tarjima-kinolar">Tarjima kinolar</a>
#             Jangari (http://uzmovi.com/jangari)
#             Fantastika (http://uzmovi.com/fantastika)
#             Treyler (http://uzmovi.com/treyler) 
#             Nomi: Qora Adam premyera uzbek o'zbek tilida 2022
#             🏳️ <b>Davlati</b>: AQSH
#             🗓 Sanasi: 2022
#             📢 Tili: O'zbek tilida (Tarjima)
#             ⌛️ Davomiyligi: 2 minut
#             👀 Ko'rildi: 125179
#             📺 Onlayn ko'rish va Yuklab olish
#             http://uzmovi.com/treyler/4090-qora-adam-premyera-uzbek-ozbek-tilida-2022.html
#         """
#     update.message.reply_photo(
#         photo=image_as_bytes,
#         caption=text,
#         parse_mode='HTML',
#         reply_markup=inline_button_generator(1)
#     )


# def callback_handler(update: Update, context: CallbackContext):
#     # update.effective_user
#     # update.effective_chat.send_message(update.callback_query.data)
#     image_as_bytes = open("next1.jpg", "rb")
#     text = """
#         <a href="http://uzmovi.com/tarjima-kinolar">Tarjima kinolar</a>
#         Jangari (http://uzmovi.com/jangari)
#         Fantastika (http://uzmovi.com/fantastika)
#         Treyler (http://uzmovi.com/treyler) 
#         <b>Nomi</b>: Ancharted xaritada yo'q maskan premyera uzbek o'zbek tilida 2022
#         🏳️ <b>Davlati</b>: AQSH
#         🗓 Sanasi: 2022
#         📢 Tili: O'zbek tilida (Tarjima)
#         ⌛️ Davomiyligi: 2 minut
#         👀 Ko'rildi: 125179
#         📺 Onlayn ko'rish va Yuklab olish
#         http://uzmovi.com/treyler/4090-qora-adam-premyera-uzbek-ozbek-tilida-2022.html
#     """
#     update.effective_chat.send_photo(
#         photo=image_as_bytes,
#         caption=text,
#         parse_mode='HTML',
#         reply_markup=inline_button_generator(int(update.callback_query.data))
#     )



# dispatcher.add_handler(CommandHandler('start', start_handler))
# dispatcher.add_handler(MessageHandler(Filters.text('📝 Biz haqimizda'), aboutus_handler))
# dispatcher.add_handler(MessageHandler(Filters.text('⌛️ Treyler'), trailers_handler))
# dispatcher.add_handler(CallbackQueryHandler(callback=callback_handler))

# updater.start_polling()
# updater.idle()

