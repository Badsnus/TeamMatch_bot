from aiogram.dispatcher.handler import ctx_data

from models import User


def get_user_from_ctx() -> User:
    return ctx_data.get().get('user')
