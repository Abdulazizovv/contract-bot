from aiogram import types
from bot.loader import dp, db, didox_manager as didox
from bot.keyboards.inline import sign_contract_cb
from bot.filters import IsLogged
import logging


@dp.callback_query_handler(
    IsLogged(), sign_contract_cb.filter(), state="*"
)
async def sign_contract(call: types.CallbackQuery, callback_data: dict):
    doc_id = callback_data["doc_id"]
    contract_id = callback_data["contract_id"]
    await call.message.edit_text("Shartnoma imzolanyabdi kuting...⏳")
    response = didox.sign_document(doc_id=doc_id)

    if response.success:
        await db.change_status_contract(contract_id=contract_id, status="Signed")
        await call.message.edit_text(
            "Shartnoma muvaffaqiyatli imzolandi!✅\n"
            "/start - bosh sahifaga qaytish")
    else:
        await call.message.edit_text("Shartnoma imzolashda xatolik yuz berdi!❌")
        logging.error(f"Error while signing contract: {response.error}")
