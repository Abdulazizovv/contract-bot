from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.keyboards.inline import check_contract_kb
from bot.keyboards.default import back_kb
from bot.filters import IsLogged
from bot.utils import get_informations_via_inn


@dp.message_handler(IsLogged(), text="📝 Shartnoma yuborish", state="*")
async def contract(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Kompaniya INN raqamini kiriting:", reply_markup=back_kb)
    await state.set_state("contract:company_inn")
    await state.update_data(message="Kompaniya INN raqamini kiriting:")
    await state.update_data(section="start")


@dp.message_handler(IsLogged(), state="contract:company_inn")
async def get_company_inn(message: types.Message, state: FSMContext):
    company_inn = message.text
    data = get_informations_via_inn(company_inn)
    if data is None:
        await message.answer("Bunday INN raqamli kompaniya topilmadi. Qaytadan kiriting:", reply_markup=back_kb)
        return

    await state.update_data(company_name=data["shortName"])
    await state.update_data(company_address=data["address"])
    await state.update_data(company_owner=data["director"])
    await state.update_data(company_mfo=data["mfo"])
    await state.update_data(company_account=data["account"])
    await state.update_data(company_oked=data["oked"])
    await state.update_data(company_inn=data["tin"])

    await message.answer("Kompaniya bankini kiriting:", reply_markup=back_kb)
    await state.set_state("contract:company_bank")


@dp.message_handler(IsLogged(), state="contract:company_bank")
async def get_company_bank(message: types.Message, state: FSMContext):
    company_bank = message.text
    await state.update_data(company_bank=company_bank)
    await message.answer("Umumiy narxni kiriting:", reply_markup=back_kb)
    await state.set_state("contract:total_price")
    await state.update_data(section="company_bank")
    await state.update_data(message="Kompaniya bankini kiriting:")


@dp.message_handler(IsLogged(), state="contract:total_price")
async def get_total_price(message: types.Message, state: FSMContext):
    total_price = message.text
    await state.update_data(total_price=total_price)
    await message.answer("Oylik to'lovni kiriting:", reply_markup=back_kb)
    await state.set_state("contract:monthly_payment")
    await state.update_data(section="total_price")
    await state.update_data(message="Umumiy narxni kiriting:")


@dp.message_handler(IsLogged(), state="contract:monthly_payment")
async def get_monthly_payment(message: types.Message, state: FSMContext):
    monthly_payment = message.text
    await state.update_data(monthly_payment=monthly_payment)
    await message.answer("Kompaniya telefon raqamini kiriting:", reply_markup=back_kb)
    await state.set_state("contract:company_phone")
    await state.update_data(section="monthly_payment")
    await state.update_data(message="Oylik to'lovni kiriting:")


@dp.message_handler(IsLogged(), state="contract:company_phone")
async def get_company_phone(message: types.Message, state: FSMContext):
    company_phone = message.text
    await state.update_data(company_phone=company_phone)
    await message.answer("Kompaniya kontakt raqamini kiriting:", reply_markup=back_kb)
    await state.set_state("contract:company_contact_phone")
    await state.update_data(section="company_phone")
    await state.update_data(message="Kompaniya telefon raqamini kiriting:")


@dp.message_handler(IsLogged(), state="contract:company_contact_phone")
async def get_company_contact_phone(message: types.Message, state: FSMContext):
    await state.update_data(section="company_contact_phone")
    await state.update_data(message="Kompaniya kontakt raqamini kiriting:")
    company_contact_phone = message.text
    await state.update_data(company_contact_phone=company_contact_phone)
    data = await state.get_data()
    await message.answer(
        "Ma'lumotlar qabul qilindi. Ma'lumotlarni tekshiring va tasdiqlang.\n\n"
        f"<b>Rahbar:</b> {data['company_owner']}\n"
        f"<b>Kompaniya:</b> {data['company_name']}\n"
        f"<b>Umumiy narx:</b> {data['total_price']}\n"
        f"<b>Oylik to'lov:</b> {data['monthly_payment']}\n"
        f"<b>Manzil:</b> {data['company_address']}\n"
        f"<b>Hisob raqam:</b> {data['company_account']}\n"
        f"<b>Bank:</b> {data['company_bank']}\n"
        f"<b>MFO:</b> {data['company_mfo']}\n"
        f"<b>INN:</b> {data['company_inn']}\n"
        f"<b>OKED:</b> {data['company_oked']}\n"
        f"<b>Telefon:</b> {data['company_phone']}\n"
        f"<b>Kontakt:</b> {data['company_contact_phone']}\n",
        reply_markup=check_contract_kb,
    )

    await state.set_state("contract:preconfirm")


    # await state.update_data(data=data)
    # await message.answer("Rahbar ismini kiriting:", reply_markup=back_kb)
    # await state.set_state("contract:company_owner")
    # await state.update_data(company_inn=company_inn)
    # await state.update_data(message="Rahbar ismini kiriting:")



# async def send_contract(message: types.Message, state: FSMContext):
#     await state.finish()

#     await message.answer("Rahbar ismini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_owner")
#     await state.update_data(message="Rahbar ismini kiriting:")
#     await state.update_data(section="start")


# @dp.message_handler(state="contract:company_owner")
# async def get_director_name(message: types.Message, state: FSMContext):
#     director_name = message.text
#     await state.update_data(company_owner=director_name)
#     await message.answer("Kompaniya nomini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_name")
#     await state.update_data(section="company_owner")
#     await state.update_data(message="Rahbar ismini kiriting:")


# @dp.message_handler(state="contract:company_name")
# async def get_company_name(message: types.Message, state: FSMContext):
#     company_name = message.text
#     await state.update_data(company_name=company_name)
#     await message.answer("Umumiy narxni kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:total_price")
#     await state.update_data(section="company_name")
#     await state.update_data(message="Kompaniya nomini kiriting:")


# @dp.message_handler(state="contract:total_price")
# async def get_total_price(message: types.Message, state: FSMContext):
#     total_price = message.text
#     await state.update_data(total_price=total_price)
#     await message.answer("Oylik to'lovni kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:monthly_payment")
#     await state.update_data(section="total_price")
#     await state.update_data(message="Umumiy narxni kiriting:")


# @dp.message_handler(state="contract:monthly_payment")
# async def get_monthly_payment(message: types.Message, state: FSMContext):
#     monthly_payment = message.text
#     await state.update_data(monthly_payment=monthly_payment)
#     await message.answer("Kompaniya manzilini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_address")
#     await state.update_data(section="monthly_payment")
#     await state.update_data(message="Oylik to'lovni kiriting:")


# @dp.message_handler(state="contract:company_address")
# async def get_company_address(message: types.Message, state: FSMContext):
#     company_address = message.text
#     await state.update_data(company_address=company_address)
#     await message.answer("Kompaniya hisob raqamini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_account")
#     await state.update_data(section="company_address")
#     await state.update_data(message="Kompaniya manzilini kiriting:")


# @dp.message_handler(state="contract:company_account")
# async def get_company_account(message: types.Message, state: FSMContext):
#     company_account = message.text
#     await state.update_data(company_account=company_account)
#     await message.answer("Kompaniya bankini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_bank")
#     await state.update_data(section="company_account")
#     await state.update_data(message="Kompaniya hisob raqamini kiriting:")


# @dp.message_handler(state="contract:company_bank")
# async def get_company_bank(message: types.Message, state: FSMContext):
#     company_bank = message.text
#     await state.update_data(company_bank=company_bank)
#     await message.answer("Kompaniya MFOsini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_mfo")
#     await state.update_data(section="company_bank")
#     await state.update_data(message="Kompaniya bankini kiriting:")


# @dp.message_handler(state="contract:company_mfo")
# async def get_company_mfo(message: types.Message, state: FSMContext):
#     company_mfo = message.text
#     await state.update_data(company_mfo=company_mfo)
#     await message.answer("Kompaniya INN raqamini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_inn")
#     await state.update_data(section="company_mfo")
#     await state.update_data(message="Kompaniya MFOsini kiriting:")


# @dp.message_handler(state="contract:company_inn")
# async def get_company_inn(message: types.Message, state: FSMContext):
#     company_inn = message.text
#     await state.update_data(company_inn=company_inn)
#     await message.answer("Kompaniya OKED raqamini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_oked")
#     await state.update_data(section="company_inn")
#     await state.update_data(message="Kompaniya INN raqamini kiriting:")


# @dp.message_handler(state="contract:company_oked")
# async def get_company_oked(message: types.Message, state: FSMContext):
#     company_oked = message.text
#     await state.update_data(company_oked=company_oked)
#     await message.answer("Kompaniya telefon raqamini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_phone")
#     await state.update_data(section="company_oked")
#     await state.update_data(message="Kompaniya OKED raqamini kiriting:")


# @dp.message_handler(state="contract:company_phone")
# async def get_company_phone(message: types.Message, state: FSMContext):
#     company_phone = message.text
#     await state.update_data(company_phone=company_phone)
#     await message.answer("Kompaniya kontakt raqamini kiriting:", reply_markup=back_kb)
#     await state.set_state("contract:company_contact_phone")
#     await state.update_data(section="company_phone")
#     await state.update_data(message="Kompaniya telefon raqamini kiriting:")


# @dp.message_handler(state="contract:company_contact_phone")
# async def get_company_contact_phone(message: types.Message, state: FSMContext):
#     await state.update_data(section="company_contact_phone")
#     await state.update_data(message="Kompaniya kontakt raqamini kiriting:")
#     company_contact_phone = message.text
#     await state.update_data(company_contact_phone=company_contact_phone)
#     data = await state.get_data()
#     await message.answer(
#         "Ma'lumotlar qabul qilindi. Ma'lumotlarni tekshiring va tasdiqlang.\n\n"
#         f"<b>Rahbar:</b> {data['company_owner']}\n"
#         f"<b>Kompaniya:</b> {data['company_name']}\n"
#         f"<b>Umumiy narx:</b> {data['total_price']}\n"
#         f"<b>Oylik to'lov:</b> {data['monthly_payment']}\n"
#         f"<b>Manzil:</b> {data['company_address']}\n"
#         f"<b>Hisob raqam:</b> {data['company_account']}\n"
#         f"<b>Bank:</b> {data['company_bank']}\n"
#         f"<b>MFO:</b> {data['company_mfo']}\n"
#         f"<b>INN:</b> {data['company_inn']}\n"
#         f"<b>OKED:</b> {data['company_oked']}\n"
#         f"<b>Telefon:</b> {data['company_phone']}\n"
#         f"<b>Kontakt:</b> {data['company_contact_phone']}\n",
#         reply_markup=check_contract_kb,
#     )
#     await state.set_state("contract:preconfirm")
