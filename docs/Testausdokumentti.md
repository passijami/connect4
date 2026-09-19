# Testausdokumentti 
  

## Yksikkötestauksen kattavuusraportti
 Lisää taulukko (poetry run invoke coverage) 

## Mitä ja miten testattu 
Käytän testauksessa erilaisia pelitilanteita, jotta testit eivät perustu vain muutamaan yksinkertaiseen tapaukseen.

## Millaisilla syötteillä testattu  
Projektin yksikkötesteillä testaan erityisesti pelilaudan toimintaa ja tekoälyn hakualgoritmia. Tarkoituksena on varmistaa, että yksittäiset metodit toimivat oikein erilaisissa pelitilanteissa ja että myöhemmin tehtävät optimoinnit eivät muuta algoritmin antamia tuloksia.  

Pelilaudalla testaan esimerkiksi siirtojen tekemistä ja peruuttamista, sallittujen siirtojen tunnistamista sekä voiton tarkistamista. Voitto testataan erikseen vaakasuunnassa, pystysuunnassa ja molemmissa diagonaalisuunnissa. Testeissä huomioin myös laudan reunat.  

Tekoälyn testeissä tarkistan esimerkiksi, että tekoäly löytää välittömän voittavan siirron ja osaa estää vastustajan välittömän voiton. Lisäksi testaan, että tekoäly palauttaa vain sallittuja siirtoja ja että minimax-haku ei muuta pelilaudan tilaa haun aikana. Tärkeä huomioida, sillä hakualgoritmi tekee siirtoja väliaikaisesti play-metodilla ja palauttaa ne undo-metodilla.

## Miten testit toistetaan
poetry run invoke test ajaa kaikki yksikkötestit. poetry run invoke coverage ajaa testit ja tulostaa kattavuusraportin. Hitaammat, laajemmat suorituskykymittaukset (syvyys x pelitilanne x algoritmiversio) ovat erillisessä benchmark.py-skriptissä, ei osa yksikkötestisarjaa. Ajetaan erikseen poetry run python benchmark.py.

## Empiirinen suorituskykytestaus
Lisää kuvaaja (benchmark.py)
