# Osingot


## Kuvaus

Sovelluksen ideana on "Dividend Capture" -strategian apuväline. Käyttäjät lisäävät tietokantaan osakkeita ja ETF:iä, jotka ovat maksamassa osinkoa lähiaikoina.

Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. Luoda, poistaa ja muokata tietokohteet. 
Jos toinen käyttäjä on luonut positioon, käyttäjä pystyy jättää komentit positiolle.
Kommentit voi myös muokata ja poistaa. 
Kohdalle kuuluvat osakkeen nimi, osingon irtoamis ja maksupäivät, sekä kauden ja alan luokat. 
Jokaista uutta positiota voidaan etsiä hakusanalla.

Tulevat parannukset:
käyttäjä pystyy luokitella positioita oman valintakriteerin perusteell. Esimerkiksi alan, kauden tai päivämäärn mukaisesti.

## Käynnistäminen

1. Kloonataan SSH-linkki repositorioon:
   "git clone "ssh-linkki""
2. Siirrytään kansioon komennolla:
   "cd Osingot"
3. Luodaan tietokanta ja ajetaan schema.sql:
   "sqlite3 database.db"
   Tämän jälkeen kopioidaan schema.sql-kansion koko sisältö tietokantaan.
4. Kopioidaan init.sql-kansion koko sisältö tietokantaan samalla tavalla.
5. Asennetaan Flask ja käynnistetään sovellus:
   "pip install flask"
   "flask run"
6. Kopioidaan localhost-linkki selaimeen ja avataan sovellus.
