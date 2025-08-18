# Třetí projekt do Engeto Online Python Akademie

Tento projekt ukazuje, jak stáhnout a zpracovat data z webu pomocí Pythonu.  
Používá knihovny:

- `requests`
- `beautifulsoup4`
- `sys` (součást Pythonu)
- `csv` (součást Pythonu)

## Instalace

1. Ujistěte se, že máte nainstalovaný Python (verze 3.6 a vyšší).  
2. Nainstalujte potřebné knihovny: `pip install -r requirements.txt`

## Spuštění

Projekt se spouští jednoduchým příkazem: python main.py "<URL>" "<vystupni_soubor.csv>"

### Příklad

`python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"`

Tento příkaz stáhne výsledky voleb z daného odkazu a uloží je do souboru `vysledky_benesov.csv`.

## Poznámky

- Soubor `requirements.txt` obsahuje všechny potřebné knihovny pro tento projekt.  
- Výstupní soubor CSV bude vytvořen ve stejném adresáři, kde je spuštěn skript.

