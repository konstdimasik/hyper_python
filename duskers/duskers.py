from ascii_art import welcome_screen, game_hub, robot


class SurvivalGame():
    def __init__(self):
        self._welcome_screen = welcome_screen
        self._game_not_over = True
        self._main_commands = {
            'play': self.ask_for_play,
            'exit': self.exit_game,
            'high': self.high_scores,
            'help': self.help,
            'back': self.run,
        }
        self._play_commands = {
            'yes': self.play,
            'no': self.dont_play,
            'menu': self.run
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
        name = input('Enter your name:\n')
        print(f'Greetings, commander {name}!')
        while True:
            print('Are you ready to begin?')
            print('[Yes] [No] Return to Main[Menu]')
            ready = input('Your command:\n').lower()
            try:
                self.play_commands.get(ready)()
            except TypeError:
                print('Invalid input')

    def play(self) -> None:
        print(game_hub)
        self.finish_game()

    def dont_play(self) -> None:
        print('How about now.')

    def high_scores(self) -> None:
        print('No scores to display.')
        print('[Back]')
        self.run()

    def run(self) -> None:
        print(welcome_screen)
        print('[Play]\n[High] scores\n[Help]\n[Exit]\n')
        while self.game_not_over:
            entry = input('Your command:\n').lower()
            try:
                self.main_commands.get(entry)()
            except TypeError:
                print('Invalid input')


def main():
    game = SurvivalGame()
    game.run()


if __name__ == '__main__':
    main()
