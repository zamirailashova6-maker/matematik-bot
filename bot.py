import telebot
from sympy import sympify
import os
from flask import Flask
from threading import Thread

# Render bepul tarifda port talab qilgani uchun kichik server
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Telegram Tokeningiz
API_TOKEN = '8245715431:AAH1qcJT3ChhKfKOUr1Sh_QwsRNttcVBTHe'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men bepul matematik botman. Misollarni yuboring (masalan: 100*10%).")

@bot.message_handler(func=lambda message: True)
def calculate(message):
    try:
        # Foiz belgisini hisoblash uchun moslashtiramiz
        text = message.text.replace('%', '/100')
        res = sympify(text)
        bot.reply_to(message, f"Natija: {float(res)}")
    except:
        bot.reply_to(message, "Xato! Misolni to'g'ri yozing.")

if __name__ == "__main__":
    # Serverni alohida oqimda ishga tushiramiz
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
