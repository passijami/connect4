# Toteutusdokumentti

Tässä kerron, miten Connect4-tekoälyni toimii tällä hetkellä ja mihin ratkaisuihin olen päätynyt.

## Ohjelman yleisrakenne

Ohjelma jakautuu kolmeen osaan:

1. `board.py` vastaa Connect4:n säännöistä ja pelitilan hallinnasta.
2. `ai.py` on projektin ydin ja hakee pelipuuta minimax-algoritmilla ja alfa-beta-karsinnalla.
3. `cli.py` on kevyt tekstikäyttöliittymä, jonka kautta pääsee pelaamaan tekoälyä vastaan.

Pelilauta on 6x7 Python-lista, jossa 0 on tyhjä ruutu, 1 pelaaja 1 ja 2 pelaaja 2. Pidin esityksen tietoisesti yksinkertaisena, koska monimutkaisempi ratkaisu (esimerkiksi bittilauta) olisi tuonut lisää työtä virheiden etsimisessä. Minimax ei kopioi koko lautaa jokaisella rekursiotasolla, vaan tekee siirron `play`-metodilla ja perii sen `undo`-metodilla. Board pitää kirjaa siirtohistoriasta, jotta myös `last_move` ja vuorossa oleva pelaaja palautuvat oikein.

## Minimax

Minimax rakentaa pelipuuta mahdollisista tulevista siirroista. Omalla vuorolla tekoäly valitsee suurimman arvon ja vastustajan vuorolla pienimmän. Ajatuksena on, että kumpikin pelaaja tekee omalta kannaltaan parhaan mahdollisen siirron.

Voittava siirto saa suuren positiivisen arvon ja häviävä suuren negatiivisen arvon. Pisteeseen lisätään jäljellä oleva hakusyvyys, jolloin tekoäly suosii nopeampaa voittoa ja pyrkii lykkäämään väistämätöntä häviötä mahdollisimman pitkälle.

Syvyysrajan saavuttanut keskeneräinen pelitilanne arvioidaan heuristisella `evaluate()`-funktiolla.

## Heuristinen arviointi

Viikolla 5 lisäsin varsinaisen heuristisen arvioinnin. Arviointi tehdään tekoälyn eli pelaajan 2 näkökulmasta.

Heuristiikka huomio:  
- keskisarakkeen hallinnan
- kaikki neljän ruudun ikkunat

Keskisarakkeessa olevista tekoälyn merkeistä saa lisäpisteitä, koska keskellä oleva merkki kuuluu todennäköisemmin useampaan mahdolliseen neljän suoraan kuin reunassa oleva merkki.

Haluan saada tekoälyn reagoimaan välittömiin uhkiin riittävän voimakkaasti. Siitä johtuen neljän ruudun ikkunoissa pisteytän erityisesti kahden ja kolmen oman merkin muodostelmia. Sen lisäksi vastustajan kolmen merkin ja yhden tyhjän ruudun uhka saa hieman suuremman negatiivisen painon kuin oma vastaava muodostelma positiivisen painon.

Heuristiikan ei ole tarkoitus ratkaista pelitilannetta täydellisesti. Sen tehtävä on järjestää syvyysrajalle jäävät tilanteet riittävän järkevään paremmuusjärjestykseen.

## Alfa-beta-karsinta

Minimax pitää yllä kahta rajaa:

- `alpha`: paras arvo, jonka maksimoiva pelaaja voi tähän mennessä varmasti saavuttaa.
- `beta`: paras arvo, jonka minimoiva pelaaja voi tähän mennessä varmasti saavuttaa.

Kun `alpha >= beta`, loput saman solmun haarat voi jättää tutkimatta, koska ne eivät voi enää muuttaa ylemmän tason päätöstä. Karsinta ei vaikuta minimaxin lopputulokseen mitenkään. Se vain vähentää tutkittavien pelitilojen määrää.

Karsinnan pitäisi muuttaa vain tutkittujen solmujen määrää, ei minimaxin lopullista arvoa. Tämän vuoksi projektissa on nyt myös erillinen `minimax_without_pruning()`-vertailutoteutus. Sitä ei käytetä varsinaisessa pelissä, vaan testeissä ja benchmarkissa alfa-beta-haun oikeellisuuden ja tehokkuuden tarkistamiseen.

Siirrot käydään oletuksena läpi keskisarakkeesta reunoja kohti. Connect4:ssa keskisarakkeet osallistuvat useampaan mahdolliseen neljän suoraan, joten tämä järjestys löytää usein hyviä siirtoja aikaisemmin ja parantaa alfa-beta-karsinnan tehokkuutta. Pelitilalle tallennetaan vain paras siirto, ei sen minimax-arvoa. Aiempi siirto kokeillaan seuraavalla kierroksella ensin.

## Iteratiivinen syveneminen

`choose_move` hakee vastausta syvyyksillä 1, 2, 3... niin pitkälle kuin aikaraja sallii. Jos jokin syvyys jää kesken, sen tulosta ei käytetä. Siten tekoälyllä on aina käytettävissään viimeisen kokonaan lasketun syvyyden paras löydetty siirto, oli aikaa käytettävissä kuinka paljon tahansa.

## Aika- ja tilavaativuus

Ilman karsintaa minimaxin aikavaativuus on `O(b^d)`, missä `b` on haarautumiskerroin (Connect4:ssa enintään 7) ja `d` hakusyvyys. Alfa-beta-karsinnan pahin tapaus on periaatteessa yhä `O(b^d)`, mutta hyvällä siirtojärjestyksellä päästään käytännössä lähelle `O(b^(d/2))`.

Hakurekursio käyttää vain `O(d)` lisätilaa, koska lautaa ei kopioida jokaiseen puun solmuun. Siirtojärjestyksen vihjesanakirja vie hieman muistia niiltä pelitiloilta jotka siihen tallennetaan, mutta se sisältää vain parhaan siirron, ei valmiita minimax-arvoja, jotka veisivät huomattavasti enemmän tilaa ja joita ei muutenkaan voisi luotettavasti käyttää uudestaan.

Heuristisen arvioinnin työmäärä on vakio suhteessa hakusyvyyteen, koska Connect4-laudan koko on aina 6x7. Käytännössä `evaluate()` käy läpi kaikki neljän ruudun ikkunat kiinteän kokoisella laudalla.

## Suorituskykyvertailu
Projektin `benchmark.py` vertaa karsimatonta minimaxia ja alfa-beta-hakua täsmälleen samassa pelitilanteessa ja samoilla hakusyvyyksillä:

| Syvyys | Paras siirto | Arvo | Minimax, solmut | Alfa-beta, solmut | Karsinnat | Minimax aika (ms) | Alfa-beta aika (ms) |
| ------: | -----------: | ---: | ---------------: | -----------------: | --------: | ----------------: | -------------------: |
| 1 | 5 | -30.0 | 8 | 8 | 0 | 0.143 | 0.133 |
| 2 | 5 | -30.0 | 57 | 37 | 4 | 0.871 | 0.499 |
| 3 | 0 | -30.0 | 392 | 213 | 20 | 5.569 | 3.027 |
| 4 | 4 | -60.0 | 2685 | 612 | 110 | 38.825 | 7.887 |
| 5 | 5 | -30.0 | 17755 | 2790 | 475 | 258.914 | 37.535 |
| 6 | 3 | -30.0 | 118645 | 3176 | 1113 | 1735.136 | 34.671 |
| 7 | 0 | -20.0 | 755103 | 18233 | 4386 | 11127.267 | 232.643 |

Ero tutkittujen solmujen määrässä kasvaa selvästi hakusyvyyden mukana.
Syvyydellä 7 tavallinen minimax tutki 755103 solmua, kun alfa-beta-haku
tutki 18233 solmua. Myös suoritusaika pieneni samalla mittauksella noin
11,1 sekunnista 0,23 sekuntiin.

## Nykyiset puutteet ja seuraavat parannukset

Tekoälyn ydintoiminta on nyt valmis kurssin vaatimusten kannalta, mutta toteutusta voisi vielä kehittää.
Nykyiset tärkeimmät rajoitteet ovat:
- heuristiikan painot ovat itse valittuja eikä niitä ole vielä systemaattisesti viritetty
- tekoäly on käyttöliittymässä aina pelaaja 2
- käytössä ei ole varsinaista transpositiotaulua, joka tallentaisi tarkkoja arvoja sekä ylä- ja alarajoja
- lauta on tavallinen Python-lista eikä bittilauta.

Jos aikaa jää, seuraava järkevä kehityskohde olisi mitata eri siirtojärjestysten ja heuristiikan painojen vaikutusta samoilla testiasemilla. Bittilautaan siirtymistä en pidä tällä hetkellä tarpeellisena, koska nykyinen rakenne on selkeä ja suorituskyvyn mahdolliset pullonkaulat voidaan ensin osoittaa mittauksilla.

## Laajojen kielimallien käyttö

Viikolla 5 käytin Claudea testitapausten ideoinnissa ja dokumentaation muotoilussa.
