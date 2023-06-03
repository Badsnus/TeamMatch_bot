from loader import bot
from models import User


async def send_message(message: str, user_id: int) -> None:
    user = await User.get(user_id=user_id)

    await bot.send_message(chat_id=user.telegram_id, text=message)
