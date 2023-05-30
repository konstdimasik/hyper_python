from typing import List, Set, Optional


class InvalidAnswerError(Exception):
    pass


class InvalidCardError(Exception):
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

def read_term(num: int, terms: Set[str]) -> str:
    term = input(f"The term for card #{num}:\n")
    while term in terms:
        print(f'The term "{term}" already exists. Try again:')
        term = input()
    terms.add(term)
    return term


def read_definition(num: int, definitions: Set[str]) -> str:
    definition = input(f"The definition for card #{num}:\n")
    while definition in definitions:
        print(f'The definition "{definition}" already exists. Try again:')
        definition = input()
    definitions.add(definition)
    return definition


def read_card(num: int, terms: Set[str], definitions: Set[str]) -> Card:
    term = read_term(num, terms)
    definition = read_definition(num, definitions)

    return Card(term, definition)


def read_cards() -> List[Card]:
    count = int(input("Input the number of cards:\n"))
    cards = []
    card_terms = set()
    card_definitions = set()
    for i in range(1, count + 1):
        card = read_card(i, card_terms, card_definitions)
        cards.append(card)
    return cards


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


def test_user_in_loop(cards: List[Card]) -> None:
    for card in cards:
        answer = read_answer(card.get_term())
        check_answer(card, answer, cards)


def exit_script():
    print("Bye bye!")
    exit()


main_commands = {
    "exit": exit_script,
    "add": read_card,
    "remove": remove_card,
    "import": import_cards,
    "export": export_cards,
    "ask": test_user_in_loop,
}

def main():
    cards = []
    card_terms = set()
    card_definitions = set()



    while True:
        entry = input("Input the action (add, remove, import, export, ask, exit):")

        try:
            main_commands.get(entry)()
        except TypeError:
            print("unknown command!")


if __name__ == '__main__':
    main()
    
