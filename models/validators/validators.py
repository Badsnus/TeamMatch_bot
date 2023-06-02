from models.exceptions import ValidationError


class StringValidator:
    def __init__(self, max_length: int = 20, min_length: int = 1) -> None:
        self.max_length = max_length
        self.min_length = min_length

    def is_valid(self, string: str) -> None:
        if not (self.max_length >= len(string) >= self.min_length):
            raise ValidationError
