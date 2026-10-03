"""Kevyt suorituskykymittaus minimax ja alfa-beta -haulle.

Aja projektin juuressa:
    poetry run python benchmark.py

Tulosteesta voidaan seurata hakusyvyyden vaikutusta solmujen ja
alfa-beta-karsintojen määrään sekä suoritusaikaan. (Ei yksikkötesti!)
"""

import math
import time
from connect4.ai import minimax, minimax_without_pruning
from connect4.board import Board

def build_position() -> Board:
    """Rakentaa ei-triviaalin pelitilanteen mittaukseen."""
    board = Board()
    for column in [3, 2, 3, 4, 2, 4, 1, 5]:
        board.play(column)
    return board

def run_alpha_beta(depth: int) -> tuple[float, int, dict[str, int], float]:
    """Ajaa alfa-beta-haun ja palauttaa tuloksen sekä mittaustiedot."""
    board = build_position()
    stats: dict[str, int] = {}
    started = time.perf_counter()
    value, best_move = minimax(
        board,
        depth,
        -math.inf,
        math.inf,
        True,
        {},
        stats=stats,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    return value, best_move, stats, elapsed_ms


def run_plain_minimax(depth: int) -> tuple[float, int, dict[str, int], float]:
    """Ajaa karsimattoman minimaxin ja palauttaa mittaustiedot."""
    board = build_position()
    stats: dict[str, int] = {}
    started = time.perf_counter()
    value, best_move = minimax_without_pruning(
        board,
        depth,
        True,
        stats=stats,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    return value, best_move, stats, elapsed_ms


def main() -> None:
    """Mitataan sama pelitilanne hakusyvyyksillä 1-7."""
    print("depth,best_move,value,nodes,cutoffs,milliseconds")

    for depth in range(1, 8):
        for name, runner in (
            ("minimax", run_plain_minimax),
            ("alpha_beta", run_alpha_beta),
        ):
            value, best_move, stats, elapsed_ms = runner(depth)
        print(
            f"{depth},{best_move},{value},"
            f"{stats.get('nodes', 0)},{stats.get('cutoffs', 0)},{elapsed_ms:.3f}"
        )


if __name__ == "__main__":
    main()
