from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import asyncio
import logging
from config_reader import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ Эхо-бот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())