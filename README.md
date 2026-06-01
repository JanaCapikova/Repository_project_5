# Project 5 - Vylepšený task Manager

## Popis projektu

Tento projekt je konzolová aplikace pro správu úkolů.

Uživatel může v aplikaci:

- přidat nový úkol,
- zobrazit úkoly se stavem nezahájeno nebo probíhá,
- aktualizovat stav úkolu,
- odstranit úkol.

Úkoly se ukládají do MySQL databáze.

## Databáze

Projekt pracuje s databází:

task_manager

V databázi se vytváří tabulka:

ukoly

Tabulka `ukoly` obsahuje tyto sloupce:

- `id`
- `nazev`
- `popis`
- `stav`
- `datum_vytvoreni`

Sloupec `stav` může obsahovat hodnoty:

- `nezahájeno`
- `probíhá`
- `hotovo`

Databáze i tabulka se vytvoří automaticky při spuštění programu, pokud ještě neexistují.

## Struktura projektu

PROJECT_5_ENGETO/
│
├── main.py
├── .env.example
├── README.md
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── db.py
│   └── ukoly.py
│
└── tests/
    ├──conftest.py
    └── test_ukoly_db.py

## Použité technologie

- Python
- MySQL
- mysql-connector-python
- python-dotenv
- pytest

## Instalace závislostí

Závislosti jsou uložené v souboru `requirements.txt`.

Instalace se provede příkazem:

pip install -r requirements.txt

## Nastavení databáze

V hlavní složce projektu je potřeba vytvořit soubor `.env`. Soubor `.env` není součástí odevzdaného projektu, protože obsahuje citlivé přihlašovací údaje k databázi.

V projektu je připravený vzorový soubor `.env.example`, obsahující přihlašovací údaje k MySQL databázi:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=vas_mysql_password
DB_NAME=task_manager

Hodnotu `DB_PASSWORD` je potřeba upravit podle vlastního hesla do MySQL.

Příklad:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=mojeheslo
DB_NAME=task_manager

## Spuštění programu

Program se spouští z hlavní složky projektu příkazem:

python main.py

Po spuštění se zobrazí hlavní menu:

--- SPRÁVCE ÚKOLŮ - Hlavní menu ---
1. Přidat úkol
2. Zobrazit úkoly
3. Změnit stav úkolu
4. Odstranit úkol
5. Ukončit program

## Testování

Projekt obsahuje automatizované testy ve složce `tests`.

Testovací soubor se jmenuje:

test_ukoly_db.py

Testy ověřují tyto funkce:

- `pridat_ukol()`
- `aktualizovat_ukol()`
- `odstranit_ukol()`

Každá funkce má dva testy:

- pozitivní test,
- negativní test.

## Spuštění testů

Testy se spouští z hlavní složky projektu příkazem:

python -m pytest tests/test_ukoly_db.py

Při úspěšném spuštění testů by se měl zobrazit výsledek podobný:

7 passed

## Testovací databáze

Testy používají testovací databázi s prefixem `test_`.

Pokud je hlavní databáze:

task_manager

testovací databáze bude:

test_task_manager

Testovací data se po testu smažou.
Po každém testu se odstraní testovací tabulka `ukoly`, aby testy trvale neměnily hlavní databázi.

## Autor

Jana Cápíková
capikovajana@gmail.com