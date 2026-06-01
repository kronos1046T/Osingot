# Osingot

*(Välipalautus 2)
* Toisen välipalautuksen mennessä sovelluksen tavoittena oli perusvaatimusten täyttyminen. Joten tässä vaiheessa se näyttä hyvin samantyyppiseltä kuin esimerkkisovellus.
*
* Kuvaus:
* Sovelluksen ideana on "Dividend Capture" strategian apuväline. Käyttäjät tulevat lisäämään tietokantaan osakkeita ja ETF:t, jotka ovat maksamassa osinkoa lähiaikoina.
* Tavoitteena on tehdä sovellus johon lisätään linkit tuloraportteihin, record date:t ja maksupäivämäärät.
* Tulevaisuudessa sovelluksessa pystyy etsimään tietokohteita hakusanoilla, ja lajitella kohtia esimerkiksi aakkosjärjestyksessä tai päivämäärän mukaan.
* Sovelluksessa tulee myös olla linkit tietojen lähteisiin (esim Reuters tai tradingview sivustoihin) joita käyttäjät pystyvät lisätä kohtien perään ja CSS design.
* Käynnistäminen:
* Käynnistämistä varten käytän Git Bash sovellusta, mikö on Linuxin komentorivi Windowille erillisessä sovelluksessa.
* Alussa kloonataan SSH linkin, jonka jälkeen löydetään oikea kansio koodilla "cd Osingot" ja avataan sen koodilla "code ."
* Tämä avaa ohjelman VSC:ssa. Avaamisen jälkeen on kopioitava tietokannat. Avataan Sqhema.sql kansio VSC:ssä, jonka jälkeen kopioidaan  jokainen taulu erikseen.
* Komentoriviin kirjoitetaa "sqlite3 database.db" ja liitetään taulut sinne. Taulun onnistunut liittääminen voidaan tarkistaa koodilla ".tables". Näin liitetään jokainen taulu.
* Kun ohjelmaa on avattava selaimessa, Git Bushin kirjoitetaa "flask run" tai "python -m flask --app app run" ja kopioidaan linkki. 
