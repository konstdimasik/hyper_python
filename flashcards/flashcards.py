import logging
import argparse
from shutil import copyfile
from random import choice
from typing import List, Optional

from classcard import Card, InvalidAnswerError


class InvalidCardError(Exception):
    pass


class FlashcardGame:
    def __init__(self, import_from: str, export_to: str):
        self.import_from = import_from
        self.export_to = export_to
        self.cards = []
        self.card_terms = set()
        self.card_definitions = set()
        self.commands = {
            "exit": self.exit_script,
            "add": self.read_card,
            "remove": self.remove_card,
            "import": self.ask_import_filename,
            "export": self.ask_export_filename,
            "ask": self.test_user_in_loop,
            "log": self.save_log,
            "hardest card": self.hardest_card,
            "reset stats": self.reset_stats,
        }
        logger = logging.getLogger('FlashcardGame')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler('flashcardgame.log', 'w')
        log_formatter = logging.Formatter('%(message)s')
        fh.setFormatter(log_formatter)
        logger.addHandler(fh)
        self.logger = logger

    def input(self, msg: str = '') -> str:
        self.logger.info(msg.strip())
        return input(msg)

    def print(self, msg: str) -> None:
        self.logger.info(msg)
        print(msg)

    def read_term(self) -> str:
        term = self.input("The card:\n")
        self.logger.info(term)
        while term in self.card_terms:
            self.print(f'The card "{term}" already exists. Try again:')
            term = self.input()
        self.card_terms.add(term)
        return term

    def read_definition(self) -> str:
        definition = self.input("The definition for card:\n")
        self.logger.info(definition)
        while definition in self.card_definitions:
            definition = self.input(f'The definition "{definition}" already exists. Try again:')
            self.logger.info(definition)
        self.card_definitions.add(definition)
        return definition

    def add_card(self, term: str, definition: str, mistakes: int = 0) -> None:
        self.cards.append(Card(term, definition, mistakes))
        self.card_terms.add(term)
        self.card_definitions.add(definition)

    def read_card(self) -> None:
        term = self.read_term()
        definition = self.read_definition()
        self.add_card(term, definition)
        self.print(f'The pair ("{term}":"{definition}") has been added.')
        return None

    def remove_card(self) -> None:
        term = self.input('Which card?\n')
        self.logger.info(term)
        card = self.find_card_from_term(term)
        if card is None:
            self.print(f'Can\'t remove "{term}": there is no such card.')
        else:
            self.card_terms.discard(card.get_term)
            self.card_definitions.discard(card.get_definition)
            self.cards.remove(card)
            self.print('The card has been removed.')

    def read_answer(self, term: str) -> str:
        answer = self.input(f'Print the definition of "{term}":\n')
        self.logger.info(answer)
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

    def check_answer(self, card: Card, answer: str) -> None:
        try:
            card.check_answer(answer)
        except InvalidAnswerError:
            right_term = self.find_term_from_definition(answer)
            card.increase_mistakes()
            if right_term is None:
                self.print(f'Wrong. The right answer is "{card.get_definition()}"')
            else:
                self.print(f'Wrong. The right answer is "{card.get_definition()}"'
                      f', but your definition is correct for "{right_term}".')
        else:
            self.print('Correct!')

    def test_user_in_loop(self) -> None:
        question_counter = int(self.input('How many times to ask?\n'))
        self.logger.info(question_counter)
        if len(self.cards) == 0:
            self.print("You don't have cards yet!")
            return
        for _ in range(question_counter):
            card = choice(self.cards)
            answer = self.read_answer(card.get_term())
            self.check_answer(card, answer)

    def exit_script(self) -> None:
        self.print("Bye bye!")
        if self.export_to:
            self.export_cards(self.export_to)
        exit()
    def ask_export_filename(self) -> None:
        filename = self.input("File name:\n")
        self.logger.info(filename)
        self.export_cards(filename)

    def export_cards(self, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as file_for_export:
            counter = 0
            for card in self.cards:
                line = ':'.join([card.get_term(), card.get_definition(), str(card.get_mistakes())])
                file_for_export.write(line + '\n')
                counter += 1
        self.print(f'{counter} cards have been saved.')

    def delete_card(self, term: str) -> None:
        card = self.find_card_from_term(term)
        self.card_terms.discard(card.get_term)
        self.card_definitions.discard(card.get_definition)
        self.cards.remove(card)

    def ask_import_filename(self) -> None:
        filename = self.input("File name:\n")
        self.logger.info(filename)
        self.import_cards(filename)

    def import_cards(self, filename: str) -> None:
        try:
            with open(filename, 'r', encoding='utf-8') as file_for_import:
                counter = 0
                for line in file_for_import:
                    term, definition, mistakes = line.strip().split(':')
                    if term in self.card_terms:
                        self.delete_card(term)
                    self.add_card(term, definition, int(mistakes))
                    counter += 1
            self.print(f'{counter} cards have been loaded.')
        except FileNotFoundError:
            self.print('File not found.')

    def compose_hardest_message(self, terms: List[str], mistakes: int) -> str:
        if mistakes == 0:
            return 'There are no cards with errors.'
        elif mistakes == 1:
            error_word = 'error'
        else:
            error_word = 'errors'
        if len(terms) == 1:
            return f'The hardest card is "{terms[0]}". You have {mistakes} {error_word} answering it.'
        terms = ['"' + x + '"' for x in terms]
        hardest_terms = ', '.join(terms)
        return f'The hardest cards are "{hardest_terms}. You have {mistakes} {error_word} answering them.'

    def hardest_card(self) -> None:
        hardest_cards = []
        max_mistakes = 0        
        for card in self.cards:
            card_mistakes = card.get_mistakes()
            if card_mistakes > max_mistakes:
                hardest_cards = [card.get_term()]
                max_mistakes = card_mistakes
            elif card_mistakes == max_mistakes:
                hardest_cards.append(card.get_term())
        message = self.compose_hardest_message(hardest_cards, max_mistakes)
        self.print(message)

    def reset_stats(self) -> None:
        for card in self.cards:
            card.set_mistakes(0)
        self.print('Card statistics have been reset.')

    def save_log(self) -> None:
        filename = self.input("File name:\n")
        self.logger.info(filename)
        copyfile('flashcardgame.log', filename)
        self.print('The log has been saved.')

    def run(self) -> None:
        if self.import_from:
            self.import_cards(self.import_from)
        while True:
            entry = self.input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)\n")

            try:
                self.commands.get(entry)()
            except TypeError:
                self.print("unknown command!\n")


def main():
    parser = argparse.ArgumentParser(description="Flashcard Game")
    parser.add_argument(
        '--import_from',
        default='',
        type=str,
        help='file name to read the initial card set from'
    )
    parser.add_argument(
        '--export_to',
        default='',
        type=str,
        help='file name to write all cards when finish the game'
    )
    args = parser.parse_args()

    game = FlashcardGame(args.import_from, args.export_to)
    game.run()


if __name__ == '__main__':
    main()
