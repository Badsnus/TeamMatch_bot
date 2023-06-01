from aiogram.types import Message

from aiogram.utils.exceptions import MessageCantBeDeleted


async def try_delete_message(message: Message) -> None:
    try:
        await message.delete()
    except MessageCantBeDeleted as _:
        pass
