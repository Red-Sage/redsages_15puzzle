# Copyright 2022 Casey Ladtkow

import numpy as np
import random


class PuzzleBoard:
    # This class represents the 15 puzzle game board.

    @staticmethod
    def _get_randome_start(rows, cols):
        # This static method creates a game board in a random configuration
        num_tries = 0
        is_valid_board = False
        while not is_valid_board and num_tries < 10:
            board = np.random.permutation(range(1, rows*cols+1))
            board = np.reshape(board, (rows, cols))

            is_valid_board = PuzzleBoard._is_valid_board(board)
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

    def __init__(self, board):
        # The constructor methods above should be used to create new boards
        # but ths __init__ method can be used to create custome boards. Note
        # that it does not check the board validity so it is possible to prank
        # your friends with imposible to solve puzzels.

        self._board = board

    @property
    def board(self):
        return self._board

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
            (self._board[blank_loc], self.board[tile_loc]
             ) = self._board[tile_loc], self._board[blank_loc]
        else:
            raise ValueError(f'Tile {tile} not adjacent to the blank tile')

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

        loc = np.where(self._board == tile)
        return (loc[0][0], loc[1][0])

    @property
    def is_complete(self):
        # Returns true if the puzzle is solved

        permutation = self._board.flatten()
        return np.all(permutation[:-1] <= permutation[1:])
