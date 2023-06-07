from welcome_art import welcome_screen


class SurvivalGame():
    def __init__(self):
        self.welcome_screen = welcome_screen
        self.main_commands = {
            'play': self.ask_for_play,
            'exit': self.exit_game,
        }
        self.play_commands = {
            'yes': self.play,
            'no': self.dont_play,
        }

    def exit_game(self) -> None:
        print('Thanks for playing, bye!')
        exit()

    def ask_for_play(self) -> None:
        name = input('Enter your name:\n')
        print(f'Greetings, commander {name}!')
        while True:
            print('Are you ready to begin?')
            print('    [Yes] [No]')
            ready = input('Your command:\n').lower()
            try:
                self.play_commands.get(ready)()
            except TypeError:
                print('Invalid input')

    def play(self) -> None:
        print("Great, now let's go code some more ;)")
        exit()

    def dont_play(self) -> None:
        print('How about now.')

    def run(self) -> None:
        print(welcome_screen)
        print('\t[Play]\n\t[Exit]\n')
        while True:
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
