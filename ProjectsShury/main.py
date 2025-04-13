from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.types.web_app_info import WebAppInfo

from aiogram.filters import Command

bot=Bot('7505769325:AAFgVhv-kcRM01SLSEkRuzxLDtBiW1O3iu8')
dp=Dispatcher()

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    kb=[
        [types.KeyboardButton(text='Open Web-apps', web_app=WebAppInfo(url='https://14e3acdd-8566-4556-b0bf-f10d159fa983-00-36fhhj5epnwbu.pike.replit.dev/'))]
    ]
    keyboard=types.ReplyKeyboardMarkup(keyboard=kb)
    await message.reply("Guten Tag!", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
