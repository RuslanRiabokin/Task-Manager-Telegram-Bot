import sqlite3
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
import asyncio
import logging
from myproject import config
from typing import Optional


# Включаємо логування, щоб не пропустити важливі повідомлення
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

# Визначаємо словник для зберігання даних користувачів
user_data = {}


class DishCallbackFactory(CallbackData, prefix="dish"):
    value: str
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


def get_dish_details(dish_id: int):
    # Підключення до бази даних
    conn = sqlite3.connect('C:/Users/user/PycharmProjects/cafe_ordering_system_bot/database.db')

    # Створення курсору
    cursor = conn.cursor()

    # Виконання запиту
    query = "SELECT dish_name, dish_price, description FROM Menu WHERE id = ?"
    cursor.execute(query, (dish_id,))

    # Витяг даних
    result = cursor.fetchone()

    # Закриття курсору та з'єднання
    cursor.close()
    conn.close()

    return result


def get_keyboard_fab():
    # Отримуємо дані з бази даних
    results = connection_to_database()

    builder = InlineKeyboardBuilder()

    for dish_id, dish_name, dish_price in results:
        builder.button(
            text=f"{dish_name}: Ціна - {dish_price}",
            callback_data=DishCallbackFactory(action="select", id=dish_id)
        )

    # Вирівнюємо кнопки в ряд
    builder.adjust(1)

    return builder.as_markup()


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Вкажіть блюдо: {new_value}",
            reply_markup=get_keyboard_fab()
        )


async def choice_of_dish(callback_query: types.CallbackQuery, callback_data: DishCallbackFactory):
    """Вибір блюда з меню"""
    dish_details = get_dish_details(callback_data.id)
    dish_name, dish_price, description = dish_details
    await callback_query.message.answer(
        f"Ви обрали: {dish_name}\n"
        f"Ціна: {dish_price}\n"
        f"Опис: {description}"
    )
    await callback_query.answer()

    # Створюємо клавіатуру з кнопками "Підтвердити" та "Повернутися до вибору страв"
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Підтвердити", callback_data=DishCallbackFactory(action="confirm", id=callback_data.id)
    )
    builder.button(
        text="Повернутися до вибору страв",
        callback_data=DishCallbackFactory(action="back_to_menu", id=callback_data.id)
    )
    builder.adjust(2)

    # Відправляємо повідомлення з клавіатурою
    await callback_query.message.answer(
        "Оберіть подальшу дію:",
        reply_markup=builder.as_markup()
    )


@dp.message(Command("start"))
async def start_command_handler(message: types.Message):
    keyboard = get_keyboard_fab()
    await message.answer("Виберіть блюдо:", reply_markup=keyboard)


@dp.message()
async def echo(message: types.Message):
    """Обробник всіх інших повідомлень. Відправляє ехо-відповідь з ім'ям та ID користувача."""
    await message.answer(f'Привіт, {message.from_user.first_name}, твій номер id: {message.from_user.id}')
    await message.answer(f'Привіт, введіть команду (/start)')


@dp.callback_query(DishCallbackFactory.filter())
async def handle_dish_callback(callback_query: types.CallbackQuery, callback_data: DishCallbackFactory):
    await choice_of_dish(callback_query, callback_data)


async def main() -> None:
    """Головна функція для запуску бота."""
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
