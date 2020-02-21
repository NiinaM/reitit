# Asennusohje

## Esivaatimukset

- python 3.x
- pip
- sqlite3

## Paikallinen asennus

1. Lataa tai kloonaa projektin repositorio.

2. Luo ja aktivoi virtuaalinen ympäristö `venv` projektin hakemistossa.

```bash
python -m venv venv
source venv/bin/activate
```

3. Asenna sovelluksen riippuvuudet:

```bash
pip install -r requirement.txt
```

4. Aja sovellusta käynnistämällä Pythonissa projektin juuressa oleva `run.py`-tiedosto.

```bash
python run.py
```

5. Sovelluksen testiversio on käytettävissä osoitteessa http://localhost:5000. Sovellus luo sqlite-tietokannan polkuun `./lines.db`.

## Asennus Herokuun

Asenna Herokun CLI-työkalut. Aja komentorivillä projektin kansiossa luodaksesi projektin Herokuun:

```bash
heroku create <haluttu-nimi>
```

Voit käyttää Postgres-tietokantaa Herokussa asentamalla Postgres-liitännäisen Herokun hallintapaneelissa ja asettamalla asetuksissa ympäristömuuttujat:

```
HEROKU=1
DATABASE_URL=postgres-kannan osoite
```
