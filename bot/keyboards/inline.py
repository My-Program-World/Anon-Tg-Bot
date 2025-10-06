from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yes", callback_data="exit_confirm"),
            InlineKeyboardButton(text="❌ No", callback_data="exit_cancel")
        ],
    ]
)