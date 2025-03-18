from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.keyboards.inline import check_contract_kb
from bot.keyboards.default import back_kb
from bot.filters import IsLogged


@dp.message_handler(IsLogged(), text="⬅️ Orqaga", state="*")
async def back_to_section(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # Get current state
    current_state = await state.get_state()

    if data.get("mode", None) == "hand":
        contract_steps = [
            "contract:company_inn",
            "contract:company_account",
            "contract:company_mfo",
            "contract:company_oked",
            "contract:company_bank",
            "contract:total_price",
            "contract:monthly_payment",
            "contract:company_phone",
            "contract:company_contact_phone",
        ]
        contract_messages = {
            "contract:company_inn": "Kompaniya INN raqamini kiriting:",
            "contract:company_account": "Kompaniya hisob raqamini kiriting:",
            "contract:company_mfo": "Kompaniya MFO raqamini kiriting:",
            "contract:company_oked": "Kompaniya OKED raqamini kiriting:",
            "contract:company_bank": "Kompaniya bankini kiriting:",
            "contract:total_price": "Umumiy narxni kiriting:",
            "contract:monthly_payment": "Oylik to'lovni kiriting:",
            "contract:company_phone": "Kompaniya telefon raqamini kiriting:",
        }
    else:
        contract_steps = [
            "contract:company_inn",
            "contract:company_bank",
            "contract:total_price",
            "contract:monthly_payment",
            "contract:company_phone",
            "contract:company_contact_phone",
        ]

        # Define the messages for each step
        contract_messages = {
            "contract:company_inn": "Kompaniya INN raqamini kiriting:",
            "contract:company_bank": "Kompaniya bankini kiriting:",
            "contract:total_price": "Umumiy narxni kiriting:",
            "contract:monthly_payment": "Oylik to'lovni kiriting:",
            "contract:company_phone": "Kompaniya telefon raqamini kiriting:",
        }

    # If user is at the first step, cancel the process
    if current_state == "contract:company_inn":
        await state.finish()
        await message.answer(
            "Shartnoma yaratish bekor qilindi!",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text="📝 Shartnoma yuborish")],
                    [types.KeyboardButton(text="⛔️ Chiqish")],
                ],
                resize_keyboard=True,
            ),
        )
        return

    # Find the index of the current step
    if current_state in contract_steps:
        current_index = contract_steps.index(current_state)
        previous_state = contract_steps[current_index - 1]  # Get the previous step
        previous_message = contract_messages[previous_state]  # Get the message

        # Set the previous state
        await state.set_state(previous_state)
        await message.answer(previous_message, reply_markup=back_kb)
        await state.update_data(section=previous_state, message=previous_message)
