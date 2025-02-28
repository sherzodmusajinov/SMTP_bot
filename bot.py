import smtplib
import random
from email.mime.text import MIMEText
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "yuor@gmail.com"
EMAIL_PASSWORD = "abcd efgs hjds lomp"

TOKEN = "YOUR BOT TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


verification_codes = {}


def send_verification_code(receiver_email):
    verification_code = str(random.randint(100000, 999999))
    verification_codes[receiver_email] = verification_code

    subject = "Ваш код подтверждения"
    body = f"Ваш код: {verification_code}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Введите ваш email:")

# Обработчик email
@dp.message_handler(lambda message: "@" in message.text and "." in message.text)
async def get_email(message: types.Message):
    email = message.text.strip()
    if send_verification_code(email):
        await message.reply("Код отправлен. Введите его:")
        dp.register_message_handler(lambda msg: verify_code(msg, email))
    else:
        await message.reply("Ошибка при отправке кода. Попробуйте позже.")


async def verify_code(message: types.Message, email):
    code = message.text.strip()
    if email in verification_codes and verification_codes[email] == code:
        await message.reply("Вы зарегистрированы ✅")
        del verification_codes[email]
    else:
        await message.reply("Неверный код. Попробуйте ещё раз.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
