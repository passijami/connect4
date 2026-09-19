"""Yksinkertainen tekstipohjainen käyttöliittymä Connect4:lle.

Ei kuulu ytimeen, ei tarvitse testausta.
"""

from connect4.ai import choose_move
from connect4.board import COLS, Board

SYMBOLS = {0: ".", 1: "X", 2: "O"}


def print_board(board: Board) -> None:
    """Tulostaa laudan yksinkertaisessa muodossa (rivi 0 ylimpänä)."""
    for row in board.grid:
        print(" ".join(SYMBOLS[cell] for cell in row))
    print(" ".join(str(c) for c in range(COLS)))


def main() -> None:
    """Pelisilmukka vuorottelee ihmisen ja tekoälyn siirtoja."""
    board = Board()
    human_turn = True
    while True:
        print_board(board)
        if board.check_win():
            winner = "Ihminen" if human_turn else "Tekoäly"
            print(f"{winner} voitti!")
            break
        if board.is_full():
            print("Tasapeli!")
            break
        if human_turn:
            column = int(input(f"Valitse sarake (0-{COLS - 1}): "))
        else:
            column = choose_move(board, time_limit_seconds=5.0)
            print(f"Tekoäly valitsee sarakkeen {column}")
        board.play(column)
        human_turn = not human_turn


if __name__ == "__main__":
    main()
