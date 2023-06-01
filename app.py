from aiogram import executor, Dispatcher

import loader
import middlewares, filters, handlers
from models import create_all_db
from utils import notify_admins, set_bot_commands


async def on_startup(dispatcher: Dispatcher) -> None:
    # default settings
    await set_bot_commands.set_default_commands(dispatcher)
    await notify_admins.on_startup_notify(dispatcher)

    await create_all_db(loader.engine)


if __name__ == '__main__':
    # TODO mb go to webhooks
    executor.start_polling(loader.dp, on_startup=on_startup)
