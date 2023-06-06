import pytest
from classcard import Card, InvalidAnswerError


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
