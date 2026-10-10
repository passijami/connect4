# Käyttöohje

## Ohjelman asennus

Projekti on toteutettu Pythonilla ja riippuvuuksien hallintaan käytetään Poetrya.

Projektin voi kloonata GitHubista komennolla:

```bash
git clone git@github.com:passijami/connect4.git
```

Siirry tämän jälkeen projektin kansioon:

```bash
cd connect4
```

Asenna projektin riippuvuudet:

```bash
poetry install
```

## Ohjelman käynnistäminen

Peli käynnistetään projektin juuresta komennolla:

```bash
poetry run python src/connect4/cli.py
```

Ohjelma käynnistää tekstipohjaisen Connect4-pelin, jossa ihminen pelaa tekoälyä vastaan.

Ihminen pelaa merkillä `X` ja tekoäly merkillä `O`. Ihminen aloittaa pelin.

Pelilauta näyttää pelin alussa tältä:

```text
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
0 1 2 3 4 5 6
```

Numerot `0-6` tarkoittavat pelilaudan sarakkeita.

## Pelaaminen

Omalla vuorolla ohjelma pyytää valitsemaan sarakkeen:

```text
Valitse sarake (0-6):
```

Pelaajan tulee antaa kokonaisluku väliltä `0-6`.

Esimerkiksi:

```text
Valitse sarake (0-6): 3
```

Tällöin pelaajan merkki pudotetaan sarakkeeseen 3.

Tämän jälkeen tekoäly laskee oman siirtonsa ja tekee sen automaattisesti.

Esimerkiksi:

```text
Tekoäly laskee siirtoa.
Tekoäly valitsee sarakkeen 4.
```

Tekoäly käyttää siirron valintaan minimax-algoritmia, alfa-beta-karsintaa, heuristista arviointia, siirtojen järjestämistä ja iteratiivista syvenemistä.

Tekoälyllä on rajallinen laskenta-aika yhtä siirtoa varten. Haku aloitetaan pienestä hakusyvyydestä ja sitä kasvatetaan niin kauan kuin aikaa on jäljellä. Jos uusi hakukierros ei valmistu aikarajan sisällä, käytetään viimeisen kokonaan valmistuneen kierroksen tulosta.

## Hyväksytyt syötteet

Pelaajan siirron tulee olla kokonaisluku väliltä `0-6`.

Hyväksyttyjä syötteitä ovat esimerkiksi:

```text
0
1
2
3
4
5
6
```

Valitussa sarakkeessa täytyy myös olla tilaa uudelle pelimerkille.

Jos käyttäjä antaa muun kuin kokonaisluvun, ohjelma ilmoittaa virheestä ja pyytää uuden syötteen.

Esimerkiksi:

```text
Valitse sarake (0-6): abc
Sarakkeen numero täytyy olla kokonaisluku.
```

Jos käyttäjä valitsee täyden tai muuten laittoman sarakkeen, ohjelma pyytää valitsemaan uuden sarakkeen.

## Pelin päättyminen

Pelin tavoitteena on saada neljä omaa pelimerkkiä peräkkäin.

Voitto voi muodostua:

- vaakasuoraan
- pystysuoraan
- nousevaan diagonaaliin
- laskevaan diagonaaliin

Kun jompikumpi pelaaja voittaa, ohjelma tulostaa lopullisen pelilaudan ja ilmoittaa voittajan.

Jos kaikki 42 ruutua täyttyvät ilman voittajaa, peli päättyy tasapeliin.

## Testien suorittaminen

Kaikki projektin yksikkötestit voidaan suorittaa komennolla:

```bash
poetry run invoke test
```

Testit testaavat sekä pelilaudan toimintaa että tekoälyn hakualgoritmia.

Testeissä tarkistetaan muun muassa:

- sallittujen siirtojen muodostaminen
- täyden sarakkeen käsittely
- siirron tekeminen ja peruuttaminen
- vaaka-, pysty- ja diagonaalivoitot
- täyden pelilaudan tunnistaminen
- tekoälyn välittömän voittosiirron löytäminen
- vastustajan välittömän voiton estäminen
- tekoälyn palauttaman siirron laillisuus
- minimax-haun pelilaudan tilan säilyminen
- heuristisen arviointifunktion toimintaa
- alfa-beta-karsinnan toimintaa
- alfa-betan ja karsimattoman minimaxin saman lopputuloksen palauttaminen

## Testikattavuus

Testit ja testikattavuusraportti voidaan suorittaa komennolla:

```bash
poetry run invoke coverage
```

Raportissa näkyy sekä rivikattavuus että haarautumakattavuus.

## Pylint

Koodin laatua voidaan tarkistaa Pylintillä:

```bash
poetry run invoke lint
```

Pylint tarkistaa esimerkiksi koodin rakennetta, nimeämistä ja yleisiä Python-tyylin ongelmia.

## Suorituskykytestaus

Minimax- ja alfa-beta-algoritmien suorituskykyä voidaan vertailla erillisellä benchmark-skriptillä:

```bash
poetry run python benchmark.py
```

Benchmark suorittaa saman pelitilanteen haun hakusyvyyksillä `1-7`.

Vertailussa käytetään:

- karsimatonta minimaxia
- alfa-beta-karsinnalla tehostettua minimaxia

Tulosteessa näkyvät seuraavat tiedot:

- `algorithm` = käytetty algoritmi
- `depth` = hakusyvyys
- `best_move` = algoritmin valitsema paras siirto
- `value` = pelitilanteelle laskettu arvo
- `nodes` = tutkittujen pelipuun solmujen määrä
- `cutoffs` = alfa-beta-karsintojen määrä
- `milliseconds` = suoritukseen kulunut aika millisekunteina

Karsimattoman minimaxin ja alfa-beta-haun pitäisi palauttaa samalla hakusyvyydellä sama pelitilanteen arvo ja sama paras siirto.

Alfa-beta-haun pitäisi kuitenkin tutkia erityisesti suuremmilla hakusyvyyksillä selvästi vähemmän pelipuun solmuja.

## Suorituskykykuvaaja

Benchmark muodostaa myös kuvaajan, jossa verrataan karsimattoman minimaxin ja alfa-beta-haun tutkimien solmujen määrää eri hakusyvyyksillä.

Kuvaaja tallennetaan tiedostoon:

```text
docs/benchmark_nodes.png
```

Kuvaajassa x-akselilla on hakusyvyys ja y-akselilla tutkittujen solmujen määrä.

Y-akselissa käytetään logaritmista asteikkoa, koska tutkittujen solmujen määrä kasvaa nopeasti hakusyvyyden kasvaessa.

## Projektin tärkeimmät komennot

Riippuvuuksien asentaminen:

```bash
poetry install
```

Pelin käynnistäminen:

```bash
poetry run python src/connect4/cli.py
```

Yksikkötestien suorittaminen:

```bash
poetry run invoke test
```

Testikattavuuden mittaaminen:

```bash
poetry run invoke coverage
```

Pylint-tarkistus:

```bash
poetry run invoke lint
```

Suorituskykytestauksen suorittaminen:

```bash
poetry run python benchmark.py
```
