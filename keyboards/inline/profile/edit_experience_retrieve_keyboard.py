from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.profile import CHANGE_EXPERIENCE_CALLBACK
from models import UserExperience


class EditExperienceRetrieveKeyboard:
    call_prefix = 'edit_experience_retrieve-'

    FIELDS = (
        ('название', UserExperience.name.key),
        ('ссылку', UserExperience.link.key),
        ('описание', UserExperience.description.key),
    )

    @classmethod
    def parse_call_data(cls,
                        call_data: str) -> tuple[str, int]:
        _, field_name, exp_id = call_data.split('-')
        return field_name, int(exp_id)

    @classmethod
    def _generate_call_data(cls,
                            field_name: str,
                            exp_id: int,
                            ) -> str:
        return f'{cls.call_prefix}{field_name}-{exp_id}'

    @classmethod
    def get_keyboard(cls, exp_id: int) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)
        for filed_translate, field_name in cls.FIELDS:
            keyboard.insert(InlineKeyboardButton(
                f'Изменить {filed_translate}',
                callback_data=cls._generate_call_data(field_name, exp_id)
            ))
        keyboard.row(InlineKeyboardButton(
            'Вернуться к опыту',
            callback_data=CHANGE_EXPERIENCE_CALLBACK,
        ))
        return keyboard
