from aiogram import types

from aiogram.dispatcher.middlewares import BaseMiddleware

from models import User


# TODO надо умный способ эт красиво сделать
# TODO заменить ключ с текста на константу
class SetUserMiddleware(BaseMiddleware):

    async def __setup_data(self, telegram_id: int, data: dict) -> None:
        self.data = data

        user = await User.get_by_telegram_id(telegram_id)
        self.data['user'] = user

    async def on_process_callback_query(self,
                                        callback: types.CallbackQuery,
                                        data: dict,
                                        ) -> None:
        await self.__setup_data(callback.from_user.id, data)

    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict,
                                 ) -> None:
        await self.__setup_data(message.from_user.id, data)
