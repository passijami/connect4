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

def run_alpha_beta(
    depth: int,
    use_transposition_table: bool,
) -> tuple[float, int, dict[str, int], float]:
    """Ajaa alfa-beta-haun valinnaisella transpositiotaululla."""

    board = build_position()
    stats: dict[str, int] = {}
    transposition_table = {} if use_transposition_table else None

    started = time.perf_counter()

    value, best_move = minimax(
        board,
        depth,
        -math.inf,
        math.inf,
        True,
        {},
        stats=stats,
        transposition_table=transposition_table,
        use_transposition_table=use_transposition_table,
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
    print("algorithm,depth,best_move,value,nodes,cutoffs,tt_hits,milliseconds")

    depths = []
    minimax_nodes = []
    alpha_beta_nodes = []
    alpha_beta_tt_nodes = []

    for depth in range(1, 8):
        depths.append(depth)

        results = [
            ("minimax", lambda d: run_plain_minimax(d)),
            ("alpha_beta", lambda d: run_alpha_beta(d, False)),
            ("alpha_beta_tt", lambda d: run_alpha_beta(d, True)),
        ]

        for name, runner in results:
            value, best_move, stats, elapsed_ms = runner(depth)

            nodes = stats.get("nodes", 0)
            cutoffs = stats.get("cutoffs", 0)
            tt_hits = stats.get("tt_hits", 0)

            print(
                f"{name},{depth},{best_move},{value},"
                f"{nodes},{cutoffs},{tt_hits},{elapsed_ms:.3f}"
            )

            if name == "minimax":
                minimax_nodes.append(nodes)
            elif name == "alpha_beta":
                alpha_beta_nodes.append(nodes)
            else:
                alpha_beta_tt_nodes.append(nodes)

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

        plt.plot(
        depths,
        alpha_beta_tt_nodes,
        marker="o",
        label="Alfa-beta + transpositiotaulu",
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

    import os
    os.startfile("docs/images/benchmark_nodes.png")


if __name__ == "__main__":
    main()
