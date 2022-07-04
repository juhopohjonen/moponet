# Moponet - Sosiaalinen media

## Mikä moponet oikein on?
Moponet on mootterikulkuneuvojen sosiaalinen media. Voit jukaista Moponet:iin oman moposi, tutkia toisten mopoja, saada tykkäyksiä ja seurauksia sekä olla yhteyksissä toisten käyttäjien kanssa mm. yksityisviestein ja kommentein.

## Tietoa projektista
Moponet on oma ohjelmointiprojektini tietokantojen sekä ohjelmointirajapintojen toteuttamisen harjoittelemista varten. Tässä projektissa harjoittelin etenkin XSS:n, SQL-injektion ja CSRF-haavoittuvuuksien ehkäisyä sekä ohjelmointirajapintojen rakentamista ja käyttöä. Moponetiin on integroitu mm. Discordin OAuth2.0 -kirjautumismahdollisuus, jotta käyttäjät voisivat kirjautua jo olemassaolevilla Discord-tunnuksilla ilman uuden käyttäjän luomista ja että käyttö olisi mahdollisimman mukavaa ja luontevaa.

Ohjelman back-end on kirjoitettu Python3:lla ja Flask-ohjelmistokehyksellä. Tietokantaa käytetään SQLAlchemyllä. Tietokantana olen käyttänyt SQLiteä, mutta Flask-SQLAlchemy tukee tämän liksäksi myös mm. MariaDB -sekä PostgreSQL -tietokantaohjelmistoja. Fronttipuolella on käytetty JavaScriptiä ja CSS-ohjelmistokehyksenä Halfmoon Css:ää.

## Miten käynnistää palvelinohjelmisto?

Tarvitset luonnollisesti Python3:sen ja PIPin. Asenna tarvittavat moduulit komennolla 'pip install -r requirements.txt' juurihakemistossa. Sitten avaa config.json -tiedosto ja muokkaa sopivat arvot muuttujiin. Config.json -tiedostossa on hieman ohjeita.

Tämän jälkeen myös app.py -tiedostossa anna URI tietokannalle. Apua tähän löytyy osoitteesta https://flask-sqlalchemy.palletsprojects.com/en/2.x/. URIn muoto SQLite -tietokannalle näyttää usein tältä: 'sqlite:////path/to/db.db'.

Fronttipuolen tarvittavat moduulit/kirjastot/frameworkit ladataan joko kyseisen sivun link rel -tahon avulla tai kirjasto on merkitty kaikkien sivujen pohjassa ladattavaksi templates/layout.html -tiedostossa.

Mukavia mopoiluhetkiä!

# In English

Moponet is my hobby project to learn about building and securing web applications and API:s. The project is a social media application about mopeds and scooters. You can explore, like and comment cool mopeds and even create your own. You can also create your own profile and chat with other users. 

Moponet is built with Python3. I have always used the db with SQLAlchemy and SQLite as the db, but Flask-SQLAlchemy should support also MariaDB and PostgreSQL.

To start the server application you first need to set up the config.json -file. If you want to use the discord ouath2.0, then you'll need to set up an application at the discord developer console and set redirect_url, client_id and client_secret. You also need to specify the database URI at app.py -file. You can read about the URI at Flask-SQLAlchemy docs. Usually the URI for SQLite looks like this: 'sqlite:////path/to/db.db'.

### Ominaisuudet
- Rekisteröidy sovellukseen sähköpostilla, käyttäjänimellä ja salasanalla
- Rekisteröidy Discord-tunnuksen avulla
- Rekisteröi moposi
- Liitä moposi mukaan kuva
- Tutki muiden mopoja
- Tykkää muiden mopoista
- Kommentoi toisten mopoja
- Seuraa muita käyttäjiä
- Lähetä yksityisviestejä ja chattaa muiden käyttäjien kanssa
- Järjestä mopomiitti
- Tutki toisten järjestämiä mopomiittejä
- Osallistu toisten järjestämiin mopomiitteihin
... ja paljon muuta!

### Varoitus!
Sovellus sisältää huumoria!

