import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime, timedelta
import os

TOKEN = "8825073782:AAErAPS8efNyLKOrPKuWBiAAJSnU6eBpc"
bot = Bot(token=TOKEN)
dp = Dispatcher()
users = {}

@dp.message(Command("start"))
async def start(m):
    await m.answer("Привет! /renew — продлить, /check — проверить, /getlink — ссылка для VPN")

@dp.message(Command("renew"))
async def renew(m):
    users[m.from_user.id] = datetime.now() + timedelta(days=30)
    await m.answer("✅ Продлено до " + users[m.from_user.id].strftime('%d.%m.%Y'))

@dp.message(Command("check"))
async def check(m):
    uid = m.from_user.id
    if uid in users:
        days = (users[uid] - datetime.now()).days
        await m.answer(f"Осталось {days} дней")
    else:
        await m.answer("Нет подписки")

@dp.message(Command("getlink"))
async def getlink(m):
    await m.answer("🔗 Ваша ссылка: https://ваша-ссылка-тут")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запускаем бота в фоне, а в это время держим порт 10000 открытым
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    # Это нужно, чтобы Render думал, что приложение работает
    import http.server
    import socketserver
    PORT = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("0.0.0.0", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()
