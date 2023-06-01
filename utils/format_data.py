from datetime import datetime, date


def format_username(username: str | None) -> str:
    return f'@{username}' if username else 'Отсутствует'


def format_date_from_timestamp(timestamp: int) -> date:
    return datetime.fromtimestamp(timestamp).date()
