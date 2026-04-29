import google.generativeai as genai
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# 1. TOKENLARNI TO'G'RI YOZAMIZ
CHANNAL_TOKEN = "8789135537:AAE2TXsA_oc7rJtEbT-Jp0BBTx3fJTfU0HQ"
# Kalitni aniq nusxalaganingizga ishonch hosil qiling
GEMINI_API_KEY = "AizaSyBppBBejdFusJ88LLuCx-Z1q84mQsCxOQs" 

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(CHANNAL_TOKEN)
user_langs = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("Rus tili")
    btn2 = KeyboardButton("Ingliz tili")
    btn3 = KeyboardButton("O'zbek tili")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Salom! Tarjima qilish uchun tilni tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Rus tili", "Ingliz tili", "O'zbek tili"])
def set_lang(message):
    user_langs[message.chat.id] = message.text
    bot.reply_to(message, f"Tushunarli, endi yuborgan matnlaringizni {message.text}ga tarjima qilaman.")

@bot.message_handler(func=lambda message: True)
def translate(message):
    # Agar foydalanuvchi til tanlamagan bo'lsa, rus tili standart bo'ladi
    lang = user_langs.get(message.chat.id, "Rus tili")
    try:
        prompt = f"Ushbu matnni {lang}ga juda aniq tarjima qil: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Xatoni aniq nima ekanligini ko'rsatish uchun e ni qo'shdim
        bot.reply_to(message, f"Tarjimada xatolik bo'ldi. Sababi: {str(e)}")

bot.infinity_polling()
            
