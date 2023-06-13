import argparse
import datetime
import random
import time
from os import path
from typing import Dict, List

from ascii_art import (
    game_loaded,
    game_saved,
    hub_bottom,
    hub_top,
    paused_menu,
    robot,
    welcome_screen,
)


def ask_for_user_command(command_options: Dict) -> None:
    ready = input('Your command:\n').lower()
    if ready in command_options:
        command_options[ready]()
    else:
        print('Invalid input')


class GameInterface:
    def __init__(self, seed: str, min_duration: int, max_duration: int, locations: str):
        self._welcome_screen = welcome_screen
        random.seed(seed)
        self.game_not_over = True
        self._player_name = ''
        self._main_menu_options = {
            'new': self.ask_for_play,
            'exit': self.exit_game,
            'high': self.high_scores,
            'help': self.help,
            'back': self.run_main_menu,
            'load': self.load_the_game,
        }
        self._commands = {
            'back': self.run_main_menu,
            'menu': self.run_main_menu,
            'exit': self.exit_game,
        }
        self._are_you_ready_menu_options = {
            'yes': self.start_the_game,
            'no': self.dont_play,
            'menu': self.run_main_menu,
        }
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.locations = locations.split(',')
        self._robots = 3
        self._titanium = 0

    def finish_game(self) -> None:
        self.game_not_over = False

    def exit_game(self) -> None:
        print('Thanks for playing, bye!')
        self.finish_game()

    def help(self) -> None:
        print('Coming SOON! Thanks for playing!')
        self.finish_game()

    def ask_for_play(self) -> None:
        self._player_name = input('Enter your name:\n')
        print(f'Greetings, commander {self._player_name}!')
        while self.game_not_over:
            print('Are you ready to begin?')
            print('[Yes] [No] Return to Main[Menu]')
            ask_for_user_command(self._are_you_ready_menu_options)

    def start_the_game(self) -> None:
        engine = GameEngine(
            self.min_duration,
            self.max_duration,
            self.locations,
            self._player_name,
            self._titanium,
            self._robots,
        )
        self._commands[engine.run_the_game()]()

    def dont_play(self) -> None:
        print('How about now.')

    def high_scores(self) -> None:
        print('No scores to display.')
        print('[Back]')
        self.run_main_menu()

    def load_the_game(self) -> None:
        slot_menu = SlotsMenu()
        session = slot_menu.run_load_menu()
        if session:
            session = session.split()
            self._player_name = session[0]
            self._titanium = int(session[2])
            self._robots = int(session[4])
            print(game_loaded)
            print(f'Welcome back, commander {self._player_name}!')
            self.start_the_game()
        self.run_main_menu()

    def run_main_menu(self) -> None:
        print(welcome_screen)
        print('[New]  Game\n[Load] Game\n[High] scores\n[Help]\n[Exit]\n')
        while self.game_not_over:
            ask_for_user_command(self._main_menu_options)


class GameEngine:
    def __init__(
        self,
        min_duration: int,
        max_duration: int,
        locations: List[str],
        name: str,
        titanium: int,
        robots: int,
    ):
        self._continue_the_game = True
        self._engine_state = ''
        self._hub_top = hub_top
        self._hub_bottom = hub_bottom
        self._robots = robots
        self._titanium = titanium
        self._game_menu_options = {
            'ex': self.explore,
            'up': self.upgrade,
            'save': self.save_game,
            'm': self.run_pause_menu,
        }
        self._commands = {
            'back': self.run_the_game,
            'main': self.return_to_main,
            'save_and_exit': self.save_game,
            'exit': self.exit,
        }
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.locations = locations
        self._player_name = name

    def run_the_game(self) -> str:
        self.print_game_hub()
        while self._continue_the_game:
            ask_for_user_command(self._game_menu_options)
        return self._engine_state

    def return_to_main(self) -> None:
        self._engine_state = 'menu'
        self._continue_the_game = False

    def show_titanium(self, titanium) -> str:
        return f'| Titanium: {titanium}                                                                  |'

    def print_game_hub(self) -> None:
        print(self._hub_top)
        print(self.make_robot_hub(self._robots))
        print(self._hub_top)
        print(self.show_titanium(self._titanium))
        print(self._hub_bottom)

    def make_robot_hub(self, robots) -> str:
        lines = robot.split('\n')
        for _ in range(len(lines)):
            lines[_] = '  |  '.join([lines[_]] * robots)
        return '\n'.join(lines)

    def run_pause_menu(self) -> None:
        pause_menu = PauseMenu()
        self._commands[pause_menu.run()]()

    def explore(self) -> None:
        exploration = Explore(self.min_duration, self.max_duration, self.locations)
        explored_titanium = exploration.run_exploration()
        self._titanium += explored_titanium
        self.run_the_game()

    def upgrade(self) -> None:
        print('Coming SOON!')
        self._engine_state = 'exit'
        self._continue_the_game = False

    def save_game(self) -> None:
        slot_menu = SlotsMenu()
        slot_menu.run_save_menu(self._player_name, self._titanium, self._robots)
        self.run_the_game()

    def exit(self) -> None:
        self._engine_state = 'exit'
        self._continue_the_game = False


class PauseMenu:
    def __init__(self):
        self._pause_menu_works = True
        self._pause_menu_state = ''
        self._pause_menu_options = {
            'back': self.back_to_game,
            'main': self.return_to_main_menu,
            'save': self.save_and_exit,
            'exit': self.exit_game,
        }

    def save_and_exit(self) -> None:
        self._pause_menu_works = False
        self._pause_menu_state = 'save_and_exit'

    def back_to_game(self) -> None:
        self._pause_menu_works = False
        self._pause_menu_state = 'back'

    def return_to_main_menu(self) -> None:
        self._pause_menu_works = False
        self._pause_menu_state = 'main'

    def exit_game(self) -> None:
        self._pause_menu_works = False
        self._pause_menu_state = 'exit'

    def run(self) -> str:
        print(paused_menu)
        while self._pause_menu_works:
            ask_for_user_command(self._pause_menu_options)
        return self._pause_menu_state


class Explore:
    def __init__(self, min_duration: int, max_duration: int, locations: List[str]):
        self._exploring = True
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.locations = locations
        self.locations_in_order = {}
        self.max_locations = random.randint(1, 9)
        self.acquired_amount = 0
        self.location_counter = 1
        self._exploration_options = {
            's': self.continue_searching,
            'back': self.back_to_hub,
        }

    def back_to_hub(self) -> None:
        self._exploring = False

    def generate_location(self, locations, max_locations):
        i = 1
        while i <= max_locations:
            yield random.choice(locations)
            i += 1

    def show_next_location(self) -> str:
        generator = self.generate_location(self.locations, self.max_locations)
        try:
            location = next(generator)
        except StopIteration:
            return ''
        return location

    def print_searching_options(self) -> None:
        for key, location in self.locations_in_order.items():
            print(f'[{key}] {location[0]}')
        print()
        print('[S] to continue searching')

    def animate_printing(self, word) -> None:
        print(f'{word}', end='')
        duration = self.min_duration + (self.max_duration - self.min_duration) / self.max_locations
        for _ in range(round(duration)):
            print('.', end='')
            time.sleep(1)
        print()

    def continue_searching(self) -> None:
        if self.location_counter <= self.max_locations:
            self.animate_printing('Searching')
            location = self.show_next_location()
            amount_titanium = random.randint(10, 100)
            self.locations_in_order[str(self.location_counter)] = (location, amount_titanium)
            self.print_searching_options()
            self.location_counter += 1
        else:
            print('Nothing more in sight.')
            print('       [Back]')

    def deploying_robots(self, location: str, amount: int) -> None:
        self.animate_printing('Deploying robots')
        print(f'{location} explored successfully, with no damage taken.')
        print(f'Acquired {amount} lumps of titanium')

    def run_exploration(self) -> str:
        self.continue_searching()
        while self._exploring:
            entry = input('Your command:\n').lower()
            if entry in self._exploration_options:
                self._exploration_options[entry]()
            elif entry in self.locations_in_order:
                location = self.locations_in_order[entry][0]
                self.acquired_amount = self.locations_in_order[entry][1]
                self.deploying_robots(location, self.acquired_amount)
                self._exploring = False
            else:
                print('Invalid input')
        return self.acquired_amount


class SlotsMenu:
    def __init__(self):
        self._slots_menu_works = True
        self.slots = {
            '1': 'empty',
            '2': 'empty',
            '3': 'empty',
        }

    def show_slots_to_select(self) -> None:
        print('\tSelect save slot:')
        for key, session in self.slots.items():
            print(f'\t[{key}] {session}')

    def check_slots_in_backup(self) -> None:
        for slot in range(1, 4):
            filename = 'save_file_' + str(slot) + '.txt'
            if path.isfile(filename):
                session = self.load_game_session_from_file(str(slot))
                self.slots[str(slot)] = session

    def save_game_session_to_file(self, slot: str, name: str, amount: int, robots: int) -> None:
        filename = 'save_file_' + slot + '.txt'  
        with open(filename, 'w', encoding='utf-8') as file_for_export:
            save_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            line = f'{name} Titanium: {amount} Robots: {robots} Last save: {save_time}'
            file_for_export.write(line)
            print(game_saved)

    def run_save_menu(self, name: str, amount: int, robots: int) -> None:
        self.check_slots_in_backup()
        while self._slots_menu_works:
            self.show_slots_to_select()
            entry = input('Your command:\n').lower()
            if entry == 'back':
                self._slots_menu_works = False
            if entry in self.slots:
                self.save_game_session_to_file(entry, name, amount, robots)
                self._slots_menu_works = False
            else:
                print('Invalid input')

    def load_game_session_from_file(self, slot: str) -> str:
        filename = 'save_file_' + slot + '.txt'
        try:
            with open(filename, 'r', encoding='utf-8') as file_for_import:
                return file_for_import.read()

        except FileNotFoundError:
            print('File not found.')

    def run_load_menu(self) -> str:
        self.check_slots_in_backup()
        while self._slots_menu_works:
            self.show_slots_to_select()
            entry = input('Your command:\n').lower()
            if entry == 'back':
                return ''
            if entry in self.slots:
                return self.load_game_session_from_file(entry)
            else:
                print('Invalid input', entry)


def main():
    parser = argparse.ArgumentParser(description="Survival Game options")
    parser.add_argument(
        'seed',
        nargs='?',
        default='',
        type=str,
        help='the seed for random',
    )
    parser.add_argument(
        'min_duration',
        nargs='?',
        default=1,
        type=int,
        help='the minimum duration of animations',
    )
    parser.add_argument(
        'max_duration',
        nargs='?',
        default=5,
        type=int,
        help='the maximum duration of animations',
    )
    parser.add_argument(
        'locations',
        nargs='?',
        default=['Nuclear power plant', 'Old beach bar'],
        type=str,
        help='the names of possible locations',
    )
    args = parser.parse_args()

    game = GameInterface(args.seed, args.min_duration, args.max_duration, args.locations)
    game.run_main_menu()


if __name__ == '__main__':
    main()
