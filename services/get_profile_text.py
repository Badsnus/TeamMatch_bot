from models import User
from utils.format_data import format_date_from_timestamp, format_username


def get_profile_text(user: User) -> str:
    return f'''
Профиль | {user.telegram_id}

Имя: {user.name}
Юзернейм: {format_username(user.telegram_username)}
Дата регистрации: {format_date_from_timestamp(user.registration_time)}
    '''
