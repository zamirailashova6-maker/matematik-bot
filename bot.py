import telebot
import google.generativeai as genai
from flask import Flask
import threading

# Token va API kalit
TELEGRAM_TOKEN = '8577700735:AAEXw5cWQSFEayqRwSpoe7Px9gtvAX1mb_c'
GEMINI_API_KEY = 'AIzaSyA7wzPPFibD3y_dNhEw7-SIJG_In1lSVik'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Al-Xorazmiy AI bot ishlamoqda!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! Men Al-Xorazmiy aqlli botiman. Menga xohlagan savolingizni bering yoki misol yuboring!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    msg_text = message.text
    try:
        # 1. Avval matematik misol sifatida tekshirib ko'ramiz
        if any(c in msg_text for c in "+-*/%"):
            try:
                # Agar bu matematik ifoda bo'lsa, hisoblaymiz
                result = eval(msg_text.replace('^', '**'))
                bot.reply_to(message, f"Natija: {result}")
            except:
                # Agar hisoblashda xato bo'lsa (matn bo'lsa), AI javob beradi
                response = model.generate_content(msg_text)
                bot.reply_to(message, response.text)
        else:
            # 2. Agar matematik belgilar bo'lmasa, to'g'ridan-to'g'ri AI javob beradi
            response = model.generate_content(msg_text)
            bot.reply_to(message, response.text)
            
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi. Iltimos, birozdan so'ng qayta yozib ko'ring.")

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.polling(none_stop=True, interval=0, timeout=20)
