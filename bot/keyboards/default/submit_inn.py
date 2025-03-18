from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def submit_inn_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True,
                                   keyboard=[
                                       [
                                           KeyboardButton(text="Davom etish➡️")
                                       ],
                                       [
                                           KeyboardButton(text="Bank ma'lumotlarini qo'lda kiritish")
                                       ]
                                   ]
                                   )
    return keyboard