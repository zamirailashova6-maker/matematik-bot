import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time

# 1. YANGILANGAN TOKENLAR
TELEGRAM_TOKEN = '8577700735:AAFwymvnVvXsv_rDJpW87HXnzUK4kS42kuM'
GEMINI_API_KEY = 'AIzaSyCzCd-T1887k828CkNz6b1POIuw02paxEs'

# 2. GEMINI AI SOZLAMASI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Al-Xorazmiy AI Bot yangi tokenda faol!"

# 3. XABARLARNI QABUL QILISH
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {str(e)}")

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("Bot yangi tokenda ishga tushmoqda...")
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            # Token yangilangani uchun endi 409 xatosi chiqmasligi kerak
            print(f"Polling xatosi: {e}")
            time.sleep(5)
