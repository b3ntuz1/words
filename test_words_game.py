import pytest
from words import words, cruid


@pytest.fixture
def newgame():
    return words.Words()


"""
# TESTCASES

case 1: start_game()
- Метод start_game() створює дві таблиці "gamedata" та "rankings"
у базі даних.
- Записує ігрові дані до таблиці "gamedata"
- Вибирає випадкове слово та повертає його.

case 2: rankings()
- Якщо гра тільки почалася і ніхто не давав відповіді, то повертуни
фразу "Nothing here"
- Повернути рядок виду "------\n| user_name | user_count |\n-------\n"
"""


def test_start_game(newgame):
    """
    Ця тестова функція перевіряє повернуте значення, його тип
    та розмір.
    """
    db = cruid.DataBase()
    game = newgame.start_game()

    # returned value should be 'str' and > 0
    assert type(game) == str
    assert len(game) > 0

    # перевірити наявність даних у таблиці "gamedata"
    gamedata = db.read("gamedata")
    assert len(gamedata) == 1


def test_rankings(newgame):
    # new game starts
    assert newgame.rankings() == "Nothing here"

    # rankings
    db = cruid.DataBase()
    db.insert("rankings", ["user1", 1])
    assert newgame.rankings() == "---------\nuser1 | 1\n"
