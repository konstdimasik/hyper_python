from random import choice
from typing import List, Optional

from classcard import Card, InvalidAnswerError


class InvalidCardError(Exception):
    pass


class FlashcardGame:
    def __init__(self):
        self.cards = []
        self.card_terms = set()
        self.card_definitions = set()
        self.commands = {
            "exit": self.exit_script,
            "add": self.read_card,
            "remove": self.remove_card,
            "import": self.import_cards,
            "export": self.export_cards,
            "ask": self.test_user_in_loop,
        }

    def read_term(self) -> str:
        term = input("The card:\n")
        while term in self.card_terms:
            print(f'The card "{term}" already exists. Try again:')
            term = input()
        self.card_terms.add(term)
        return term

    def read_definition(self) -> str:
        definition = input("The definition for card:\n")
        while definition in self.card_definitions:
            print(f'The definition "{definition}" already exists. Try again:')
            definition = input()
        self.card_definitions.add(definition)
        return definition

    def add_card(self, term: str, definition: str) -> None:
        self.cards.append(Card(term, definition))
        self.card_terms.add(term)
        self.card_definitions.add(definition)

    def read_card(self) -> None:
        term = self.read_term()
        definition = self.read_definition()
        self.add_card(term, definition)
        print(f'The pair ("{term}":"{definition}") has been added.')
        return None

    def remove_card(self) -> None:
        term = input('Which card?\n')
        card = self.find_card_from_term(term)
        if card is None:
            print(f'Can\'t remove "{term}": there is no such card.')
        else:
            self.card_terms.discard(card.get_term)
            self.card_definitions.discard(card.get_definition)
            self.cards.remove(card)
            print('The card has been removed.')

    def read_answer(self, term: str) -> str:
        answer = input(f'Print the definition of "{term}":\n')
        return answer

    def find_card_from_term(self, term: str) -> Optional[Card]:
        for card in self.cards:
            if term == card.get_term():
                return card
        return None

    def find_term_from_definition(self, definition: str) -> Optional[str]:
        for card in self.cards:
            if definition == card.get_definition():
                return card.get_term()
        return None

    def check_answer(self, card: Card, answer: str, cards: List[Card]) -> None:
        try:
            card.check_answer(answer)
        except InvalidAnswerError:
            right_term = self.find_term_from_definition(answer)
            if right_term is None:
                print(f'Wrong. The right answer is "{card.get_definition()}"')
            else:
                print(f'Wrong. The right answer is "{card.get_definition()}"'
                      f', but your definition is correct for "{right_term}".')
        else:
            print('Correct!')

    def test_user_in_loop(self) -> None:
        question_counter = int(input('How many times to ask?\n'))
        # if len(self.cards) == 0:
        #     print("You don't have cards yet!")
        #     return
        for _ in range(question_counter):
            card = choice(self.cards)
            answer = self.read_answer(card.get_term())
            self.check_answer(card, answer, self.cards)

    def exit_script(self) -> None:
        print("Bye bye!")
        exit()

    def export_cards(self) -> None:
        filename = input("File name:\n")
        with open(filename, 'w', encoding='utf-8') as file_for_export:
            counter = 0
            for card in self.cards:
                file_for_export.write(card.get_term() + ':' + card.get_definition() + '\n')
                counter += 1
        print(f'{counter} cards have been saved.')

    def import_cards(self) -> None:
        filename = input("File name:\n")
        with open(filename, 'r', encoding='utf-8') as file_for_import:
            counter = 0
            for line in file_for_import:
                term, definition = line.strip().split(':')
                self.add_card(term, definition)
                counter += 1
        print(f'{counter} cards have been saved.')

    def run(self) -> None:
        while True:
            entry = input("Input the action (add, remove, import, export, ask, exit):\n")

            try:
                self.commands.get(entry)()
            except TypeError as error:
                print("unknown command!\n", error)


def main():
    game = FlashcardGame()
    game.run()


if __name__ == '__main__':
    main()
