import pytest
from classcard import Card
from classcard import InvalidAnswerError


def test_happy_path():
	test_card = Card("term", "definition")
	try:
		test_card.check_answer("definition")
	except InvalidAnswerError:
		assert False


def test_invalid_answer():
	test_card = Card("term", "definition")
	try:
		test_card.check_answer("abracadabra")
	except InvalidAnswerError:
		pass
	else:
		assert False
