from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from training_code.simple_row import make_row_keyboard

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_food_names = ["Суши", "Спагетти", "Хачапури"]
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]

available_drinks_names = ["Tea", "Latte", "Cappuccino"]
available_drinks_sizes = ["Маленький", "Средний", "Большой"]


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()
    choosing_drinks_name = State()
    choosing_drinks_size = State()


@router.message(Command("food"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите блюдо:",
        reply_markup=make_row_keyboard(available_food_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderFood.choosing_food_name)

# Этап выбора блюда #


@router.message(Command("drinks"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите напиток:",
        reply_markup=make_row_keyboard(available_drinks_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderFood.choosing_drinks_name)


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
    await state.set_state(OrderFood.choosing_food_size)


@router.message(OrderFood.choosing_drinks_name, F.text.in_(available_drinks_names))
async def food_chosen(message: Message, state: FSMContext):
    """Выбираем размер напитка"""
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер напитка:",
        reply_markup=make_row_keyboard(available_drinks_sizes)
    )
    await state.set_state(OrderFood.choosing_drinks_size)


@router.message(StateFilter("OrderFood:choosing_food_name"))
async def food_chosen_incorrectly(message: Message):
    """Обработка неверного выбора блюда"""
    await message.answer(
        text="Я не знаю такого блюда.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_food_names)
    )


@router.message(StateFilter("OrderFood:choosing_drinks_name"))
async def drinks_chosen_incorrectly(message: Message):
    """Обработка неверного выбора напитка"""
    await message.answer(
        text="Я не знаю такого напитка.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_drinks_names)
    )
# Этап выбора размера порции и отображение сводной информации #


@router.message(OrderFood.choosing_food_size, F.text.in_(available_food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
             f"Попробуйте теперь заказать напитки: /drinks",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(OrderFood.choosing_drinks_size, F.text.in_(available_drinks_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {message.text.lower()}  {user_data['chosen_food']}.\n"
             f"Хотите ли вы ещё заказать напитки, еду или выйти из меню: /drinks, /food, /end ",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого размера порции.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )


# Команда завершения чата
@router.message(Command(commands=['end']))
async def end_chat(message: types.Message, state: FSMContext):
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()
    await message.answer(
        text="Чат завершён. Если вам снова потребуется помощь, просто отправьте любое сообщение.",
        reply_markup=types.ReplyKeyboardRemove()
    )