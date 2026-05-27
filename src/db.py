# Import knihoven potřebných pro práci s databází a .env souborem
import os
import mysql.connector
from dotenv import load_dotenv

# Načtení proměnných ze souboru .env
load_dotenv()

# Konstanta s názvem tabulky
DB_UKOLY_NAZEV_TABULKY = "ukoly"


def pripojeni_k_databazi(prefix=""):
    # Funkce vytvoří připojení k MySQL databázi
    try:
        db_name = prefix + os.getenv("DB_NAME")

        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        conn.close()

        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=db_name
        )

        print("Připojení k databázi proběhlo úspěšně.")
        return conn

    except mysql.connector.Error as err:
        print(f"Chyba při připojení k databázi: {err}")
        return None


def vytvoreni_tabulky(conn):
    # Funkce vytvoří tabulku ukoly, pokud ještě neexistuje
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DB_UKOLY_NAZEV_TABULKY} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM('nezahájeno', 'probíhá', 'hotovo') NOT NULL DEFAULT 'nezahájeno',
            datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()


def vytvor_data(conn):
    # Funkce vloží ukázkový úkol.
    # V hlavním programu se nepoužívá, může sloužit pro vytvoření testovacích dat
    cursor = conn.cursor()

    cursor.execute(f"""
        INSERT INTO {DB_UKOLY_NAZEV_TABULKY} (nazev, popis, stav)
        VALUES (%s, %s, %s)
    """, ("Testovací úkol", "Toto je testovací popis.", "nezahájeno"))

    conn.commit()
    cursor.close()


def vrat_ukoly_db(conn):
    # Funkce vrátí všechny úkoly z databáze
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT id, nazev, popis, stav, datum_vytvoreni
        FROM {DB_UKOLY_NAZEV_TABULKY}
        ORDER BY id
    """)

    ukoly = cursor.fetchall()
    cursor.close()

    return ukoly