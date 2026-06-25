import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime, timedelta
import os

TOKEN = "8825073782:AAEY_ynopBO_Jy83_FAHjYVhrM90codVokw"
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
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

async def keep_alive():
    from aiohttp import web
    app = web.Application()
    async def hello(request):
        return web.Response(text="Бот работает!")
    app.router.add_get('/', hello)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 10000)))
    await site.start()
    print(f"✅ Веб-сервер запущен на порту {os.environ.get('PORT', 10000)}")
    await asyncio.Event().wait()

async def main_with_server():
    await asyncio.gather(main(), keep_alive())

if __name__ == "__main__":
    asyncio.run(main_with_server())
