from ascii_art import welcome_screen, robot, hub_top, hub_game, hub_bottom


class GameInterface():
    def __init__(self):
        self._welcome_screen = welcome_screen
        self._game_not_over = True
        self._player_name = ''
        self._main_menu = {
            'play': self.ask_for_play,
            'exit': self.exit_game,
            'high': self.high_scores,
            'help': self.help,
            'back': self.run_main_menu,
        }
        self._are_you_ready_menu = {
            'yes': self.start_the_game,
            'no': self.dont_play,
            'menu': self.run_main_menu,
        }

    def finish_game(self) -> None:
        self._game_not_over = False

    def exit_game(self) -> None:
        print('Thanks for playing, bye!')
        self.finish_game()

    def help(self) -> None:
        print('Coming SOON! Thanks for playing!')
        self.finish_game()

    def ask_for_play(self) -> None:
        self._player_name = input('Enter your name:\n')
        print(f'Greetings, commander {self._player_name}!')
        while self._game_not_over:
            print('Are you ready to begin?')
            print('[Yes] [No] Return to Main[Menu]')
            ready = input('Your command:\n').lower()
            try:
                self._are_you_ready_menu.get(ready)()
            except TypeError:
                print('Invalid input')

    def start_the_game(self) -> None:
        engine = GameEngine(self)
        engine.run_the_game()

    def dont_play(self) -> None:
        print('How about now.')

    def high_scores(self) -> None:
        print('No scores to display.')
        print('[Back]')
        self.run_main_menu()

    def run_main_menu(self) -> None:
        print(welcome_screen)
        print('[Play]\n[High] scores\n[Help]\n[Exit]\n')
        while self._game_not_over:
            entry = input('Your command:\n').lower()
            try:
                self._main_menu.get(entry)()
            except TypeError:
                print('Invalid input')


class GameEngine():
    def __init__(self, interface: GameInterface):
        self._hub_top = hub_top
        self._hub_game = hub_game
        self._hub_bottom = hub_bottom
        self._interface = interface

    def run_the_game(self) -> None:
        self.print_game_hub()
        self._interface.finish_game()

    def print_game_hub(self) -> None:
        print(self._hub_top)
        print(self._hub_game)
        print(self._hub_bottom)


def main():
    game = GameInterface()
    game.run_main_menu()


if __name__ == '__main__':
    main()
