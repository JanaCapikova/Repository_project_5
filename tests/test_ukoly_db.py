import pytest
from src.db import DB_UKOLY_NAZEV_TABULKY, vrat_ukoly_db, pripojeni_k_databazi, vytvoreni_tabulky
from src.ukoly import pridat_ukol, aktualizovat_ukol, odstranit_ukol


@pytest.fixture(scope="function")
def conn():
    # Připojení k testovací databázi
    print("pripoj se k databazi")
    conn = pripojeni_k_databazi("test_")

    # Vytvoření testovací tabulky před každým testem
    print("✅ VYTVORENI TABULEK A DAT")
    vytvoreni_tabulky(conn)

    yield conn

    # Smazání testovací tabulky po každém testu
    with conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {DB_UKOLY_NAZEV_TABULKY}")
    conn.commit()

    print("\n✅ SMAZANI TABULEK A DAT")
    conn.close()


def test_pridat_ukol_pozitivni(conn, monkeypatch):
    # Arrange
    vstupy = iter(["Nakoupit", "Koupit mléko"])
    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # Act
    pridat_ukol(conn)

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert len(ukoly) == 1
    assert ukoly[0][1] == "Nakoupit"
    assert ukoly[0][2] == "Koupit mléko"
    assert ukoly[0][3] == "nezahájeno"


def test_pridat_ukol_negativni(conn, monkeypatch):
    # Arrange
    vstupy = iter(["", "Nakoupit", "Koupit mléko"])
    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # Act
    pridat_ukol(conn)

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert len(ukoly) == 1
    assert ukoly[0][1] == "Nakoupit"


def test_aktualizovat_ukol_pozitivni(conn, monkeypatch):
    # Arrange
    with conn.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO {DB_UKOLY_NAZEV_TABULKY} (nazev, popis, stav)
            VALUES (%s, %s, %s)
        """, ("Uklidit", "Uklidit kuchyň", "nezahájeno"))
    conn.commit()

    ukoly = vrat_ukoly_db(conn)
    ukol_id = ukoly[0][0]

    vstupy = iter([str(ukol_id), "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # Act
    aktualizovat_ukol(conn)

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert ukoly[0][3] == "hotovo"


def test_aktualizovat_ukol_negativni(conn, monkeypatch):
    # Arrange
    with conn.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO {DB_UKOLY_NAZEV_TABULKY} (nazev, popis, stav)
            VALUES (%s, %s, %s)
        """, ("Uklidit", "Uklidit kuchyň", "nezahájeno"))
    conn.commit()

    vstupy = iter(["abc"])
    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # Act
    aktualizovat_ukol(conn)

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert len(ukoly) == 1
    assert ukoly[0][3] == "nezahájeno"


def test_odstranit_ukol_pozitivni(conn, monkeypatch):
    # Arrange
    with conn.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO {DB_UKOLY_NAZEV_TABULKY} (nazev, popis, stav)
            VALUES (%s, %s, %s)
        """, ("Uklidit", "Uklidit kuchyň", "nezahájeno"))
    conn.commit()

    ukoly = vrat_ukoly_db(conn)
    ukol_id = ukoly[0][0]

    monkeypatch.setattr("builtins.input", lambda _: str(ukol_id))

    # Act
    odstranit_ukol(conn)

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert len(ukoly) == 0


def test_odstranit_ukol_negativni(conn, monkeypatch):
    # Arrange
    with conn.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO {DB_UKOLY_NAZEV_TABULKY} (nazev, popis, stav)
            VALUES (%s, %s, %s)
        """, ("Uklidit", "Uklidit kuchyň", "nezahájeno"))
    conn.commit()

    monkeypatch.setattr("builtins.input", lambda _: "abc")

    # Act
    odstranit_ukol(conn)

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert len(ukoly) == 1