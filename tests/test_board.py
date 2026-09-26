"""Testit Board-luokalle.

Voitontarkistuksen pitää toimia oikein sekä ilmeisissä että
reunatapauksissa.
"""

import pytest
from connect4.board import Board, COLS

def play_moves(board: Board, moves: list[int]) -> None:
    """Testilauta: annettu siirtosarja."""
    for column in moves:
        board.play(column)

def test_empty_board_has_all_legal_moves():
    board = Board()
    assert board.legal_moves() == list(range(COLS))

def test_full_column_is_not_legal():
    board = Board()
    for _ in range(6):
        board.play(0)

    assert 0 not in board.legal_moves()
    with pytest.raises(ValueError):
        board.play(0)

def test_horizontal_win():
    board = Board()
    play_moves(board, [0, 0, 1, 1, 2, 2, 3])
    assert board.check_win()

def test_vertical_win():
    board = Board()
    play_moves(board, [0, 1, 0, 1, 0, 1, 0])
    assert board.check_win()

def test_diagonal_win_rising_to_right():
    board = Board()
    play_moves(board, [0, 1, 1, 2, 4, 2, 2, 3, 4, 3, 5, 3, 3])
    assert board.check_win()

def test_diagonal_win_falling_to_right():
    board = Board()
    play_moves(board, [3, 2, 2, 1, 4, 1, 1, 0, 4, 0, 5, 0, 0])
    assert board.check_win()

def test_undo_restores_board_state():
    board = Board()
    play_moves(board, [3, 2, 3])

    grid_before = [row[:] for row in board.grid]
    player_before = board.current_player
    last_move_before = board.last_move

    board.play(4)
    board.undo(4)

    assert board.grid == grid_before
    assert board.current_player == player_before
    assert board.last_move == last_move_before

def test_undo_rejects_wrong_column():
    board = Board()
    board.play(3)

    with pytest.raises(ValueError):
        board.undo(2)

def test_edge_horizontal_win():
    board = Board()
    play_moves(board, [3, 3, 4, 4, 5, 5, 6])
    assert board.check_win()

def test_invalid_column_raises_value_error():
    board = Board()
    with pytest.raises(ValueError):
        board.play(-1)
    with pytest.raises(ValueError):
        board.play(COLS)
