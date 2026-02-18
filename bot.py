import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time
import os

# 1. TOKEN VA KALITLAR (Siz bergan oxirgi ma'lumotlar)
TELEGRAM_TOKEN = '8577700735:AAEXw5cWQSFEayqRwSpoe7Px9gtvAX1mb_c'
GEMINI_API_KEY = 'AIzaSyCzCd-T1887k828CkNz6b1POIuw02paxEs'

# 2. GEMINI AI SOZLAMASI (404 xatosi tuzatilgan holati)
genai.configure(api_key=GEMINI_API_KEY)
# Model nomiga '-latest' qo'shildi, bu 404 xatosini hal qiladi
model = genai.GenerativeModel('gemini-1.5-flash-latest')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

# 3. RENDER UCHUN VEB-SERVER (Bot o'chib qolmasligi uchun)
@app.route('/')
def home():
    return "Al-Xorazmiy AI Bot faol holatda!"

def run_flask():
    # Render 8080 portini kutadi
    app.run(host='0.0.0.0', port=8080)

# 4. XABARLARNI QABUL QILISH
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini AI dan javob olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Agar xato bo'lsa, Telegramga xabar beradi
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

# 5. BOTNI ISHGA TUSHIRISH (409 Conflict xatosi tuzatilgan holati)
if __name__ == "__main__":
    # Flaskni alohida oqimda yurgizish
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()
    
    print("Bot ulanmoqda...")
    # Bot o'chib qolsa, avtomatik qayta ulanadi
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            print(f"Xato: {e}")
            time.sleep(5)
