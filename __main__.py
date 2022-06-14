from puzzle15 import PuzzleBoard
from colorama import init, Fore, Back, Style
import os
import sys
import time

init()

def main():
    puzzle = PuzzleBoard.get_random_board()

    while True:
        os.system('cls')
        print_board(puzzle.board)
        text = input("Move the blank to any adjacent number by entering it here (q to quit):")
        try:
            move = int(text)
        except:
            if text in ['q', 'quit']:
                os.system('cls')
                break
            print(Fore.RED + f'{text} is not a valid move.')
            time.sleep(1)
            continue

        try:
            puzzle.move(move)
            if puzzle.is_complete:
                print(Fore.GREEN + 'You Win!')
                time.sleep(5)
        except ValueError as e:
            print(Fore.RED + str(e))
            time.sleep(1.5)
            
    return 0

def print_board(board):
    row_format = (Back.BLACK + "|" + Back.WHITE + "{:>3}" + Back.BLACK + "|") * board.shape[1]
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

        #row_text = Back.WHITE + row_format.format(*row)
        #print(row_text)
        #print(Back.BLACK + '-'*len(row_text))

if __name__ == '__main__':
    # TODO: Add a fancy QT Quick GUI
    sys.exit(main())
