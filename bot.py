import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os

# Telegram va Gemini tokenlari
TELEGRAM_TOKEN = '8577700735:AAEXw5cWQSFEayqRwSpoe7Px9gtvAX1mb_c'
GEMINI_API_KEY = 'AIzaSyA7wzPPFibD3y_dNhEw7-SIJG_In1lSVik' 

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Al-Xorazmiy AI botiman. Savollaringizga javob beraman!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Xatolik! API kalitingizni tekshiring.")

if __name__ == "__main__":
    # Flask-ni alohida oqimda ishga tushirish (Render uchun)
    t = threading.Thread(target=run_flask)
    t.start()
    # Botni ishga tushirish
    bot.polling(none_stop=True)
