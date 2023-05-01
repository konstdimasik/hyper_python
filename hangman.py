import random
from string import ascii_lowercase


def make_hint(hidden_word, guessed_letters):
    hint = ""
    for i in range(len(hidden_word)):
        if hidden_word[i] in guessed_letters:
            hint += hidden_word[i]
        else:
            hint += "-"
    return hint


def check__correct_input(letter) -> bool:
    if len(letter) != 1:
        print("Please, input a single letter.")
        return False
    elif letter not in ascii_lowercase:
        print("Please, enter a lowercase letter from the English alphabet.")
        return False
    else:
        return True


def play():
    words = ["python", "java", "swift", "javascript"]
    hidden_word = random.choice(words)
    guessed_letters = set()
    attempts = 8
    while attempts > 0:
        hint = make_hint(hidden_word, guessed_letters)
        print(f"\n{hint}")
        if hint == hidden_word:
            print(f"You guessed the word {hint}!\nYou survived!")
            return 1
        guess_letter = input("Input a letter:")
        if not check__correct_input(guess_letter):
            continue
        if guess_letter in guessed_letters:
            print("You've already guessed this letter.")
            continue
        guessed_letters.add(guess_letter)
        if guess_letter not in hidden_word:
            print("That letter doesn't appear in the word.")
            attempts -= 1
        if attempts == 0:
            print("You lost!")
            return -1


def main():
    print("H A N G M A N")
    count_win = 0
    count_lost = 0
    while True:
        option = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit')
        if option == 'exit':
            exit()
        elif option == "results":
            print(f'You won: {count_win} times')
            print(f'You lost: {count_lost} times')
        elif option == 'play':
            result = play()
            if result == -1:
                count_lost += 1
            elif result == 1:
                count_win += 1


if __name__ == '__main__':
    main()
