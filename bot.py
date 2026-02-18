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
    return "Al-Xorazmiy AI Bot faol holatda!"

# 3. XABARLARNI QABUL QILISH
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini AI dan javob olish
        response = model.generate_content(message.text)
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Kechirasiz, ma'lumot topolmadim.")
    except Exception as e:
        # Xatolikni Telegramda ko'rish uchun
        bot.reply_to(message, f"Xatolik: {str(e)}")

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 4. BOTNI ISHGA TUSHIRISH (Eng muhim qismi)
if __name__ == "__main__":
    # Flaskni orqa fonda ishga tushirish
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Eskidan qolib ketgan webhookni o'chirish
    bot.remove_webhook()
    time.sleep(1) 
    
    print("Bot ishga tushdi...")
    
    # skip_pending=True: Bot o'chiqligida yozilgan eski xabarlarni e'tiborsiz qoldiradi
    # Bu botning "tiqilib" qolishini oldini oladi
    bot.polling(none_stop=True, skip_pending=True)
