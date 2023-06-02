from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.profile import CHANGE_SKILL_CALLBACK
from models import UserSkill


class DeleteSkillKeyboard:
    TEXT = 'При нажатии на кнопку с скиллом - скилл удалится'
    delete_skill_call = 'profile_skill_delete-'

    @classmethod
    def parse_skill_id_by_callback(cls, callback_data: str) -> int:
        return int(callback_data.replace(cls.delete_skill_call, ''))

    @classmethod
    def _generate_callback(cls, skill_id: int) -> str:
        return cls.delete_skill_call + str(skill_id)

    @classmethod
    def get_keyboard(cls, skills: list[UserSkill]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=4)
        for skill in skills:
            keyboard.insert(InlineKeyboardButton(
                text=skill.name,
                callback_data=cls._generate_callback(skill.id),
            ))
        keyboard.row(InlineKeyboardButton(
            'Вернуться к меню скиллов',
            callback_data=CHANGE_SKILL_CALLBACK,
        ))
        return keyboard
