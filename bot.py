import os
import threading
import requests
from time import sleep
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.error import Conflict

# Инициализация Flask сервера
server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is running!"

# Загрузка базы FAQ
with open("faq.json", encoding="utf-8") as f:
    faq_data = json.load(f)

# Инициализация Telegram бота
token = os.getenv("TELEGRAM_BOT_TOKEN", "8163235507:AAGWWz1guEqNBQdH6lHNRxGQXl4KyoHia4I")
app = ApplicationBuilder().token(token).build()

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Направления", "Сроки"],
                ["Вступительные", "Стоимость"],
                ["Общежитие", "Контакты"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я — бот приёмной комиссии СПбУТУиЭ. Задайте вопрос или выберите тему:",
        reply_markup=reply_markup
    )

# Поиск ответа по ключевым словам
def find_answer(user_message):
    text = user_message.lower()
    for item in faq_data:
        if any(keyword in text for keyword in item["keywords"]):
            return item["answer"]
    return "Пожалуйста, уточните вопрос или выберите тему из меню."

# Обработка сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = find_answer(user_message)
    await update.message.reply_text(response)

# Функция для поддержания активности
def keep_alive():
    while True:
        try:
            requests.get("https://tg-bot-spbute.onrender.com")
        except:
            pass
        sleep(300)

# Функция для запуска бота
def run_bot():
    try:
        # Добавляем обработчики
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        app.run_polling()
    except Conflict:
        print("⚠️ Бот уже запущен в другом месте!")

if __name__ == '__main__':
    # Запускаем все компоненты
    threading.Thread(target=keep_alive, daemon=True).start()
    threading.Thread(target=run_bot, daemon=True).start()
    server.run(host='0.0.0.0', port=8000)
