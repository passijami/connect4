"""Testit tekoälylle.

Periaate: tekoäly löytää varman voiton, kun sellainen on
olemassa käytetyllä syvyydellä.
"""

import math
from connect4.ai import WIN_SCORE, choose_move, minimax
from connect4.board import Board

def play_moves(board: Board, moves: list[int]) -> None:
    for column in moves:
        board.play(column)

def snapshot(board: Board):
    return (
        [row[:] for row in board.grid],
        board.current_player,
        board.last_move,
        list(board._move_history),
    )

def test_ai_finds_winning_move():
    board = Board()
    # Tekoäly voittaa vuorollaan sarakkeeseen 3.
    play_moves(board, [6, 0, 6, 1, 5, 2, 4])

    value, move = minimax(board, 1, -math.inf, math.inf, True, {})

    assert move == 3
    assert value >= WIN_SCORE

def test_ai_blocks_opponents_immediate_win():
    board = Board()
    # Ihmisellä on alarivissä sarakkeissa 0,1,2. Tekoäly on vuorossa.
    play_moves(board, [0, 6, 1, 6, 2])

    _, move = minimax(board, 2, -math.inf, math.inf, True, {})

    assert move == 3

def test_choose_move_returns_legal_move():
    board = Board()
    for _ in range(6):
        board.play(3)

    move = choose_move(board, time_limit_seconds=0.02)

    assert move in board.legal_moves()

def test_minimax_does_not_mutate_board():
    board = Board()
    play_moves(board, [3, 2, 3, 4, 2])
    before = snapshot(board)

    minimax(board, 4, -math.inf, math.inf, True, {})

    assert snapshot(board) == before

def test_alpha_beta_pruning_produces_cutoffs():
    board = Board()
    play_moves(board, [3, 2, 3, 4, 2, 4])
    stats: dict[str, int] = {}

    minimax(
        board,
        5,
        -math.inf,
        math.inf,
        True,
        {},
        stats=stats,
    )

    assert stats["nodes"] > 0
    assert stats.get("cutoffs", 0) > 0
