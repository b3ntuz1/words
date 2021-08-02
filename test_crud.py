import pytest
import sqlite3
from words import crud
from os.path import exists
from os import remove


@pytest.fixture()
def dbname():
    return "testdb.sqlite3"


@pytest.fixture()
def database(dbname):
    # setup
    db = sqlite3.connect(dbname)
    # test case
    yield db
    # teardown
    db.close()
    remove(dbname)


def test_db(database, dbname):
    """ Перевірити чи зʼявився файл з БД """
    assert exists(dbname)


def test_create(database, dbname):
    db = crud.DataBase(dbname)
    db.create("test_table", {"key": "TEXT", "value": "TEXT"})
    table = database.execute("SELECT * FROM test_table")
    assert table.fetchall() == []


def test_read(database, dbname):
    db = crud.DataBase(dbname)
    db.create("test_table", {"key": "TEXT", "value": "TEXT"})
    assert db.read("test_table") == []
    database.execute("insert into test_table values('tkey', 'tval')")
    database.commit()
    assert db.read("test_table", row="key") == ["tkey"]
    assert db.read("test_table") == ["tkey, tval"]
    database.execute("insert into test_table values('tkey1', 'tval1')")
    database.commit()
    assert db.read("test_table", row="key") == ["tkey", "tkey1"]
    assert db.read("test_table") == ["tkey, tval", "tkey1, tval1"]


def test_update(database, dbname):
    db = crud.DataBase(dbname)
    db.create("test_table", {"key": "TEXT", "value": "TEXT"})
    db.update()
