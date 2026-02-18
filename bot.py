import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time

# Tokenlar
TELEGRAM_TOKEN = '8577700735:AAEXw5cWQSFEayqRwSpoe7Px9gtvAX1mb_c'
GEMINI_API_KEY = 'AIzaSyCzCd-T1887k828CkNz6b1POIuw02paxEs'

# Gemini sozlamasi
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot faol holatda!"

# Xabarlarni qayta ishlash
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
    # Flaskni alohida oqimda ishga tushirish
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Botni qayta-qayta ulanishga majburlash (Conflict bo'lmasligi uchun)
    while True:
        try:
            print("Bot ulanmoqda...")
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            print(f"Pollingda xato: {e}")
            time.sleep(5)
