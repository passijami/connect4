# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelma on jaettu kolmeen pääosaan:

1. `board.py` vastaa Connect4-pelin säännöistä ja pelitilan hallinnasta.
2. `ai.py` vastaa pelipuun hakemisesta minimax-algoritmilla ja alfa-beta-karsinnalla.
3. `cli.py` on kevyt tekstikäyttöliittymä, jonka kautta ihminen voi pelata tekoälyä vastaan.

Pelilauta on 6 x 7 Python-lista. Arvo 0 tarkoittaa tyhjää ruutua, 1 pelaajaa 1 ja
2 pelaajaa 2. Minimax ei kopioi koko lautaa jokaisessa rekursiotasossa, vaan tekee
siirron `play`-metodilla ja palauttaa laudan ennalleen `undo`-metodilla. Board pitää
siirtohistoriaa, jotta myös `last_move` ja vuorossa oleva pelaaja palautuvat oikein.

## Minimax

Minimax muodostaa pelipuuta mahdollisista tulevista siirroista. Tekoälyn vuorolla
valitaan suurin arvo ja vastustajan vuorolla pienin arvo. Tämä vastaa oletusta, että
molemmat pelaajat tekevät omalta kannaltaan parhaan mahdollisen siirron.

Voittava tekoälyn siirto saa suuren positiivisen arvon ja vastustajan voitto suuren
negatiivisen arvon. Tasapeli saa arvon 0. Viikon 4 versiossa myös syvyysrajalle
päätynyt keskeneräinen peli saa arvon 0. Varsinainen heuristinen arvio lisätään
seuraavalla viikolla.

## Alfa-beta-karsinta

Minimax ylläpitää kahta rajaa:

- `alpha`: paras arvo, jonka maksimoiva pelaaja pystyy tähän mennessä varmasti saamaan.
- `beta`: paras arvo, jonka minimoiva pelaaja pystyy tähän mennessä varmasti saamaan.

Kun `alpha >= beta`, jäljellä olevat saman solmun haarat voidaan jättää tutkimatta,
koska ne eivät voi enää muuttaa ylemmän tason päätöstä. Karsinta ei muuta minimaxin
palauttamaa tulosta, vaan vähentää tutkittavien pelitilojen määrää.

Siirrot käydään lähtökohtaisesti läpi keskisarakkeesta reunoille. Connect4:ssa
keskisarakkeet osallistuvat useampiin mahdollisiin neljän suoriin kuin reunat, joten
tämä järjestys löytää usein lupaavia siirtoja aikaisin ja parantaa alfa-beta-karsintaa.
Iteratiivisessa syvenemisessä edellisen valmiin hakukierroksen paras siirto voidaan
kokeilla seuraavalla kierroksella ensimmäisenä.

## Iteratiivinen syveneminen

`choose_move` suorittaa haut syvyyksillä 1, 2, 3, ... aikarajan puitteissa. Jos
seuraava syvyys jää kesken, sen tulosta ei käytetä. Näin tekoälyllä on aina käytössä
viimeinen kokonaan laskettu siirtoehdotus.

## Aika- ja tilavaativuus

Ilman karsintaa minimaxin aikavaativuus on `O(b^d)`, missä `b` on haarautumiskerroin
Connect4:ssa enintään 7 ja `d` hakusyvyys. Alfa-beta-karsinnan pahin tapaus on edelleen
`O(b^d)`, mutta hyvällä siirtojärjestyksellä paras tunnettu tapaus lähestyy
`O(b^(d/2))`.

Hakurekursion pino käyttää `O(d)` lisätilaa. Pelilautaa ei kopioida hakupuun jokaiseen
solmuun. Nykyinen siirtojärjestyksen vihjesanakirja käyttää lisäksi muistia niille
pelitiloille, jotka siihen tallennetaan; se sisältää vain parhaan siirron, ei valmiita
minimax-arvoja.

## Nykyiset puutteet ja seuraavat parannukset

Viikon 4 tärkein tarkoituksellinen puute on heuristinen arviointifunktio. Koska
syvyysrajalla palautetaan 0, tekoäly erottaa tällä hetkellä toisistaan vain sellaiset
vaihtoehdot, joissa voitto tai tappio näkyy hakusyvyyden sisällä. Seuraavaksi on tarkoitus lisätä heuristiikka, joka arvioi esimerkiksi avoimia neljän ruudun ikkunoita, kolmen ja kahden merkin uhkia sekä keskisarakkeen hallintaa.

Myöhemmin voidaan mitata myös varsinaisen transpositiotaulun hyötyä, mutta sitä ei ole
lisätty vielä, jotta viikon 4 ydinalgoritmi pysyy helposti tarkistettavana.

## Laajojen kielimallien käyttö

Viikolla 4 käytin testitapausten ideoimisessa ja dokumentaation muotoilussa Claudea.
