import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os

# 1. TOKENLARNI SOZLASH
# Telegram Bot Tokeningiz
TELEGRAM_TOKEN = '8577700735:AAEXw5cWQSFEayqRwSpoe7Px9gtvAX1mb_c'

# Siz bergan yangi Google API kaliti
GEMINI_API_KEY = 'AIzaSyA7wzPPFibD3y_dNhEw7-SIJG_In1lSVik'

# 2. GEMINI AI NI SOZLASH
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

# 3. RENDER UCHUN "YASHASH BELGISI" (FLASK)
@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlayapti!"

def run_flask():
    # Render 8080 portini kutadi
    app.run(host='0.0.0.0', port=8080)

# 4. BOT BUYRUQLARI
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Al-Xorazmiy aqlli AI botiman. Savollaringizga javob beraman!")

# 5. ASOSIY XABARLARNI QAYTA ISHLASH (AI VA MATEMATIKA)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Avval matematik misol ekanini tekshiramiz
        if any(c in message.text for c in "+-*/%"):
            try:
                # Misolni hisoblash
                result = eval(message.text.replace('^', '**'))
                bot.reply_to(message, f"Natija: {result}")
            except:
                # Agar misol bo'lmasa, AI javob beradi
                response = model.generate_content(message.text)
                bot.reply_to(message, response.text)
        else:
            # Oddiy matn bo'lsa, AI javob beradi
            response = model.generate_content(message.text)
            bot.reply_to(message, response.text)
            
    except Exception as e:
        bot.reply_to(message, "Kechirasiz, hozir javob bera olmayman. API kalitini tekshirib ko'ring.")

# 6. BOTNI ISHGA TUSHIRISH
if __name__ == "__main__":
    # Flaskni alohida oqimda ishga tushiramiz
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Telegram botni ishga tushiramiz
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)
