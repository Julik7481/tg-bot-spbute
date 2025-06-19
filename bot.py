import json
import os
from flask import Flask, request
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Инициализация Flask сервера
server = Flask(__name__)

# Загрузка базы FAQ
with open("faq.json", encoding="utf-8") as f:
    faq_data = json.load(f)

# Получаем токен и создаём бота
TOKEN = os.getenv("8163235507:AAGWWz1guEqNBQdH6lHNRxGQXl4KyoHia4I")
WEBHOOK_URL = os.getenv("https://tg-bot-spbute.onrender.com")  # Пример: https://tg-bot-spbute.onrender.com

bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Направления", "Сроки"],
                ["Вступительные", "Стоимость"],
                ["Общежитие", "Контакты"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я — бот приёмной комиссии СПбУТУиЭ. Задайте вопрос или выберите тему:",
        reply_markup=reply_markup
    )

# Обработка сообщений
def find_answer(user_message):
    text = user_message.lower()
    for item in faq_data:
        if any(keyword in text for keyword in item["keywords"]):
            return item["answer"]
    return "Пожалуйста, уточните вопрос или выберите тему из меню."

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = find_answer(user_message)
    await update.message.reply_text(response)

# Flask обрабатывает POST-запросы от Telegram
@server.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

# Установка webhook вручную (один раз)
@server.route('/set_webhook', methods=['GET'])
def set_webhook():
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    return "Webhook установлен"

# Добавляем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Запускаем сервер
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    server.run(host='0.0.0.0', port=port)
