"""
author: Jana Cápíková
email: capikovajana@gmail.com
"""
# Import funkcí pro práci s databází
from src.db import pripojeni_k_databazi, vytvoreni_tabulky

# Import funkcí pro práci s úkoly
from src.ukoly import pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, odstranit_ukol


def hlavni_menu(conn):
    # Hlavní menu programu běží v nekonečné smyčce
    # Dokud uživatel nezvolí ukončení programu
    while True:
        print("\n--- SPRÁVCE ÚKOLŮ - Hlavní menu ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Změnit stav úkolu")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        # Načtení volby od uživatele
        volba = input("Zadejte číslo volby: ").strip()

        if volba == "1":
            pridat_ukol(conn)
        elif volba == "2":
            zobrazit_ukoly(conn)
        elif volba == "3":
            aktualizovat_ukol(conn)
        elif volba == "4":
            odstranit_ukol(conn)
        elif volba == "5":
            print("Ukončuji program")
            break
        else:
            print("Neplatná volba. Zadej číslo 1 - 5")


if __name__ == "__main__":
    conn = pripojeni_k_databazi()

    # Pokud se připojení podaří, vytvoří se tabulka a spustí se menu
    if conn:
        vytvoreni_tabulky(conn)

        hlavni_menu(conn)

        # Po ukončení programu se spojení s databází uzavře
        conn.close()