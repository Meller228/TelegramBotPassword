import telebot
import random
import string

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    text = (
        "Привет! Я бот для работы с паролями.\n\n"
        "🔹 /password — сгенерировать надежный пароль (16 символов)\n"
        "🔹 /check 12345 — проверить надежность пароля"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['password'])
def generate_password(message):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(16))

    bot.reply_to(message, f"🔐 Твой новый пароль:\n`{password}`\n\n(Скопируй его, кликнув по нему)",
                 parse_mode='Markdown')


@bot.message_handler(commands=['check'])
def check_password(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        bot.reply_to(message, "Напиши пароль через пробел после команды. Например: /check qwerty123")
        return

    password = parts[1]
    score = 0
    tips = []

    if len(password) >= 12:
        score += 1
    else:
        tips.append("• Слишком короткий (нужно 12+ символов)")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        tips.append("• Добавь хотя бы одну цифру")

    if any(char.isupper() for char in password):
        score += 1
    else:
        tips.append("• Добавь заглавную букву")


    if score == 3:
        bot.reply_to(message, "🟢 Отличный пароль! Его сложно взломать.")
    elif score == 2:
        bot.reply_to(message, f"🟡 Нормальный пароль, но можно лучше:\n" + "\n".join(tips))
    else:
        bot.reply_to(message, f"🔴 Слабый пароль!\n" + "\n".join(tips))


if __name__ == '__main__':
    print("Кибер-бот запущен...")
    bot.infinity_polling()