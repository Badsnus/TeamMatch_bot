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

    @staticmethod
    def __assert_handler_is_not_register():
        return current_handler.get() != registrate_user

    async def __check_user(self,
                           message: types.Message,
                           ) -> None:

        if not self.user:

            if self.__assert_handler_is_not_register():
                await self.__send_register_message(message)

            raise CancelHandler()

    async def on_process_callback_query(self,
                                        callback: types.CallbackQuery,
                                        data: dict,
                                        ) -> None:
        self.user = data['user']

        try:
            await self.__check_user(
                callback.message,
            )

        except CancelHandler as er:
            if self.__assert_handler_is_not_register():
                raise er
        else:
            if not self.__assert_handler_is_not_register():
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
