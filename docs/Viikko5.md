# Viikkoraportti 5

Viikolla 4 sain projektin ensimmäisen oikeasti toimivan version valmiiksi. Tämän viikon tärkein tavoite oli saada tekoälyn ydintoiminta valmiiksi ja päivittää testaus- ja toteutusdokumentaatio vastaamaan oikeaa toteutusta.

Suurin muutos oli heuristisen arviointifunktion toteuttaminen. Nyt tekoäly pystyy tekemään järkevämpiä päätöksiä myös silloin, kun voitto tai tappio ei vielä näy suoraan hakusyvyyden sisällä. Lisäsin myös erillisen karsimattoman minimax-version vertailua varten. Sitä ei käytetä varsinaisessa pelissä, vaan sen avulla pystyn testaamaan, että alfa-beta-karsinta palauttaa saman tuloksen kuin tavallinen minimax. Samalla voidaan mitata konkreettisesti, kuinka paljon alfa-beta vähentää tutkittavien solmujen määrää. Testejä laajensin 15 testistä 25 testiin. Uusissa testeissä tarkistetaan esim. heuristiikan tärkeimmät ominaisuudet. Nykyisessä ajossa kaikki 25 testiä menevät läpi.

Benchmark päivitettiin vertaamaan karsimatonta minimaxia ja alfa-beta-hakua suoraan toisiinsa. Erot alkavat näkyä selvästi syvyyden kasvaessa. Esimerkiksi syvyydellä 6 karsimaton minimax tutki viikon mittauksessa 118645 solmua ja alfa-beta 3248 solmua, vaikka molemmat palauttivat saman arvon ja parhaan siirron.

Tämän viikon jälkeen projektin ydintoiminta on mielestäni valmis. Seuraavaksi keskityn enemmän suorituskyvyn mittaamiseen, mahdollisiin pieniin optimointeihin, dokumentaation viimeistelyyn ja siihen, että lopullinen palautus on mahdollisimman selkeä ja helposti toistettavissa.

Tuntimäärällisesti aikaa meni noin 7 tuntia.
