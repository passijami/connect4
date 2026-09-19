# Testausdokumentti 
Lisää taulukko (poetry run invoke coverage)   

## Yksikkötestauksen kattavuusraportti


## Mitä ja miten testattu 


## Millaisilla syötteillä testattu  


## Miten testit toistetaan
poetry run invoke test ajaa kaikki yksikkötestit. poetry run invoke coverage ajaa testit ja tulostaa kattavuusraportin. Hitaammat, laajemmat suorituskykymittaukset (syvyys x pelitilanne x algoritmiversio) ovat erillisessä benchmark.py-skriptissä, ei osa yksikkötestisarjaa. Ajetaan erikseen poetry run python benchmark.py.

## Empiirinen suorituskykytestaus
Lisää kuvaaja (benchmark.py)
