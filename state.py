from aiogram.dispatcher.filters.state import StatesGroup, State


class HousesSearchState(StatesGroup):
    search_by_room_count = State()
    price_start = State()
    price_end = State()