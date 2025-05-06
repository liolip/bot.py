import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import time
import json

# Словарь для хранения общего объема спермы по пользователю
user_total = {}
# Словарь для хранения времени последнего вызова
user_last_time = {}

# Загружаем данные из файла
def load_data():
    global user_total, user_last_time
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            user_total = data.get("user_total", {})
            user_last_time = data.get("user_last_time", {})
    except FileNotFoundError:
        user_total = {}
        user_last_time = {}

# Сохраняем данные в файл
def save_data():
    data = {
        "user_total": user_total,
        "user_last_time": user_last_time
    }
    with open("data.json", "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, напиши /dildobek, чтобы узнать сколько ты залил в беку 🍆")

async def dildobek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_time = time.time()

    # Проверяем таймер — раз в 3600 секунд (1 час)
    if user_id in user_last_time and current_time - user_last_time[user_id] < 3600:
        remaining = int(3600 - (current_time - user_last_time[user_id]))
        minutes = remaining // 60
        seconds = remaining % 60
        await update.message.reply_text(f"Подожди ещё {minutes} мин. {seconds} сек. перед следующим заливом.")
        return

    # Генерация "размера"
    size = round(random.uniform(3.0, 25.0), 1)
    emojis = "🍆" * int(size // 3)

    # Обновление общего объема
    if user_id not in user_total:
        user_total[user_id] = 0
    user_total[user_id] += size
    total = round(user_total[user_id], 1)

    # Сохраняем время последнего вызова
    user_last_time[user_id] = current_time

    save_data()  # Сохраняем данные после изменения

    await update.message.reply_text(
        f"Ты залил в беку {size} л. спермы {emojis}\nВсего ты залил {total} л. 🧪"
    )

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_total:
        await update.message.reply_text("Пока что никто ничего не залил 🤷‍♂️")
        return

    # Сортировка пользователей по объему
    top_users = sorted(user_total.items(), key=lambda x: x[1], reverse=True)[:20]

    message = "🏆 Топ 20 по заливам в беку:\n"
    for i, (user_id, total) in enumerate(top_users, start=1):
        try:
            user = await context.bot.get_chat(user_id)
            name = user.first_name or "Неизвестный"
        except:
            name = "Неизвестный"
        message += f"{i}. {name} — {round(total, 1)} л. 🧪\n"

    await update.message.reply_text(message)

# Загружаем данные при запуске
load_data()

# Запуск бота
app = ApplicationBuilder().token("7926480170:AAG_fCvQuSM-w74K137NbE4sfVTgGasdgtA").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("dildobek", dildobek))
app.add_handler(CommandHandler("top", top))

app.run_polling()
