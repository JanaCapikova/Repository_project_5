from src.db import DB_UKOLY_NAZEV_TABULKY, vrat_ukoly_db
from src.ukoly import pridat_ukol, aktualizovat_ukol, odstranit_ukol

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


def test_pridat_ukol_negativni_prazdny_popis(conn, monkeypatch, capsys):
    # Arrange
    vstupy = iter(["Nakoupit", "", "Nakoupit", "Koupit mléko"])
    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # Act
    pridat_ukol(conn)
    vystup = capsys.readouterr()

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert len(ukoly) == 1
    assert ukoly[0][1] == "Nakoupit"
    assert ukoly[0][2] == "Koupit mléko"
    assert "Nezadal(a) jsi popis úkolu" in vystup.out


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

    vstupy = iter([str(ukol_id), "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # Act
    aktualizovat_ukol(conn)

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert ukoly[0][3] == "hotovo"


def test_aktualizovat_ukol_negativni(conn, monkeypatch, capsys):
    # Arrange
    with conn.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO {DB_UKOLY_NAZEV_TABULKY} (nazev, popis, stav)
            VALUES (%s, %s, %s)
        """, ("Uklidit", "Uklidit kuchyň", "nezahájeno"))
    conn.commit()

    ukoly = vrat_ukoly_db(conn)
    ukol_id = ukoly[0][0]

    vstupy = iter(["999", str(ukol_id), "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # Act
    aktualizovat_ukol(conn)
    vystup = capsys.readouterr()

    # Assert
    ukoly = vrat_ukoly_db(conn)

    assert len(ukoly) == 1
    assert ukoly[0][3] == "hotovo"
    assert "Úkol s tímto ID nebyl nalezen" in vystup.out


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