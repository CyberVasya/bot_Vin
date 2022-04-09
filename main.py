
import telebot
from telebot.types import KeyboardButton,ReplyKeyboardMarkup
from telebot import types
import time

TOKEN = " "
 
bot = telebot.TeleBot(TOKEN)
ask = "🖌 Опишіть Ваше Замовлення 📖\n(Крамницю,Товари та їх кількість):"
addr = "📖 Вкажіть Вашу Адресу 🏚:"
cat = "⬇️Оберіть Категорію⬇️ :"
finsms = '⬇️Підтвердити замовлення ?⬇️ :'

@bot.message_handler(commands='start')
def start(message):
    bot.send_message(message.chat.id,
                     '''👋Привіт,{0.first_name}!👋\n🔍Оберіть будь ласка Район 🏡\n🚴 Для пошуку кур"єра 🚴 :'''.format(
                         message.from_user), reply_markup=city_markup)

@bot.message_handler(content_types=['text'])
def text(message):
    if message.chat.type == 'private':
        if message.text in city:
            category(message)

def category(message):  
    bot.send_message(message.from_user.id,cat,reply_markup=menu_markup)
    bot.register_next_step_handler(message,description_msg,{'city':message.text})

def description_msg(message,data:dict):
    if message.text == back_text :
        start(message)
        return
        
    if message.text in cat_menu:
        data['category'] = message.text
        bot.send_message(message.from_user.id, ask,reply_markup=back_markup)
        bot.register_next_step_handler(message, adress,data)
    else:
        bot.send_message(message.from_user.id,text="💁‍♂️Ні,я такого не розумію,почнемо від початку...💁‍♂️")
        start(message)
        return

def adress(message,data: dict):
    if message.text == back_text :
        start(message)
        return 
    data['description'] = message.text
    bot.send_message(message.from_user.id,addr,reply_markup=back_markup)
    bot.register_next_step_handler(message,phone_msg, data)
 
def phone_msg(message,data: dict):
    if message.text == back_text :
        adress(message,data)
        return   
    data['adress'] = message.text
    bot.send_message(message.from_user.id, "📨 Надішліть або напишіть номер Вашого телефона 📱: ", reply_markup=but_phone())
    bot.register_next_step_handler(message, last_msg, data)


def last_msg(message, data: dict):
    if back_text == message.text:
        start(message)
        return
    try:
        data['phone'] = message.contact.phone_number
    except AttributeError:
        data['phone']=message.text
    bot.send_message(message.from_user.id,
                     text=f"✅ Ваше замовлення :\n  Район :{data['city']}\n  Категорія :{data['category']}\n  Замовлення :{data['description']}\n  Адреса:{data['adress']}\n  Телефон :{data['phone']}")
    bot.send_message(message.from_user.id,finsms,reply_markup=YN_markup)
    
    bot.register_next_step_handler(message,finish,data)

def finish(message,data:dict):
       
    if message.text == "✅Так":
        bot.send_message(message.chat.id, text="🙏 Дякуємо за замовленя! ✅\n📃Ваша заявка передається на обробку!\n🚴 Кур'єр з Вами зв'яжеться протягом 10 хвилин 🕑",reply_markup=types.ReplyKeyboardRemove())
        push_mess(data)
        time.sleep(5)
        bot.send_message(message.chat.id, text="↪️Для повторного замовлення Очистіть історію!↪️")
    elif message.text == "❌Ні": 
        start(message)

def push_mess(data: dict):
    bot.send_message(chat_id=-795915256,
                     text=f"✅ Нове замовлення :\n  Район :{data['city']}\n  Категорія :{data['category']}\n  Замовлення :{data['description']}\n  Адреса:{data['adress']}\n  Телефон :{data['phone']}")

     
back_text = "❌Відмінити" 
cat_menu = ["🥩🥛Магазин","🥔🥕Ринок","🍔🍱Фастфуд","💊🌡Аптека","⛽️АЗС","🤷Інше","❌Відмінити"]
city = ['👨‍🎓Академічний', '🌍Бл.Замостя', '🍒Вишенька', '🌍Дал.Замостя', '💥Елеткромережа', '💐Київська', '🎎Корея', '🌻Поділля',
        '⛳Пятничани', '🌊Св.Масив', '👱Словянка', '🌆Старе Місто', '⚓Тяжилів', '🌾Урожай', '🏢Центр']
yes_no = ["✅Так","❌Ні"]

city_markup = ReplyKeyboardMarkup(row_width=2).add(*[KeyboardButton(i) for i in city])
menu_markup = ReplyKeyboardMarkup(row_width=2).add(*[KeyboardButton(i) for i in cat_menu])
back_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(back_text))
YN_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(*[KeyboardButton(i) for i in yes_no])

def but_phone():
    button_phone = ReplyKeyboardMarkup(resize_keyboard=True)
    bu1 = KeyboardButton(text="📲 Надіслати 📲", request_contact=True)
    bu2 = KeyboardButton(text="❌Відмінити")
    button_phone.add(bu1,bu2)
    return button_phone
 
 
bot.polling(non_stop=True,timeout=150)
