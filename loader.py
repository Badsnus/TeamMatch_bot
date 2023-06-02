from asyncio import current_task

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    async_scoped_session,
    create_async_engine,
)

from data import config

bot = Bot(
    disable_web_page_preview=True,
    parse_mode=types.ParseMode.HTML,
    token=config.BOT_TOKEN,
)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
engine = create_async_engine(config.DB_PATH, echo=True)
session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory,
    current_task,
)
