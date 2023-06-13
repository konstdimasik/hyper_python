import argparse
import random
from typing import Dict, List

from ascii_art import hub_bottom, hub_top, pause_menu, robot, welcome_screen


def ask_for_user_command(command_options: Dict) -> None:
    ready = input('Your command:\n').lower()
    if ready in command_options:
        command_options[ready]()
    else:
        print('Invalid input')


class GameInterface():
    def __init__(self, seed: str, min_dutation: int, max_duration: int, locations: str):
        self._welcome_screen = welcome_screen
        random.seed(seed)
        self.game_not_over = True
        self._player_name = ''
        self._main_menu_options = {
            'play': self.ask_for_play,
            'exit': self.exit_game,
            'high': self.high_scores,
            'help': self.help,
            'back': self.run_main_menu,
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
        self.min_dutation = min_dutation
        self.max_duration = max_duration
        self.locations = locations.split(',')

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
        engine = GameEngine(self.min_dutation, self.max_duration, self.locations)
        self._commands[engine.run_the_game()]()

    def dont_play(self) -> None:
        print('How about now.')

    def high_scores(self) -> None:
        print('No scores to display.')
        print('[Back]')
        self.run_main_menu()

    def run_main_menu(self) -> None:
        print(welcome_screen)
        print('[Play]\n[High] scores\n[Help]\n[Exit]\n')
        while self.game_not_over:
            ask_for_user_command(self._main_menu_options)


class GameEngine():
    def __init__(self, min_dutation: int, max_duration: int, locations: List[str], robots: int = 3, titanium: int = 0):
        self._continue_the_game = True
        self._engine_state = ''
        self._hub_top = hub_top
        self._hub_bottom = hub_bottom
        self._number_of_robots = robots
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
        self.min_dutation = min_dutation
        self.max_duration = max_duration
        self.locations = locations

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
        print(self.make_robot_hub(self._number_of_robots))
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
        exploration = Explore(self.min_dutation, self.max_duration, self.locations)
        result = exploration.run_exploration()
        self._titanium += result
        self.run_the_game()

    def upgrade(self) -> None:
        print('Coming SOON!')
        self._engine_state = 'exit'
        self._continue_the_game = False

    def save_game(self) -> None:
        print('Coming SOON!')
        self._engine_state = 'exit'
        self._continue_the_game = False

    def exit(self) -> None:
        self._engine_state = 'exit'
        self._continue_the_game = False


class PauseMenu():
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
        print(pause_menu)
        while self._pause_menu_works:
            ask_for_user_command(self._pause_menu_options)
        return self._pause_menu_state

class Explore():
    def __init__(self, min_dutation: int, max_duration: int, locations: List[str]):
        self._exploring = True
        self.min_dutation = min_dutation
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

    def generate_location(self, locations, max_locations) -> str:
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
        for key, value in self.locations_in_order.items():
            print(f'[{key}] {value[0]}')
        print()
        print('[S] to continue searching')

    def continue_searching(self) -> None:
        if self.location_counter <= self.max_locations:
            print('Searching')
            location = self.show_next_location()
            amount_titanium = random.randint(10, 100)
            self.locations_in_order[str(self.location_counter)] = (location, amount_titanium)
            self.print_searching_options()
            self.location_counter += 1
        else:
            print('Nothing more in sight.')
            print('       [Back]')

    def deploying_robots(self, location: str, amount: int) -> None:
        print('Deploying robots')
        print(f'{location} explored successfully, with no damage taken.')
        print(f'Acquired {amount} lumps of titanium')


    def run_exploration(self) -> str:
        self.continue_searching() 
        while self._exploring:
            ready = input('Your command:\n').lower()
            if ready in self._exploration_options:
                self._exploration_options[ready]()
            elif ready in self.locations_in_order:
                location = self.locations_in_order[ready][0]
                self.acquired_amount = self.locations_in_order[ready][1]
                self.deploying_robots(location, self.acquired_amount)
                self._exploring = False
            else:
               print('Invalid input')
        return self.acquired_amount

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
