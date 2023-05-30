from random import choice
from typing import List, Optional


class InvalidAnswerError(Exception):
    pass


class InvalidCardError(Exception):
    pass


class Card:
    cards = []
    card_terms = set()
    card_definitions = set()

    def __init__(self, term: str, definition: str) -> None:
        self._term = term
        self._definition = definition
        Card.cards.append(self)
        Card.card_terms.add(term)
        Card.card_definitions.add(definition)

    def check_answer(self, answer: str) -> None:
        if answer != self._definition:
            raise InvalidAnswerError

    def get_term(self) -> str:
        return self._term

    def get_definition(self) -> str:
        return self._definition


def read_term() -> str:
    term = input("The card:\n")
    while term in Card.card_terms:
        print(f'The card "{term}" already exists. Try again:')
        term = input()
    Card.card_terms.add(term)
    return term


def read_definition() -> str:
    definition = input("The definition for card:\n")
    while definition in Card.card_definitions:
        print(f'The definition "{definition}" already exists. Try again:')
        definition = input()
    Card.card_definitions.add(definition)
    return definition


def read_card() -> None:
    term = read_term()
    definition = read_definition()
    Card(term, definition)
    print(f'The pair ("{term}":"{definition}") has been added.')
    return None


def remove_card() -> None:
    term = input('Which card?\n')
    if term in Card.card_terms:
        Card.card_terms.discard(term)
        print('The card has been removed.')
    else:
        print(f'Can\'t remove "{term}": there is no such card.')


def read_answer(term: str) -> str:
    answer = input(f'Print the definition of "{term}":\n')
    return answer


def find_term(definition: str, cards: List[Card]) -> Optional[str]:
    for card in cards:
        if definition == card.get_definition():
            return card.get_term()
    return None


def check_answer(card: Card, answer: str, cards: List[Card]) -> None:
    try:
        card.check_answer(answer)
    except InvalidAnswerError:
        right_term = find_term(answer, cards)
        if right_term is None:
            print(f'Wrong. The right answer is "{card.get_definition()}"')
        else:
            print(f'Wrong. The right answer is "{card.get_definition()}"'
                f', but your definition is correct for "{right_term}".')
    else:
        print('Correct!')


def test_user_in_loop() -> None:
    question_counter = int(input('How many times to ask?\n'))
    for _ in range(question_counter):
        card = choice(Card.cards)
        answer = read_answer(card.get_term())
        check_answer(card, answer, Card.cards)


def exit_script():
    print("Bye bye!")
    exit()


main_commands = {
    "exit": exit_script,
    "add": read_card,
    "remove": remove_card,
    # "import": import_cards,
    # "export": export_cards,
    "ask": test_user_in_loop,
}


def main():
    while True:
        entry = input("Input the action (add, remove, import, export, ask, exit):\n")

        try:
            main_commands.get(entry)()
        except TypeError as error:
            print("unknown command!\n", error)


if __name__ == '__main__':
    main()
