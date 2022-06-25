# Copyright 2022 Casey Ladtkow

from puzzle15 import PuzzleBoard
from colorama import init, Fore, Back, Style
import os
import sys
import time

init()


def main():
    puzzle = PuzzleBoard.get_random_board()
    run = True
    while run:
        print_board(puzzle.board)
        print(Fore.WHITE + f"Score: {puzzle.score}")
        print(Fore.WHITE + "Move the blank to any adjacent number by entering"
              "it here (q to quit):", end='')
        text = input()
        try:
            move = int(text)
        except ValueError as e:
            if text in ['q', 'quit']:
                print(Style.RESET_ALL, end='')
                os.system('cls')
                break
            print(Fore.RED + f'{text} is not a valid move.')
            time.sleep(1)
            continue

        try:
            puzzle.move(move)
            if puzzle.is_complete:
                print_board(puzzle.board)
                print(Fore.GREEN + f'You Win! Score: {puzzle.score}')

                while True:
                    print(Fore.WHITE + "Play Again Y/N:", end='')
                    response = input()
                    if response.lower() == 'y':
                        puzzle = PuzzleBoard.get_random_board()
                        break
                    elif response.lower() == 'n':
                        run = False
                        break
        except ValueError as e:
            print(Fore.RED + str(e))
            time.sleep(1.5)

    return 0


def print_board(board):

    print(Back.BLACK)
    os.system('cls')
    for row in board:
        for col in row:
            if col == board.size:
                print(Back.WHITE + '', end='')
                print(Fore.BLACK, end='')
                print(' '*4, end='')
                print(Back.BLACK + '  ', end='')
            else:

                print(Back.WHITE + '', end='')
                print(Fore.BLACK, end='')
                print('{:>3}'.format(str(col)) + ' ', end='')
                print(Back.BLACK + '  ', end='')

        print(Back.BLACK)        
        print('\r'*2)


if __name__ == '__main__':
    # TODO: Add a fancy QT Quick GUI
    sys.exit(main())
