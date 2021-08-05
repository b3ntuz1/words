import pytest
import sqlite3
from words import cruid
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
    db = cruid.DataBase(dbname)
    db.create("test_table", {"key": "TEXT", "value": "TEXT"})
    table = database.execute("SELECT * FROM test_table")
    assert table.fetchall() == []


def test_read(database, dbname):
    db = cruid.DataBase(dbname)
    db.create("test_table", {"key": "TEXT", "value": "TEXT"})
    assert db.read("test_table") == []

    database.execute("insert into test_table values('tkey', 'tval')")
    database.commit()
    assert db.read("test_table", col="key") == ["tkey"]
    assert db.read("test_table") == ["tkey|tval"]

    database.execute("insert into test_table values('tkey1', 'tval1')")
    database.commit()
    assert db.read("test_table", col="key") == ["tkey", "tkey1"]
    assert db.read("test_table") == ["tkey|tval", "tkey1|tval1"]

    # test where statemend
    assert db.read("test_table", where="key='tkey1'") == ['tkey1|tval1']


def test_insert(database, dbname):
    db = cruid.DataBase(dbname)
    db.create("test_table", {"key": "TEXT", "value": "TEXT"})
    # insert section
    db.insert("test_table", ["user", "name"])
    assert db.read("test_table") == ["user|name"]


def test_delete_row(database, dbname):
    db = cruid.DataBase(dbname)
    db.create("test_table", {"key": "TEXT", "value": "TEXT"})
    database.execute("insert into test_table values('user', 'name')")
    database.commit()
    db.delete_row('test_table', 'key="user"')
    assert db.read('test_table') == []


def test_delete_table(database, dbname):
    db = cruid.DataBase(dbname)
    db.create("test_table", {"key": "TEXT", "value": "TEXT"})
    database.execute("insert into test_table values('user', 'name')")
    database.commit()
    assert db.read("test_table") == ["user|name"]

    db.delete("test_table")
    with pytest.raises(sqlite3.OperationalError):
        db.read("test_table")
