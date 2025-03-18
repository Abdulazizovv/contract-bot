from didox.manager import DidoxManager
import base64
from pdf_editor.main import GoogleDocsProcessor
from datetime import datetime

# DidoxManager ob'ektini yaratamiz
didox = DidoxManager.new()

# Google Docs orqali PDF generatsiya qilish uchun kerakli ma'lumotlar
credentials_path = "src/service-account.json"
template_id = "1pRNYL7ITxcdYWfr8nO2JWSqGCYjr25fhu1lA9QzG8A8"
destination_folder_id = "1aUC2DkkYgmDmX3uXNAIj6KGKej5izOKn"

processor = GoogleDocsProcessor(credentials_path, template_id, destination_folder_id)

# O'zgartiriladigan maydonlar

replacements = {
    "date": datetime.now().strftime("%d.%m.%Y"),
    "company_name": "ZM-1",
    "company_owner": "Komiljonov Shukurulloh Ravshan o'g'li",
    "summa": "100000 (yuz ming so'm)",
    "month_summa": "20000 (yigirma ming so'm",
    "company_address": "Toshkent shahar, Yunusobod tumani, 1-uy",
    "company_account": "20210000400100100001",
    "company_bank": "Aloqabank",
    "company_mfo": "005",
    "company_inn": "123456789",
    "company_oked": "123456789",
    "company_phone": "+998 99 999 99 99",
    "contact_phone": "+998 99 999 99 99",
}

# PDF faylni Base64 formatida olish
def get_pdf_base64(replacements: dict, file_name: str) -> str:
    table_data = [
        ["Column1", "Column2", "Column3"],
        ["Column1 Row1", "Column2 Row1", "Column3 Row1"],
        ["Column1 Row2", "Column2 Row2", "Column3 Row2"],
    ]
    base64_pdf = processor.process_document(replacements=replacements, file_name=file_name, table_data=table_data)
    return base64_pdf

# Hujjat uchun kerakli ma'lumotlarni shakllantirish
def get_document_data() -> dict:
    doc_date_str = datetime.now().strftime("%Y-%m-%d")

    return {
        "data": {
            "Document": {
                "DocumentNo": "тест",
                "DocumentDate": doc_date_str,
                "DocumentName": "тест"
            },
            "ContractDoc": {
                "ContractNo": "тест",
                "ContractDate": doc_date_str
            },
            "SellerTin": "52205036910072",
            "Seller": {
                "Name": "",
                "BranchCode": "",
                "BranchName": "",
                "Address": ""
            },
            "BuyerTin": "302936161",
            "Buyer": {
                "Name": "\"VENKON GROUP\" MCHJ",
                "Address": "Фидойилар МФЙ, Махтумкули кучаси,  ",
                "BranchCode": "",
                "BranchName": ""
            }
        },
        "document": f"data:application/pdf;base64,{get_pdf_base64(replacements, 'Filled_Template 2')}"
    }

# Asosiy funksiya
def main():
    print("Ishlamoqda...")
    response = didox.create_document(
        doc_type="000",
        data=get_document_data(),
    )
    document_id = response.data["_id"]
    print(f"Document ID: {document_id}")
    signed_document = didox.sign_document(document_id)
    if signed_document.success:
        print("Hujjat muvaffaqiyatli imzalandi")
    else:
        print(signed_document.error)
        print("Hujjat imzalanmadi")
    print("OK...")

# Funksiyani ishga tushiramiz
# main()
