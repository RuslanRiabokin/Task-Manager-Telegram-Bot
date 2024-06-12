from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import asyncio
import logging
from config_reader import config
from database import Db

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

# Создаем экземпляр класса Db
db = Db()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    # Обработчик команды /start, отправляет приветственное сообщение с инструкциями
    await message.reply("Привет! Я бот для управления задачами.\n"
                        "Вот что я умею:\n"
                        "/add <текст задачи> - Добавить новую задачу.\n"
                        "/remove <id задачи> - Удалить задачу.\n"
                        "/complete <id задачи> - Пометить задачу как выполненную.\n"
                        "/list - Показать список задач.")

@dp.message(Command(commands=['add']))
async def add_task(message: Message):
    # Обработчик команды /add, добавляет новую задачу
    task_text = message.text[len('/add '):].strip()  # Получаем текст задачи
    if task_text:
        db.add_task(task_text, message.from_user.id)  # Добавляем задачу в базу данных
        await message.reply("Задача добавлена!")
    else:
        await message.reply("Пожалуйста, укажите текст задачи после команды /add.")

@dp.message(Command(commands=['remove']))
async def remove_task(message: Message):
    # Обработчик команды /remove, удаляет задачу по ID
    try:
        task_id = int(message.text[len('/remove '):].strip())  # Получаем ID задачи
        db.remove_task(task_id, message.from_user.id)  # Удаляем задачу из базы данных
        await message.reply("Задача удалена!")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректный ID задачи после команды /remove.")

@dp.message(Command(commands=['complete']))
async def complete_task(message: Message):
    # Обработчик команды /complete, отмечает задачу как выполненную по ID
    try:
        task_id = int(message.text[len('/complete '):].strip())  # Получаем ID задачи
        db.complete_task(task_id, message.from_user.id)  # Обновляем задачу в базе данных
        await message.reply("Задача отмечена как выполненная!")
    except ValueError:
        await message.reply("Пожалуйста, укажите корректный ID задачи после команды /complete.")

@dp.message(Command(commands=['list']))
async def list_tasks(message: Message):
    # Обработчик команды /list, выводит список задач
    tasks = db.list_tasks(message.from_user.id)  # Получаем список задач из базы данных
    if tasks:
        task_list = "\n".join([f"{task_id}. {task_text} - {'Выполнена' if is_completed else 'Не выполнена'}"
                               for task_id, task_text, is_completed in tasks])  # Форматируем список задач
        await message.reply("Ваши задачи:\n" + task_list)
    else:
        await message.reply("У вас нет задач.")

async def main() -> None:
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск основного события
    asyncio.run(main())
