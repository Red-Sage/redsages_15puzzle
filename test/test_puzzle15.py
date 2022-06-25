# Copyright 2022 Casey Ladtkow

import pytest
from puzzle15 import PuzzleBoard
import numpy as np


@pytest.fixture
def test_array_1():
    # Returns an array representing board with the blank near the center
    array = np.array([
                      [1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 16, 12],
                      [13, 14, 11, 15]
                     ])

    return array


@pytest.fixture
def completed_array():
    # Returns an array representing a completed board

    array = np.array([
                      [1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12],
                      [13, 14, 15, 16]
                     ])

    return array


@pytest.fixture
def test_array_2():
    # Returns an array with the 1 tile one move from being complete

    array = np.array([
                      [16, 1, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 2, 12],
                      [13, 14, 11, 15]
                     ])

    return array


@pytest.fixture
def test_array_3():
    # Returns a test array with a score of zero and the blank in the middle

    array = np.array([
                      [2, 1, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 16, 12],
                      [13, 14, 11, 15]
                     ])

    return array


def swap_array_tiles(array, tile1, tile2):
    # This helper function swaps tiles (a.k.a. number in an array)

    loc1 = np.where(array == tile1)
    loc2 = np.where(array == tile2)

    row1 = loc1[0][0]
    col1 = loc1[1][0]
    row2 = loc2[0][0]
    col2 = loc2[1][0]

    array[row1, col1], array[row2, col2] = array[row2, col2], array[row1, col1]

    return array


def test_completed_puzzle_true():
    # Test is_completed is true
    board = PuzzleBoard.get_completed_board()
    assert board.is_complete


def test_completed_puzzle_false():
    # Test is_completed is false
    board = PuzzleBoard.get_random_board()
    assert not board.is_complete


def test_15_14_puzzle():
    # Test that the 15/14 puzzle is correctly rejected

    puzzle_1415 = np.array(range(1, 16+1))
    puzzle_1415 = np.reshape(puzzle_1415, (4, 4))
    puzzle_1415[3, 1], puzzle_1415[3, 2] = puzzle_1415[3, 2], puzzle_1415[3, 1]
    print(puzzle_1415)

    assert not PuzzleBoard._is_valid_board(puzzle_1415)


def test_valid_puzzle(test_array_1):
    # Test that a valid array retruns valid

    assert PuzzleBoard._is_valid_board(test_array_1)


@pytest.mark.parametrize("direction", [[-1, 0], [0, 1], [1, 0], [0, -1]])
def test_valid_move_by_tile_number(direction, test_array_1):
    # Makes the move specified by direction and checks the result

    test_board = test_array_1

    blank_location = np.array([2, 2])
    new_location = blank_location + direction
    new_board = test_board.copy()
    tile_number = test_board[new_location[0], new_location[1]]

    new_board = swap_array_tiles(new_board, tile_number, 16)

    puzzle = PuzzleBoard(test_board)
    puzzle.move(tile_number)

    assert np.all(puzzle.board-new_board == 0)


@pytest.mark.parametrize("bad_move", [1, 6, 15, 100])
def test_invalid_move_not_adjacent(bad_move, test_array_1):
    # Test that invalid moves result in an error

    with pytest.raises(ValueError) as execinfo:
        puzzle = PuzzleBoard(test_array_1)
        puzzle.move(bad_move)


@pytest.mark.parametrize("test_tile", list(range(1, 17)))
def test_tile_loc(test_tile, completed_array):
    # Test to ensure that the location of all tiles is returned

    puzzle = PuzzleBoard(completed_array)

    tiles = np.array(range(1, 17))

    row = np.linspace(0, 3, 4, dtype=np.uint)
    col = row.copy()
    rr, cc = np.meshgrid(row, col, indexing='ij')

    test_tile_idx = np.where(tiles == test_tile)
    test_tile_idx = test_tile_idx[0][0]

    rv = rr.flatten()
    cv = cc.flatten()

    solution = (rv[test_tile_idx], cv[test_tile_idx])

    assert solution == puzzle.get_tile_loc(test_tile)


def test_valid_moves_centered(test_array_1):
    # Test that valid moves are returned correctly

    valid_moves = [7, 12, 11, 10]

    puzzle = PuzzleBoard(test_array_1)

    assert all(val in valid_moves for val in puzzle.valid_moves)


def test_valid_moves_corner(completed_array):
    # Test that valid moves are returned correctly

    valid_moves = [12, 15]

    puzzle = PuzzleBoard(completed_array)

    assert all(val in valid_moves for val in puzzle.valid_moves)


def test_score_1_tile(test_array_2):
    # Test that the score goes to 9 when the 1 tile is moved into place

    puzzle = PuzzleBoard(test_array_2)

    puzzle.move_direction(1)

    assert puzzle.score == 9


def test_score_1_move(test_array_3):
    # Test that one move costs 1 point

    puzzle = PuzzleBoard(test_array_3)

    puzzle.move_direction(0)
    puzzle.move_direction(1)
    puzzle.move_direction(2)
    puzzle.move_direction(3)

    assert puzzle.score == -4


def test_complete_board_score(completed_array):
    # Test that the score is correct when the board is complete

    puzzle = PuzzleBoard(completed_array)

    assert puzzle.score == 160
