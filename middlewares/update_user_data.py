import time

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from models import User
from loader import session


# TODO надо умный способ, как это красивее сделать
class UpdateUserDataMiddleware(BaseMiddleware):

    async def __update_data(self,
                            user: User | None,
                            new_info: types.User
                            ) -> None:
        # это надо вынести отсюда
        if user is None:
            return

        if user.telegram_username != new_info.username:
            user.telegram_username = new_info.username

        user.last_active = time.time()
        await session.commit()

    async def on_process_callback_query(self,
                                        callback: types.CallbackQuery,
                                        data: dict,
                                        ) -> None:
        await self.__update_data(data.get('user'), callback.from_user)

    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict,
                                 ) -> None:
        await self.__update_data(data.get('user'), message.from_user)
