from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="⛔️ Chiqish", state="*")
async def logout(message: types.Message, state: FSMContext):

    await state.finish()

    await db.logout_user(user_id=message.from_user.id)
    await message.answer(
        "Siz muvaffaqiyatli hisobdan chiqdingiz!",
        reply_markup=types.ReplyKeyboardRemove(),
    )
