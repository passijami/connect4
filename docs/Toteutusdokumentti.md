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

Voittava siirto saa suuren positiivisen arvon, häviävä suuren negatiivisen ja tasapeli arvon 0. Tällä viikolla myös syvyysrajalle päättynyt, vielä kesken oleva peli, saa arvon 0. Tämä on tietoinen yksinkertaistus. Varsinainen heuristinen arviointi tulee mukaan ensi viikolla.

## Alfa-beta-karsinta

Minimax pitää yllä kahta rajaa:

- `alpha`: paras arvo, jonka maksimoiva pelaaja voi tähän mennessä varmasti saavuttaa.
- `beta`: paras arvo, jonka minimoiva pelaaja voi tähän mennessä varmasti saavuttaa.

Kun `alpha >= beta`, loput saman solmun haarat voi jättää tutkimatta, koska ne eivät voi enää muuttaa ylemmän tason päätöstä. Karsinta ei vaikuta minimaxin lopputulokseen mitenkään. Se vain vähentää tutkittavien pelitilojen määrää.

Siirrot käydään läpi keskisarakkeesta reunoja kohti, koska Connect4:ssa keskisarakkeet osallistuvat useampaan mahdolliseen neljän suoraan kuin reunat. Tämä järjestys löytää lupaavia siirtoja usein aikaisin, mikä tehostaa karsintaa huomattavasti. Iteratiivisen syvenemisen ansiosta myös edellisen valmiin hakukierroksen parasta siirtoa voi kokeilla seuraavalla kierroksella ensimmäisenä.

## Iteratiivinen syveneminen

`choose_move` hakee vastausta syvyyksillä 1, 2, 3... niin pitkälle kuin aikaraja sallii. Jos jokin syvyys jää kesken, sen tulosta ei käytetä. Siten tekoälyllä on aina käytettävissään viimeisen kokonaan lasketun syvyyden paras löydetty siirto, oli aikaa käytettävissä kuinka paljon tahansa.

## Aika- ja tilavaativuus

Ilman karsintaa minimaxin aikavaativuus on `O(b^d)`, missä `b` on haarautumiskerroin (Connect4:ssa enintään 7) ja `d` hakusyvyys. Alfa-beta-karsinnan pahin tapaus on periaatteessa yhä `O(b^d)`, mutta hyvällä siirtojärjestyksellä päästään käytännössä lähelle `O(b^(d/2))`.

Hakurekursio käyttää vain `O(d)` lisätilaa, koska lautaa ei kopioida jokaiseen puun solmuun. Siirtojärjestyksen vihjesanakirja vie hieman muistia niiltä pelitiloilta jotka siihen tallennetaan, mutta se sisältää vain parhaan siirron, ei valmiita minimax-arvoja, jotka veisivät huomattavasti enemmän tilaa ja joita ei muutenkaan voisi luotettavasti käyttää uudestaan.

## Nykyiset puutteet ja seuraavat parannukset

Tämän viikon selkein ja tarkoituksellinen puute on heuristinen arviointifunktio. Koska syvyysrajalla palautetaan tällä hetkellä aina 0, tekoäly osaa erottaa toisistaan vain ne vaihtoehdot, joissa voitto tai tappio näkyy jo hakusyvyyden sisällä. Seuraavaksi on tarkoitus lisätä heuristiikka, joka arvioi esimerkiksi avoimia neljän ruudun ikkunoita, kolmen ja kahden merkin uhkia sekä keskisarakkeen hallintaa.

Transpositiotaulun hyötyä voisi mitata myöhemmin, mutta en ole vielä lisännyt sitä. Halusin pitää viikon 4 ydinalgoritmin vielä yksinkertaisena, jotta sen pystyy vielä helposti tarkistamaan rivi riviltä.

## Laajojen kielimallien käyttö

Viikolla 4 käytin Claudea testitapausten ideoinnissa ja dokumentaation muotoilussa.
