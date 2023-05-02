def matrix(inputs):
    counter = 0
    movies = []
    for i in range(3):
        movies.append([])
        for j in range(3):
            movies[i].append(inputs[counter])
            counter += 1
    return movies


def print_game(movies):
    print('---------')
    for i in range(3):
        print('|', end=' ')
        for j in range(3):
            print(movies[i][j], end=' ')
        print('|')
    print('---------')


def is_three(moves, char) -> bool:
    for i in range(3):
        if moves[i][0] == moves[i][1] == moves[i][2] == char:
            return True
    for j in range(3):
        if moves[0][j] == moves[1][j] == moves[2][j] == char:
            return True
    if moves[0][0] == moves[1][1] == moves[2][2] == char:
        return True
    if moves[2][0] == moves[1][1] == moves[0][2] == char:
        return True
    return False


def have_empty(moves) -> bool:
    for i in range(3):
        for j in range(3):
            if moves[i][j] == '_':
                return True


def is_impossible(moves):
    count_x = 0
    count_o = 0
    for i in range(3):
        for j in range(3):
            if moves[i][j] == "X":
                count_x += 1
            elif moves[i][j] == "O":
                count_o += 1
    if abs(count_x - count_o) > 1:
        return True


def analyze_state(moves) -> str:
    if is_three(moves, "O") and is_three(moves, "X") or is_impossible(moves):
        return "Impossible"
    elif not is_three(moves, "O") and not is_three(moves, "X") and have_empty(moves):
        return "Game not finished"
    elif not is_three(moves, "O") and not is_three(moves, "X") and not have_empty(moves):
        return "Draw"
    elif is_three(moves, "O"):
        return "O wins"
    elif is_three(moves, "X"):
        return "X wins"


def ask_for_move(movies):
    while True:
        move = input()
        try:
            x, y = (int(i) for i in move.split(" "))
        except ValueError:
            print("You should enter numbers!")
            continue
        # except Exception:
        #     print("You should enter numbers!")
        #     continue
        else:
            if x < 1 or x > 3 or y < 1 or y > 3:
                print("Coordinates should be from 1 to 3!")
                continue
            if movies[x - 1][y - 1] in ('X', 'O'):
                print("This cell is occupied! Choose another one!")
                continue
        break
    return x, y


def add_move(moves, x, y, switch):
    if switch % 2:
        moves[x - 1][y - 1] = 'X'
    else:
        moves[x - 1][y - 1] = 'O'
    return moves


def main():
    moves = matrix("_________")
    print_game(moves)
    game_over = False
    switch = 1
    while not game_over:
        x, y = ask_for_move(moves)
        moves = add_move(moves, x, y, switch)
        switch += 1
        print_game(moves)
        analysis = analyze_state(moves)
        if analysis != "Game not finished":
            print(analysis)
            game_over = True


if __name__ == '__main__':
    main()
