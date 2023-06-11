from ascii_art import welcome_screen, robot, hub_top, hub_bottom, pause_menu


class GameInterface():
    def __init__(self):
        self._welcome_screen = welcome_screen
        self.game_not_over = True
        self._player_name = ''
        self._main_menu_options = {
            'play': self.ask_for_play,
            'exit': self.exit_game,
            'high': self.high_scores,
            'help': self.help,
            'back': self.run_main_menu,
        }
        self._are_you_ready_menu_options = {
            'yes': self.start_the_game,
            'no': self.dont_play,
            'menu': self.run_main_menu,
        }

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
            ready = input('Your command:\n').lower()
            try:
                self._are_you_ready_menu_options.get(ready)()
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
        while self.game_not_over:
            entry = input('Your command:\n').lower()
            try:
                self._main_menu_options.get(entry)()
            except TypeError:
                print('Invalid input')


class GameEngine():
    def __init__(self, main_menu: GameInterface):
        self._hub_top = hub_top
        # self._hub_game = hub_game
        self._hub_bottom = hub_bottom
        self._main_menu = main_menu
        self._game_menu_options = {
            'ex': self.explore,
            'up': self.upgrade,
            'save': self.save_game,
            'm': self.run_pause_menu,
        }

    def run_the_game(self) -> None:
        self.print_game_hub()
        while self._main_menu.game_not_over:
            entry = input('Your command:\n').lower()
            try:
                self._game_menu_options.get(entry)()
            except TypeError:
                print('Invalid input')

    def print_game_hub(self) -> None:
        print(self._hub_top)
        print(self.make_robot_hub())
        print(self._hub_bottom)

    def make_robot_hub(self) -> str:
        lines = robot.split('\n')
        for i in range(len(lines)):
            lines[i] = lines[i] + '  |  ' + lines[i] + '  |  ' + lines[i]
        return '\n'.join(lines)

    def run_pause_menu(self) -> None:
        pause_menu = PauseMenu(self, self._main_menu)
        pause_menu.run()

    def explore(self) -> None:
        print('Coming SOON!')
        self._main_menu.finish_game()

    def upgrade(self) -> None:
        print('Coming SOON!')
        self._main_menu.finish_game()

    def save_game(self) -> None:
        print('Coming SOON!')
        self._main_menu.finish_game()


class PauseMenu():
    def __init__(self, game_engine: GameEngine, main_menu: GameInterface):
        self._main_menu = main_menu
        self._engine = game_engine
        self._pause_menu_options = {
            'back': self._engine.run_the_game,
            'main': self._main_menu.run_main_menu,
            'save': self.save_and_exit,
            'exit': self._main_menu.exit_game,
        }

    def save_and_exit(self) -> None:
        self._engine.save_game()
        self._main_menu.exit_game()

    def run(self) -> None:
        print(pause_menu)
        while self._main_menu.game_not_over:
            entry = input('Your command:\n').lower()
            try:
                self._pause_menu_options.get(entry)()
            except TypeError:
                print('Invalid input')


def main():
    game = GameInterface()
    game.run_main_menu()


if __name__ == '__main__':
    main()
