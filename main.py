import google.generativeai as genai
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

CHANNAL_TOKEN = "8789135537:AAE2TXsA_oc7rJtEbT-JpOBBTx3fJTfU0HQ"
GEMINI_API_KEY = "AIzaSyBppBBejdFusJ88LLuCx-Z1q84mQsCxOQs"

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
    bot.send_message(message.chat.id, "Salom! Men Render.com da ishlayapman. Tilni tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Rus tili", "Ingliz tili", "O'zbek tili"])
def set_language(message):
    user_langs[message.chat.id] = message.text
    bot.reply_to(message, f"Tushunarli, endi yuborgan matnlaringizni {message.text}ga tarjima qilaman.")

@bot.message_handler(func=lambda message: True)
def translate_text(message):
    target_lang = user_langs.get(message.chat.id, "Rus tili")
    try:
        prompt = f"Matnni {target_lang}ga tarjima qil: {message.text}. Faqat tarjimani o'zini yubor."
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Tarjimada xatolik bo'ldi.")

bot.polling(none_stop=True)
