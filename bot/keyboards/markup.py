from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

home = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🔍 Search')],
        [KeyboardButton(text='👤 Profile'), KeyboardButton(text='ℹ️ Info')]
    ],
    resize_keyboard=True
)

search = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🛑 Stop Search')]
    ],
    resize_keyboard=True
)

chatting = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🚷 Skip')],
        [KeyboardButton(text='🚪 Exit')]
    ],
    resize_keyboard=True
)