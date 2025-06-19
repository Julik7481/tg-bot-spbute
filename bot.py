import os
import logging

logging.basicConfig(level=logging.INFO)  # Включите логирование

async def start(update, context):
    print("Команда /start получена!")  # Должно появиться в логах Render
    await update.message.reply_text("🔄 Тестовый ответ")

token = os.getenv("TELEGRAM_BOT_TOKEN")
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))

print("Бот запущен!")  # Контрольная точка
app.run_polling()
