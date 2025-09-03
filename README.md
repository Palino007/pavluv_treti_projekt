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

## Ukázka z výstupního CSV souboru:
code	location	registered	envelopes	valid	Občanská demokratická strana	Řád národa - Vlastenecká unie	CESTA ODPOVĚDNÉ SPOLEČNOSTI	Česká str.sociálně demokrat.
529303	Benešov	13104	8485	8437	1052	10	2	624
532568	Bernartice	191	148	148	4	0	0	17
530743	Bílkovice	170	121	118	7	0	0	15
532380	Blažejovice	96	80	77	6	0	0	5
532096	Borovnice	73	54	53	2	0	0	2
532924	Bukovany	598	393	393	50	0	0	20
529451	Bystřice	3490	2206	2200	204	6	2	187
532690	Ctiboř	106	83	83	3	0	0	5
529478	Čakov	93	71	71	7	0	0	6
