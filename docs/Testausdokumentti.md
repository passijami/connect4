# Testausdokumentti

## Yksikkötestauksen kattavuusraportti

Yksikkötestien kattavuus mitataan `coverage`-työkalulla. Kattavuusraportti voidaan muodostaa komennolla:

```bash
poetry run invoke coverage
```

Lisää tähän viimeisimmän kattavuusajon tulokset:

| Kohde                   | Kattavuus |
| ----------------------- | --------: |
| `src/connect4/ai.py`    |      93 % |
| `src/connect4/board.py` |      95 % |
| `tests/test_ai.py`      |      100 % |
| `tests/test_board.py`   |      100 % |
| Yhteensä                |      96 % |

Nykyisessä viikon 4 versiossa yksikkötestejä on yhteensä 15. Testeillä tarkistetaan sekä pelilaudan toimintaa että tekoälyn hakualgoritmin keskeisiä ominaisuuksia.

Testiajon jälkeen tulokset:

```text
Testejä: 15
Hyväksyttyjä: 15
Hylättyjä: 0
```

Kattavuusprosenttien lisäksi tarkastelen sitä, mitkä ohjelman haarat ja reunatapaukset jäävät vielä testaamatta. Pelkkä korkea kattavuusprosentti ei yksin tarkoita, että algoritmin oikeellisuus olisi riittävästi testattu.

## Mitä ja miten testattu

Käytän testauksessa erilaisia ennalta rakennettuja pelitilanteita, jotta testit eivät perustu vain muutamaan yksinkertaiseen tapaukseen. Testit on suunniteltu siten, että testattavan tilanteen odotettu lopputulos tunnetaan etukäteen.

Projektin nykyiset yksikkötestit voidaan jakaa pelilaudan toimintaa testaaviin testeihin ja tekoälyn toimintaa testaaviin testeihin.

Pelilaudan testeissä tarkistetaan muun muassa, että:

* kaikki sarakkeet ovat sallittuja siirtoja tyhjällä laudalla 
* täyttä saraketta ei hyväksytä sallittuna siirtona
* virheelliset sarakeindeksit hylätään
* siirto voidaan tehdä ja perua oikein
* väärästä sarakkeesta ei voida perua siirtoa
* vaakasuora voitto tunnistetaan
* pystysuora voitto tunnistetaan
* molemmat diagonaaliset voitot tunnistetaan
* laudan reunaan muodostuva neljän suora tunnistetaan oikein

Tekoälyn testeissä tarkistetaan muun muassa, että:

* tekoäly löytää välittömän voittavan siirron
* tekoäly osaa estää vastustajan välittömän voiton
* tekoälyn valitsema siirto on sallittu siirto
* minimax-haku ei muuta alkuperäisen pelilaudan tilaa
* alfa-beta-karsinta tapahtuu haun aikana

Minimax-haun kannalta erityisen tärkeä testi on pelilaudan tilan säilyminen. Hakualgoritmi tekee väliaikaisesti siirtoja `play()`-metodilla ja peruu ne `undo()`-metodilla. Haun jälkeen pelilaudan täytyy olla täsmälleen samassa tilassa kuin ennen hakua.

Alfa-beta-karsinnan toimintaa testataan keräämällä haun aikana tilastotietoa. Testissä tarkistetaan, että tutkittujen solmujen määrä kasvaa ja että haussa syntyy vähintään yksi alfa-beta-karsinta.

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

Suorituskykytestauksessa voidaan myöhemmin vertailla esim. eri hakusyvyyksiä, eri pelitilanteita ja erilaisia algoritmiversioita.

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

| Hakusyvyys | Tutkitut solmut (`nodes`) | Alfa-beta-karsinnat (`cutoffs`) | Aika |
| ---------: | ------------------------: | ------------------------------: | ---: |
|          1 |                         8 |                               0 | 0,024 ms |
|          2 |                         21 |                               6 | 0,045 ms |
|          3 |                         70 |                               12 | 0,123 ms |
|          4 |                         125 |                               60 | 0,272 ms |
|          5 |                         551 |                               75 | 1,006 ms |
|          6 |                         999 |                               481 | 2,227 ms |
|          7 |                         4599 |                               663 | 8,626 ms |

### Suorituskykytestauksen kuvaaja

Empiirisen suorituskykytestauksen tulokset esitetään myös graafisesti.

## Testauksen jatkokehitys

Kun heuristinen arviointifunktio toteutetaan, testejä täydennetään tilanteilla, joissa tarkistetaan esimerkiksi, että:

* tekoälyn kannalta hyvä keskeneräinen pelitilanne saa suuremman arvon kuin huonompi pelitilanne
* vastustajan vaarallinen asema pienentää pelitilanteen arvoa
* kahden ja kolmen oman merkin muodostelmia arvioidaan suunnitellulla tavalla
* tekoäly pystyy löytämään voittoja myös useamman siirron päästä

Lisäksi suorituskykytestausta täydennetään algoritmin kehittyessä niin, että mahdolliset optimoinnit voidaan verrata aiempaan toteutukseen samoilla pelitilanteilla ja hakusyvyyksillä.
