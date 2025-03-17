from aiogram import types
from bot.loader import dp
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="Bekor qilish ❌", state="*")
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(
        "Shartnoma yaratish bekor qilindi!",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="📝 Shartnoma yuborish"),
                ],
                [types.KeyboardButton(text="⛔️ Chiqish")],
            ],
            resize_keyboard=True,
        ),
    )
