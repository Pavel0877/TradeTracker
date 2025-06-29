from telegram.ext import filters
import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === Загрузка токена из .env файла ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# === Многоязычная система ===
TEXTS = {
    'ru': {
        'choose_lang': "Выберите язык:\n1. Deutsch\n2. English\n3. Русский",
        'welcome': "Добро пожаловать! Я ваш торговый ассистент.",
        'connect_ebay': "Пожалуйста, подключите свой аккаунт eBay: /connect_ebay",
        'connected': "✅ eBay-аккаунт успешно подключён!",
        'commands': (
            "Доступные команды:\n"
            "/report_day — Отчёт за день\n"
            "/report_week — Отчёт за неделю\n"
            "/report_month — Отчёт за месяц\n"
            "/year_report — Годовой отчёт"
        ),
        'not_connected': "Сначала подключите eBay аккаунт: /connect_ebay"
    },
    'en': {
        'choose_lang': "Choose your language:\n1. Deutsch\n2. English\n3. Русский",
        'welcome': "Welcome! I'm your trading assistant.",
        'connect_ebay': "Please connect your eBay account: /connect_ebay",
        'connected': "✅ eBay account successfully connected!",
        'commands': (
            "Available commands:\n"
            "/report_day — Daily report\n"
            "/report_week — Weekly report\n"
            "/report_month — Monthly report\n"
            "/year_report — Yearly report"
        ),
        'not_connected': "First connect your eBay account: /connect_ebay"
    },
    'de': {
        'choose_lang': "Sprache wählen:\n1. Deutsch\n2. English\n3. Русский",
        'welcome': "Willkommen! Ich bin Ihr Handelsassistent.",
        'connect_ebay': "Bitte verbinden Sie Ihr eBay-Konto: /connect_ebay",
        'connected': "✅ eBay-Konto erfolgreich verbunden!",
        'commands': (
            "Verfügbare Befehle:\n"
            "/report_day — Tagesbericht\n"
            "/report_week — Wochenbericht\n"
            "/report_month — Monatsbericht\n"
            "/year_report — Jahresbericht"
        ),
        'not_connected': "Bitte zuerst eBay verbinden: /connect_ebay"
    }
}

# === Хранение данных пользователей (в файле users.json) ===
user_data_file = 'users.json'

def load_user_data():
    try:
        with open(user_data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open(user_data_file, 'w') as f:
        json.dump(data, f, indent=4)

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users = load_user_data()

    if user_id not in users:
        users[user_id] = {'lang': 'de', 'connected': False}
        save_user_data(users)

    await update.message.reply_text(TEXTS['de']['choose_lang'])

# === Обработка выбора языка ===
async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    choice = update.message.text.strip()
    lang_map = {'1': 'de', '2': 'en', '3': 'ru'}
    lang = lang_map.get(choice, 'de')

    users = load_user_data()
    users[user_id]['lang'] = lang
    save_user_data(users)

    await update.message.reply_text(TEXTS[lang]['welcome'])
    await update.message.reply_text(TEXTS[lang]['connect_ebay'])

# === Команда /connect_ebay ===
async def connect_ebay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users = load_user_data()
    lang = users[user_id]['lang']

    users[user_id]['connected'] = True
    save_user_data(users)

    await update.message.reply_text(TEXTS[lang]['connected'])
    await update.message.reply_text(TEXTS[lang]['commands'])

# === Проверка подключения к eBay ===
def is_connected(user_id):
    users = load_user_data()
    return users.get(user_id, {}).get('connected', False)

# === Пример отчётов ===
async def report_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users = load_user_data()
    lang = users[user_id]['lang']

    if not is_connected(user_id):
        await update.message.reply_text(TEXTS[lang]['not_connected'])
        return

    await update.message.reply_text("📅 Отчёт за день: 123 €")

async def report_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users = load_user_data()
    lang = users[user_id]['lang']

    if not is_connected(user_id):
        await update.message.reply_text(TEXTS[lang]['not_connected'])
        return

    await update.message.reply_text("📅 Отчёт за неделю: 999 €")

async def report_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users = load_user_data()
    lang = users[user_id]['lang']

    if not is_connected(user_id):
        await update.message.reply_text(TEXTS[lang]['not_connected'])
        return

    await update.message.reply_text("📅 Отчёт за месяц: 3421 €")

async def year_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users = load_user_data()
    lang = users[user_id]['lang']

    if not is_connected(user_id):
        await update.message.reply_text(TEXTS[lang]['not_connected'])
        return

    await update.message.reply_text("📅 Годовой отчёт: 38 000 €")

# === Запуск бота ===
async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^[123]$'), handle_language_choice))
    app.add_handler(CommandHandler("connect_ebay", connect_ebay))
    app.add_handler(CommandHandler("report_day", report_day))
    app.add_handler(CommandHandler("report_week", report_week))
    app.add_handler(CommandHandler("report_month", report_month))
    app.add_handler(CommandHandler("year_report", year_report))

    logger.info("🚀 Запуск бота...")
    await app.run_polling()

# === Точка входа ===
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())