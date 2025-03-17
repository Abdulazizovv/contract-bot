from aiogram import types
from bot.keyboards.inline import check_contract_cb
from bot.keyboards.inline import sign_contract_kb
from bot.loader import (
    dp,
    google_docs_processor as processor,
    didox_manager as didox,
    db,
    bot,
)
from aiogram.dispatcher import FSMContext
from aiogram import Bot
from datetime import datetime
from io import BytesIO
from bot.filters import IsLogged
from bot.data.config import JSHIR


async def didox_process(bot: Bot, chat_id: str, replacements: dict, file_name: str):
    table_data = [
        ["Column1", "Column2", "Column3"],
        ["Column1 Row1", "Column2 Row1", "Column3 Row1"],
        ["Column1 Row2", "Column2 Row2", "Column3 Row2"],
    ]

    base64_pdf, pdf_content = await processor.process_document(
        bot=bot,
        chat_id=chat_id,
        replacements=replacements,
        file_name=file_name,
        table_data=table_data,
    )

    contract_id = await db.create_contract(
        user_id=chat_id,
        data={
            "company_name": replacements["company_name"],
            "company_owner": replacements["company_owner"],
            "summa": replacements["summa"],
            "month_summa": replacements["month_summa"],
            "company_address": replacements["company_address"],
            "company_account": replacements["company_account"],
            "company_bank": replacements["company_bank"],
            "company_mfo": replacements["company_mfo"],
            "company_inn": replacements["company_inn"],
            "company_oked": replacements["company_oked"],
            "company_phone": replacements["company_phone"],
            "contact_phone": replacements["contact_phone"],
            "pdf_file": pdf_content,
        },
    )

    didox_response = await didox.create_document(
        doc_type="000",  # 000 - Erkin shartnoma
        data={
            "data": {
                "Document": {
                    "DocumentNo": f"{contract_id}",
                    "DocumentDate": replacements["date"],
                    "DocumentName": f"{replacements['company_name']}- OOO \"Sector Soft\" shartnomasi",
                },
                "ContractDoc": {
                    "ContractNo": f"{contract_id}",
                    "ContractDate": replacements["date"],
                },
                "SellerTin": str(JSHIR),
                "Seller": {
                    "Name": "",
                    "BranchCode": "",
                    "BranchName": "",
                    "Address": "",
                },
                "BuyerTin": replacements["company_inn"],
                "Buyer": {
                    "Name": replacements["company_name"],
                    "Address": replacements["company_address"],
                    "BranchCode": "",
                    "BranchName": "",
                },
            },
            "document": f"data:application/pdf;base64,{base64_pdf}",
        },
    )
    if didox_response.success:
        contract_pdf_file_response = didox.doc_to_pdf(didox_response.data["_id"])
        if contract_pdf_file_response.success:
            pdf_file = contract_pdf_file_response.data
            pdf_file.name = f"{file_name}.pdf"
            await bot.send_document(chat_id=chat_id, document=pdf_file)
            await bot.send_message(
                chat_id,
                "Shartnoma muvaffaqiyatli yaratildi!\n" "Shartnoma imzolaysizmi?",
                reply_markup=sign_contract_kb(didox_response.data["_id"], contract_id),
            )
        else:
            await bot.send_message(chat_id, "Shartnoma yaratishda xatolik yuz berdi!")
            print(contract_pdf_file_response.error)
    else:
        await bot.send_message(chat_id, "Shartnoma yaratishda xatolik yuz berdi!")
        print(didox_response.error)


@dp.callback_query_handler(
    IsLogged(), check_contract_cb.filter(), state="contract:preconfirm"
)
async def precontract_check(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    confirm_status = callback_data.get("status")
    data = await state.get_data()
    replacements = {
        "date": datetime.now().strftime("%d.%m.%Y"),
        "company_name": data["company_name"],
        "company_owner": data["company_owner"],
        "summa": data["total_price"],
        "month_summa": data["monthly_payment"],
        "company_address": data["company_address"],
        "company_account": data["company_account"],
        "company_bank": data["company_bank"],
        "company_mfo": data["company_mfo"],
        "company_inn": data["company_inn"],
        "company_oked": data["company_oked"],
        "company_phone": data["company_phone"],
        "contact_phone": data["company_contact_phone"],
    }

    if confirm_status == "confirm":
        await call.message.edit_reply_markup()
        await call.message.reply(
            "Ma'lumotlar tasdiqlandi!\n" "Shartnoma yaratish boshlandi..."
        )
        await didox_process(
            bot=bot,
            chat_id=call.message.chat.id,
            replacements=replacements,
            file_name=f"{data['company_name']}-Shartnoma",
        )
    elif confirm_status == "cancel":
        await call.message.edit_reply_markup()
        await call.message.reply(
            "Ma'lumotlar tasdiqlanmadi!\n" "Shartnoma yaratish bekor qilindi..."
        )
    await state.finish()
