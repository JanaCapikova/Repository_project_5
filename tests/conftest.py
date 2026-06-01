import pytest
from src.db import DB_UKOLY_NAZEV_TABULKY, pripojeni_k_databazi, vytvoreni_tabulky

@pytest.fixture(scope="function")
def conn():
    # Připojení k testovací databázi
    print("pripoj se k databazi")
    conn = pripojeni_k_databazi("test_")

    # Vytvoření testovací tabulky před každým testem
    print("VYTVORENI TABULEK A DAT")
    vytvoreni_tabulky(conn)

    yield conn

    # Smazání testovací tabulky po každém testu
    with conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {DB_UKOLY_NAZEV_TABULKY}")
    conn.commit()

    print("\nSMAZANI TABULEK A DAT")
    conn.close()