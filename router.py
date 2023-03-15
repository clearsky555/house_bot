from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from bot_utils import handlers as hs
from state import HousesSearchState

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Router
# Commands
dp.register_message_handler(hs.welcome_message, commands=['start'])
dp.register_message_handler(hs.update_db, commands=['update_db'])


# text message
dp.register_message_handler(
    hs.search_by_room_count,
    content_types=['text'],
    state=HousesSearchState.search_by_room_count
)

dp.register_message_handler(hs.get_houses_by_room, commands='search_by_room_count')
dp.register_message_handler(hs.get_houses_by_price, commands='search_by_price')
dp.register_message_handler(hs.delete_old_posts, commands='delete_posts')


dp.register_message_handler(hs.get_start_price, state=HousesSearchState.price_start)
dp.register_message_handler(hs.get_end_price, state=HousesSearchState.price_end)


# Callbacks
dp.register_callback_query_handler(
    hs.get_categories,
    lambda c: c.data == 'category'
)

dp.register_callback_query_handler(
    hs.get_houses_by_room1,
    lambda c: c.data == 'search_by_room_count'
)

dp.register_callback_query_handler(
    hs.get_houses_by_price1,
    lambda c: c.data == 'search_by_price'
)