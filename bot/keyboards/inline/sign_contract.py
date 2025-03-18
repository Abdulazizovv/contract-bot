from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

sign_contract_cb = CallbackData("sign_contract", "doc_id", "contract_id")

def sign_contract_kb(doc_id: str, contract_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="📝 Shartnomani imzolash",
            callback_data=sign_contract_cb.new(doc_id=doc_id, contract_id=contract_id),
        )
    )
    return kb