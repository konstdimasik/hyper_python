class InvalidAnswerError(Exception):
    pass


class Card:
    def __init__(self, term: str, definition: str, mistakes: int = 0) -> None:
        self._term = term
        self._definition = definition
        self._mistakes = mistakes

    def check_answer(self, answer: str) -> None:
        if answer != self._definition:
            raise InvalidAnswerError

    def get_term(self) -> str:
        return self._term

    def get_definition(self) -> str:
        return self._definition

    def get_mistakes(self) -> int:
        return self._mistakes

    def set_mistakes(self, mistakes: int) -> None:
        self._mistakes = mistakes

    def increase_mistakes(self) -> None:
        self._mistakes += 1
