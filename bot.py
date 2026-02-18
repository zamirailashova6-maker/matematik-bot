import telebot
from sympy import sympify, solve

# Telegram'dan olgan Tokeningni shu yerga qo'y
API_TOKEN = '8245715431:AAHlqcJT3ChhKfKOUrlSh_QwsRNttcVBT hE'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men matematik botman. \nMisollarni yozing (masalan: 2+2 yoki 100*5% yoki x**2 - 4 = 0)")

@bot.message_handler(func=lambda message: True)
def calculate(message):
    try:
        text = message.text.lower()
        
        # Foiz belgisini /100 ga almashtiramiz
        text = text.replace('%', '/100')
        
        if '=' in text:
            parts = text.split('=')
            equation = sympify(parts[0]) - sympify(parts[1])
            res = solve(equation)
        else:
            res = sympify(text)
            
        bot.reply_to(message, f"Natija: {res}")
    except Exception as e:
        bot.reply_to(message, "Xatolik! Misolni to'g'ri yozganingizni tekshiring.")

bot.polling()
