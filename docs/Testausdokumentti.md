# Testausdokumentti

## Yksikkötestauksen kattavuusraportti

Yksikkötestien kattavuus mitataan `coverage`-työkalulla. Kattavuusraportti voidaan muodostaa komennolla:

```bash
poetry run invoke coverage
```

Lisää tähän viimeisimmän kattavuusajon tulokset:

| Kohde                   | Kattavuus |
| ----------------------- | --------: |
| `src/connect4/ai.py`    |      91 % |
| `src/connect4/board.py` |      98 % |
| `tests/test_ai.py`      |      100 % |
| `tests/test_board.py`   |      100 % |
| Yhteensä                |      95 % |

Nykyisessä viikon 5 versiossa yksikkötestejä on yhteensä 25. Testeillä tarkistetaan sekä pelilaudan toimintaa että tekoälyn hakualgoritmin keskeisiä ominaisuuksia.

Testiajon jälkeen tulokset:

```text
Testejä: 25
Hyväksyttyjä: 25
Hylättyjä: 0
```

Kattavuusprosenttien lisäksi tarkastelen testien sisältöä. Pelkkä korkea kattavuusprosentti ei yksin tarkoita, että algoritmin oikeellisuus olisi riittävästi testattu.

## Mitä ja miten testattu

Käytän testauksessa erilaisia ennalta rakennettuja pelitilanteita, jotta testit eivät perustu vain muutamaan yksinkertaiseen tapaukseen. Testit on suunniteltu siten, että testattavan tilanteen odotettu lopputulos tunnetaan etukäteen.

Projektin nykyiset yksikkötestit voidaan jakaa pelilaudan toimintaa testaaviin testeihin ja tekoälyn toimintaa testaaviin testeihin.

## Pelilauta

`Board`-luokan testeissä tarkistan, että:

- tyhjällä laudalla kaikki seitsemän saraketta ovat sallittuja
- tyhjällä laudalla ei ole voittajaa
- täyttä saraketta ei hyväksytä sallittuna siirtona
- liian pieni ja liian suuri sarakeindeksi hylätään
- siirto voidaan tehdä ja perua niin, että koko pelitila palautuu ennalleen
- väärästä sarakkeesta ei voi perua viimeisintä siirtoa
- tyhjältä laudalta ei voi perua siirtoa
- vaakasuora voitto tunnistetaan
- pystysuora voitto tunnistetaan
- molemmat diagonaaliset voitot tunnistetaan
- laudan reunaan muodostuva neljän suora tunnistetaan
- täysi 42 ruudun lauta tunnistetaan täydeksi
- `position_key()` palautuu samaksi `play()`/`undo()`-parin jälkeen

## Tekoäly

Tekoälyn testeissä tarkistan, että:

- tekoäly löytää välittömän voittavan siirron
- tekoäly estää vastustajan välittömän voiton
- `choose_move()` palauttaa vain laillisen siirron
- ilman laskenta-aikaa valitaan turvallinen keskeltä alkava oletussiirto
- minimax ei muuta alkuperäistä pelilautaa
- alfa-beta-haussa tapahtuu oikeasti karsintoja
- alfa-beta palauttaa samoissa tilanteissa saman arvon ja parhaan siirron kuin karsimaton minimax
- alfa-beta tutkii samalla syvyydellä vähemmän solmuja kuin karsimaton minimax
- heuristiikka suosii tekoälyn keskisarakkeen hallintaa
- heuristiikka palkitsee tekoälyn kolmen merkin muodostelmaa
- heuristiikka rankaisee vastustajan välittömästä kolmen merkin uhasta

Minimax-haun kannalta erityisen tärkeä testi on pelilaudan tilan säilyminen. Hakualgoritmi tekee väliaikaisesti siirtoja `play()`-metodilla ja peruu ne `undo()`-metodilla. Haun jälkeen pelilaudan täytyy olla täsmälleen samassa tilassa kuin ennen hakua.

Alfa-beta-karsinnan toimintaa testataan keräämällä haun aikana tilastotietoa. Testissä tarkistetaan, että tutkittujen solmujen määrä kasvaa ja että haussa syntyy vähintään yksi alfa-beta-karsinta.

Myös benchmark-mittauksessa molemmat algoritmit palauttivat kaikilla testatuilla syvyyksillä saman arvon ja saman parhaan siirron.

## Millaisilla syötteillä testattu

Projektin yksikkötesteillä testaan erityisesti pelilaudan toimintaa ja tekoälyn hakualgoritmia. Tarkoituksena on varmistaa, että yksittäiset metodit toimivat oikein erilaisissa pelitilanteissa ja että myöhemmin tehtävät optimoinnit eivät muuta algoritmin antamia tuloksia.

Pelilaudalla testaan esim. siirtojen tekemistä ja peruuttamista, sallittujen siirtojen tunnistamista sekä voiton tarkistamista. Voitto testataan erikseen vaakasuunnassa, pystysuunnassa ja molemmissa diagonaalisuunnissa. Testeissä huomioin myös laudan reunat.

Tekoälyn testeissä tarkistan esimerkiksi, että tekoäly löytää välittömän voittavan siirron ja osaa estää vastustajan välittömän voiton. Lisäksi testaan, että tekoäly palauttaa vain sallittuja siirtoja ja että minimax-haku ei muuta pelilaudan tilaa haun aikana. Tämä on tärkeää huomioida, sillä hakualgoritmi tekee siirtoja väliaikaisesti `play()`-metodilla ja palauttaa ne `undo()`-metodilla.

Testisyötteet ovat pääasiassa käsin rakennettuja siirtosarjoja. Tämän etuna on se, että jokaisen testitilanteen oikea tulos voidaan määrittää etukäteen.

Esim. voitontarkistuksen testeissä rakennetaan tarkoituksellisesti:

* vaakasuora neljän suora
* pystysuora neljän suora
* nouseva diagonaalinen neljän suora
* laskeva diagonaalinen neljän suora.

Tekoälyn testeissä puolestaan rakennetaan tilanteita, joissa tekoälyllä on yksi tunnettu välitön voittava siirto tai joissa vastustaja voittaisi seuraavalla siirrolla ilman tekoälyn torjuntaa.

Käsin rakennettujen syötteiden avulla voidaan testata juuri haluttua algoritmin ominaisuutta ilman, että testin onnistuminen riippuu satunnaisesti muodostuneesta pelitilanteesta.

Heuristiikan testeissä käytetään keskeneräisiä pelitilanteita. Niiden avulla tarkistetaan, että esim. kolmen merkin muodostelma saa paremman arvion kuin heikompi muodostelma ja että vastustajan vaarallinen asema vaikuttaa arvioon negatiivisesti.

Karsimattoman minimaxin ja alfa-beta-version vertailussa molemmat algoritmit saavat täsmälleen saman lähtötilanteen ja hakusyvyyden. Näin voidaan tarkistaa, että optimointi vähentää tehtävän työn määrää muuttamatta lopputulosta.

## Miten testit toistetaan

Projektin riippuvuudet asennetaan ensin komennolla:

```bash
poetry install
```

Kaikki yksikkötestit voidaan ajaa komennolla:

```bash
poetry run invoke test
```

Yksikkötestit ja niiden kattavuusraportti voidaan ajaa komennolla:

```bash
poetry run invoke coverage
```

Hitaammat ja laajemmat suorituskykymittaukset eivät kuulu normaaliin yksikkötestisarjaan. Ne suoritetaan erillisellä `benchmark.py`-skriptillä:

```bash
poetry run python benchmark.py
```

Benchmark ei kuulu normaaliin yksikkötestisarjaan, koska erityisesti karsimattoman minimaxin suorittaminen suuremmilla hakusyvyyksillä on huomattavasti hitaampaa.

Ohjelman toimintaa voidaan lisäksi testata manuaalisesti käynnistämällä peli:

```bash
poetry run python src/connect4/cli.py
```

Manuaalisessa testauksessa tarkistetaan, että peli käynnistyy, pelaajan ja tekoälyn vuorot vaihtuvat oikein, tekoäly tekee sallittuja siirtoja ja peli voidaan pelata loppuun asti.

## Empiirinen suorituskykytestaus

Projektin suorituskykyä testataan `benchmark.py`-skriptillä. Benchmarkissa minimax-hakua suoritetaan useilla eri hakusyvyyksillä ja hausta kerätään tietoa algoritmin tekemän työn määrästä.

Benchmarkissa seurataan erityisesti seuraavia arvoja:

* `depth` kertoo käytetyn hakusyvyyden
* `best_move` kertoo algoritmin valitseman parhaan siirron
* `value` kertoo pelitilanteelle palautetun minimax-arvon
* `nodes` kertoo tutkittujen pelipuun solmujen määrän
* `cutoffs` kertoo alfa-beta-karsintojen määrän
* `milliseconds` kertoo haun suorittamiseen kuluneen ajan

**`nodes`** on suorituskykyvertailun tärkein mittari. Se kuvaa suoraan, kuinka monta pelitilannetta algoritmin täytyy tutkia.

**`cutoffs`** kertoo alfa-beta-karsinnan toiminnasta. Mitä enemmän karsintaa voidaan tehdä, sitä useampia pelipuun haaroja voidaan jättää tutkimatta ilman, että minimaxin lopullinen tulos muuttuu.

**`milliseconds`** on hyödyllinen täydentävä mittari. Huom! suoritusaikaa ei kuitenkaan pidä tulkita liian tarkasti. Saman algoritmin suorittamiseen käytetty aika voi vaihdella esim. tietokoneen muun kuormituksen vuoksi.

Lisää tähän viimeisimmän `benchmark.py`-ajon tulokset:
| Syvyys | Paras siirto | Arvo | Minimax, solmut | Alfa-beta, solmut | Karsinnat | Minimax aika (ms) | Alfa-beta aika (ms) |
| ------: | -----------: | ---: | ---------------: | -----------------: | --------: | ----------------: | -------------------: |
| 1 | 5 | -30,0 | 8 | 8 | 0 | 0,143 | 0,133 |
| 2 | 5 | -30,0 | 57 | 37 | 4 | 0,871 | 0,499 |
| 3 | 0 | -30,0 | 392 | 213 | 20 | 5,569 | 3,027 |
| 4 | 4 | -60,0 | 2685 | 612 | 110 | 38,825 | 7,887 |
| 5 | 5 | -30,0 | 17755 | 2790 | 475 | 258,914 | 37,535 |
| 6 | 3 | -30,0 | 118645 | 3176 | 1113 | 1735,136 | 34,671 |
| 7 | 0 | -20,0 | 755103 | 18233 | 4386 | 11127,267 | 232,643 |

Ero algoritmien tekemän työn määrässä kasvaa selvästi hakusyvyyden kasvaessa. Syvyydellä 7 karsimaton minimax tutki 755103 pelipuun solmua, kun alfa-beta-haku tutki 18233 solmua.

### Suorituskykytestauksen kuvaaja

Empiirisen suorituskykytestauksen tulokset esitetään myös graafisesti.

## Testauksen jatkokehitys

Yksikkötestit kattavat tällä hetkellä pelilaudan tärkeimmät operaatiot, heuristisen arvioinnin sekä minimax- ja alfa-beta-haun keskeiset oikeellisuusominaisuudet.

Projektin loppuvaiheessa testausta voi vielä täydentää esimerkiksi:

* iteratiivisen syvenemisen aikarajan tarkemmalla testauksella
* eri siirtojärjestysten suorituskykyvertailulla

Lisäksi suorituskykytestausta täydennetään algoritmin kehittyessä niin, että mahdolliset optimoinnit voidaan verrata aiempaan toteutukseen samoilla pelitilanteilla ja hakusyvyyksillä.
