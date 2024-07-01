import sqlite3
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
import asyncio
import logging
from myproject import config


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

# Определяем словарь для хранения данных пользователей
user_data = {}


class DishCallbackFactory(CallbackData, prefix="dish"):
    action: str
    id: int


def connection_to_database():
    # Підключення до бази даних
    conn = sqlite3.connect('C:/Users/user/PycharmProjects/cafe_ordering_system_bot/database.db')

    # Створення курсору
    cursor = conn.cursor()

    # Виконання запиту
    query = "SELECT id, dish_name, dish_price FROM Menu WHERE category = 'Закуски';"
    cursor.execute(query)

    # Витяг даних
    results = cursor.fetchall()

    # Закриття курсору та з'єднання
    cursor.close()
    conn.close()

    return results


def get_keyboard_fab():
    # Получаем данные из базы данных
    results = connection_to_database()

    builder = InlineKeyboardBuilder()

    for dish_id, dish_name, dish_price in results:
        builder.button(
            text=f"{dish_name}:  Ціна - {dish_price}",
            callback_data=DishCallbackFactory(action="select", id=dish_id)
        )


    # Выравниваем кнопки в ряд
    builder.adjust(1)

    return builder.as_markup()


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Вкажить блюдо: {new_value}",
            reply_markup=get_keyboard_fab()
        )



async def choice_of_dish(callback_query: types.CallbackQuery, callback_data: DishCallbackFactory):
    """Вибір блюда з меню"""
    await callback_query.message.edit_text(
        f"Ви обрали: {callback_data.id}",
        reply_markup=get_keyboard_fab()
    )




@dp.message(Command("start"))
async def start_command_handler(message: types.Message):
    keyboard = get_keyboard_fab()
    await message.answer("Выберите блюдо:", reply_markup=keyboard)


@dp.message()
async def echo(message: types.Message):
    """Обработчик всех остальных сообщений. Отправляет эхо-ответ с именем и ID пользователя."""
    await message.answer(f'Привет, {message.from_user.first_name}, твой номер id: {message.from_user.id}')
    await message.answer(f'Привет, введите команду (/start)')



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