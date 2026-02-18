import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time

# 1. TOKENLAR
TELEGRAM_TOKEN = '8577700735:AAEXw5cWQSFEayqRwSpoe7Px9gtvAX1mb_c'
GEMINI_API_KEY = 'AIzaSyCzCd-T1887k828CkNz6b1POIuw02paxEs'

# 2. GEMINI AI SOZLAMASI
# Model nomini Google kutubxonasiga moslab eng barqaror holatga keltirdik
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

# 3. RENDER UCHUN YASHASH BELGISI
@app.route('/')
def home():
    return "Al-Xorazmiy AI bot ishlamoqda!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 4. XABARLARNI QAYTA ISHLASH
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # AI dan javob olish
        response = model.generate_content(message.text)
        # Agar AI bo'sh javob qaytarsa yoki muammo bo'lsa
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Kechirasiz, savolingizga javob topolmadim.")
    except Exception as e:
        # Xatoni aniq ko'rsatish
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

# 5. BOTNI ISHGA TUSHIRISH
if __name__ == "__main__":
    # Flask serverni orqa fonda yurgizish
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("Bot ulanmoqda...")
    # Bot o'chib qolsa, avtomatik qayta ulanadi (Conflict xatosini oldini oladi)
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            print(f"Ulanishda xato: {e}")
            time.sleep(5)
