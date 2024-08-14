from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)


@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Start message')
    await message.answer('Привет! Я бот, помогающий Вашему здоровью. Напиши Calories, чтобы начать подсчёт',
                         reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Отлично, введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Супер, теперь введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Ещё чуть-чуть! Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if 'age' in data and 'growth' in data and 'weight' in data:
        try:
            age = float(data['age'])
            growth = float(data['growth'])
            weight = float(data['weight'])
            norma_man = 10 * weight + 6.25 * growth - 5 * age + 5
            await message.answer(f'Ваша норма калорий - {norma_man}')
        except ValueError:
            await message.answer('Пожалуйста, введите числовые значения.')
    else:
        await message.answer('Пожалуйста, заполните все необходимые поля.')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    print('Мы получили сообщение')
    await message.answer('Введите команду /start, чтобы узнать свою норму калорий (для мужчин)')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
