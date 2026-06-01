# Import konstanty s názvem tabulky z db.py
from src.db import DB_UKOLY_NAZEV_TABULKY


def pridat_ukol(conn):
    # Funkce slouží pro přidání nového úkolu do databáze.
    while True:
        print()
        # Načtení názvu úkolu od uživatele
        novy_ukol_nazev = input("Zadejte název úkolu: ").strip()

        # Kontrola, jestli uživatel zadal název
        if not novy_ukol_nazev:
            print("Nezadal(a) jsi název úkolu. Zkus to znovu.")
            continue
        
        # Načtení popisu úkolu od uživatele
        novy_ukol_popis = input("Zadejte popis úkolu: ").strip()

        # Kontrola, jestli uživatel zadal popis
        if not novy_ukol_popis:
            print("Nezadal(a) jsi popis úkolu. Zkus to znovu.")
            continue

        cursor = conn.cursor()

        # Vložení nového úkolu do databáze
        cursor.execute(f"""
            INSERT INTO {DB_UKOLY_NAZEV_TABULKY} (nazev, popis, stav)
            VALUES (%s, %s, %s)
        """, (novy_ukol_nazev, novy_ukol_popis, "nezahájeno"))

        conn.commit()
        cursor.close()

        print(f"Úkol '{novy_ukol_nazev}' byl přidán.")
        break


def zobrazit_ukoly(conn):
    # Funkce zobrazí úkoly se stavem "nezahájeno" nebo "probíhá"
    cursor = conn.cursor()

    # Načtení pouze úkolů se stavem "nezahájeno" nebo "probíhá"
    cursor.execute(f"""
        SELECT id, nazev, popis, stav, datum_vytvoreni
        FROM {DB_UKOLY_NAZEV_TABULKY}
        WHERE stav IN ('nezahájeno', 'probíhá')
        ORDER BY id
    """)

    ukoly = cursor.fetchall()
    cursor.close()

    if not ukoly:
        print()
        print("Žádné úkoly nebyly nalezeny.")
    else:
        print("\nSeznam úkolů:")
        for ukol in ukoly:
            print(f"{ukol[0]}. {ukol[1]} - {ukol[2]} | stav: {ukol[3]} | vytvořeno: {ukol[4]}")


def aktualizovat_ukol(conn):
    # Funkce změní stav vybraného úkolu.
    zobrazit_ukoly(conn)
    print()

    while True:
        ukol_id = input("Zadejte ID úkolu, u kterého chcete změnit stav: ").strip()

        if not ukol_id.isdigit():
            print("Neplatný vstup. Zadejte číslo úkolu ze seznamu.")
            continue

        cursor = conn.cursor()

        # Ověření, zda úkol se zadaným ID existuje
        cursor.execute(f"""
            SELECT id
            FROM {DB_UKOLY_NAZEV_TABULKY}
            WHERE id = %s
        """, (ukol_id,))

        existujici_ukol = cursor.fetchone()
        cursor.close()

        if not existujici_ukol:
            print("Úkol s tímto ID nebyl nalezen. Zkuste to znovu.")
            continue

        break

    print("\nVyberte nový stav:")
    print("1. probíhá")
    print("2. hotovo")

    volba_stavu = input("Zadejte číslo stavu: ").strip()

    # Převod volby uživatele na hodnotu ukládanou do databáze
    if volba_stavu == "1":
        novy_stav = "probíhá"
    elif volba_stavu == "2":
        novy_stav = "hotovo"
    else:
        print("Neplatná volba stavu.")
        return

    cursor = conn.cursor()

    # Aktualizace stavu úkolu v databázi
    cursor.execute(f"""
        UPDATE {DB_UKOLY_NAZEV_TABULKY}
        SET stav = %s
        WHERE id = %s
    """, (novy_stav, ukol_id))

    conn.commit()
    cursor.close()

    print("Stav úkolu byl změněn.")


def odstranit_ukol(conn):
    # Funkce odstraní vybraný úkol z databáze.
    zobrazit_ukoly(conn)
    print()

    # Načtení ID úkolu, který chce uživatel odstranit
    ukol_id = input("Zadejte ID úkolu, který chcete odstranit: ").strip()

    # Kontrola, jestli uživatel zadal číslo
    if not ukol_id.isdigit():
        print("Neplatný vstup. Zadejte číslo úkolu ze seznamu.")
        return

    cursor = conn.cursor()

    # Odstranění úkolu z databáze podle ID
    cursor.execute(f"""
        DELETE FROM {DB_UKOLY_NAZEV_TABULKY}
        WHERE id = %s
    """, (ukol_id,))

    conn.commit()
    
    # Kontrola, jestli byl úkol skutečně odstraněn
    if cursor.rowcount == 0:
        print("Úkol s tímto ID nebyl nalezen.")
    else:
        print("Úkol byl odstraněn.")

    cursor.close()