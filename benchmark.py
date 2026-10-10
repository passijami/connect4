"""Kevyt suorituskykymittaus minimax ja alfa-beta -haulle.

Aja projektin juuressa:
    poetry run python benchmark.py

Tulosteesta voidaan seurata hakusyvyyden vaikutusta solmujen ja
alfa-beta-karsintojen määrään sekä suoritusaikaan. (Ei yksikkötesti!)
"""

import math
import time
import matplotlib.pyplot as plt
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
    """Vertaa algoritmeja samalla pelitilanteella hakusyvyyksillä 1-7."""
    print("algorithm,depth,best_move,value,nodes,cutoffs,milliseconds")

    depths = []
    minimax_nodes = []
    alpha_beta_nodes = []

    for depth in range(1, 8):
        depths.append(depth)

        for name, runner in (
            ("minimax", run_plain_minimax),
            ("alpha_beta", run_alpha_beta),
        ):
            value, best_move, stats, elapsed_ms = runner(depth)

            nodes = stats.get("nodes", 0)
            cutoffs = stats.get("cutoffs", 0)

            print(
                f"{name},{depth},{best_move},{value},"
                f"{nodes},{cutoffs},{elapsed_ms:.3f}"
            )

            if name == "minimax":
                minimax_nodes.append(nodes)
            else:
                alpha_beta_nodes.append(nodes)

    plt.figure(figsize=(8, 5))

    plt.plot(
        depths,
        minimax_nodes,
        marker="o",
        label="Karsimaton minimax",
    )

    plt.plot(
        depths,
        alpha_beta_nodes,
        marker="o",
        label="Alfa-beta",
    )

    plt.xlabel("Hakusyvyys")
    plt.ylabel("Tutkitut solmut")
    plt.title("Minimaxin ja alfa-beta-haun suorituskyky")

    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("docs/images/benchmark_nodes.png")
    plt.close()


if __name__ == "__main__":
    main()
