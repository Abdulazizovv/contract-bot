from dataclasses import dataclass
from datetime import datetime
import os
from typing import Any, Dict, List, Tuple

import requests

from constants import BACK, month_year_map, END_MONTH, END_YEAR

from telegram import KeyboardButton, ReplyKeyboardMarkup as RKM


from dotenv import load_dotenv

load_dotenv()


PFX_FILE_PATH = "keys/DS522050369100720001.pfx"
PFX_PASSWORD = os.getenv("PFX_PASSWORD")
ALIAS ="cn=abdulazizov ulug‘bek murotali o‘g‘li,name=ulug‘bek,surname=abdulazizov,l=farg`ona shahri,st=farg`ona viloyati,c=uz,uid=638131851,1.2.860.3.16.1.2=52205036910072,serialnumber=785d0338,validfrom=2024.05.01 17:49:48,validto=2026.05.01 17:49:48"
JSHIR = os.getenv("JSHIR")

HOST = os.getenv("HOST")


def split_payments(
    price: float, split: int, index: int, length: int, tariff: str, payment_day: int
) -> List[Tuple[datetime, float]]:

    month, year = month_year_map[index]

    # Validate the provided month integers
    if not (0 <= index <= 10):
        raise ValueError(
            "Invalid month index integer provided. Must be between 1 and 10."
        )

    if not (1 <= payment_day <= 31):
        raise ValueError("Invalid payment day provided. Must be between 1 and 31.")

    # Generate the list of all months in the academic year
    months = []
    current_year = year
    current_month = month

    while current_year < END_YEAR or (
        current_year == END_YEAR and current_month <= END_MONTH
    ):
        months.append((current_year, current_month))
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
        if tariff == "STANDART" and len(months) >= split:
            break

    # Check if there are enough months to split
    total_months = len(months)
    print(total_months, split, type(total_months), type(split))
    if total_months < split:
        raise ValueError("Not enough months to split the payments.")

    # Calculate the monthly payment
    monthly_payment = round(price / split, 2)

    # Calculate the step value
    step = total_months / split

    # Select the months for the payments
    payment_dates = []
    for i in range(split):
        index = round(i * step)
        if index >= total_months:
            index = total_months - 1  # Ensure we do not go out of range
        year, month = months[index]

        # Calculate the payment date
        payment_date = datetime(year, month, payment_day)
        # formatted_date = payment_date.strftime("%d-%B-%Y")
        payment_dates.append((payment_date, monthly_payment))

    return payment_dates


@dataclass
class EImzoToken:
    pkcs7: str
    signature: str


def get_eimzo_token(data: str = None):
    
    res: requests.Response = requests.post(
        # "http://eimzotoken/generate",
        "http://127.0.0.1:8080/generate",
        
        json={
            "pfxFilePath": PFX_FILE_PATH,
            "password": PFX_PASSWORD,
            "alias": "cn=abdulazizov ulug‘bek murotali o‘g‘li,name=ulug‘bek,surname=abdulazizov,l=farg`ona shahri,st=farg`ona viloyati,c=uz,uid=638131851,1.2.860.3.16.1.2=52205036910072,serialnumber=785d0338,validfrom=2024.05.01 17:49:48,validto=2026.05.01 17:49:48",
            "data": data or JSHIR,
            "attached": True,
        },
    )
    
    return EImzoToken(**res.json())


def to_absolute_url(path: str):
    return f"{HOST}{path}"


class ReplyKeyboardMarkup(RKM):
    def __init__(
        self,
        _keyboard: List[List[str | KeyboardButton]] = None,
        back: bool = True,
        resize_keyboard: bool | None = True,
        one_time_keyboard: bool | None = None,
        selective: bool | None = None,
        input_field_placeholder: str | None = None,
        is_persistent: bool | None = None,
        *,
        api_kwargs: Dict[str, Any] | None = None,
    ):
        keyboard = _keyboard or []

        if back:
            keyboard.append([BACK])

        super().__init__(
            keyboard,
            resize_keyboard,
            one_time_keyboard,
            selective,
            input_field_placeholder,
            is_persistent,
            api_kwargs=api_kwargs,
        )


def convert_range_to_index(cell: str) -> tuple[int, int]:
    import re

    match = re.match(r"([A-Z]+)(\d+)", cell)
    if not match:
        raise ValueError("Invalid cell format")

    col_str, row_str = match.groups()
    row_index = int(row_str) - 1
    col_index = (
        sum(
            (ord(char) - ord("A") + 1) * (26**i)
            for i, char in enumerate(reversed(col_str))
        )
        - 1
    )
    return row_index, col_index


def safe_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: str, default: float = 0) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def int_to_month(month: int):
    return {
        1: "Sentabr",
        2: "Oktabr",
        3: "Noyabr",
        4: "Dekabr",
        5: "Yanvar",
        6: "Fevral",
        7: "Mart",
        8: "Aprel",
        9: "May",
        10: "Iyun",
    }.get(month)
