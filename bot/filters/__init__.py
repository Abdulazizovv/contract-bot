from aiogram import Dispatcher

from bot.loader import dp
from .is_admin import IsAdmin
from .is_group import IsGroup
from .is_logged import IsLogged


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsLogged)
    pass


if __name__ == "filters":
    # dp.filters_factory.bind(IsAdmin)
    pass