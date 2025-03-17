from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

check_contract_cb = CallbackData("contract_check", "status")

check_contract_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=check_contract_cb.new(status="confirm")),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=check_contract_cb.new(status="cancel"))
        ]
    ]
)