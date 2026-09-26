# Viikkoraportti 4  

Viime viikolla jäin hieman jälkeen aikataulusta, joten tällä viikolla oli tarkoitus huolehtia siitä, että:
- pelilauta toimii  
- minimax toimii 
- alfa-beta toimii
- tekoäly valitsee siirron
- peliä voi oikeasti pelata AI:ta vastaan.


Testaukset kunnossa:  
- kaikkien suuntien voitot (pysty, vaaka ja risteävät)
- reunassa oleva neljän suora
- täysi sarake
- väärä sarakeindeksi
- play() + undo()
- minimaxin välitön voitto
- vastustajan välittömän voiton blokkaaminen
- tekoälyn palauttaman siirron laillisuus
- minimax ei muuta alkuperäistä lautaa
- alfa-beta tekee karsintoja


Tällä viikolla aloitin yksikkötestejä täydentävän testauksen luomalla benchmark.py-tiedoston, jonka avulla voin testata tekoälyn suorituskykyä. Sen avulla tarkastelen minimax-haun ja alfa-beta-karsinnan toimintaa eri hakusyvyyksillä. Suorituskykytestauksessa seuraan erityisesti kolmea arvoa:  
- tutkittujen solmujen määrää (`nodes`)
- alfa-beta-karsintojen määrää (`prunings`)
- haun suorittamiseen kulunutta aikaa (`time`).

Myöhemmin voidaan vertailla esim. minimax ilman alfa-betaa vs. minimax alfa-betalla.

Päivitin testausdokumenttia sekä aloitin toteutusdokumentin rakentamisen.
