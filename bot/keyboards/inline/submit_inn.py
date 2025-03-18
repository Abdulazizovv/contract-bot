from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

submit_inn_callback = CallbackData("submit_inn", "action")

def submit_inn_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Davom etish", callback_data=submit_inn_callback.new(action="submit")),
            ],
            [
                InlineKeyboardMarkup(text="Hisob raqamni o'zgartirish", callback_data=submit_inn_callback.new(action="edit_hr"))
            ]
        ]
    )
    return keyboard