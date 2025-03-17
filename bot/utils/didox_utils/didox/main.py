from manager import DidoxManager
import base64
from pdf_editor.main import GoogleDocsProcessor
from datetime import datetime

didox = DidoxManager.new()


credentials_path = "service-account.json"
template_id = "1pRNYL7ITxcdYWfr8nO2JWSqGCYjr25fhu1lA9QzG8A8"
destination_folder_id = "1aUC2DkkYgmDmX3uXNAIj6KGKej5izOKn"

processor = GoogleDocsProcessor(credentials_path, template_id, destination_folder_id)


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

def edit_document(replacement: dict, file_name: str):
    file_name = "Filled_Template"

    table_data = [
        ["Column1", "Column2", "Column3"],
        ["Column1 Row1", "Column2 Row1", "Column3 Row1"],
        ["Column1 Row2", "Column2 Row2", "Column3 Row2"],
    ]
    pdf_document = processor.process_document(replacement=replacement, file_name=file_name, table_data=table_data)


def pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        base64_string = base64.b64encode(pdf_file.read()).decode("utf-8")
    return base64_string


def main():
    pdf_content = edit_document(replacements, "test")
    print("1)" + pdf_content)
    base64_pdf = pdf_to_base64(pdf_content)
    print(base64_pdf)