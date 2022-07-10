# Copyright 2022 Casey Ladtkow

from ast import Pass
import numpy as np
import random


class PuzzleBoard:
    # This class represents the 15 puzzle game board.

    @staticmethod
    def _get_randome_start(rows, cols):
        # This static method creates a game board in a random configuration
        num_tries = 0
        is_valid_board = False
        while not is_valid_board:
            board = np.random.permutation(range(1, rows*cols+1))
            board = np.reshape(board, (rows, cols))

            is_valid_board = PuzzleBoard._is_valid_board(board)

            # This should never be the case but it gards agains an infinite
            # loop. The error is raised because no valid board was found.
            if num_tries > 100:
                raise ValueError('Could not generate a vaid board')
            
            num_tries += 1

        return board

    @staticmethod
    def _is_valid_board(board):
        # This method validates the board.

        # Get information about the permutation
        permutation = board.flatten()
        num_tiles = permutation.shape[0]

        # Make sure the elements of the array are unique
        unique_items = np.unique(board)

        if len(unique_items) != num_tiles:
            return False

        # Calculate the number of move to place the blank where it appears on
        # board
        blank_location = np.where(board == board.shape[0]*board.shape[1])
        moves = (board.shape[0]-1-blank_location[0][0]
                 + (board.shape[1]-1)-blank_location[1][0]
                 )

        # Calculate permutations required to order the board in the final
        # configuration
        num_transpositions = 0
        for num in range(1, num_tiles+1):

            num_idx = np.where(permutation == num)
            num_idx = num_idx[0][0]

            if num_idx+1 != num:
                # Put the number where it belongs
                permutation[[num-1, num_idx]] = permutation[[num_idx, num-1]]
                num_transpositions += 1

        if num_transpositions % 2 != moves % 2:
            return False

        return True

    @staticmethod
    def get_tile_from_board(board, tile):
        # Returns the coordinates of the specified tile

        loc = np.where(board == tile)
        return (loc[0][0], loc[1][0])

    @classmethod
    def get_random_board(cls, size=(4, 4)):
        # Generates a valid randome permutation of the board
        board = PuzzleBoard._get_randome_start(*size)
        return cls(board)

    @classmethod
    def get_completed_board(cls, size=(4, 4)):
        board = np.array(range(1, size[0]*size[1]+1))
        board = np.reshape(board, size)
        return cls(board)

    @classmethod
    def get_this_board(cls, board):
        # Takes a numpy array as imput and ensures that it is a valid state.
        # Returns an instance of PuzzleBoard if the array is valid and errors
        # otherwise.

        if PuzzleBoard._is_valid_board(board):
            return cls(board)
        else:
            raise ValueError('The board you passed is not reachable.')

    def __init__(self, board):
        # The constructor methods above should be used to create new boards
        # but ths __init__ method can be used to create custome boards. Note
        # that it does not check the board validity so it is possible to prank
        # your friends with imposible to solve puzzels.

        self._board = np.copy(board)
        self._move_score = 0

    @property
    def board(self):
        return self._board

    @property
    def score(self):
        # Calculate the score of the current board

        tile_score = 0
        permutation = self.board.flatten()

        for pos, item in enumerate(permutation):
            if item == pos + 1:
                tile_score += 10
            else:
                break

        return tile_score + self._move_score

    def _execute_move(self, blank_loc, tile_loc):
        # Helper function to move tiles and increment score

        (self._board[blank_loc], self.board[tile_loc]
         ) = self._board[tile_loc], self._board[blank_loc]

        self._move_score -= 1

    def move(self, tile):
        # Moves the tile on the board

        # Determine if the tile exists
        if tile not in np.unique(self.board):
            raise ValueError('The tile you requested does not exist')

        # Determine if the tile is adjacent to the blank
        permutation = self._board.flatten()
        num_tiles = permutation.shape[0]

        blank_loc = self.get_tile_loc(num_tiles)

        tile_loc = self.get_tile_loc(tile)

        if(
           np.abs(blank_loc[0]-tile_loc[0])
           + np.abs(blank_loc[1]-tile_loc[1])
           == 1
           ):
            self._execute_move(blank_loc, tile_loc)
        else:
            raise ValueError(f'Tile {tile} not adjacent to the blank tile')

    def move_direction(self, dir):
        # move by direction where 0, 1, 2, 3 represent up, right, left, down

        blank_loc = self.get_tile_loc(self.board.size)

        if dir in self.valid_move_directions:

            if dir == 0:
                tile_loc = (blank_loc[0] - 1, blank_loc[1])
            elif dir == 1:
                tile_loc = (blank_loc[0], blank_loc[1] + 1)
            elif dir == 2:
                tile_loc = (blank_loc[0] + 1, blank_loc[1])
            elif dir == 3:
                tile_loc = (blank_loc[0], blank_loc[1] - 1)

            self._execute_move(blank_loc, tile_loc)

        else:
            self._move_score -= 2  # Trying to move off the board penelty 2

    @property
    def valid_move_directions(self):
        # Returns a list of valid directional moves

        move_directions = []
        blank_loc = self.get_tile_loc(self.board.size)

        move_directions.append(0) if blank_loc[0] > 0 else None
        move_directions.append(1) if blank_loc[1] < 3 else None
        move_directions.append(2) if blank_loc[0] < 3 else None
        move_directions.append(3) if blank_loc[1] > 0 else None

        return move_directions

    @property
    def valid_moves(self):
        # Returns a list of all valid moves
        blank_loc = self.get_tile_loc(self.board.size)

        # Go around the tile clockwise from the 12 o'clock position
        clock_positions = [(blank_loc[0]-1, blank_loc[1]),
                           (blank_loc[0], blank_loc[1]+1),
                           (blank_loc[0]+1, blank_loc[1]),
                           (blank_loc[0], blank_loc[1]-1)
                           ]
        moves = []

        for position in clock_positions:
            if(
                    position[0] >= 0
                    and position[1] >= 0
                    and position[0] <= self._board.shape[0]-1
                    and position[1] <= self._board.shape[1]-1
               ):

                moves.append(self.board[position])

        return moves

    def get_tile_loc(self, tile):
        # Returns the coordinates of the specified tile

        loc = self.get_tile_from_board(self.board, tile)
        return loc

    @property
    def is_complete(self):
        # Returns true if the puzzle is solved

        permutation = self._board.flatten()
        return np.all(permutation[:-1] <= permutation[1:])
