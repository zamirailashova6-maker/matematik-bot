import telebot
import google.generativeai as genai

# Telegram Tokeningiz (O'zgartirmang)
TELEGRAM_TOKEN = '8577700735:AAEXw5cWQSFEayqRwSpoe7Px9gtvAX1mb_c'

# Boya nusxa olgan kalitingizni mana bu yerga, qo'shtirnoq ichiga qo'ying
GEMINI_API_KEY = 'AIzaSyA7wzPPFibD3y_dNhEw7-SIJG_In1lSVik'

# AI ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Al-Xorazmiy AI botiman. Savollaringizga javob beraman!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # AI dan javob olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi. Kalitni tekshirib ko'ring.")

bot.polling()
