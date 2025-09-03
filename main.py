"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Pavol Medo
email: palimedo@gmail.com
"""

import sys
import csv

import requests
from bs4 import BeautifulSoup


def over_argumenty():
    """
    Zkontroluje, zda byly předány přesně dva argumenty skriptu.
    Pokud ne, vypíše chybu a ukončí program.
    """
    if len(sys.argv) != 3:
        print(
            "Chyba: Skript potřebuje přesně dva argumenty.",
            "Použití: python main.py 'URL_na_ps32' 'vystupni_soubor.csv'",
            sep="\n",
        )
        sys.exit(1)


def stahni_stranku(url_adresa):
    """
    Stáhne HTML obsah stránky z dané URL.

    :param url_adresa: URL adresa stránky.
    :type url_adresa: str
    :return: HTML obsah stránky.
    :rtype: str
    """
    odpoved = requests.get(url_adresa)
    if not odpoved.ok:
        print("Chyba při stahování stránky:", url_adresa)
        sys.exit(1)
    return odpoved.text


def najdi_obce_na_strance_vyber_obce(url_adresa_ps32):
    """
    Z výběru obcí PS32 získá seznam obcí a URL na detail obce.

    :param url_adresa_ps32: URL na stránku výběru obcí.
    :type url_adresa_ps32: str
    :return: Seznam trojic (kód obce, název obce, URL detailu obce).
    :rtype: list[tuple[str, str, str]]
    """
    html_text = stahni_stranku(url_adresa_ps32)
    pole_obci = []

    soup = BeautifulSoup(html_text, "html.parser")
    vsechny_tabulky = soup.find_all("table")

    for jedna_tabulka in vsechny_tabulky:
        vsechny_radky = jedna_tabulka.find_all("tr")
        # první dva řádky jsou hlavičky tabulky – přeskočíme je
        for jeden_radek in vsechny_radky[2:]:
            vsechny_bunky = jeden_radek.find_all("td")
            if len(vsechny_bunky) < 2:
                continue

            bunka_kod = vsechny_bunky[0]
            bunka_nazev = vsechny_bunky[1]

            odkaz_v_kodu = bunka_kod.find("a")
            if odkaz_v_kodu is None or "href" not in odkaz_v_kodu.attrs:
                continue  # řádky bez odkazu přeskočíme

            kod_obce_text = bunka_kod.get_text(strip=True)
            nazev_obce_text = bunka_nazev.get_text(strip=True)
            url_detail_obce = "https://www.volby.cz/pls/ps2017nss/" + odkaz_v_kodu["href"]

            if kod_obce_text != "" and nazev_obce_text != "":
                pole_obci.append((kod_obce_text, nazev_obce_text, url_detail_obce))

    return pole_obci


def ziskej_prehled_stran_a_hlasu_ze_soup(soup_objekt):
    """
    Z detailu obce (ps311) projde tabulky 'část 1' a 'část 2' a vrátí:
    - seznam_nazvu_stran (list názvů stran v pořadí)
    - slovnik_hlasu (mapa {název_strany: hlasy_celkem} pro tuto obec)
    Filtrace: bereme jen řádky, kde první buňka je číslo (1–30),
    druhá buňka obsahuje text (název strany) a třetí buňka je počet hlasů.

    :param soup_objekt: BeautifulSoup objekt stránky detailu obce.
    :type soup_objekt: bs4.BeautifulSoup
    :return: 
        - seznam názvů stran v pořadí,
        - slovník {název strany: hlasy}.
    :rtype: tuple[list[str], dict[str, str]]
    """
    seznam_nazvu_stran = []
    slovnik_hlasu = {}

    vsechny_tabulky = soup_objekt.find_all("table")

    for jedna_tabulka in vsechny_tabulky:
        vsechny_radky = jedna_tabulka.find_all("tr")
        for jeden_radek in vsechny_radky:
            vsechny_bunky = jeden_radek.find_all("td")
            if len(vsechny_bunky) < 3:
                continue

            text_cislo = vsechny_bunky[0].get_text(strip=True)
            text_nazev = vsechny_bunky[1].get_text(strip=True)
            text_hlasy_celkem = vsechny_bunky[2].get_text(strip=True).replace("\xa0", "")

            # vyfiltrujeme jen řádky se stranami (první buňka je celé číslo a druhá obsahuje písmena)

            if text_cislo.isdigit() and any(znak.isalpha() for znak in text_nazev):
                if text_nazev not in seznam_nazvu_stran:
                    seznam_nazvu_stran.append(text_nazev)
                slovnik_hlasu[text_nazev] = text_hlasy_celkem

    return seznam_nazvu_stran, slovnik_hlasu


def zpracuj_detail_obce(
        kod_obce,
        nazev_obce,
        url_detail_obce,
        pevne_poradi_stran
):
    """
    Vytvoří jeden řádek pro CSV s hlasy pro všechny strany.

    :param kod_obce: Kód obce.
    :type kod_obce: str
    :param nazev_obce: Název obce.
    :type nazev_obce: str
    :param url_detail_obce: URL detailu obce.
    :type url_detail_obce: str
    :param pevne_poradi_stran: Pevné pořadí názvů stran.
    :type pevne_poradi_stran: list[str]
    :return: Jeden řádek s údaji o obci a hlasy pro strany.
    :rtype: list[str]
    """
    html_text = stahni_stranku(url_detail_obce)
    soup = BeautifulSoup(html_text, "html.parser")

    # souhrnné počty

    bunka_volici = soup.find("td", {"headers": "sa2"})
    bunka_obalky = soup.find("td", {"headers": "sa3"})
    bunka_platne = soup.find("td", {"headers": "sa6"})

    volici_v_seznamu = (
        bunka_volici.get_text(strip=True).replace("\xa0", "")
        if bunka_volici
        else ""
    )
    
    vydane_obalky = (
        bunka_obalky.get_text(strip=True).replace("\xa0", "")
        if bunka_obalky
        else ""
    )

    platne_hlasy = (
        bunka_platne.get_text(strip=True).replace("\xa0", "")
        if bunka_platne
        else ""
    )

    # hlasy pro strany (vezmeme slovník a pak srovnáme do pevného pořadí z první obce)

    _, slovnik_hlasu = ziskej_prehled_stran_a_hlasu_ze_soup(soup)

    hlasy_v_poradi = []
    for nazev_strany in pevne_poradi_stran:
        hodnota = slovnik_hlasu.get(nazev_strany, "0")
        hlasy_v_poradi.append(hodnota)

    jeden_radek = [kod_obce,
                   nazev_obce,
                   volici_v_seznamu,
                   vydane_obalky,
                   platne_hlasy] + hlasy_v_poradi
    return jeden_radek


#### HLAVNÍ FUNKCE PROGRAMU


def hlavni():
    """
    Hlavní funkce skriptu:
    - Kontroluje argumenty,
    - Stáhne seznam obcí,
    - Získá pevné pořadí stran,
    - Zpracuje všechny obce a uloží výsledky do CSV.
    """
    over_argumenty()

    url_adresa_ps32 = sys.argv[1]
    vystupni_csv = sys.argv[2]

    #### získání seznamu obcí

    seznam_obci = najdi_obce_na_strance_vyber_obce(url_adresa_ps32)
    if len(seznam_obci) == 0:
        print("Nebyla nalezena žádná obec.")
        sys.exit(1)

    # z první obce získáme pevné pořadí názvů stran (30 sloupců)

    prvni_obec_url = seznam_obci[0][2]
    html_text_prvni = stahni_stranku(prvni_obec_url)
    soup_prvni = BeautifulSoup(html_text_prvni, "html.parser")
    nazvy_stran_prvni_obec, _ = ziskej_prehled_stran_a_hlasu_ze_soup(soup_prvni)

    if len(nazvy_stran_prvni_obec) == 0:
        print("Nepodařilo se zjistit názvy stran z detailu první obce.")
        sys.exit(1)

    #### příprava hlavičky csv

    hlavicka = [
        "code",
        "location",
        "registered",
        "envelopes",
        "valid"] + nazvy_stran_prvni_obec

    #### zpracování všech obcí

    vsechny_radky = []
    for kod_obce, nazev_obce, url_detail_obce in seznam_obci:
        jeden_radek = zpracuj_detail_obce(
            kod_obce,
            nazev_obce,
            url_detail_obce,
            nazvy_stran_prvni_obec
        )

        vsechny_radky.append(jeden_radek)

    #### zápis do csv

    with open(vystupni_csv, mode="w", newline="", encoding="utf-8-sig") as csv_soubor:
        zapisovac = csv.writer(csv_soubor, delimiter=";")
        zapisovac.writerows([hlavicka, *vsechny_radky])

    print("Hotovo! Data byla uložena do souboru:", vystupni_csv)

if __name__ == "__main__":
    hlavni()
