"""Tekoäly: minimax (alfa-beta-karsinta) + iteratiivinen syveneminen.
"""

import math
import time
from connect4.board import (
    Board,
    COLS,
    EMPTY,
    PLAYER_ONE,
    PLAYER_TWO,
    ROWS,
)

WIN_SCORE = 1000000
CENTER_FIRST = tuple(sorted(range(COLS), key=lambda column: abs(column - COLS // 2)))

# Heuristiikan painot
CENTER_WEIGHT = 5
THREE_WEIGHT = 100
TWO_WEIGHT = 10
OPPONENT_THREE_WEIGHT = 120
OPPONENT_TWO_WEIGHT = 10

class SearchTimeout(Exception):
    """Sisäinen poikkeus, aikarajan täyttynyt haku keskeytetään.  
    """

def choose_move(board: Board, time_limit_seconds: float) -> int:
    """Valitsee parhaan sarakkeen annetulla aikarajalla.

    Haku syvenee yksi taso kerrallaan. Palautettavaksi hyväksytään aina vain
    viimeisen kokonaan valmistuneen hakusyvyyden tulos. Jos aikaraja täyttyy
    kesken syvemmän kierroksen, keskeneräinen tulos hylätään.

    move_order_hint elää vain yhden vuoron ajan. Siihen tallennetaan
    pelitilanteelle aiemmin parhaaksi arvioitu siirto, ei minimax-arvoa.
    """

    legal_moves = board.legal_moves()
    if not legal_moves:
        raise ValueError("Tekoälylle ei ole laillisia siirtoja")

    ordered_legal_moves = _ordered_moves(board, {})
    best_move = ordered_legal_moves[0]

    if time_limit_seconds <= 0:
        return best_move

    deadline = time.monotonic() + time_limit_seconds
    move_order_hint: dict[object, int] = {}
    max_depth = sum(cell == 0 for row in board.grid for cell in row)

    for depth in range(1, max_depth + 1):
        try:
            _, candidate = minimax(
                board=board,
                depth=depth,
                alpha=-math.inf,
                beta=math.inf,
                maximizing=True,
                move_order_hint=move_order_hint,
                deadline=deadline,
            )
        except SearchTimeout:
            break

        if candidate != -1:
            best_move = candidate

        if time.monotonic() >= deadline:
            break

    return best_move


def minimax(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing: bool,
    move_order_hint: dict | None = None,
    deadline: float | None = None,
    stats: dict[str, int] | None = None,
) -> tuple[float, int]:
    """Minimax alfa-beta-karsinnalla, yksi kiinteä syvyys.

    Tekoäly (pelaaja 2) on maksimoiva pelaaja. Pelaaja 1 minimoi arvon.
    Edellisen iteratiivisen syvenemiskierroksen tietoa käytetään vain
    siirtojärjestykseen, ei valmiiden pelitila-arvojen palauttamiseen.

    Args:
        board: nykyinen pelitilanne, play/undo
        depth: jäljellä oleva hakusyvyys
        alpha: Paras tähän asti varmistettu arvo maksimoivalle pelaajalle
        beta: Paras tähän asti varmistettu arvo minimoivalle pelaajalle
        maximizing: onko vuorossa pelaaja jota maksimoidaan
        move_order_hint: edellisen iteraation hajautustaulu siirtojen
            järjestämiseen.
        deadline: Absoluuttinen monotonic-kellon aikaraja. None poistaa aikarajan.
        stats: Valinnainen sanakirja tutkittujen solmujen ja karsintojen laskentaan.

    Returns:
        (arvo, paras_sarake).
    """
    
    _check_deadline(deadline)

    if stats is not None:
        stats["nodes"] = stats.get("nodes", 0) + 1

    if move_order_hint is None:
        move_order_hint = {}
    if depth == 0 or board.is_full():
        return evaluate(board), -1

    moves = _ordered_moves(board, move_order_hint)
    if not moves:
        return 0.0, -1

    position_key = board.position_key()

    if maximizing:
        best_value = -math.inf
        best_move = moves[0]

        for column in moves:
            _check_deadline(deadline)
            board.play(column)
            try:
                if board.check_win():
                    value = WIN_SCORE + depth
                elif board.is_full():
                    value = 0.0
                else:
                    value, _ = minimax(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        False,
                        move_order_hint,
                        deadline=deadline,
                        stats=stats,
                    )
            finally:
                board.undo(column)

            if value > best_value:
                best_value = value
                best_move = column

            alpha = max(alpha, best_value)
            if alpha >= beta:
                if stats is not None:
                    stats["cutoffs"] = stats.get("cutoffs", 0) + 1
                break

    else:
        best_value = math.inf
        best_move = moves[0]

        for column in moves:
            _check_deadline(deadline)
            board.play(column)
            try:
                if board.check_win():
                    value = -(WIN_SCORE + depth)
                elif board.is_full():
                    value = 0.0
                else:
                    value, _ = minimax(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        True,
                        move_order_hint,
                        deadline=deadline,
                        stats=stats,
                    )
            finally:
                board.undo(column)

            if value < best_value:
                best_value = value
                best_move = column

            beta = min(beta, best_value)
            if alpha >= beta:
                if stats is not None:
                    stats["cutoffs"] = stats.get("cutoffs", 0) + 1
                break

    move_order_hint[position_key] = best_move
    return best_value, best_move

def minimax_without_pruning(
    board: Board,
    depth: int,
    maximizing: bool,
    stats: dict[str, int] | None = None,
) -> tuple[float, int]:
    """Karsimaton minimax vertailukohdaksi testeihin ja benchmarkiin.

    Tätä versiota ei käytetä pelin käyttöliittymässä. Käytän tätä vertailukohtana alfa-beta-karsinnan oikeellisuudelle.
    Tarkoitus näyttää, kuinka paljon karsinta vähentää tutkittujen solmujen määrää.
    """
    if stats is not None:
        stats["nodes"] = stats.get("nodes", 0) + 1

    if depth == 0 or board.is_full():
        return evaluate(board), -1

    moves = _ordered_moves(board, {})
    if not moves:
        return 0.0, -1

    if maximizing:
        best_value = -math.inf
        best_move = moves[0]

        for column in moves:
            board.play(column)
            try:
                if board.check_win():
                    value = WIN_SCORE + depth
                elif board.is_full():
                    value = 0.0
                else:
                    value, _ = minimax_without_pruning(
                        board, depth - 1, False, stats
                    )
            finally:
                board.undo(column)

            if value > best_value:
                best_value = value
                best_move = column

        return best_value, best_move

    best_value = math.inf
    best_move = moves[0]

    for column in moves:
        board.play(column)
        try:
            if board.check_win():
                value = -(WIN_SCORE + depth)
            elif board.is_full():
                value = 0.0
            else:
                value, _ = minimax_without_pruning(
                    board, depth - 1, True, stats
                )
        finally:
            board.undo(column)

        if value < best_value:
            best_value = value
            best_move = column

    return best_value, best_move

def evaluate(board: Board) -> float:
    """Arvioi keskeneräisen pelitilanteen pelaajan 2 näkökulmasta.

    Arvioinnissa huomioidaan keskisarakkeen hallinta sekä kaikki neljän ruudun
    ikkunat vaaka-, pysty- ja diagonaalisuunnissa. Kolmen oman merkin ja yhden
    tyhjän ruudun muodostelma saa suuren positiivisen arvon. Vastustajan
    vastaava uhka saa hieman suuremman negatiivisen arvon, jotta tekoäly
    reagoisi herkästi.
    """
    score = 0

    center_column = COLS // 2
    center_values = [board.grid[row][center_column] for row in range(ROWS)]
    score += center_values.count(PLAYER_TWO) * CENTER_WEIGHT
    score -= center_values.count(PLAYER_ONE) * CENTER_WEIGHT

    for row in range(ROWS):
        for column in range(COLS - 3):
            window = board.grid[row][column : column + 4]
            score += _score_window(window)

    for column in range(COLS):
        for row in range(ROWS - 3):
            window = [board.grid[row + offset][column] for offset in range(4)]
            score += _score_window(window)

    for row in range(ROWS - 3):
        for column in range(COLS - 3):
            window = [
                board.grid[row + offset][column + offset]
                for offset in range(4)
            ]
            score += _score_window(window)

    for row in range(3, ROWS):
        for column in range(COLS - 3):
            window = [
                board.grid[row - offset][column + offset]
                for offset in range(4)
            ]
            score += _score_window(window)

    return float(score)


def _score_window(window: list[int]) -> int:
    """Pisteyttää yhden neljän ruudun ikkunan."""
    ai_count = window.count(PLAYER_TWO)
    opponent_count = window.count(PLAYER_ONE)
    empty_count = window.count(EMPTY)

    if ai_count == 4:
        return WIN_SCORE
    if opponent_count == 4:
        return -WIN_SCORE

    score = 0

    if ai_count == 3 and empty_count == 1:
        score += THREE_WEIGHT
    elif ai_count == 2 and empty_count == 2:
        score += TWO_WEIGHT

    if opponent_count == 3 and empty_count == 1:
        score -= OPPONENT_THREE_WEIGHT
    elif opponent_count == 2 and empty_count == 2:
        score -= OPPONENT_TWO_WEIGHT

    return score

def _ordered_moves(board: Board, move_order_hint: dict) -> list[int]:
    """Palauttaa lailliset siirrot keskeltä reunoille, aiempi vihje ensin."""

    legal = set(board.legal_moves())
    moves = [column for column in CENTER_FIRST if column in legal]

    hinted_move = move_order_hint.get(board.position_key())
    if hinted_move in legal:
        moves.remove(hinted_move)
        moves.insert(0, hinted_move)

    return moves


def _check_deadline(deadline: float | None) -> None:
    """Keskeyttää haun, jos annetun aikarajan määräaika on saavutettu."""

    if deadline is not None and time.monotonic() >= deadline:
        raise SearchTimeout
