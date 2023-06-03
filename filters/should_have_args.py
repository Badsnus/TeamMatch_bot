from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ShouldHaveArgs(BoundFilter):
    key = 'have_args'

    def __init__(self, should_have=False) -> None:
        self.should_have = should_have

    async def check(self, message: types.Message) -> bool:
        return bool(message.get_args()) == self.should_have
