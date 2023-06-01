from aiogram import types

from aiogram import Dispatcher


async def set_default_commands(dp: Dispatcher) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
        ],
    )
