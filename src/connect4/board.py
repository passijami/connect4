"""Connect4-pelilaudan logiikka: siirrot, voitontarkistus, tilan hallinta.

Lauta on 6 riviä x 7 saraketta. Sallittujen siirtojen generointi,
voitontarkistus ja siirron suoritus toteutetaan itse.
"""

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2


class Board:
    """Connect4-pelilauta.
 
    Sisäinen esitys self.grid on lista, jossa on ROWS listaa (rivi 0 = ylin rivi),
    kukin pituudeltaan COLS. Arvot: 0 = tyhjä, 1 = pelaaja 1, 2 = pelaaja 2.
    self.current_player kertoo kumman pelaajan vuoro on.
    self.last_move on viimeisin siirto (rivi, sarake) tai None. Tämä on oleellinen  
    tehokkaaseen voitontarkistukseen!
 
    Minimax käyttää samaa Board-oliota koko haun ajan. Siksi siirrot voidaan  
    tehdä play-metodilla ja perua undo-metodilla ilman, että lautaa  
    tarvitsee kopioida jokaisessa hakupuun solmussa.
    """

    def __init__(self) -> None:
        """Alusta tyhjä lauta ja pelaaja 1 aloittajaksi.  
        """
        self.grid = [[EMPTY] * COLS for _ in range(ROWS)]
        self.current_player = PLAYER_ONE
        self.last_move: tuple[int, int] | None = None
        self._move_history: list[tuple[int, int, int]] = []

    def legal_moves(self) -> list[int]:
        """Palauttaa sarakkeet (0..COLS-1), joihin voi pudottaa merkin.

        Lista sarakeindekseistä 0-6. Laillinen sarake, jos ylin ruutu on tyhjä.
        """
        return [column for column in range(COLS) if self.grid[0][column] == EMPTY]


    def play(self, column: int) -> None:
        """Pudottaa vuorossa olevan pelaajan merkin sarakkeeseen.

        Tieto viimeisimmästä siirrosta (rivi, sarake) tarvitaan tehokkaaseen  
        voitontarkistukseen. ValueError, jos sarake on täynnä tai indeksi ei  
        ole laudalla.
        """
        if column < 0 or column >= COLS:
            raise ValueError(f"Sarakkeen täytyy olla välillä 0-{COLS - 1}")

        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][column] == EMPTY:
                player = self.current_player
                self.grid[row][column] = player
                self._move_history.append((row, column, player))
                self.last_move = (row, column)
                self.current_player = self._other_player(player)
                return

        raise ValueError(f"Sarake {column} on täynnä")

    def undo(self, column: int) -> None:
        """Peruuttaa viimeisimmän siirron sarakkeessa.

        Mahdollistaa minimaxin vetäytymisen ilman koko
        laudan kopiointia joka rekursiotasolla.  
        Minimax kutsuu metodeja play(column) ja undo(column) pareittain.  
        Peruuttaminen vain viimeksi pelatulle sarakkeelle. Tämä auttaa havaitsemaan  
        hakualgoritmin ohjelmointivirheet.
        """
        if not self._move_history:
            raise ValueError("Siirtoa ei voi perua tyhjältä laudalta")

        row, last_column, player = self._move_history[-1]
        if column != last_column:
            raise ValueError("Vain viimeisimmän siirron voi perua")

        self._move_history.pop()
        self.grid[row][column] = EMPTY
        self.current_player = player
        self.last_move = (
            self._move_history[-1][0],
            self._move_history[-1][1],
        ) if self._move_history else None

    def check_win(self) -> bool:
        """Onko viimeisin siirto muodostanut nelirivin?

        Tarkista VAIN ne suunnat, jotka kulkevat viimeisimmän siirron  
        ruudun kautta, ei koko laudan läpikäyntiä.  
        True, jos viimeisin siirto muodosti vähintään neljän suoran yhden pelaajan
        merkeillä, muulloin False.
        """
        if self.last_move is None:
            return False

        row, column = self.last_move
        player = self.grid[row][column]
        if player == EMPTY:
            return False

        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for row_delta, col_delta in directions:
            count = 1
            count += self._count_direction(row, column, row_delta, col_delta, player)
            count += self._count_direction(row, column, -row_delta, -col_delta, player)
            if count >= 4:
                return True

        return False

    def is_full(self) -> bool:
        """Palauttaa True, jos laudalle ei mahdu enää yhtään kiekkoa (tasapeli)."""
        return all(self.grid[0][column] != EMPTY for column in range(COLS))

    def position_key(self):
        """Palauttaa muuttumattoman avaimen nykyisestä pelitilanteesta.

        Avainta käytetään tällä viikolla vain iteratiivisen syvenemisen edellisen
        kierroksen parhaan siirron muistamiseen ja siirtojärjestyksen parantamiseen.
        Pelitilan arvoja ei vielä talleteta transpositiotauluun.
        """
        return tuple(tuple(row) for row in self.grid), self.current_player

    @staticmethod
    def _other_player(player: int) -> int:
        """Palauttaa vastustajan pelaajanumeron."""
        return PLAYER_TWO if player == PLAYER_ONE else PLAYER_ONE

    def _count_direction(
        self,
        row: int,
        column: int,
        row_delta: int,
        col_delta: int,
        player: int,
    ) -> int:
        """Laskee peräkkäiset kiekot (yhdeltä pelaajalta) yhteen suuntaan."""
        count = 0
        next_row = row + row_delta
        next_column = column + col_delta

        while (
            0 <= next_row < ROWS
            and 0 <= next_column < COLS
            and self.grid[next_row][next_column] == player
        ):
            count += 1
            next_row += row_delta
            next_column += col_delta

        return count
