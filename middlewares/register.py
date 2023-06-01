from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from handlers.users.register import registrate_user
from keyboards.inline.register_keyboard import RegisterKeyboard
from utils.delete_callback_message import try_delete_message


class RegisterMiddleware(BaseMiddleware):
    user = None

    @staticmethod
    async def __send_register_message(message: types.Message) -> None:
        # TODO это надо вынести отсюда
        await message.answer(
            'Перед использованием бота нужно принять правила',
            reply_markup=RegisterKeyboard.keyboard,
        )

    async def __check_user(self,
                           message: types.Message,
                           ) -> None:

        if not self.user:
            await self.__send_register_message(message)
            raise CancelHandler()

    async def on_process_callback_query(self,
                                        callback: types.CallbackQuery,
                                        data: dict,
                                        ) -> None:
        self.user = data['user']

        handler = current_handler.get()

        try:
            await self.__check_user(
                callback.message,
            )

        except CancelHandler as er:
            if handler != registrate_user:
                raise er
        else:
            if handler == registrate_user:
                await try_delete_message(callback.message)
                raise CancelHandler()

    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict,
                                 ) -> None:
        self.user = data['user']

        await self.__check_user(
            message,
        )
