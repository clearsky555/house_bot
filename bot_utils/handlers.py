from aiogram import types
from aiogram.dispatcher import FSMContext


from state import HousesSearchState
from .keybords import get_menu_button, get_post_url_button
from db.database import manager


# Аннотация переменных или объектов
# сообщает к какому классу или объекту относится данная переменная или аргумент
async def welcome_message(message: types.Message):
    text = '''
    Привет, я бот для поиска жилья в Бишкеке. В базе данных квартиры стоимостью до 5_000_000 сом.
    '''
    markup = get_menu_button()
    await message.answer(text, reply_markup=markup)


async def get_categories(callback: types.CallbackQuery):
    await callback.message.answer('Вы нажали кнопку категории')

# ДЛЯ КНОПКИ
async def get_houses_by_room1(callback: types.CallbackQuery):
    text = 'Пожалуйста, отправьте желаемое количество комнат в квартире'
    await HousesSearchState.search_by_room_count.set()
    await callback.message.answer(text)


async def get_houses_by_price1(callback: types.CallbackQuery):
    await callback.message.answer('Вы нажали кнопку поиска по цене')
    text = 'Введите, пожалуйста, минимальную цену в сомах'
    await HousesSearchState.price_start.set()
    await callback.message.answer(text)


# ДЛЯ КОМАНДЫ
async def get_houses_by_room(message: types.Message):
    text = 'Пожалуйста, отправьте желаемое количество комнат в квартире'
    await HousesSearchState.search_by_room_count.set()
    await message.answer(text)


async def get_houses_by_price(message: types.Message):
    await message.answer('Вы нажали кнопку поиска по цене')
    text = 'Введите, пожалуйста, минимальную цену в сомах'
    await HousesSearchState.price_start.set()
    await message.answer(text)


async def search_by_room_count(message: types.Message, state: FSMContext):
    houses = manager.search_by_room_count(message.text)
    await state.finish()
    if houses:
        for house in houses:
            text = f'''
            <b>Квартира:</b> {house[1]},
            <b>Стоимость:</b> 
                1) {house[2]} сом,
                2) {house[3]} $,
            <b>Телефон:</b> {house[4]}
            '''
            markup = get_post_url_button(house[-2])
            await message.answer(text, reply_markup=markup, parse_mode='HTML')
    else:
        await message.answer('В базе данных не найдено')


async def get_start_price(message: types.Message, state: FSMContext):
    start_price = message.text
    async with state.proxy() as data:
        data['start_price'] = start_price
    await HousesSearchState.price_end.set()
    await message.answer('Введите максимальную цену в сомах')


async def get_end_price(message: types.Message, state: FSMContext):
    end_price = message.text
    start_price = 0
    async with state.proxy() as data:
        start_price = data['start_price']
    await state.finish()
    houses = manager.search_by_price(start=start_price, end=end_price)
    print(f'{start_price} - {end_price}')
    if houses:
        for house in houses:
            text = f'''
            Квартира: {house[1]},
            Стоимость: 
                1) {house[2]} сом,
                2) {house[3]} $,
            Телефон: {house[4]}
            '''
            markup = get_post_url_button(house[-2])
            await message.answer(text, reply_markup=markup)
    else:
        await message.answer('В базе данных не найдено')


from parser.main import main
import asyncio


async def update_db(message: types.Message):
    asyncio.create_task(main())
    await message.answer('Обновление базы данных запущено успешно')


# удаление старых постов
from datetime import datetime, timedelta


async def delete_old_posts(message: types.Message):
    old_time = datetime.now() - timedelta(minutes=1)
    manager.delete_post(old_time)
    await message.answer('Посты, созданные более 7 дней назад, удалены!')