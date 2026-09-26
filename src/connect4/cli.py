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

def _read_human_move(board: Board) -> int:
    """Pyytää käyttäjältä laillisen sarakkeen."""
    while True:
        raw_value = input(f"Valitse sarake (0-{COLS - 1}): ")
        try:
            column = int(raw_value)
        except ValueError:
            print("Sarakkeen numero täytyy olla kokonaisluku.")
            continue

        if column not in board.legal_moves():
            print("Sarakkeeseen ei käytössä, valitse toinen.")
            continue

        return column

def main() -> None:
    """Pelisilmukka vuorottelee ihmisen ja tekoälyn siirtoja.  
    Ihminen on X, tekoäly 0."""
    board = Board()
    print("Connect4: sinä olet X, tekoäly on O.")
    print("Ensimmäisenä neljä omaa merkkiä riviin saanut voittaa.\n")

    while True:
        print_board(board)
        current_player = board.current_player

        if current_player == 1:
            column = _read_human_move(board)
        else:
            print("Tekoäly laskee siirtoa.")
            column = choose_move(board, time_limit_seconds=2.0)
            print(f"Tekoäly valitsee sarakkeen {column}.")

        board.play(column)

        if board.check_win():
            print_board(board)
            winner = "Ihminen" if human_turn else "Tekoäly"
            print(f"{winner} voitti!")
            break
        if board.is_full():
            print("Tasapeli!")
            break


if __name__ == "__main__":
    main()
