# Connect4
Tämä on Helsingin yliopiston Tietojenkäsittelytieteen kandiohjelman Algoritmit ja tekoäly -kurssilla suoritettava projekti, jossa luon Connect4 -pelille tekoälyn hyödyntämällä minimax-algoritmia.

## Ohjelman suorittaminen
Asenna ensin projektin riippuvuudet:

```bash
poetry install
```

Käynnistä peli:
```
poetry run python src/connect4/cli.py
```

Pelissä ihminen (pelaaja 1) pelaa merkillä X ja tekoäly (pelaaja 2) merkillä O.
Pelaaja antaa vuorollaan sarakkeen numeron väliltä 0-6.

## Testit
Aja yksikkötestit:
```
poetry run invoke test
```
Aja testit ja kattavuusraportti:
```
poetry run invoke coverage
```
Aja pylint:
```
poetry run invoke lint
```

## Suorituskykytestaus
Karsimattoman minimaxin ja alfa-beta-haun suorituskykyä vertaillaan komennolla:
```
poetry run python benchmark.py
```
Benchmark suorittaa haut hakusyvyyksillä 1-7, mitataan muun muassa:
* paras löydetty siirto
* pelitilanteen arvo
* tutkittujen solmujen määrä
* alfa-beta-karsintojen määrä
* suoritusaika

Benchmark muodostaa myös suorituskykykuvaajan dokumentaatiota varten.


## Dokumentaatio
[Määrittelydokumentti](docs/Määrittelydokumentti.md)  
[Testausdokumentti](docs/Testausdokumentti.md)  
[Toteutusdokumentti](docs/Toteutusdokumentti.md)

## Viikkoraportit  
[Viikko 1](docs/Viikko1.md)  
[Viikko 2](docs/Viikko2.md)  
[Viikko 3](docs/Viikko3.md)  
[Viikko 4](docs/Viikko4.md)  
[Viikko 5](docs/Viikko5.md)  
[Viikko 6](docs/Viikko6.md)
