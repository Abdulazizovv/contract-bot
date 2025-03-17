from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import (
    dp,
    db,
    didox_manager as didox,
    google_docs_processor as processor,
)
from datetime import datetime
from aiogram.dispatcher import FSMContext


# replacements = {
#     "date": datetime.now().strftime("%d.%m.%Y"),
#     "company_name": "ZM-1",
#     "company_owner": "Komiljonov Shukurulloh Ravshan o'g'li",
#     "summa": "100000 (yuz ming so'm)",
#     "month_summa": "20000 (yigirma ming so'm",
#     "company_address": "Toshkent shahar, Yunusobod tumani, 1-uy",
#     "company_account": "20210000400100100001",
#     "company_bank": "Aloqabank",
#     "company_mfo": "005",
#     "company_inn": "123456789",
#     "company_oked": "123456789",
#     "company_phone": "+998 99 999 99 99",
#     "contact_phone": "+998 99 999 99 99",
# }

# # PDF faylni Base64 formatida olish
# async def get_pdf_base64(replacements: dict, file_name: str) -> str:
#     table_data = [
#         ["Column1", "Column2", "Column3"],
#         ["Column1 Row1", "Column2 Row1", "Column3 Row1"],
#         ["Column1 Row2", "Column2 Row2", "Column3 Row2"],
#     ]
#     base64_pdf, pdf_content = await processor.process_document(replacements=replacements, file_name=file_name, table_data=table_data)
#     return base64_pdf

# # Hujjat uchun kerakli ma'lumotlarni shakllantirish
# async def get_document_data() -> dict:
#     doc_date_str = datetime.now().strftime("%Y-%m-%d")

#     return {
#         "data": {
#             "Document": {
#                 "DocumentNo": "тест",
#                 "DocumentDate": doc_date_str,
#                 "DocumentName": "тест"
#             },
#             "ContractDoc": {
#                 "ContractNo": "тест",
#                 "ContractDate": doc_date_str
#             },
#             "SellerTin": "52205036910072",
#             "Seller": {
#                 "Name": "",
#                 "BranchCode": "",
#                 "BranchName": "",
#                 "Address": ""
#             },
#             "BuyerTin": "302936161",
#             "Buyer": {
#                 "Name": "\"VENKON GROUP\" MCHJ",
#                 "Address": "Фидойилар МФЙ, Махтумкули кучаси,  ",
#                 "BranchCode": "",
#                 "BranchName": ""
#             }
#         },
#         "document": f"data:application/pdf;base64,{await get_pdf_base64(replacements, 'Filled_Template 2')}"
#     }


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):

    await state.finish()

    user = await db.add_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
    )

    if user["is_checked"]:
        await message.answer(
            f"Assalomu alaykum, {message.from_user.full_name}!\n" "Xush kelibsiz! \n",
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
    else:
        await message.answer(
            "Assalomu alaykum!\n" "Iltimos, parolni kiriting:",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.set_state("password")
