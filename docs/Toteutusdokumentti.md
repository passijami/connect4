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


## Nykyiset puutteet ja seuraavat parannukset

Tämän viikon selkein ja tarkoituksellinen puute on heuristinen arviointifunktio. Koska syvyysrajalla palautetaan tällä hetkellä aina 0, tekoäly osaa erottaa toisistaan vain ne vaihtoehdot, joissa voitto tai tappio näkyy jo hakusyvyyden sisällä. Seuraavaksi on tarkoitus lisätä heuristiikka, joka arvioi esimerkiksi avoimia neljän ruudun ikkunoita, kolmen ja kahden merkin uhkia sekä keskisarakkeen hallintaa.

Transpositiotaulun hyötyä voisi mitata myöhemmin, mutta en ole vielä lisännyt sitä. Halusin pitää viikon 4 ydinalgoritmin vielä yksinkertaisena, jotta sen pystyy vielä helposti tarkistamaan rivi riviltä.

## Laajojen kielimallien käyttö

Viikolla 4 käytin Claudea testitapausten ideoinnissa ja dokumentaation muotoilussa.
