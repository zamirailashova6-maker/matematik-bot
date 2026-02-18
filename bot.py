import telebot
import google.generativeai as genai
from flask import Flask
import threading

# 1. TOKEN VA YANGI API KALIT
TELEGRAM_TOKEN = '8577700735:AAEXw5cWQSFEayqRwSpoe7Px9gtvAX1mb_c'
GEMINI_API_KEY = 'AIzaSyCzCd-T1887k828CkNz6b1POIuw02paxEs'

# 2. GEMINI AI SOZLAMASI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishga tushdi!"

# 3. ASOSIY XABARLARNI QABUL QILISH
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini AI dan javob olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Xatolik yuz bersa, uning turini ko'rsatadi
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # Render uchun Flaskni alohida oqimda yurgizish
    threading.Thread(target=run_flask).start()
    # Botni ishga tushirish
    print("Al-Xorazmiy bot ishga tushirildi...")
    bot.polling(none_stop=True, interval=0, timeout=20)
