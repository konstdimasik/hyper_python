import sys
from typing import List

import pytest
from classcard import Card, InvalidAnswerError
from flashcards import IO, FlashcardGame


class MyTestIO(IO):
    def __init__(self, msgs: List[str]):
        self.msgs = msgs
        self.output = []

    def input(self, msg: str = '') -> str:
        self.output.append(msg)
        print('inp__', msg, file=sys.stderr)
        return self.msgs.pop(0)

    def print(self, msg: str) -> None:
        print('out__', msg, file=sys.stderr)
        self.output.append(msg)


def test_happy_path():
    test_card = Card("term", "definition")
    try:
        test_card.check_answer("definition")
    except InvalidAnswerError:
        raise AssertionError()


def test_invalid_answer():
    test_card = Card("term", "definition")
    try:
        test_card.check_answer("abracadabra")
    except InvalidAnswerError:
        pass
    else:
        raise AssertionError()


def test_reset_empty():
    msgs = [
        'reset stats',
        'exit',
    ]
    expected_output = [
        'Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n',
        'Card statistics have been reset.',
        'Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n',
        'Bye bye!',
    ]
    testio = MyTestIO(msgs)
    game = FlashcardGame(testio, '', '')
    with pytest.raises(SystemExit):
        game.run()
    if not expected_output == testio.output:
        raise AssertionError
