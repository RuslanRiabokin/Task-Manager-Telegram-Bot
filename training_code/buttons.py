from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
import asyncio
import logging
from myproject import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

@dp.message(Command("пюрешка"))
async def cmd_pureshka(message: types.Message):
    """Обработчик команды /пюрешка. Отправляет клавиатуру с вариантами ответа."""
    kb = [
        [types.KeyboardButton(text="С пюрешкой")],
        [types.KeyboardButton(text="Без пюрешки")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    """Обработчик сообщения 'с пюрешкой'. Отправляет ответ 'Отличный выбор!'."""
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    """Обработчик сообщения 'без пюрешки'. Отправляет ответ 'Так невкусно!'."""
    await message.reply("Так невкусно! Лучше с пюрешкой", reply_markup=types.ReplyKeyboardRemove())

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    """Обработчик команды /start. Отправляет приветственное сообщение."""
    await message.reply("Привет!\nЯ Эхо-бот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")

@dp.message()
async def echo(message: types.Message):
    """Обработчик всех остальных сообщений. Отправляет эхо-ответ с именем и ID пользователя."""
    await message.answer(f'Привет, {message.from_user.first_name}, твой номер id: {message.from_user.id}')

async def main() -> None:
    """Главная функция для запуска бота."""
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
