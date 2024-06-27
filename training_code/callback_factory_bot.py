from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
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


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="-1", callback_data=NumbersCallbackFactory(action="change", value=-1)
    )
    builder.button(
        text="-20", callback_data=NumbersCallbackFactory(action="change", value=-20)
    )
    builder.button(
        text="-200", callback_data=NumbersCallbackFactory(action="change", value=-200)
    )
    builder.button(
        text="-1000", callback_data=NumbersCallbackFactory(action="change", value=-1000)
    )
    builder.button(
        text="+1", callback_data=NumbersCallbackFactory(action="change", value=1)
    )
    builder.button(
        text="+20", callback_data=NumbersCallbackFactory(action="change", value=20)
    )
    builder.button(
        text="+200", callback_data=NumbersCallbackFactory(action="change", value=200)
    )
    builder.button(
        text="+1000", callback_data=NumbersCallbackFactory(action="change", value=1000)
    )
    builder.button(
        text="Подтвердить", callback_data=NumbersCallbackFactory(action="finish")
    )
    # Выравниваем кнопки по 4 в ряд, чтобы получилось 4 + 1
    builder.adjust(4)
    return builder.as_markup()


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Укажите число: {new_value}",
            reply_markup=get_keyboard_fab()
        )


@dp.message(Command("numbers_fab"))
async def cmd_numbers_fab(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard_fab())


# Нажатие на одну из кнопок: -2, -1, +1, +2
@dp.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    # Текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    user_data[callback.from_user.id] = user_value + callback_data.value
    await update_num_text_fab(callback.message, user_value + callback_data.value)
    await callback.answer()


# Нажатие на кнопку "подтвердить"
@dp.callback_query(NumbersCallbackFactory.filter(F.action == "finish"))
async def callbacks_num_finish_fab(callback: types.CallbackQuery):
    # Текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()


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
