from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def monthly_payment_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="150000 ( сто пятьдесят тысяч ) сум")
            ],
            [
                KeyboardButton(text="⬅️ Orqaga")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard