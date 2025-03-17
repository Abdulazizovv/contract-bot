from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot.data import config
from bot.loader import db


class IsLogged(BoundFilter):
    async def check(self, message: types.Message):
        return await db.get_user_check(message.from_user.id)
