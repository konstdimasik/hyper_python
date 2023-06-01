class InvalidAnswerError(Exception):
    pass


class Card:
    def __init__(self, term: str, definition: str) -> None:
        self._term = term
        self._definition = definition

    def check_answer(self, answer: str) -> None:
        if answer != self._definition:
            raise InvalidAnswerError

    def get_term(self) -> str:
        return self._term

    def get_definition(self) -> str:
        return self._definition
