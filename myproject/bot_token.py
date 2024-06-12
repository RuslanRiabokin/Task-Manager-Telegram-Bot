from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import asyncio

async def read_token() -> str:
    with open("token.txt", "r") as file:
        return file.read().strip()

async def main() -> None:
    API_TOKEN = await read_token()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def send_welcome(message: types.Message):
        await message.reply("Привет!\nЯ Эхо-бот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")

    @dp.message()
    async def echo(message: types.Message):
        await message.answer(message.text)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
