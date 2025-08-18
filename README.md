# Třetí projekt do Engeto Online Python Akademie

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí najdete [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace

Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

pip --version
pip install -r requirements.txt 

## Spuštění

Projekt se spouští jednoduchým příkazem: python main.py "<URL>" "<vystupni_soubor.csv>"

### Příklad

`python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"`

Tento příkaz stáhne výsledky voleb z daného odkazu a uloží je do souboru `vysledky_benesov.csv`.

## Poznámky
 
- Výstupní soubor CSV bude vytvořen ve stejném adresáři, kde je spuštěn skript.


