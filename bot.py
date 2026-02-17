import telebot
from sympy import sympify, solve

# Telegram’dan olgan Tokeningni shu yerga qo‘y
API_TOKEN = '8245715431:AAHlqcJT3ChhKfKOUrlSh_QwsRNttcVBThE'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men matematik botman. \nMisollarni yozing (masalan: 2+2 yoki x**2 - 4 = 0)")

@bot.message_handler(func=lambda message: True)
def calculate(message):
    try:
        text = message.text.lower()
        if '=' in text:
            # Tenglamani yechish
            parts = text.split('=')
            equation = sympify(parts[0].strip() + "- (" + parts[1].strip() + ")")
            result = solve(equation)
            bot.reply_to(message, f"Tenglama javobi: {result}")
        else:
            # Oddiy misolni hisoblash
            result = sympify(text)
            bot.reply_to(message, f"Natija: {result}")
    except Exception as e:
        bot.reply_to(message, "Kechirasiz, misolni tushunmadim. To'g'ri formatda yozing.")

bot.polling()
