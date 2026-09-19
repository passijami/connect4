# Viikkoraportti 3

Aloitin projektin työstämisen tällä viikolla palautteen läpikäynnillä. Sain neuvoa transpositiotaulun käytöstä myöhemmin, jos haluan viedä tekoälyä kurssin vaatimuksia pidemmälle. Palataan tähän, jos jää aikaa. Ymmärsin tarkemmin, miksi hyvä siirtojen järjestäminen johtaa siihen että yhä useampi hajautustauluun laskettu arvo on vain yläraja tarkan arvon sijaan. Tällä viikolla työstin käyttöliittymää, tutustuin pylint-tarkistuksen toimintaan ja loin testausdokumentille rungon.

Varsinainen algoritmin toteutus (board.py:n ja ai.py:n metodit) ovat vielä kesken. Lähden seuraavalla viikolla edistämään näitä.

Suurin epävarmuus on nyt siinä, miten toteutus oikeasti sujuu kun aloitan kirjoittamisen. Suunnitelma vaikuttaa paperilla selvältä, mutta esim. minimaxin ja alfa-betan yhdistäminen vaatii opiskelua. Myös Benchmark-skripti vaatii työstöä.

Aloitan board.py:n toteutuksen metodi kerrallaan, kirjoittaen kunkin testin samaan aikaan koodin kanssa, aloittaen check_win-metodista ja sen reunatapauksista. Sen jälkeen evaluate() ja minimax ilman karsintaa. Lopuksi alfa-beta ja loput optimoinnit. Neljännellä viikolla tavoitteena on saada ydintoiminta lähes valmiiksi vertaisarviointia varten, joten pyrin saamaan perustoteutuksen toimimaan jo tämän viikon aikana, jotta koodista voi jo antaa mielekästä palautetta.

Tuntimäärällisesti käytin tällä viikolla projektiin suunnilleen 10 tuntia.
