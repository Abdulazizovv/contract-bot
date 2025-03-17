import requests
import json
from dataclasses import dataclass
import os
from typing import Optional, Any, Dict, TypeVar, Generic, Union
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PFX_FILE_PATH = "keys/DS522050369100720001.pfx"
PFX_PASSWORD = os.getenv("PFX_PASSWORD")
ALIAS ="cn=abdulazizov ulug‘bek murotali o‘g‘li,name=ulug‘bek,surname=abdulazizov,l=farg`ona shahri,st=farg`ona viloyati,c=uz,uid=638131851,1.2.860.3.16.1.2=52205036910072,serialnumber=785d0338,validfrom=2024.05.01 17:49:48,validto=2026.05.01 17:49:48"
JSHIR = "638131851"

T = TypeVar("T")

@dataclass
class EImzoToken:
    pkcs7: str
    signature: str


def get_eimzo_token(data: str = None):
    res: requests.Response = requests.post(
        "http://eimzo:8080/generate",
        # "http://127.0.0.1:8080/generate",
        json={
            "pfxFilePath": PFX_FILE_PATH,
            "password": PFX_PASSWORD,
            "alias": ALIAS,
            "data": data or JSHIR,
            "attached": True,
        },
    )

    return EImzoToken(**res.json())

# Custom response class
class DidoxResponse(Generic[T]):
    def __init__(
        self, success: bool, data: Optional[T] = None, error: Optional[str] = None
    ):
        self.success = success
        self.data = data
        self.error = error


class IDidoxInterface:
    pass


class DidoxManager:
    base_url = "https://stage.goodsign.biz/"
    # base_url = "https://api-partners.didox.uz/"

    def __init__(self, token: str):
        self.token = token

    @classmethod
    def new(cls):
        eimzo_token = get_eimzo_token()
        timestamp = cls.get_timestamp(eimzo_token.pkcs7, eimzo_token.signature)


        token = cls.get_token(JSHIR, timestamp["timeStampTokenB64"])


        print(token['token'])

        return DidoxManager(token["token"])

    @classmethod
    def get_timestamp(
        cls, pkcs7: str, signatureHex: str
    ) -> Optional[Dict[str, Union[str, bool]]]:
        response = requests.post(
            f"{cls.base_url}v1/dsvs/timestamp",
            json={"pkcs7": pkcs7, "signatureHex": signatureHex},
        )
        if response.status_code == 200:
            return response.json()
        
        return None

    @classmethod
    def get_token(cls, jshir: str, timestampToken: str) -> Optional[Dict[str, str]]:
        response = requests.post(
            f"{cls.base_url}/v1/auth/{jshir}/token/uz",
            json={"signature": timestampToken},
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(response.text)
            return None

    def get_documents(self, owner: int = 0) -> DidoxResponse[Optional[IDidoxInterface]]:
        headers = {"user-key": self.token}
        response = requests.get(
            f"{self.base_url}/v2/documents/?owner={owner}", headers=headers
        )

        if response.status_code == 200:
            return DidoxResponse(success=True, data=response.json())
        return DidoxResponse(success=False, error=response.text)

    async def create_document(self, doc_type: str, data: Any) -> DidoxResponse[Optional[Any]]:
        headers = {"user-key": self.token}
        response = requests.post(
            f"{self.base_url}/v1/documents/{doc_type}/create",
            json=data,
            headers=headers,
        )

        if 200 <= response.status_code <= 299:
            return DidoxResponse(success=True, data=response.json())
        return DidoxResponse(success=False, error=response.text)

    def doc_to_pdf(self, doc_id: str) -> DidoxResponse[BytesIO]:
        headers = {"user-key": self.token}
        response = requests.get(
            f"{self.base_url}/v1/documents/{doc_id}/pdf/ru",
            headers=headers,
            stream=True,
        )

        if response.status_code == 200:
            pdf_bytes = BytesIO(response.content)
            return DidoxResponse(success=True, data=pdf_bytes)
        return DidoxResponse(success=False, error=response.text)

    def get_document(self, doc_id: str) -> DidoxResponse[Optional[dict]]:
        headers = {"user-key": self.token}
        response = requests.get(
            f"{self.base_url}/v1/documents/{doc_id}?owner=1", headers=headers
        )

        if response.status_code == 200:
            return DidoxResponse(success=True, data=response.json())
        return DidoxResponse(success=False, error=response.text)

    def sign_document(self, doc_id: str) -> DidoxResponse[Optional[dict]]:
        document_response = self.get_document(doc_id)
        if not document_response.success:
            return document_response

        data = document_response.data["data"]["json"]
        data_f_b64 = json.dumps(data)

        key = get_eimzo_token(data_f_b64)

        timestamp = DidoxManager.get_timestamp(key.pkcs7, key.signature)
        if not timestamp:
            return DidoxResponse(success=False, error="Failed to get timestamp")

        headers = {"user-key": self.token}
        response = requests.post(
            f"{self.base_url}/v1/documents/{doc_id}/sign",
            json={"signature": timestamp["timeStampTokenB64"]},
            headers=headers,
        )

        if response.status_code == 200:
            return DidoxResponse(success=True, data=response.json())
        return DidoxResponse(success=False, error=response.text)


    # Hujjat uchun kerakli ma'lumotlarni shakllantirish
    def get_document_data(self, base64_pdf: str) -> dict:
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
            "document": f"data:application/pdf;base64,{base64_pdf}"
        }
    
