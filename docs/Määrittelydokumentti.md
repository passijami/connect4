# Määrittelydokumentti
Helsingin yliopiston Aineopintojen harjoitustyö: Algoritmit ja tekoäly.  
Suoritan kurssin syksyllä 2026 Tietojenkäsittelytieteen kandiohjelmassa (TKT).

## Aihe ja toteutus
Harjoitustyössä toteutetaan Pythonilla tekoäly Connect4-pelille, jota pelataan 6x7-kokoisella laudalla. Pelaajat pudottavat vuorotellen kiekkoja sarakkeisiin, ja ensimmäinen, joka saa neljä omaa kiekkoa suoraan riviin (vaaka-, pysty- tai vinosuunnassa) voittaa.

Tekoäly perustuu minimax-algoritmiin, jota tehostetaan alfa-beta-karsinnalla. Koska peliä ei yleensä voida laskea loppuun asti kohtuullisessa ajassa, haku pysäytetään tietyn syvyyden jälkeen ja pelitilannetta arvioidaan heuristisella funktiolla. Pelin sovelluslogiikka (lailliset siirrot, siirron tekeminen ja voiton tarkistus) toteutetaan itse ilman valmiita kirjastoja. Suurin osa kehitysajasta käytetään tekoälyyn ja sen tehostamiseen. Käyttöliittymä on yksinkertainen tekstipohjainen, eikä sitä testata.

Kullakin vuorolla tekoäly valitsee sarakkeen, johon pudottaa oman pelimerkkinsä, niin että valinta on paras mahdollinen annetulla laskenta-ajalla. Minimax-algoritmi käy pelipuuta läpi olettaen, että molemmat pelaajat pelaavat itselleen parhaalla mahdollisella tavalla. Koska koko peliä ei ehditä laskea läpi, käytetään heuristista arviointifunktiota rajallisen syvyyden pelitilanteille, ja haku syvennetään iteratiivisesti niin pitkälle kuin aikaraja sallii.

Toimiakseen algoritmi tarvitsee seuraavat tiedot:
  1. pelitilanne
  2. käytettävissä oleva laskenta-aika eli iteratiivisen syvenemisen kierrokset ennen siirron palauttamista

| Algoritmi | Aikavaativuus | Tilavaativuus | Tehtävä |
|---|---|---|---|
| Minimax ilman karsintaa | `O(b^d)` | `O(d)` | Käy rekursiivisesti läpi kaikki mahdolliset siirrot syvyyteen `d` asti. `b` on haarautumiskerroin (max 7 saraketta). |
| Minimax + karsinta (alfa-beta) | Parhaimmillaan `O(b^(d/2))`, pahimmillaan `O(b^d)` | `O(d)` | Karsii pois haarat, jotka eivät voi enää vaikuttaa lopputulokseen. Hyöty riippuu siitä, kuinka onnistuneesti siirrot on järjestetty. |

Tilavaativuus on aina `O(d)`, sillä lauta pidetään muistissa yhtenä oliona, ja siirtoja tehdään ja perutaan rekursion edetessä sen sijaan, että lautaa kopioitaisiin jokaisessa rekursion solmussa.

## Projektin kielet
Käytän työssäni Pythonia.  
Vertaisarvioinnissa muiden yleisten kielten arviointi ja seuraaminen onnistuu.  
Sovellus ja dokumentaatio on suomeksi.


## Lähteet
[Connect4 (Wikipedia)](https://en.wikipedia.org/wiki/Connect_Four)  
[Minimax (Wikipedia)](https://en.wikipedia.org/wiki/Minimax)  
[Alfa-Beta](https://www.geeksforgeeks.org)
