import pytest
from words import words


@pytest.fixture
def newgame():
    return words.Words()


"""
Метод start_game() повинен створити у базі даних нову, пусту, турнірну таблицю та
нову ігрову таблицю (gametable). А у відповідь повернути випадкове слово з якого
почнеться гра.
"""


def test_start_game(newgame):
    """
    Ця тестова функція перевіряє повернуте значення, його тип та розмір.
    """
    game = newgame.start_game()

    # returned value should be 'str' and > 0
    assert type(game) == str
    assert len(game) > 0


def test_rankings(newgame):
    pass
