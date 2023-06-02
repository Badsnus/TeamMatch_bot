def format_username(username: str | None) -> str:
    return f'@{username}' if username else 'Отсутствует'
