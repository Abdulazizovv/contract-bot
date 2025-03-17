from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.data.config import BOT_PASSWORD


@dp.message_handler(state="password")
async def get_password(message: types.Message, state: FSMContext):
    password = message.text
    if password == BOT_PASSWORD:
        await db.check_user(user_id=message.from_user.id)
        await message.delete()
        await message.answer(
            "Parol to'g'ri kiritildi! Siz muvaffaqiyatli tizimga kirdingiz!",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text="📝 Shartnoma yuborish")],
                    [types.KeyboardButton(text="⛔️ Chiqish")],
                ],
                resize_keyboard=True,
            ),
        )
        await state.finish()
    else:
        await message.answer(
            "Parol noto'g'ri kiritildi! Iltimos, qaytadan urinib ko'ring!",
            reply_markup=types.ReplyKeyboardRemove(),
        )
