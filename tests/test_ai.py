"""Testit tekoälylle.

Periaate: tekoäly löytää varman voiton, kun sellainen on
olemassa käytetyllä syvyydellä.
"""

import math
import time
import pytest
from connect4.ai import (
    WIN_SCORE,
    choose_move,
    evaluate,
    minimax,
    minimax_without_pruning,
)
from connect4.board import Board

def play_moves(board: Board, moves: list[int]) -> None:
    """Testilauta annetusta siirtosarjasta"""
    for column in moves:
        board.play(column)

def snapshot(board: Board):
    """Kopio laudan tilasta testeille"""
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
    # Ihmisellä on alarivissä sarakkeissa 0,1,2, kun tekoäly on vuorossa.
    play_moves(board, [0, 6, 1, 6, 2])

    _, move = minimax(board, 2, -math.inf, math.inf, True, {})

    assert move == 3

def test_choose_move_returns_legal_move():
    board = Board()
    for _ in range(6):
        board.play(3)

    move = choose_move(board, time_limit_seconds=0.02)

    assert move in board.legal_moves()

def test_minimax_stops_on_expired_deadline():
    board = Board()
    expired_deadline = time.monotonic() - 1.0

    with pytest.raises(SearchTimeout):
        minimax(
            board,
            4,
            -math.inf,
            math.inf,
            True,
            {},
            deadline=expired_deadline,
        )


def test_choose_move_raises_when_board_is_full():
    board = Board()
    for column in range(7):
        for _ in range(6):
            board.play(column)

    with pytest.raises(ValueError, match="ei ole laillisia siirtoja"):
        choose_move(board, time_limit_seconds=1.0)

def test_choose_move_without_time_uses_center_first_order():
    board = Board()

    move = choose_move(board, time_limit_seconds=0)

    assert move == 3

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

def test_alpha_beta_matches_unpruned_minimax():
    positions = [
        [3, 2, 3, 4],
        [0, 6, 1, 5],
        [3, 3, 2, 4, 2],
        [1, 2, 3, 2, 4],
    ]

    for moves in positions:
        board = Board()
        play_moves(board, moves)

        maximizing = board.current_player == 2
        alpha_beta_value, alpha_beta_move = minimax(
            board,
            4,
            -math.inf,
            math.inf,
            maximizing,
            {},
        )
        plain_value, plain_move = minimax_without_pruning(
            board,
            4,
            maximizing,
        )

        assert alpha_beta_value == plain_value
        assert alpha_beta_move == plain_move


def test_alpha_beta_searches_fewer_nodes_than_plain_minimax():
    board = Board()
    play_moves(board, [3, 2, 3, 4, 2, 4])

    alpha_beta_stats: dict[str, int] = {}
    plain_stats: dict[str, int] = {}

    minimax(
        board,
        5,
        -math.inf,
        math.inf,
        True,
        {},
        stats=alpha_beta_stats,
    )
    minimax_without_pruning(board, 5, True, stats=plain_stats)

    assert alpha_beta_stats["nodes"] < plain_stats["nodes"]


def test_evaluate_prefers_center_control_for_ai():
    center_board = Board()
    play_moves(center_board, [0, 3])

    edge_board = Board()
    play_moves(edge_board, [0, 6])

    assert evaluate(center_board) > evaluate(edge_board)


def test_evaluate_rewards_ai_three_in_a_row():
    strong_board = Board()
    play_moves(strong_board, [6, 0, 6, 1, 5, 2])

    weaker_board = Board()
    play_moves(weaker_board, [6, 0, 5, 1])

    assert evaluate(strong_board) > evaluate(weaker_board)


def test_evaluate_penalizes_opponents_three_in_a_row():
    dangerous_board = Board()
    play_moves(dangerous_board, [0, 6, 1, 6, 2])

    safer_board = Board()
    play_moves(safer_board, [0, 6, 1])

    assert evaluate(dangerous_board) < evaluate(safer_board)

# minimax
def test_minimax_maximizing_selects_highest_child_value(monkeypatch):
    """Maksimoiva taso valitsee lapsista suurimman heuristisen arvon.
    Testaa, että kun minimax on maksimoivan pelaajan vuorossa, se valitsee vaihtoehdoista sen,
    jolla on suurin arvo. Esim. jos siirtojen arvot ovat 10, 20, 30 ja 70,
    minimaxin pitää valita arvo 70."""
    board = Board()
    board.play(6)  # Pelaaja 2 seuraavaksi vuorossa

    values_by_column = {
        0: 10.0,
        1: 20.0,
        2: 30.0,
        3: 70.0,
        4: 40.0,
        5: 50.0,
        6: 60.0,
    }

    def fake_evaluate(test_board: Board) -> float:
        assert test_board.last_move is not None
        return values_by_column[test_board.last_move[1]]

    monkeypatch.setattr("connect4.ai.evaluate", fake_evaluate)

    value, move = minimax(
        board,
        1,
        -math.inf,
        math.inf,
        True,
        {},
    )

    assert move == 3
    assert value == 70.0

def test_minimax_accounts_for_opponents_best_response(monkeypatch):
    """Minimax valitsee siirron parhaan vastustajan vastauksen huomioiden.
    Jos joku siirto näyttää ensin hyvältä mutta vastustaja pystyy vastaamaan siihen niin,
    että lopputulos on huono, minimaxin pitää valita toinen, turvallisempi siirto."""
    board = Board()
    board.play(6)  # Pelaaja 2 (maksimoiva) on seuraavana vuorossa.

    def fake_evaluate(test_board: Board) -> float:
        history = test_board._move_history
        root_move = history[-2][1]
        opponent_response = history[-1][1]

        # Sarake 0 näyttää yleensä erittäin hyvältä,
        # mutta vastustajalla on vastaus, joka tekee siitä huonon.
        if root_move == 0:
            return -100.0 if opponent_response == 6 else 100.0

        # Sarake 1 antaa varmasti arvon +10 riippumatta vastauksesta.
        if root_move == 1:
            return 10.0

        return -50.0

    monkeypatch.setattr("connect4.ai.evaluate", fake_evaluate)

    value, move = minimax(
        board,
        2,
        -math.inf,
        math.inf,
        True,
        {},
    )

    assert move == 1
    assert value == 10.0
