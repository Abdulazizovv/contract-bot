from typing import List, Tuple
from telegram.ext.filters import Text


BACK = "🔙 Ortga"

EXCLUDE = ~Text(["/start", BACK])


MONTHS = {
    "Sentabr": 1,
    "Oktabr": 2,
    "Noyabr": 3,
    "Dekabr": 4,
    "Yanvar": 5,
    "Fevral": 6,
    "Mart": 7,
    "Aprel": 8,
    "May": 9,
}


END_MONTH = 6
START_YEAR = 2024
END_YEAR = 2025

month_year_map: List[Tuple[int]] = [
    ((9 + index - 1) % 12 + 1, 2024 + (index >= 4)) for index in range(10)
]


REGISTER_PHONE = "REGISTER_PHONE"

REGISTER_JSHIR = "REGISTER_JSHIR"

REGISTER_CONFIRM = "REGISTER_CONFIRM"

REGISTER_NOTIFY_CONFIRM = "REGISTER_NOTIFT_CONFIRM"

REGISTER_NOTIFY_JSHIR_FOUND = "REGISTER_NOTIFY_JSHIR_FOUND"

MENU = "MENU"



CAME_LIVE_LOCATION = "CAME_LIVE_LOCATION"

CAME_LIVE_LOCATION_ACCURATE_UPDATE = "CAME_LIVE_LOCATION_ACCURATE_UPDATE"