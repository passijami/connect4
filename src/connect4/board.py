"""Connect4-pelilaudan logiikka: siirrot, voitontarkistus, tilan hallinta.

Lauta on 6 riviä x 7 saraketta. Sallittujen siirtojen generointi,
voitontarkistus ja siirron suoritus toteutetaan itse.
"""

ROWS = 6
COLS = 7


class Board:
    """Connect4-pelilauta.
 
    Sisäinen esitys self.grid on lista, jossa on ROWS listaa (rivi 0 = ylin rivi),
    kukin pituudeltaan COLS. Arvot: 0 = tyhjä, 1 = pelaaja 1, 2 = pelaaja 2.
    self.current_player kertoo kumman pelaajan vuoro on.
    self.last_move on (rivi, sarake) tai None. Tämä on oleellinen tehokkaaseen
    voitontarkistukseen!
 
    Käytän aluksi tarkoituksella yksinkertaista listapohjaista esitystä.  
    Jos myöhemmin käy ilmi, että laudan käsittely hidastaa tekoälyn  
    hakua merkittävästi, voin harkita bittilaudan käyttämistä.  
    En kuitenkaan halua optimoida rakennetta ennen kuin siihen on oikeasti tarvetta.
    """

    def __init__(self):
        """Alusta tyhjä lauta ja vuorossa oleva pelaaja.  
        TODO: self.grid = [[0] * COLS for _ in range(ROWS)]
              self.current_player = 1
              self.last_move = None
        """
        raise NotImplementedError

    def legal_moves(self) -> list[int]:
        """Palauttaa sarakkeet (0..COLS-1), joihin voi pudottaa merkin.

        TODO.
        """
        raise NotImplementedError

    def play(self, column: int) -> None:
        """Pudottaa vuorossa olevan pelaajan merkin sarakkeeseen.

        TODO: päivitä myös tieto viimeisimmästä siirrosta (rivi, sarake),
        tarvitaan tehokkaaseen voitontarkistukseen.
        """
        raise NotImplementedError

    def undo(self, column: int) -> None:
        """Peruuttaa viimeisimmän siirron sarakkeessa.

        TODO: tämä mahdollistaa minimaxin vetäytymisen ilman koko
        laudan kopiointia joka rekursiotasolla.
        """
        raise NotImplementedError

    def check_win(self) -> bool:
        """Onko viimeisin siirto muodostanut nelirivin?

        TODO: tarkista VAIN ne suunnat,
        jotka kulkevat viimeisimmän siirron ruudun kautta, ei koko
        laudan läpikäyntiä (ks. Määrittelydokumentti).
        """
        raise NotImplementedError

    def is_full(self) -> bool:
        """Onko peli päättynyt tasapeliin (lauta täynnä)? TODO."""
        raise NotImplementedError
